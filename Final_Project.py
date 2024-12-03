import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """
    Load data from a hardcoded CSV file.
    """
    file_path = r'C:\Users\Radio\CS 256\gym_members_exercise_tracking.csv'
    try:
        # Load the CSV file
        data = pd.read_csv(file_path)
        
        # Show dataset preview
        print("Dataset Preview:")
        print(data.head())  # Display the first few rows

        # Strip whitespace from column names
        data.columns = data.columns.str.strip()

        # Show column names after cleaning
        print("Cleaned Column Names:")
        print(data.columns)

        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def descriptive_stats(data, column):
    """
    Calculate basic statistics for a given column.
    """
    if column not in data.columns:
        print(f"Error: Column '{column}' not found in the dataset!")
        return None

    stats = {
        "Mean": np.mean(data[column]),
        "Median": np.median(data[column]),
        "Standard Deviation": np.std(data[column], ddof=1),
        "Variance": np.var(data[column], ddof=1),
        "Range": np.ptp(data[column])
    }
    return stats

def t_test(data, group_col, value_col):
    """
    Perform a two-sample t-test on the data.
    """
    if group_col not in data or value_col not in data:
        print(f"Error: '{group_col}' or '{value_col}' column not found in the dataset.")
        return None

    # Ensure there are exactly two groups
    groups = data[group_col].unique()
    if len(groups) != 2:
        print("Error: T-test requires exactly two groups.")
        return None

    # Extract values for each group
    group1 = data.loc[data[group_col] == groups[0], value_col]
    group2 = data.loc[data[group_col] == groups[1], value_col]

    # Perform the t-test
    t_stat, p_val = stats.ttest_ind(group1, group2)
    return t_stat, p_val


def anova(data, group_col, value_col):
    """
    Perform one-way ANOVA on the data.
    """
    if group_col not in data or value_col not in data:
        print(f"Error: '{group_col}' or '{value_col}' column not found.")
        return None

    # Extract data for each group
    groups = [group[value_col] for _, group in data.groupby(group_col)]

    # Perform ANOVA
    try:
        return stats.f_oneway(*groups)
    except Exception as e:
        print(f"Error performing ANOVA: {e}")
        return None

    """
    Here we will use this function to plot the data <-- Code I used in STATS 361/461
    """
def plot_data(data, group_col, value_col):
    """
    Visualize the data with boxplots and histograms.
    """
    sns.boxplot(x=group_col, y=value_col, data=data)
    plt.title(f"Boxplot of {group_col} vs {value_col}")
    plt.show()

    data[value_col].hist()
    plt.title(f"Histogram of {value_col}")
    plt.show()

if __name__ == "__main__":
    data = load_data()

    if data is not None:
        # Columns for descriptive stats
        columns = ["Age", "BMI", "Calories_Burned"]
        for column in columns:
            print(f"Descriptive Statistics for '{column}':")
            stats_result = descriptive_stats(data, column)
            if stats_result:
                print(stats_result)

        # Perform t-test
        print("T-Test Results (Gender vs BMI):")
        ttest_results = t_test(data, "Gender", "BMI")
        if ttest_results:
            print(f"T-statistic: {ttest_results[0]}, P-value: {ttest_results[1]}")

        # Perform ANOVA
        print("ANOVA Results (Workout_Type vs Calories_Burned):")
        anova_results = anova(data, "Workout_Type", "Calories_Burned")
        if anova_results:
            print(f"F-statistic: {anova_results[0]}, P-value: {anova_results[1]}")

        # Generate plots
        print("Generating Plots for 'Workout_Type' vs 'Calories_Burned'...")
        plot_data(data, "Workout_Type", "Calories_Burned")

