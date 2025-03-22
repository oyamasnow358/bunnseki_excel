import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_development_chart(file_path):
    # CSVデータの読み込み
    df = pd.read_csv(file_path)
    
    # 年ごとのデータが9年分あることを前提に整形
    years = [f'Year{i}' for i in range(1, 10)]
    df_long = df.melt(id_vars=['Category'], value_vars=years, 
                       var_name='Year', value_name='Score')
    
    # 年の順序を整理
    df_long['Year'] = df_long['Year'].str.extract(r'(\d+)').astype(int)
    df_long = df_long.sort_values(by=['Category', 'Year'])
    
    # 可視化
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_long, x='Year', y='Score', hue='Category', marker='o')
    plt.title('Development Chart Over 9 Years')
    plt.xlabel('Year')
    plt.ylabel('Score')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid()
    plt.show()
    
    return df_long
