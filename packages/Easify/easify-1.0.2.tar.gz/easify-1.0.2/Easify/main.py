def print_preprocessing_code():
    code = """
Command to start jupyter notebook-> jupyter notebook

IMPORTANT LIBRARIES->
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
pip install mlxtend
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import seaborn as sns


Upload dataset on Jupyter notebook->
data = pd.read_csv('dataset.csv')  # Replace 'dataset.csv' with your file name

ASSIGNMENT 1---->
# 1. Display first 5 rows
data.head()

# 2. Display last 5 rows
data.tail()

# 3. Shape of the dataset
data.shape

# 4. Describe (summary statistics)
data.describe()

# 5. Info about the dataset
data.info()

# 6. Check for duplicates
data_clean = data.drop_duplicates()

# 7. Identify missing values
missing_values = data.isnull().sum()

# 8. Fill missing values with the mean of each column
data_filled_mean = data.fillna(data.mean())

# 9. Drop rows with missing values
data_dropped = data.dropna()

# 10. Statistical operations
data.mean()

#For considering only numeric values, example->
print("\nMean of Numerical Columns:\n", df.mean(numeric_only=True))
print("\nMedian of Numerical Columns:\n", df.median(numeric_only=True))
print("\nStandard Deviation of Numerical Columns:\n", df.std(numeric_only=True))






ASSIGNMENT 2---->
# Identify the missing values
missing_values = data.isnull().sum()

#  Ignore the missing values (drop rows)
# Drop rows with any NaN values
data_dropped_any = data.dropna()

# Drop rows with all NaN values
data_dropped_all = data.dropna(how='all')

# Drop rows with more than 2 NaN values
data_dropped_more_than_2 = data.dropna(thresh=len(data.columns)-2)

# Drop rows with NaN values in a specific column
data_dropped_column = data.dropna(subset=['column_name'])

# Use default values to handle missing data (e.g., '0')
data_filled_zero = data.fillna(0)

# Impute values using mean, median, etc.
data_filled_mean = data.fillna(data.mean())
data_filled_median = data.fillna(data.median())
data_filled_mode = data.fillna(data.mode().iloc[0])

# Identify Duplicates
duplicates = data.duplicated()

# Remove the duplicates
data_no_duplicates = data.drop_duplicates()



ASSIGNMENT 3---->
# Perform Pearson’s correlation analysis
correlation = data.corr(method='pearson')

# Display the correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()

# Perform data visualization
# Histogram
data['numeric_column'].hist(bins=30)
plt.title('Histogram')
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.show()

# Density Plot
sns.kdeplot(data['numeric_column'], shade=True)
plt.title('Density Plot')
plt.xlabel('Values')
plt.ylabel('Density')
plt.show()

# Boxplot
sns.boxplot(x=data['numeric_column'])
plt.title('Boxplot')
plt.show()

# Scatter Plot
sns.scatterplot(x=data['numeric_column'], y=data['other_numeric_column'])
plt.title('Scatter Plot')
plt.xlabel('Column 1')
plt.ylabel('Column 2')
plt.show()

# Scale data using Min/Max scaling
scaler_minmax = MinMaxScaler()
data['scaled_minmax'] = scaler_minmax.fit_transform(data[['numeric_column']])

# Scale data using Z-Score scaling
scaler_zscore = StandardScaler()
data['scaled_zscore'] = scaler_zscore.fit_transform(data[['numeric_column']])

# Smooth data using binning
binning = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')
data['binned_column'] = binning.fit_transform(data[['numeric_column']])

# Select and visualize the most significant features
X = data.drop(columns=['target_column'])
y = data['target_column']

selector = SelectKBest(f_classif, k=5)
X_new = selector.fit_transform(X, y)

# Visualize the selected features
selected_features = X.columns[selector.get_support()]
sns.barplot(x=selected_features, y=selector.scores_[selector.get_support()])
plt.title('Significant Features')
plt.show()



ASSIGNMENT 6---->
# Importing necessary libraries
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import seaborn as sns
import matplotlib.pyplot as plt

# Sample transaction dataset
dataset = [['milk', 'bread', 'butter'],
           ['bread', 'butter', 'jam'],
           ['milk', 'bread', 'butter', 'jam'],
           ['milk', 'bread'],
           ['butter', 'jam']]

# Convert the dataset into one-hot encoded format
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)

# Convert to DataFrame
df = pd.DataFrame(te_ary, columns=te.columns_)

# Display the one-hot encoded dataframe
print("One-hot encoded dataset:")
print(df)

# 1. Apply Apriori algorithm to find frequent itemsets with minimum support threshold of 0.5
frequent_itemsets = apriori(df, min_support=0.5, use_colnames=True)

# Display the frequent itemsets
print("\nFrequent Itemsets:")
print(frequent_itemsets)

# 2. Generate Association Rules from the frequent itemsets using confidence as metric
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# Display the association rules
print("\nAssociation Rules:")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift', 'conviction']])

# 3. Visualize the association rules with Lift vs Confidence
sns.scatterplot(x='confidence', y='lift', data=rules, hue='support', palette='viridis')
plt.title('Lift vs Confidence')
plt.xlabel('Confidence')
plt.ylabel('Lift')
plt.legend(title='Support')
plt.show()

# Additional visualization: Plot Support vs Confidence
sns.scatterplot(x='support', y='confidence', data=rules, hue='lift', palette='coolwarm')
plt.title('Support vs Confidence')
plt.xlabel('Support')
plt.ylabel('Confidence')
plt.legend(title='Lift')
plt.show()

# 4. Finding frequent itemsets
print("\nFrequent Itemsets with support >= 0.5:")
print(frequent_itemsets[frequent_itemsets['support'] >= 0.5])

# 5. For Closed Itemsets (extra logic required - comparing supports manually)
# A closed itemset is one where no proper superset has the same support
# Here we check for closed itemsets manually
closed_itemsets = []
for index, row in frequent_itemsets.iterrows():
    is_closed = True
    for other_index, other_row in frequent_itemsets.iterrows():
        if set(row['itemsets']).issubset(set(other_row['itemsets'])) and row['support'] == other_row['support']:
            if row['itemsets'] != other_row['itemsets']:
                is_closed = False
                break
    if is_closed:
        closed_itemsets.append(row)

print("\nClosed Itemsets:")
for itemset in closed_itemsets:
    print(itemset)



ASSIGNMENT 7---->
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the dataset (example with iris dataset, replace with your dataset)
from sklearn.datasets import load_iris
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# 2. Split the dataset into features (X) and target (y)
X = df.drop('target', axis=1)  # Features
y = df['target']  # Target variable

# 3. Split data into training and testing sets (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. Apply cross-validation to evaluate the models
# Logistic Regression
logreg = LogisticRegression(max_iter=1000)
logreg_cv = cross_val_score(logreg, X_train, y_train, cv=5)
print("Logistic Regression Cross-Validation Score:", logreg_cv.mean())

# Random Forest Classifier
rf = RandomForestClassifier()
rf_cv = cross_val_score(rf, X_train, y_train, cv=5)
print("Random Forest Cross-Validation Score:", rf_cv.mean())

# Support Vector Classifier (SVC)
svc = SVC()
svc_cv = cross_val_score(svc, X_train, y_train, cv=5)
print("SVC Cross-Validation Score:", svc_cv.mean())

# Naive Bayes
nb = GaussianNB()
nb_cv = cross_val_score(nb, X_train, y_train, cv=5)
print("Naive Bayes Cross-Validation Score:", nb_cv.mean())

# 5. Train the classifiers and make predictions

# Logistic Regression
logreg.fit(X_train, y_train)
logreg_pred = logreg.predict(X_test)

# Random Forest Classifier
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

# Support Vector Classifier (SVC)
svc.fit(X_train, y_train)
svc_pred = svc.predict(X_test)

# Naive Bayes
nb.fit(X_train, y_train)
nb_pred = nb.predict(X_test)

# 6. Evaluate the models with Accuracy, Precision, Recall, F1 Score, and Confusion Matrix

# Logistic Regression Evaluation
print("\nLogistic Regression Performance:")
print("Accuracy:", accuracy_score(y_test, logreg_pred))
print("Precision:", precision_score(y_test, logreg_pred, average='macro'))
print("Recall:", recall_score(y_test, logreg_pred, average='macro'))
print("F1 Score:", f1_score(y_test, logreg_pred, average='macro'))
print("Confusion Matrix:\n", confusion_matrix(y_test, logreg_pred))

# Random Forest Evaluation
print("\nRandom Forest Performance:")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print("Precision:", precision_score(y_test, rf_pred, average='macro'))
print("Recall:", recall_score(y_test, rf_pred, average='macro'))
print("F1 Score:", f1_score(y_test, rf_pred, average='macro'))
print("Confusion Matrix:\n", confusion_matrix(y_test, rf_pred))

# Support Vector Classifier Evaluation
print("\nSVC Performance:")
print("Accuracy:", accuracy_score(y_test, svc_pred))
print("Precision:", precision_score(y_test, svc_pred, average='macro'))
print("Recall:", recall_score(y_test, svc_pred, average='macro'))
print("F1 Score:", f1_score(y_test, svc_pred, average='macro'))
print("Confusion Matrix:\n", confusion_matrix(y_test, svc_pred))

# Naive Bayes Evaluation
print("\nNaive Bayes Performance:")
print("Accuracy:", accuracy_score(y_test, nb_pred))
print("Precision:", precision_score(y_test, nb_pred, average='macro'))
print("Recall:", recall_score(y_test, nb_pred, average='macro'))
print("F1 Score:", f1_score(y_test, nb_pred, average='macro'))
print("Confusion Matrix:\n", confusion_matrix(y_test, nb_pred))

# 7. Plot Confusion Matrices for better visualization

# Logistic Regression Confusion Matrix
plt.figure(figsize=(6,6))
sns.heatmap(confusion_matrix(y_test, logreg_pred), annot=True, fmt='d', cmap='Blues', xticklabels=data.target_names, yticklabels=data.target_names)
plt.title('Logistic Regression Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

# Random Forest Confusion Matrix
plt.figure(figsize=(6,6))
sns.heatmap(confusion_matrix(y_test, rf_pred), annot=True, fmt='d', cmap='Blues', xticklabels=data.target_names, yticklabels=data.target_names)
plt.title('Random Forest Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

# SVC Confusion Matrix
plt.figure(figsize=(6,6))
sns.heatmap(confusion_matrix(y_test, svc_pred), annot=True, fmt='d', cmap='Blues', xticklabels=data.target_names, yticklabels=data.target_names)
plt.title('SVC Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

# Naive Bayes Confusion Matrix
plt.figure(figsize=(6,6))
sns.heatmap(confusion_matrix(y_test, nb_pred), annot=True, fmt='d', cmap='Blues', xticklabels=data.target_names, yticklabels=data.target_names)
plt.title('Naive Bayes Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()




ASSIGNMENT 8->
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import seaborn as sns
import scipy.cluster.hierarchy as sch
from sklearn.datasets import make_blobs

# Step 1: Load/Create a Dataset
dataset, _ = make_blobs(n_samples=300, centers=3, random_state=42)

# Step 2: K-means Clustering
# Create K-means object with desired number of clusters (K=3)
kmeans = KMeans(n_clusters=3)

# Fit the K-means model to the dataset
kmeans.fit(dataset)

# Get cluster labels
labels = kmeans.labels_

# Get the centroids of the clusters
centroids = kmeans.cluster_centers_

# Step 3: Visualize K-means Clusters
plt.figure(figsize=(8, 6))
plt.scatter(dataset[:, 0], dataset[:, 1], c=labels, cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', s=200, c='red')  # Centroids in red
plt.title('K-means Clustering')
plt.show()

# Step 4: Performance Evaluation for K-means
# Inertia (Within-cluster sum of squares)
print("K-means Inertia:", kmeans.inertia_)

# Silhouette Score (Measure of clustering quality)
silhouette_avg = silhouette_score(dataset, labels)
print("Silhouette Score for K-means:", silhouette_avg)

# Step 5: Hierarchical Clustering
# Create Agglomerative Clustering object
hierarchical = AgglomerativeClustering(n_clusters=3)

# Fit the model and get cluster labels
labels_hierarchical = hierarchical.fit_predict(dataset)

# Step 6: Visualize Hierarchical Clustering (Dendrogram)
plt.figure(figsize=(10, 7))
dendrogram = sch.dendrogram(sch.linkage(dataset, method='ward'))
plt.title('Hierarchical Clustering Dendrogram')
plt.show()

# Step 7: Visualize Hierarchical Clusters
plt.figure(figsize=(8, 6))
plt.scatter(dataset[:, 0], dataset[:, 1], c=labels_hierarchical, cmap='viridis')
plt.title('Hierarchical Clustering')
plt.show()

# Step 8: Performance Evaluation for Hierarchical Clustering
# Silhouette Score for hierarchical clustering
silhouette_avg_hierarchical = silhouette_score(dataset, labels_hierarchical)
print("Silhouette Score for Hierarchical clustering:", silhouette_avg_hierarchical)
"""
    print(code)
