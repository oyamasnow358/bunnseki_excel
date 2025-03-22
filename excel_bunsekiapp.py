import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ------------------------------
# フォント設定（IPAexゴシックを使用）
font_path = os.path.abspath("ipaexg.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rcParams["font.family"] = font_prop.get_name()
else:
    font_prop = None

st.title("回帰分析（発達段階の成長傾向分析）")

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

# ------------------------------
# 回帰分析の実行
if st.sidebar.button("回帰分析を実行"):
    if len(data_list) < 2:
        st.warning("データが不足しています。最低2回分のデータをアップロードしてください。")
    else:
        # 線形回帰モデル
        X = np.array(range(len(data_list))).reshape(-1, 1)  # 経過時間
        y = np.array(data_list)

        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        # モデル評価
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        st.subheader("モデル評価")
        st.write(f"平均二乗誤差 (MSE): **{mse:.4f}**")
        st.write(f"決定係数 (R²): **{r2:.4f}**")

        # ------------------------------
        # 予測結果の可視化：実測値 vs 予測値
        st.subheader("予測結果の可視化")
        fig, ax = plt.subplots()
        ax.scatter(y, y_pred, alpha=0.7, edgecolors="b", label="実測値 vs 予測値")
        ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2, label="完全一致ライン")
        ax.set_xlabel("実測値", fontproperties=font_prop)  
        ax.set_ylabel("予測値", fontproperties=font_prop)
        ax.set_title("回帰分析の結果", fontproperties=font_prop)
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# ------------------------------
# データがある場合のみ可視化
if data_list:
    st.subheader(f"{selected_category}の成長傾向")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(date_labels, data_list, marker="o", linestyle="-", color="b", label=selected_category)
    ax.set_xlabel("経過時間", fontproperties=font_prop)
    ax.set_ylabel("スコア", fontproperties=font_prop)
    ax.set_title(f"{selected_category}の成長傾向", fontproperties=font_prop)
    ax.set_xticklabels(date_labels, rotation=45, fontproperties=font_prop)
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
else:
    st.warning("データが不足しています。Excelをアップロードしてください。")
