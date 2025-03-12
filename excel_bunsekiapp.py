import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import os

# フォント設定
font_path = os.path.abspath("ipaexg.ttf")
font_prop = None
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rcParams["font.family"] = font_prop.get_name()
    plt.rc("font", family=font_prop.get_name())
    st.write(f"✅ フォント設定: {mpl.rcParams['font.family']}")
else:
    st.error("❌ フォントファイルが見つかりません。")

st.title("発達段階の推移分析")

# UIの整理（3列レイアウト）
cols = st.columns(3)

uploaded_files = {}
date_inputs = {}

# 各時点のデータをアップロード
for i in range(12):
    with cols[i % 3]:  # 3列で横に並べる
        uploaded_files[i] = st.file_uploader(f"{i+1}回目の発達段階", type=["xlsx", "xls"], key=f"file_{i}")
        date_inputs[i] = st.text_input(f"{i+1}回目の日付（YYYY-MM-DD）", key=f"date_{i}")

# アップロードされたデータを格納するリスト
data_frames = []
labels = []

# ファイルを読み込む
for i, file in uploaded_files.items():
    if file is not None:
        df = pd.read_excel(file, sheet_name=0, usecols="A:D", skiprows=1, nrows=12)
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df = df.fillna(0)
        if not df.empty:
            data_frames.append(df)
            date_label = date_inputs[i] if date_inputs[i] else f"{i+1}回目"
            labels.append(date_label)

# データフレームの共通カラムを取得
common_columns = list(set.intersection(*(set(df.columns) for df in data_frames)))

if not common_columns:
    st.error("共通する項目がありません。データのフォーマットを確認してください。")
else:
    averages = []
    for df in data_frames:
        avg = df[common_columns].mean(numeric_only=True).fillna(0)
        averages.append(avg)

    # 変化のあった項目を検出
changes = {}
for col in common_columns:
    values = [avg[col] for avg in averages if col in avg]

    # 値が空ならスキップ
    if not values:
        st.warning(f"項目 '{col}' のデータがありません。")
        continue

    # 数値データでない場合はエラーを回避
    try:
        if max(values) - min(values) > 0:  # 変化があるかチェック
            changes[col] = values
    except ValueError as e:
        st.error(f"項目 '{col}' で数値以外のデータが検出されました: {e}")
        continue

    # averages のデバッグ
st.write("デバッグ: averages の内容", averages)

# 選択した項目が averages に含まれているかチェック
valid_values = [avg[selected_col] for avg in averages if selected_col in avg]

if not valid_values:
    st.error(f"選択した項目 '{selected_col}' のデータが見つかりません。")
else:
    plt.figure(figsize=(8, 5))
    plt.plot(labels, valid_values, marker="o", label=selected_col)
    plt.xlabel("経過年数", fontproperties=font_prop if font_prop else None)
    plt.ylabel("スコア", fontproperties=font_prop if font_prop else None)
    plt.title("発達段階の推移", fontproperties=font_prop if font_prop else None)
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=45)
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    latest_df = data_frames[-1]
    if not latest_df.empty:
     st.write("### 最新の発達段階（レーダーチャート）")

    # 各能力の平均値を計算
    radar_values = latest_df.mean(numeric_only=True).fillna(0).values
    radar_labels = latest_df.columns

    num_vars = len(radar_labels)

    if num_vars > 1:  # 1つのデータしかないとエラーになるためチェック
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        radar_values = np.append(radar_values, radar_values[0])  # 最後に最初の値を追加して閉じる
        angles.append(angles[0])  # 角度も閉じる

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, radar_values, color='blue', alpha=0.3)
        ax.plot(angles, radar_values, color='blue', linewidth=2)

        # ラベル設定
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(radar_labels, fontproperties=font_prop if font_prop else None)

        st.pyplot(fig)
    else:
        st.warning("レーダーチャートを作成するには、最低2つの項目が必要です。")