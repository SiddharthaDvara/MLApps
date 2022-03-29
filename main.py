import streamlit as st
import pandas as pd
import time
import sys
import subprocess
#subprocess.check_call([sys.executable, '-m', 'pip', 'install','scikit-learn'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install','openpyxl'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install','xlsxwriter'])
from sklearn.impute import KNNImputer
from io import BytesIO
from outlier import detect_outliers
import Normal
import numpy as np
uploaded_files = st.sidebar.file_uploader("Choose a CSV/xlsx file", accept_multiple_files=False,type=['xlsx','csv'])
df=pd.DataFrame()
if uploaded_files :

    st.title("Preview")
    Missing_value = st.sidebar.checkbox('Missing value treatment')
    Outlier = st.sidebar.checkbox('Outlier')
    feature_scaling = st.sidebar.checkbox('Feature Scaling ')
    export = st.sidebar.checkbox('Export to file')

    if uploaded_files.name.split('.')[1]=='csv':
        df=pd.read_csv(uploaded_files)

    if uploaded_files.name.split('.')[1]=='xlsx':
        df=pd.read_excel(uploaded_files)

    if Missing_value:
        st.write("Missing value selected")
        missing_value_menu=st.sidebar.selectbox("Enter option to fill numeric values",["Mean","Median","Mode","KNN"])
        dt = df.copy()
        for p in df.columns:
            if df[p].dtype in ["int64","float64"]:
                dt[p] = dt[p].fillna(0)
                dt[p] = dt[p].astype('float')
                if missing_value_menu=="Mean":
                    df[p] = df[p].fillna(dt[p].mean())
                elif missing_value_menu=="Median":
                    df[p] = df[p].fillna(dt[p].median())
                elif missing_value_menu == "Mode":
                    df[p] = df[p].fillna(dt[p].mode().iloc[0])
                else:
                    imputer = KNNImputer(n_neighbors=3)
                    df[[p]] = imputer.fit_transform(df[[p]])
                    pass
            elif df[p].dtype in ["object","str"]:
                df[p]=df[p].fillna(" ")
                #st.write(df[p].dtype)

        #st.write(t)

    if Outlier:
        Outlier_menu = st.sidebar.selectbox("Select the option to be imputed for outlier treatment ",
                                            ["mean", "median"], )
        st.write("In outlier treatment,the values are imputed")
        for t in df.columns:
            if df[t].dtypes in ["int64", "float64"]:
                p = detect_outliers(df[t])
                rep = None
                if Outlier_menu == "mean":
                    rep = df[t].mean()
                if Outlier_menu == "median":
                    rep = df[t].median()
                for t in p:
                    df.replace(to_replace=t, value=rep)

    if feature_scaling:
        feature_scaling_menu=None
        p=len(df.columns[df.isna().any()].tolist())
        if p>0:
            st.error("Perform missing value treatment")
        else:
            feature_scaling_menu = st.sidebar.selectbox("Select the option to be imputed for feature Scaling",['Standard Scalar', 'Min Max Scalar', 'Robust Scalar','Max Absolute scalar'])
            st.title(feature_scaling_menu)
            expression={'Min Max Scalar':r'''x_{i}=(x_{i}-x_{min})/(x_{max}-x_{min})''',
                        'Robust Scalar':r'''x_{i}=(x_{i}-q_{1})/(q_{3}-q_{1})''',
                        'Standard Scalar':r'''x_{i}=(x_{i}-x_{mean})/(x_{stddev})''',
                        'Max Absolute scalar': r'''x_{i}=x_{i}/|x_{mean}|'''
                        }
            st.latex(expression[feature_scaling_menu])
            for p in df.columns:
                if df[p].dtype in ["int64","float64"]:


                    if feature_scaling_menu == 'Standard Scalar':
                        l = Normal.StandardScaler(pd.DataFrame(df[p]))

                    elif feature_scaling_menu == 'Min Max Scalar':
                        l = Normal.MinMaxScaler(pd.DataFrame(df[p]))

                    elif feature_scaling_menu == 'Robust Scalar':
                        l = Normal.RobustScaler(pd.DataFrame(df[p]))

                    else:
                        l = Normal.MaxScaled(pd.DataFrame(df[p]))

                    df["Feature Scaled (" + feature_scaling_menu + ")" + p] = l

    if export:

        options = st.sidebar.selectbox("Enter the file to be exported", ['csv', 'xlsx'], )
        name = st.sidebar.text_input("Enter filename")
        if options == "csv":
            data = df.to_csv().encode('utf-8')

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

with st.spinner('Wait for it...'):
    time.sleep(5)