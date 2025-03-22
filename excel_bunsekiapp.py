import pandas as pd
import matplotlib.pyplot as plt
import io

def load_data_from_uploaded_files(uploaded_files, target_column):
    all_data = []

    for file in uploaded_files:
        if file is not None:
            try:
                # `UploadedFile` を `BytesIO` に変換
                df = pd.read_excel(io.BytesIO(file.getvalue()))

                if target_column in df.columns:
                    year = file.name.split('.')[0]  # "2015.xlsx" → "2015"
                    all_data.append((int(year), df[target_column].mean()))  # 平均値を取得
                else:
                    print(f"Warning: {file.name} に {target_column} が含まれていません")
            
            except Exception as e:
                print(f"Error: {file.name} の読み込みに失敗しました - {e}")

    # データフレーム化して年順にソート
    return pd.DataFrame(all_data, columns=['Year', 'Average']).sort_values(by='Year')

def plot_growth(data, target_column):
    plt.figure(figsize=(10, 5))
    plt.plot(data['Year'], data['Average'], marker='o', linestyle='-')
    plt.xlabel('Year')
    plt.ylabel('Average Score')
    plt.title(f'{target_column} Growth Over Time')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

# 使用例
import streamlit as st

st.title("Excel 分析アプリ")

uploaded_files = st.file_uploader("Excelファイルをアップロード", type=["xlsx"], accept_multiple_files=True)
target_column = "言語理解"  # 分析したい項目

if uploaded_files:
    data = load_data_from_uploaded_files(uploaded_files, target_column)
    if not data.empty:
        st.write("データのプレビュー:", data)
        st.pyplot(plot_growth(data, target_column))
    else:
        st.warning("データが見つかりませんでした")
