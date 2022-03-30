import pandas as pd
#import matplotlib.pyplot as plt
import streamlit as st
#import graph

def MaxScaled(df):
    #st.title("Max scaled columns")
    df_max_scaled = pd.DataFrame(df.copy())

    for column in df_max_scaled.columns:
        df_max_scaled[column] = df_max_scaled[column] /df_max_scaled[column].abs().max()
        #x/|max(x)|
    return pd.DataFrame(df_max_scaled)


def MinMaxScaler(df):
    #st.title("Min Max feature scaling")
    df_min_max=pd.DataFrame(df.copy())
    for column in df_min_max.columns:
        st.write(column+" minimum ",df_min_max[column].min(),"maximum",df_min_max[column].max())
        df_min_max[column]=(df_min_max[column]-df_min_max[column].min())/(df_min_max[column].max()-df_min_max[column].min())
    return pd.DataFrame(df_min_max)

def RobustScaler(df):
    #st.title("Robust Scaler feature scaling")
    df_Robust_Scaler=pd.DataFrame(df.copy())
    for column in df_Robust_Scaler.columns:
        q1=df_Robust_Scaler[column].quantile(0.25)
        q3 = df_Robust_Scaler[column].quantile(0.75)
        st.write("For Column "+column)
        st.write("Q1=",q1)
        st.write("Q3=",q3)

        df_Robust_Scaler[column]=(df_Robust_Scaler[column]-q1)/(q3-q1)
    return pd.DataFrame(df_Robust_Scaler)

def StandardScaler(df):

    df_standard_scaler=pd.DataFrame(df.copy())

    for column in df_standard_scaler.columns:
        st.write("Standard deviation for "+column,df_standard_scaler[column].std())
        st.write("Mean for " + column, df_standard_scaler[column].mean())
        df_standard_scaler[column]=(df_standard_scaler[column]-df_standard_scaler[column].mean())/df_standard_scaler[column].std()
    return pd.DataFrame(df_standard_scaler)
