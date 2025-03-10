import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import os

# フォント設定
font_path = os.path.abspath("ipaexg.ttf")  # 絶対パス
font_prop = None
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rcParams["font.family"] = font_prop.get_name()
    plt.rc("font", family=font_prop.get_name())
    st.write(f"✅ フォント設定: {mpl.rcParams['font.family']}")
else:
    st.error("❌ フォントファイルが見つかりません。")

st.title("発達段階の推移分析")

# アップロード用の辞書を用意
uploaded_files = {}
date_inputs = {}

# UIのレイアウトを改善（横並びにする）
st.write("### データアップロード")
cols = st.columns(3)  # 3列レイアウト

for i in range(12):
    with cols[i % 3]:  # 3列に分割して配置
        uploaded_files[i] = st.file_uploader(f"{i+1}回目のデータ", type=["xlsx", "xls"], key=f"file_{i}")
        date_inputs[i] = st.text_input(f"日付 (YYYY-MM-DD)", key=f"date_{i}")

# アップロードされたデータを格納するリスト
data_frames = []
labels = []

# ファイルを読み込む
for i, file in uploaded_files.items():
    if file is not None:
        df = pd.read_excel(file, sheet_name=0, usecols="A:D", skiprows=1, nrows=12)
        df.columns = df.columns.str.strip()
        data_frames.append(df)
        date_label = date_inputs[i] if date_inputs[i] else f"{i+1}回目"
        labels.append(date_label)

# データが複数ある場合、比較分析を行う
if len(data_frames) > 1:
    st.write("### 各時点のデータ")
    for i, df in enumerate(data_frames):
        st.write(f"#### {labels[i]}")
        st.dataframe(df)

    # 推移をグラフで可視化
    st.write("### 発達段階の推移（平均値）")
    averages = [df.mean(numeric_only=True) for df in data_frames]
    
    plt.figure(figsize=(8, 5))
    for col in data_frames[0].columns:
        plt.plot(labels, [avg[col] for avg in averages], marker="o", label=col)

    if font_prop:
        plt.xlabel("経過年数", fontproperties=font_prop)
        plt.ylabel("スコア", fontproperties=font_prop)
        plt.title("発達段階の推移", fontproperties=font_prop)
        plt.xticks(ticks=range(len(labels)), labels=labels, fontproperties=font_prop, rotation=45)
        plt.legend(prop=font_prop)
    else:
        plt.xlabel("経過年数")
        plt.ylabel("スコア")
        plt.title("発達段階の推移")
        plt.xticks(ticks=range(len(labels)), labels=labels, rotation=45)
        plt.legend()
    
    plt.grid()
    st.pyplot(plt)

    # レーダーチャートで最新のデータを可視化
    st.write("### 最新の発達段階（レーダーチャート）")
    latest_df = data_frames[-1]
    categories = latest_df.columns.tolist()
    values = latest_df.mean(numeric_only=True).tolist()
    values += values[:1]  # 閉じた形にするため最初の値を最後に追加
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # 閉じた形にするため
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='b', alpha=0.3)
    ax.plot(angles, values, color='b', linewidth=2)
    ax.set_yticklabels([])  # メモリを非表示
    ax.set_xticks(angles[:-1])
    
    if font_prop:
        ax.set_xticklabels(categories, fontproperties=font_prop)
    else:
        ax.set_xticklabels(categories)
    
    st.pyplot(fig)
else:
    st.info("少なくとも2つのファイルをアップロードすると、推移を分析できます。")
