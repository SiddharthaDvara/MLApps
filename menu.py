import streamlit as st
import pandas as pd
#from sklearn.impute import KNNImputer
from io import BytesIO
from outlier import detect_outliers
import Normal
uploaded_files = st.sidebar.file_uploader("Choose a CSV/xlsx file", accept_multiple_files=False,type=['xlsx','csv'])

df=pd.DataFrame()
if uploaded_files != None :

    st.title("Preview")
    Missing_value = st.sidebar.checkbox('Missing value treatment')
    #Feature_encoding = st.sidebar.checkbox('Feature encoding')
    Outlier = st.sidebar.checkbox('Outlier')
    feature_scaling = st.sidebar.checkbox('Feature Scaling ')
    export = st.sidebar.checkbox('Export to file')

    if uploaded_files.name.split('.')[1]=='csv':
        df=pd.read_csv(uploaded_files)

    if uploaded_files.name.split('.')[1]=='xlsx':
        df=pd.read_excel(uploaded_files)


    if Outlier:
        for t in df.columns:
            if df[t].dtypes in ["int64","float64"]:
                m=["Mean","Median"]
                menu = st.sidebar.selectbox("Select the option to be imputed for outlier treatment ", m)
                p=detect_outliers(df[t])
                rep=None
                if menu == "Mean":
                    rep=df[t].mean()
                if menu == "Median":
                    rep=df[t].median()
                for t in p:
                    df.replace(to_replace=t,value=rep)
        pass

    if Missing_value:
        for t in df.columns:
            if df[t].dtypes in ["int64","float64"]:


                dt = df.copy()
                dt[t] = dt[t].fillna(0)
                dt[t] = dt[t].astype('float')
                l = ["Mean", 'Median', 'Mode', 'KNN']
                df[t] = df[t].astype('float')
                menu = st.sidebar.selectbox("Select the option to be imputed for Missing value treatment", l)
                if menu == "Mean":
                    df[t] = df[t].fillna(dt[t].mean())

                elif menu == "Median":
                    df[t] = df[t].fillna(dt[t].median())

                elif menu == "Mode":
                    df[t] = df[t].fillna(dt[t].mode().iloc[0])
                #else:
                    #imputer = KNNImputer(n_neighbors=3)
                    #df[[t]] = imputer.fit_transform(df[[t]])

            elif df[t].dtypes == "object":

                df[t]=df[t].fillna(" ")

    if  feature_scaling:
        for t in df.columns:
            options=""
            if df[t].dtypes  in ["int64","float64"]:
                null_sum = df[t].isna().sum()
                if null_sum > 0:
                    st.error("Perform missing value treatment")
                else:
                    options = st.sidebar.selectbox("Select feature scaling methods",
                                                   ['Standard Scalar', 'Min Max Scalar', 'Robust Scalar',
                                                    'Max Absolute scalar'])
                    if options == 'Standard Scalar':
                        l=Normal.StandardScaler(pd.DataFrame(df[t]))

                    if options == 'Robust Scalar':
                        l=Normal.RobustScaler(pd.DataFrame(df[t]))


                    if options== 'Min Max Scalar':
                        l=Normal.MinMaxScaler(pd.DataFrame(df[t]))


                    if options== 'Max Absolute scalar':
                        l=Normal.MaxScaled(pd.DataFrame(df[t]))
                        
                    df["Feature Scaled ("+ options+")"+ t] = l
  


    if export:

        options=st.sidebar.selectbox("Enter the file to be exported",['csv','xlsx'])
        name=st.sidebar.text_input("Enter filename")
        if options=="csv":
            data=df.to_csv().encode('utf-8')

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
        if name != None:
            st.sidebar.download_button(label="Download data as "+options,data=data,file_name=name+"."+options,)

    st.table(df)

