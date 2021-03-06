import streamlit as st
import pandas as pd
import time
import os
path=os.getcwd()
path += r"\temp.csv"
st.write(path)
from sklearn.impute import KNNImputer
from io import BytesIO
from outlier import detect_outliers
import Normal
import numpy as np


#####################
def spin():
    with st.spinner('App reloading...'):
        time.sleep(1)


##############################
def LoadFile():
    if uploaded_files.name.split('.')[1]=='csv':
        df=pd.read_csv(uploaded_files)

    elif uploaded_files.name.split('.')[1]=='xlsx':
        df=pd.read_excel(uploaded_files)
    #st.write("load file")
    #st.write(df)
    return df
################################
uploaded_files = st.sidebar.file_uploader("Choose a CSV/xlsx file", accept_multiple_files=False,type=['xlsx','csv'])
#st.write(uploaded_files)
if uploaded_files == None :
    #st.write("Initial")
    st.session_state.Missing_value_session = 0
    st.session_state.Outlier_treatment_session = 0
    st.session_state.Feature_scaling_treatment_session = 0

else :


    spin()
    st.title("Preview")
    Missing_value = st.sidebar.checkbox('Missing value treatment')
    Outlier = st.sidebar.checkbox('Outlier')
    feature_scaling = st.sidebar.checkbox('Feature Scaling ')
    export = st.sidebar.checkbox('Export to file')
    df = LoadFile()
    #df.to_csv(path,index=False)


    #dn = df.copy()
    #dn.to_csv(path, index=False)


    if Missing_value:
        spin()


        st.write("Missing value selected")
        missing_value_menu=st.sidebar.selectbox("Enter option to fill numeric values",["Mean","Median","Mode","KNN"])
        colums_options_number_missing = st.sidebar.multiselect('Select numeric columns to be filled for missing value',[l for l in df.columns if df[l].dtype in ["int64","float64"]],)
        colums_options_text_missing = st.sidebar.multiselect('Select text columns to be filled for missing value',[l for l in df.columns if df[l].dtype in ["object", "str"]], )
        old=pd.read_csv(path)
        dt=pd.read_csv(path)
        dm=pd.read_csv(path)

        for p in colums_options_number_missing:

            dt[p] = dt[p].fillna(0.0)
            dt[p] = dt[p].astype('float')
            if missing_value_menu=="Mean":
                dm[p] = dm[p].fillna(dt[p].mean())
            elif missing_value_menu=="Median":
                dm[p] = dm[p].fillna(dt[p].median())
            elif missing_value_menu == "Mode":
                dm[p] = dm[p].fillna(dt[p].mode().iloc[0])
            else:
                imputer = KNNImputer(n_neighbors=3)
                dm[[p]] = imputer.fit_transform(df[[p]])

        for p in colums_options_text_missing:
            dm[p]=df[p].fillna(" ")

        #st.write(dm)

        #if st.session_state['Missing_value_session']==0 :
        missing_confirm = st.sidebar.button("Confirmation Yes for missing value")
        if st.session_state['Missing_value_session']==0:
            #st.write("step1")
            if missing_confirm  :
                #st.write("step2")
                st.session_state['Missing_value_session']+= 1
                #st.write(st.session_state['Missing_value_session'])
                st.write("Writing to file")
                dm.to_csv(path,index=False)

            else:
                st.warning("please confirm for missing value treatment")


        #st.write(t)

    if Outlier:
        spin()

        dt=pd.read_csv(path)
        st.write(dt)

        st.write(st.session_state['Missing_value_session'])
        Outlier_menu = st.sidebar.selectbox("Select the option to be imputed for outlier treatment ",
                                            ["Mean", "Median"], )
        colums_options_number_missing = st.sidebar.multiselect('Select numeric columns to be filled for outlier',
                                                               [l for l in df.columns if
                                                                df[l].dtype in ["int64", "float64"]], )

        st.write("In outlier treatment,the values are imputed")
        for t in colums_options_number_missing:

            p = detect_outliers(dt[t])
            rep = 0

            if Outlier_menu == "Mean":
                rep = dt[t].mean()
            if Outlier_menu == "Median":
                rep = dt[t].median()
            for t in p:
                dt.replace(to_replace=t, value=rep,inplace=True)

        #if st.session_state['Outlier_treatment_session']==0 :
        outlier_confirm = st.sidebar.button("Confirmation Yes for outlier value")
        if st.session_state['Outlier_treatment_session']==0:
            if outlier_confirm :
                st.session_state['Outlier_treatment_session']+= 1
                #st.write(st.session_state['Missing_value_session'])
                dt.to_csv(path,index=False)
            else:
                st.warning("please confirm for Outlier ")

        #st.write(df)

    if feature_scaling:
        spin()
        columns_options_number_scaling = st.sidebar.multiselect('Select numeric columns for feature scaling', [l for l in df.columns if
                                                                                          df[l].dtype in ["int64",
                                                                                                          "float64"]], )
        feature_scaling_menu=None
        dp=pd.read_csv(path)
        st.write(dp)
        pl=pd.DataFrame(dp[columns_options_number_scaling].isna().sum())
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
                        'Max Absolute scalar': r'''x_{i}=x_{i}/|x_{mean}|'''
                        }
            st.latex(expression[feature_scaling_menu])
            for p in columns_options_number_scaling:

                if feature_scaling_menu == 'Standard Scalar':
                    l = Normal.StandardScaler(pd.DataFrame(dp[p]))

                elif feature_scaling_menu == 'Min Max Scalar':
                    l = Normal.MinMaxScaler(pd.DataFrame(df[p]))

                elif feature_scaling_menu == 'Robust Scalar':
                    l = Normal.RobustScaler(pd.DataFrame(dp[p]))

                else:
                    l = Normal.MaxScaled(pd.DataFrame(dp[p]))

                dp[p] = l
                feature_scaling_confirm = st.sidebar.button("Confirmation Yes for missing value")
                if st.session_state['Feature_scaling_treatment_session'] == 0:
                    # st.write("step1")
                    if feature_scaling_confirm:
                        # st.write("step2")
                        st.session_state['Missing_value_session'] += 1
                        # st.write(st.session_state['Missing_value_session'])
                        #st.write("Writing to file")
                        dp.to_csv(path, index=False)

                    else:
                        st.warning("please confirm for feature scaling")


    if export:
        spin()
        options = st.sidebar.selectbox("Enter the file to be exported", ['csv', 'xlsx'], )
        #name = st.sidebar.text_input("Enter filename")
        if options == "csv":
            data = df.to_csv().encode('utf-8')

        elif options == "xlsx":
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


    #st.write(pd.read_csv(path))

