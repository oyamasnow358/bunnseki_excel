import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data_from_excel(folder_path, target_column):
    all_data = []
    
    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path)
            
            if target_column in df.columns:
                year = file.split('.')[0]  # ファイル名から年を取得（例: "2015.xlsx" → "2015"）
                all_data.append((year, df[target_column].mean()))  # 平均値を取得
            else:
                print(f"Warning: {file} に {target_column} が含まれていません")
    
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
folder_path = "./data"  # データフォルダのパス
target_column = "言語理解"  # 分析したい項目
data = load_data_from_excel(folder_path, target_column)
if not data.empty:
    plot_growth(data, target_column)
else:
    print("データが見つかりませんでした")
