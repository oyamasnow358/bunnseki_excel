import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import os

# フォント設定
font_path = os.path.abspath("ipaexg.ttf")  # 絶対パス
font_prop = None
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rcParams["font.family"] = font_prop.get_name()
    plt.rc("font", family=font_prop.get_name())  # 追加
    st.write(f"✅ フォント設定: {mpl.rcParams['font.family']}")
else:
    st.error("❌ フォントファイルが見つかりません。")

st.title("発達段階の推移分析")

# アップロード用の辞書を用意
uploaded_files = {}

# 各時点のデータをアップロード
for i in range(6):
    uploaded_files[i] = st.file_uploader(f"アップロードボタン {i+1}（{i}年目の発達段階）", type=["xlsx", "xls"], key=f"file_{i}")

# アップロードされたデータを格納するリスト
data_frames = []
labels = []

# ファイルを読み込む
for i, file in uploaded_files.items():
    if file is not None:
        df = pd.read_excel(file, sheet_name=0, usecols="A:D", skiprows=1, nrows=12)
        df.columns = df.columns.str.strip()  # 列名の前後の空白を削除
        data_frames.append(df)
        labels.append(f"{i}年目")

# データが複数ある場合、比較分析を行う
if len(data_frames) > 1:
    st.write("### 各時点のデータ")
    for i, df in enumerate(data_frames):
        st.write(f"#### {labels[i]}")
        st.dataframe(df)

    # 推移をグラフで可視化
    st.write("### 発達段階の推移（平均値）")

    # 各データの平均値を計算
    averages = [df.mean(numeric_only=True) for df in data_frames]
    st.write("**デバッグ情報: 計算された平均値**", averages)  # デバッグ用出力
    
    plt.figure(figsize=(8, 5))
    for col in data_frames[0].columns:
        if all(col in avg for avg in averages):  # すべての平均データに `col` があるか確認
            plt.plot(labels, [avg[col] for avg in averages], marker="o", label=col)
        else:
            st.warning(f"列 '{col}' が一部のデータに存在しません。")

    if font_prop:
        plt.xlabel("経過年数", fontproperties=font_prop)
        plt.ylabel("スコア", fontproperties=font_prop)
        plt.title("発達段階の推移", fontproperties=font_prop)
        plt.legend(prop=font_prop)
    else:
        plt.xlabel("経過年数")
        plt.ylabel("スコア")
        plt.title("発達段階の推移")
        plt.legend()
    
    plt.grid()
    st.pyplot(plt)
else:
    st.info("少なくとも2つのファイルをアップロードすると、推移を分析できます。")
