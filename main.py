import streamlit as st
import pandas as pd
import time
import os
path=os.getcwd()


from sklearn.impute import KNNImputer
from io import BytesIO
from outlier import detect_outliers
import Normal
import numpy as np
#missing_confirm = True
#outlier_confirm = True

def spin():
    with st.spinner('App reloading...'):
        time.sleep(1)
st.sidebar.title("Data preprocessing app")
uploaded_files = st.sidebar.file_uploader("Choose a CSV/xlsx file", accept_multiple_files=False,type=['xlsx','csv'])
df=pd.DataFrame()
if uploaded_files :

    spin()
    st.title("Preview")
    Missing_value = st.sidebar.checkbox('Missing value treatment')
    Outlier = st.sidebar.checkbox('Outlier')
    feature_scaling = st.sidebar.checkbox('Feature Scaling ')
    delete_columns = st.sidebar.checkbox("Select columns to delete")
    export = st.sidebar.checkbox('Export to file')



    if uploaded_files.name.split('.')[1]=='csv':
        df=pd.read_csv(uploaded_files)

    if uploaded_files.name.split('.')[1]=='xlsx':
        df=pd.read_excel(uploaded_files)

    if Missing_value:
        spin()
        st.write("Missing value selected")
        missing_value_menu=st.sidebar.selectbox("Enter option to fill numeric values",["Mean","Median","Mode","KNN"])
        colums_options_number_missing = st.sidebar.multiselect('Select numeric columns to be filled for missing value',[l for l in df.columns if df[l].dtype in ["int64","float64"]],)
        colums_options_text_missing = st.sidebar.multiselect('Select text columns to be filled for missing value',[l for l in df.columns if df[l].dtype in ["object", "str"]], )

        dt=df.copy()
        dm=df.copy()
        for p in colums_options_number_missing:

            dt[p] = dt[p].fillna(0.0)
            dt[p] = dt[p].astype('float')
            if missing_value_menu=="Mean":
                df[p] = df[p].fillna(dt[p].mean())
            elif missing_value_menu=="Median":
                df[p] = df[p].fillna(dt[p].median())
            elif missing_value_menu == "Mode":
                df[p] = df[p].fillna(dt[p].mode().iloc[0])
            else:
                imputer = KNNImputer(n_neighbors=3)
                dm[[p]] = imputer.fit_transform(df[[p]])

        for p in colums_options_text_missing:
            df[p]=df[p].fillna(" ")

        #st.write(dm)



        #st.write(t)
    if delete_columns:
        colums_options_number_missing = st.sidebar.multiselect('Select numeric columns to be dropped',[l for l in df.columns], )
        for o in colums_options_number_missing:
            del df[o]

    if Outlier:
        spin()
        #st.write(st.session_state['Missing_value'])
        Outlier_menu = st.sidebar.selectbox("Select the option to be imputed for outlier treatment ",
                                            ["Mean", "Median"], )
        #k=df.select_dtypes(include=['float64'])
        colums_options_number_missing = st.sidebar.multiselect('Select numeric columns to be filled for outlier',
                                                               [l for l in df.select_dtypes(include=['float64','int64'])], )

        st.write("In outlier treatment,the values are imputed")
        for t in colums_options_number_missing:
            st.write(t)
            #p=[]
            #st.write(df[t])
            p = detect_outliers(df[t])
            rep = 0
            if Outlier_menu == "Mean":
                rep = df[t].mean()
            if Outlier_menu == "Median":
                rep = df[t].median()

            #st.write(rep)

            s=",".join(str(x) for x in p)
            #st.write(" ".join(str(p)))
            st.write("The outliers for "+t+" are "+s)
            for c in p:
                df[t].mask(df[t] == c, rep, inplace=True)
                #df.replace(to_replace=t, value=rep,inplace=True)

    if feature_scaling:
        spin()
        columns_options_number_scaling = st.sidebar.multiselect('Select numeric columns for feature scaling', [l for l in df.select_dtypes(include=['float64','int64'])], )
        feature_scaling_menu=None
        pl=pd.DataFrame(df[columns_options_number_scaling].isna().sum())
        pl = pl.loc[pl[0] != 0]

        p=len(pl)

        if p>0:

            dg=[n for n in pl.index]
            #st.write(dg)
            dg=",".join(dg)
            #st.write(dg)
            st.error("Perform missing value treatment for "+dg+" Column(s)")
        else:
            feature_scaling_menu = st.sidebar.selectbox("Select the option to be imputed for feature Scaling",['Standard Scalar', 'Min Max Scalar', 'Robust Scalar','Max Absolute scalar'])


            st.title(feature_scaling_menu)
            expression={'Min Max Scalar':r'''x_{i}=(x_{i}-x_{min})/(x_{max}-x_{min})''',
                        'Robust Scalar':r'''x_{i}=(x_{i}-q_{1})/(q_{3}-q_{1})''',
                        'Standard Scalar':r'''x_{i}=(x_{i}-x_{mean})/(x_{stddev})''',
                        'Max Absolute scalar': r'''x_{i}=x_{i}/|x_{max}|'''
                        }
            st.latex(expression[feature_scaling_menu])
            for p in columns_options_number_scaling:

                if feature_scaling_menu == 'Standard Scalar':
                    l = Normal.StandardScaler(pd.DataFrame(df[p]))

                elif feature_scaling_menu == 'Min Max Scalar':
                    l = Normal.MinMaxScaler(pd.DataFrame(df[p]))

                elif feature_scaling_menu == 'Robust Scalar':
                    l = Normal.RobustScaler(pd.DataFrame(df[p]))

                else:
                    l = Normal.MaxScaled(pd.DataFrame(df[p]))

                df[p] = l

    if export:
        spin()
        options = st.sidebar.selectbox("Enter the file to be exported", ['csv', 'xlsx'], )
        #name = st.sidebar.text_input("Enter filename")
        if options == "csv":
            data = df.to_csv(index=False).encode('utf-8')

        if options == "xlsx":
            #write into file as bytes
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            format1 = workbook.add_format({'num_format': '0.00'})
            worksheet.set_column('A:A', None, format1)
            writer.save()
            data = output.getvalue()


        st.sidebar.download_button(label="Download data as "+options,data=data,file_name="export"+"."+options,)


    st.table(df)

