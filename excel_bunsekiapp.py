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

# 分析対象の項目リスト
valid_items = [
    "認知力・操作", "認知力・注意力", "集団参加", "生活動作", "言語理解", "表出言語", "記憶", "読字", "書字", "粗大運動", "微細運動", "数の概念"
]

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
if data_frames:
    common_columns = list(set.intersection(*(set(df.columns) for df in data_frames)) & set(valid_items))
else:
    common_columns = []

if not common_columns:
    st.error("共通する項目がありません。データのフォーマットを確認してください。")
else:
    averages = [df[common_columns].mean(numeric_only=True).fillna(0) for df in data_frames]

    # 表示する情報の選択
    display_option = st.selectbox("表示する情報を選択してください", ["段階", "項目", "現在の実態", "発達年齢"])
    selected_col = st.selectbox("表示する項目を選択してください", common_columns)

    # 変化があった項目を検出
    if len(averages) > 1:
        changes = {col: averages[-1][col] - averages[-2][col] for col in common_columns}
        changed_items = [col for col, diff in changes.items() if abs(diff) > 0]
        if changed_items:
            st.write("### 変化のあった項目")
            st.write(", ".join(changed_items))
        else:
            st.write("変化のあった項目はありません。")

    # 選択した項目のデータ取得
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

    # レーダーチャートの表示
    if data_frames:
        latest_df = data_frames[-1]  # 最後のデータを取得

        if not latest_df.empty:
            st.write("### 最新の発達段階（レーダーチャート）")

            # 数値データのみを抽出
            numeric_df = latest_df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                st.warning("レーダーチャートを作成するための数値データがありません。")
            else:
                radar_values = numeric_df.mean().values
                radar_labels = numeric_df.columns

                num_vars = len(radar_labels)

                if num_vars > 1:  # 1つのデータしかないとエラーになるためチェック
                    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                    radar_values = np.append(radar_values, radar_values[0])  # 最後に最初の値を追加
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
