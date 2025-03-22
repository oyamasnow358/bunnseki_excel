import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file):
    df = pd.read_excel(file, sheet_name=None)
    return df

def plot_growth(df, category):
    if category not in df.columns:
        st.error(f"選択したカテゴリ '{category}' はデータに含まれていません。")
        return
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['年度'], df[category], marker='o', linestyle='-')
    plt.xlabel('年度')
    plt.ylabel(category)
    plt.title(f'{category} の成長推移')
    plt.grid()
    st.pyplot(plt)

st.title('成長傾向の可視化アプリ')

uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx", "xls"])

if uploaded_file:
    data = load_data(uploaded_file)
    sheet_name = st.selectbox("シートを選択", list(data.keys()))
    df = data[sheet_name]
    
    if '年度' not in df.columns:
        st.error("データに '年度' カラムが見つかりません。")
    else:
        category = st.selectbox("表示する項目を選択", df.columns[1:])
        plot_growth(df, category)
