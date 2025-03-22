import pandas as pd
import matplotlib.pyplot as plt

def load_data_from_uploaded_files(uploaded_files, target_column):
    all_data = []

    for file in uploaded_files:
        if file is not None:
            df = pd.read_excel(file)

            if target_column in df.columns:
                year = file.name.split('.')[0]  # "2015.xlsx" → "2015"
                all_data.append((int(year), df[target_column].mean()))  # 平均値を取得
            else:
                print(f"Warning: {file.name} に {target_column} が含まれていません")

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
uploaded_files = [...]  # アップロードされたファイルのリスト（Streamlit などで取得）
target_column = "言語理解"  # 分析したい項目

data = load_data_from_uploaded_files(uploaded_files, target_column)
if not data.empty:
    plot_growth(data, target_column)
else:
    print("データが見つかりませんでした")