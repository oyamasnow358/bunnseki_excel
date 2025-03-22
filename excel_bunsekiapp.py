import pandas as pd
import matplotlib.pyplot as plt
import os

def load_and_process_data(directory, selected_column):
    all_data = []
    years = []
    
    files = sorted([f for f in os.listdir(directory) if f.endswith('.xlsx')])
    
    for file in files:
        year = file.split('.')[0]  # Assume file name format contains the year
        df = pd.read_excel(os.path.join(directory, file))
        
        if selected_column in df.columns:
            mean_value = df[selected_column].mean()
            all_data.append(mean_value)
            years.append(year)
        else:
            print(f"Warning: {selected_column} not found in {file}")
    
    return years, all_data

def plot_growth_trend(years, data, selected_column):
    plt.figure(figsize=(10, 5))
    plt.plot(years, data, marker='o', linestyle='-', color='b')
    plt.xlabel("Year")
    plt.ylabel("Average Score")
    plt.title(f"Growth Trend of {selected_column}")
    plt.grid(True)
    plt.show()

# Example usage
directory = "path_to_excel_files"  # Update with actual path
selected_column = "言語理解"  # Change to desired analysis column
years, data = load_and_process_data(directory, selected_column)

if years and data:
    plot_growth_trend(years, data, selected_column)
else:
    print("No valid data found for analysis.")
