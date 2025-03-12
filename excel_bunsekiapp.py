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

if len(data_frames) > 1:
    st.write("### 各時点のデータ")
    for i, df in enumerate(data_frames):
        st.write(f"#### {labels[i]}")
        st.dataframe(df)

    st.write("### 発達段階の推移（平均値）")

    common_columns = set(data_frames[0].columns)
    for df in data_frames[1:]:
        common_columns &= set(df.columns)

    common_columns = sorted(common_columns)

    averages = []
    for df in data_frames:
        avg = df[common_columns].mean(numeric_only=True).fillna(0)
        averages.append(avg)

    # 変化のあった項目を検出
    changes = {}
    for col in common_columns:
        values = [avg[col] for avg in averages]
        if max(values) - min(values) > 0:  # 変化があるかチェック
            changes[col] = values
    
    if changes:
        st.write("### 変化のあった項目")
        for col, values in changes.items():
            st.write(f"- **{col}**: {values}")

    selected_col = st.selectbox("表示する項目を選択", common_columns)

    plt.figure(figsize=(8, 5))
    try:
        plt.plot(labels, [avg[selected_col] for avg in averages], marker="o", label=selected_col)
    except KeyError:
        st.warning(f"列 '{selected_col}' が一部のデータに存在しません。")

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

        radar_values = latest_df.mean(numeric_only=True).fillna(0).values
        radar_labels = latest_df.columns

        if len(radar_values) == len(radar_labels):
            num_vars = len(radar_labels)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            radar_values = np.concatenate((radar_values, [radar_values[0]]))
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.fill(angles, radar_values, color='blue', alpha=0.3)
            ax.plot(angles, radar_values, color='blue', linewidth=2)

            ax.set_yticklabels([])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(radar_labels, fontproperties=font_prop if font_prop else None)

            st.pyplot(fig)
        else:
            st.warning("レーダーチャートのデータ数が一致しません。表示できません。")
else:
    st.info("少なくとも2つのファイルをアップロードすると、推移を分析できます。")