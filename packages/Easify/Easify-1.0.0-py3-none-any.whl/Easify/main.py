def print_preprocessing_code():
    code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
data = pd.read_csv('your_dataset.csv')  # Replace with your dataset file

# Checking for missing values
print("Missing values before handling:\\n", data.isnull().sum())

# Dropping rows with missing values
data_dropped = data.dropna()

# Replacing missing values with mean/median/mode
data['column_name'] = data['column_name'].fillna(data['column_name'].mean())  # Mean
data['column_name'] = data['column_name'].fillna(data['column_name'].median())  # Median
data['column_name'] = data['column_name'].fillna(data['column_name'].mode()[0])  # Mode

print("Missing values after handling:\\n", data.isnull().sum())

# Checking for duplicates
print("Number of duplicates:", data.duplicated().sum())

# Removing duplicates
data = data.drop_duplicates()

print("Duplicates after handling:", data.duplicated().sum())

# Replacing specific values
data['column_name'] = data['column_name'].replace('old_value', 'new_value')

# Replacing based on condition
data['column_name'] = data['column_name'].apply(lambda x: 'new_value' if x == 'condition' else x)

# Min-Max Scaling
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
data[['column1', 'column2']] = scaler.fit_transform(data[['column1', 'column2']])

# Log Transformation
data['log_column'] = np.log1p(data['numeric_column'])

# Square Root Transformation
data['sqrt_column'] = np.sqrt(data['numeric_column'])

# Box-Cox Transformation (requires positive values)
from scipy.stats import boxcox
data['boxcox_column'], _ = boxcox(data['numeric_column'] + 1)

# Label Encoding
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
data['categorical_column'] = le.fit_transform(data['categorical_column'])

# One-Hot Encoding
data = pd.get_dummies(data, columns=['categorical_column'])

# Plotting histogram
data['numeric_column'].plot(kind='hist', bins=30, edgecolor='black', title='Histogram')
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.show()

# Correlation Matrix
correlation_matrix = data.corr()

# Heatmap of Correlation Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap')
plt.show()
"""
    print(code)
