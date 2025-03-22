import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import os

# フォント設定（IPAexゴシックがある場合）
font_path = os.path.abspath("ipaexg.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rcParams["font.family"] = font_prop.get_name()
else:
    font_prop = None

st.title("発達段階の成長傾向分析")

# 解析する項目リスト
categories = ["認知力・操作", "認知力・注意力", "集団参加", "生活動作", 
              "言語理解", "表出言語", "記憶", "読字", "書字", "粗大運動", 
              "微細運動", "数の概念"]

# ユーザーが分析したい項目を選択
selected_category = st.selectbox("分析する項目を選択してください", categories)

# アップロード欄（9回分）
uploaded_files = []
dates = []
for i in range(9):
    col1, col2 = st.columns([2, 1])
    with col1:
        file = st.file_uploader(f"{i+1}回目の発達データ", type=["xlsx", "xls"], key=f"file_{i}")
    with col2:
        date = st.text_input(f"{i+1}回目の日付 (YYYY-MM-DD)", key=f"date_{i}")
    
    uploaded_files.append(file)
    dates.append(date)

# データの処理
data_list = []
date_labels = []
for i, file in enumerate(uploaded_files):
    if file is not None:
        df = pd.read_excel(file, sheet_name=0, usecols="A:D", skiprows=1, nrows=12)
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df = df.fillna(0)
        
        # 選択した項目のデータを取得
        row = df[df.iloc[:, 0] == selected_category]
        if not row.empty:
            value = row.iloc[0, 1]  # B列の数値データ
            data_list.append(value)
            date_labels.append(dates[i] if dates[i] else f"{i+1}回目")

# データがある場合のみ可視化
if data_list:
    plt.figure(figsize=(8, 5))
    plt.plot(date_labels, data_list, marker="o", linestyle="-", color="b", label=selected_category)
    plt.xlabel("経過時間", fontproperties=font_prop if font_prop else None)
    plt.ylabel("スコア", fontproperties=font_prop if font_prop else None)
    plt.title(f"{selected_category}の成長傾向", fontproperties=font_prop if font_prop else None)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)
else:
    st.warning("データが不足しています。Excelをアップロードしてください。")
