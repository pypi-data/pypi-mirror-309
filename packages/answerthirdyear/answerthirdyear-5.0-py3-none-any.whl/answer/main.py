def dpv(num):
    if num == 1:
        print("""1. Load the dataset shooting.csv and perform below operation:
a. Print column names of dataset
b. Display the count of each unique value in armed and race attribute.
c. Identify the mean of “age” whose “armed” is “gun”
d. Group the dataset based on “manner_of_death” and “armed” and find mean of “latitude”
e. Perom Stack and unstack operation
Solution:
import pandas as pd
# Assuming you load your dataset as follows
# df = pd.read_csv("shooting.csv")
# Sample dataset creation for demonstration (remove this part when you load your own dataset)
data = {
'age': [34, 45, 23, 35, 29, 40],
'armed': ['gun', 'knife', 'gun', 'gun', 'unarmed', 'gun'],
'race': ['White', 'Black', 'Hispanic', 'White', 'Black', 'Hispanic'],
'manner_of_death': ['shot', 'shot and Tasered', 'shot', 'shot', 'shot', 'shot and Tasered'],
'latitude': [34.0522, 36.1699, 40.7128, 39.9526, 34.0522, 36.7783]
}
df = pd.DataFrame(data)
# 1. Print column names of the dataset
print("Column Names:", df.columns.tolist())
# 2. Display the count of each unique value in 'armed' and 'race' attributes
print("\nCount of each unique value in 'armed':")
print(df['armed'].value_counts())
print("\nCount of each unique value in 'race':")
print(df['race'].value_counts())
# 3. Identify the mean of "age" where "armed" is "gun"
mean_age_gun = df[df['armed'] == 'gun']['age'].mean()
print("\nMean age where 'armed' is 'gun':", mean_age_gun)
# 4. Group the dataset by "manner_of_death" and "armed" and find the mean of "latitude"
grouped_latitude_mean = df.groupby(['manner_of_death', 'armed'])['latitude'].mean()
print("\nMean of 'latitude' grouped by 'manner_of_death' and 'armed':")
print(grouped_latitude_mean)
# 5. Perform stack and unstack operations
stacked_df = df.stack()
print("\nStacked DataFrame:")
print(stacked_df)
unstacked_df = stacked_df.unstack()
print("\nUnstacked DataFrame:")
print(unstacked_df)""")

    elif num == 2:
        print("""2. Write a python program to diagnose the missing value in NO2_Location_B based on all numeric
attributes in airdata.csv using ptest and boxplot.
Solution:
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
# Load the dataset
df = pd.read_csv("airdata.csv")
# Sample data creation for demonstration (remove this part when you load your own dataset)
data = {
'NO2_Location_B': [20.5, None, 18.2, 21.1, None, 19.5, 22.3, None, 20.0, 21.7],
'Attribute1': [50, 52, 51, 53, 54, 52, 55, 56, 50, 53],
'Attribute2': [30.1, 30.5, 29.9, 30.2, 30.4, 30.3, 30.5, 30.6, 30.0, 30.3]
}
df = pd.DataFrame(data)
# Separate rows with and without missing values in NO2_Location_B
df_missing = df[df['NO2_Location_B'].isnull()]
df_not_missing = df[df['NO2_Location_B'].notnull()]
# 1. T-Test for numeric attributes between missing and non-missing NO2_Location_B groups
numeric_cols = df.select_dtypes(include='number').columns.drop('NO2_Location_B')
for col in numeric_cols:
stat, p_value = ttest_ind(df_missing[col], df_not_missing[col], nan_policy='omit')
print(f"T-test for {col}: p-value = {p_value:.4f}")
# 2. Boxplot to visualize distributions of each numeric attribute for missing and non-missing
NO2_Location_B
for col in numeric_cols:
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x=df['NO2_Location_B'].isnull(), y=col)
plt.title(f"Boxplot of {col} grouped by missing values in NO2_Location_B")
plt.xlabel("NO2_Location_B is Missing")
plt.ylabel(col)
plt.show()""")

    elif num == 3:
        print("""3. Consider Temperature_data.csv and Temperature_data1.csv. Identify the challenge and fix it and
then integrate the dataset.
Solution:
import pandas as pd
# Creating example datasets
data1 = {
'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
'City': ['Mumbai', 'Mumbai', 'Mumbai', 'Delhi', 'Delhi'],
'Temperature': [28, 27, 30, 18, 19]
}
data2 = {
'Date': ['2024-01-03', '2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09'],
'City': ['Mumbai', 'Delhi', 'Delhi', 'Chennai', 'Chennai'],
'Temperature': [30, 20, 21, 32, 33]
}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
# Merge the datasets
df_combined = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
# Convert 'Date' to datetime for sorting
df_combined['Date'] = pd.to_datetime(df_combined['Date'])
# Sort by Date
df_combined = df_combined.sort_values(by='Date')
# Display the integrated dataset
print(df_combined)""")

    elif num == 5:
        print("""5. Load kidney_disease and perform the following
a. Find the missing value in each column and overall count.
b. Remove duplicates in datasets
c. apply forward fill, backward fill, fillna methods to fill missing value
d. apply interpolate method to replace missing values
Solution:
import pandas as pd
# Load the dataset
df = pd.read_csv('kidney_disease.csv')
# 1. Find the Missing Value Count
# Column-wise missing values
missing_per_column = df.isnull().sum()
# Overall missing values
total_missing = df.isnull().sum().sum()
print("Missing values per column:\n", missing_per_column)
print("\nTotal missing values:", total_missing)
# 2. Remove Duplicates
df = df.drop_duplicates()
# 3. Apply Interpolation Method to Replace Missing Values
# Interpolate missing values based on the data (linear interpolation by default)
df_interpolated = df.interpolate()
# Verify if there are any remaining missing values
remaining_missing = df_interpolated.isnull().sum().sum()
print("\nTotal missing values after interpolation:", remaining_missing)
# Display the interpolated data
print("\nData after interpolation:\n", df_interpolated.head())""")

    elif num == 6:
        print("""6. Write a python program to find outliers in the time series dataset CustomerEnteries. Deal the
outliers with log transformation.
Solution:
import pandas as pd
import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
# Load the dataset
# Assuming a CSV file with a column 'entries' for the customer entries data
data = pd.read_csv("CustomerEntries.csv")
# Plot original data
plt.figure(figsize=(12, 6))
plt.plot(data['entries'], label="Original Data")
plt.title("Customer Entries - Original Data")
plt.legend()
plt.show()
# Detecting outliers using Z-score
data['z_score'] = zscore(data['entries'])
threshold = 3 # Define a Z-score threshold for outliers
outliers = data[np.abs(data['z_score']) > threshold]
# Display outliers
print("Outliers in the dataset:")
print(outliers)
# Handling outliers with log transformation
data['log_entries'] = np.log1p(data['entries']) # log1p handles zero values
# Plot transformed data
plt.figure(figsize=(12, 6))
plt.plot(data['log_entries'], label="Log Transformed Data")
plt.title("Customer Entries - Log Transformed")
plt.legend()
plt.show()
# Cleanup (drop the z-score column)
data.drop(columns=['z_score'], inplace=True)""")

    elif num == 7:
        print("""7. Write a python program to detect the bivariate outlier between Height and gender of response.csv
dataset and deal it by replace with the upper cap or lower cap.
Solution:
import pandas as pd
import numpy as np
# Load the dataset
data = pd.read_csv("response.csv")
# Check initial data structure
print(data.head())
# Define a function to handle outliers within each gender category
def cap_outliers(df, column):
# Calculate Q1, Q3, and IQR
Q1 = df[column].quantile(0.25)
Q3 = df[column].quantile(0.75)
IQR = Q3 - Q1
# Define the upper and lower bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
# Cap outliers with the lower and upper bounds
df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
return df
# Apply outlier capping separately for each gender
data = data.groupby("Gender").apply(lambda x: cap_outliers(x, "Height"))
# Display results
print("Data after capping outliers:")
print(data)
# Optional: save the processed data to a new CSV file
data.to_csv("response_processed.csv", index=False)""")

    elif num == 8:
        print("""8. Consider the two sources of data Electricity Data 2016_2017 was retrieved from the local
electricity provider that holds the electricity consumption and Temperature 2016.csv was retrieved
from the local weather station and includes temperature. Deal with data cleaning issues and analyze
how the amount of electricity consumption is affected by the weather using data fusion technique.
Solution:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
# Step 1: Load the data
electricity_data = pd.read_csv("Electricity_Data_2016_2017.csv")
temperature_data = pd.read_csv("Temperature_2016.csv")
# Step 2: Data Cleaning
# Check for missing values
print(electricity_data.isnull().sum())
print(temperature_data.isnull().sum())
# Fill or drop missing values as necessary
electricity_data = electricity_data.fillna(method='ffill') # Forward fill as an example
temperature_data = temperature_data.fillna(method='ffill')
# Check if there are duplicates and drop them
electricity_data = electricity_data.drop_duplicates()
temperature_data = temperature_data.drop_duplicates()
# Ensure time consistency (if both have a time column like 'Date')
electricity_data['Date'] = pd.to_datetime(electricity_data['Date'])
temperature_data['Date'] = pd.to_datetime(temperature_data['Date'])
# Step 3: Data Fusion - Merge the datasets based on 'Date'
merged_data = pd.merge(electricity_data, temperature_data, on='Date', how='inner')
# Step 4: Exploratory Data Analysis (EDA)
# Visualizing the relationship between electricity consumption and temperature
plt.figure(figsize=(10, 6))
plt.scatter(merged_data['Temperature'], merged_data['ElectricityConsumption'], alpha=0.6)
plt.title("Electricity Consumption vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Electricity Consumption (kWh)")
plt.show()
# Check correlation between temperature and electricity consumption
correlation = merged_data[['Temperature', 'ElectricityConsumption']].corr()
print("Correlation between Temperature and Electricity Consumption:")
print(correlation)
# Step 5: Modeling - Predicting electricity consumption using temperature
X = merged_data[['Temperature']] # Features
y = merged_data['ElectricityConsumption'] # Target
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)
# Predicting the electricity consumption
y_pred = model.predict(X_test)
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
# Plot the predicted vs actual values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.title("Actual vs Predicted Electricity Consumption")
plt.xlabel("Actual Consumption")
plt.ylabel("Predicted Consumption")
plt.show()
# Step 6: Conclusion
# Model interpretation
print("Linear Regression Coefficients:")
print(f"Intercept: {model.intercept_}")
print(f"Slope (Temperature coefficient): {model.coef_[0]}")
# From the slope, we can determine how temperature affects electricity consumption.
""")

    elif num == 9:
        print("""9. Consider the churn.csv dataset; normalize the attribute and finding the best subset of independent
attributes using KNN.
Solution:
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
# Step 1: Load the dataset
data = pd.read_csv("churn.csv")
# Step 2: Data Preprocessing
# Check for missing values
print(data.isnull().sum())
# Handle missing values (e.g., by filling with median or dropping)
data = data.dropna() # Alternatively, use fillna(data.median()) to fill missing values
# If categorical features exist, apply encoding (example for binary encoding)
data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1}) # Example of encoding
# Assuming 'Churn' is the target column and other columns are features
X = data.drop(columns=['Churn'])
y = data['Churn']
# Step 3: Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Step 4: Feature Selection - Using SelectKBest with ANOVA F-test
selector = SelectKBest(f_classif, k='all') # Select all features initially
selector.fit(X_scaled, y)
# Get the scores of each feature
scores = pd.DataFrame(selector.scores_, index=X.columns, columns=["Score"])
print("Feature Scores:")
print(scores.sort_values(by='Score', ascending=False))
# Step 5: Select top k features based on scores
k = 5 # Number of top features to select (can be adjusted)
selector = SelectKBest(f_classif, k=k)
X_selected = selector.fit_transform(X_scaled, y)
# Step 6: Train KNN Model using the selected features
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)
# Create KNN model
knn = KNeighborsClassifier(n_neighbors=5)
# Train the model
knn.fit(X_train, y_train)
# Evaluate the model
y_pred = knn.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
# Step 7: Cross-validation (optional) to check model's performance
cv_scores = cross_val_score(knn, X_selected, y, cv=5)
print(f"Cross-validation scores: {cv_scores}")
print(f"Average CV score: {np.mean(cv_scores)}")""")

    elif num == 10:
        print("""10. Load the dataset index.csv and perform listed data transformation:
a. Binary coding b. Ranking transformation
c. Discretization d. Log transformation
Solution:
import pandas as pd
import numpy as np
# Step 1: Load the dataset
data = pd.read_csv("index.csv")
# Display first few rows of the dataset to understand its structure
print("Original Data:")
print(data.head())
# Step 2: Binary Coding (for categorical variables with two categories)
# Assume there is a column called 'Category' with values 'Yes' and 'No'
if 'Category' in data.columns:
data['Category'] = data['Category'].map({'Yes': 1, 'No': 0})
print("\nData after Binary Coding:")
print(data[['Category']].head())
# Step 3: Ranking Transformation (rank numerical columns)
# Assuming we want to apply ranking transformation on 'Score' column
if 'Score' in data.columns:
data['Score_rank'] = data['Score'].rank()
print("\nData after Ranking Transformation:")
print(data[['Score', 'Score_rank']].head())
# Step 4: Discretization (binning continuous data)
# Discretizing the 'Age' column into categories ('Young', 'Middle-aged', 'Old')
if 'Age' in data.columns:
bins = [0, 25, 50, 100] # Define age bins
labels = ['Young', 'Middle-aged', 'Old']
data['Age_category'] = pd.cut(data['Age'], bins=bins, labels=labels)
print("\nData after Discretization:")
print(data[['Age', 'Age_category']].head())
# Step 5: Log Transformation (applied to numerical columns)
# Apply log transformation to 'Salary' (assuming Salary is a numerical column)
if 'Salary' in data.columns:
# Applying log transformation (adding a small constant to avoid log(0) error)
data['Salary_log'] = np.log1p(data['Salary']) # log1p is log(1+x) to avoid log(0)
print("\nData after Log Transformation:")
print(data[['Salary', 'Salary_log']].head())
# Save the transformed data (optional)
data.to_csv("index_transformed.csv", index=False)""")

    elif num == 11:
        print("""11. Consider the below data Test Data:
School_code class_name name dob
0 s001 v Alberto Franco 15/05/2002
1 s002 vi Gino Mcneill 17/05/2002
2 s003 v Ryan Parkes 16/02/1999
3 s001 v Eesha Hinton 15/09/1997
a. Create a pandas dataframe for the above data
b. Display the value “Gino Mcneill ”
c. Display the student name who belong to school_code s001
d. Rename column as date_Of_Birth as DOB
e. Write a Pandas program to display the default index and set a column as an Index in a
given dataframe.
Solution:
import pandas as pd
# Step 1: Create a pandas DataFrame
data = {
'School_code': ['s001', 's002', 's003', 's001'],
'class_name': ['v', 'vi', 'v', 'v'],
'name': ['Alberto Franco', 'Gino Mcneill', 'Ryan Parkes', 'Eesha Hinton'],
'dob': ['15/05/2002', '17/05/2002', '16/02/1999', '15/09/1997']
}
# Create DataFrame
df = pd.DataFrame(data)
# Step 2: Display the value “Gino Mcneill”
gino_name = df[df['name'] == 'Gino Mcneill']
print("Display 'Gino Mcneill':")
print(gino_name)
# Step 3: Display the student names who belong to school_code 's001'
school_s001 = df[df['School_code'] == 's001']
print("\nStudents belonging to school_code 's001':")
print(school_s001['name'])
# Step 4: Rename column 'dob' as 'DOB'
df.rename(columns={'dob': 'DOB'}, inplace=True)
print("\nDataFrame after renaming column 'dob' to 'DOB':")
print(df)
# Step 5: Display the default index and set a column as an Index
print("\nDataFrame with default index:")
print(df)
# Set 'name' column as the index
df.set_index('name', inplace=True)
print("\nDataFrame after setting 'name' as the index:")
print(df)""")

    elif num == 12:
        print("""12. i)Draw horizontal boxplot of all the numerical columns of adult.csv dataset in plot, set the figure
size, give title for each of them.
Solution:
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Step 1: Load the dataset
df = pd.read_csv('adult.csv')
# Step 2: Select only the numerical columns
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
# Step 3: Set the figure size for the plots
plt.figure(figsize=(10, 6))
# Step 4: Create a horizontal boxplot for each numerical column
for col in numerical_columns:
plt.figure(figsize=(10, 4)) # Set figure size for each boxplot
sns.boxplot(x=df[col])
plt.title(f'Boxplot of {col}') # Title for each plot
plt.show()
ii) Write the python program for the following
a. Create a 3x3 matrix with values ranging from 2 to 11 using numpy
b. Check the dimension, size and shape of the array
c. slice the array to get the first two rows and columns
d. Find the median of array along X-axis
e. create a null vector of size 10 and update the sixth value to 11
Solution:
import numpy as np
# Step 1: Create a 3x3 matrix with values ranging from 2 to 11
matrix = np.arange(2, 11).reshape(3, 3)
# Step 2: Check the dimension, size, and shape of the array
dimension = matrix.ndim # Dimension of the array
size = matrix.size # Number of elements in the array
shape = matrix.shape # Shape of the array
# Step 3: Slice the array to get the first two rows and columns
sliced_array = matrix[:2, :2]
# Step 4: Find the median of the array along the X-axis (axis=1)
median_x_axis = np.median(matrix, axis=1)
# Step 5: Create a null vector of size 10 and update the sixth value to 11
null_vector = np.zeros(10)
null_vector[5] = 11
# Output the results
print("3x3 Matrix:\n", matrix)
print("\nDimension of the array:", dimension)
print("Size of the array:", size)
print("Shape of the array:", shape)
print("\nSliced Array (first two rows and columns):\n", sliced_array)
print("\nMedian along X-axis:", median_x_axis)
print("\nNull Vector with updated value:\n", null_vector)""")

    elif num == 13:
        print("""13. i)Write Python code to display dataset adult.csv using histogram and boxplot of Matplotlib
visualizations. Show visualization before and after standardization of the dataset.
Solution:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
# Step 1: Load the dataset
df = pd.read_csv('adult.csv')
# Step 2: Select only numerical columns for visualization
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
# Step 3: Plot histograms before standardization
plt.figure(figsize=(12, 8))
for i, col in enumerate(numerical_columns, 1):
plt.subplot(2, 3, i)
df[col].hist(bins=20, edgecolor='black')
plt.title(f'Histogram of {col}')
plt.xlabel(col)
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
# Step 4: Plot boxplots before standardization
plt.figure(figsize=(12, 8))
for i, col in enumerate(numerical_columns, 1):
plt.subplot(2, 3, i)
sns.boxplot(x=df[col])
plt.title(f'Boxplot of {col}')
plt.xlabel(col)
plt.tight_layout()
plt.show()
# Step 5: Standardize the numerical columns
scaler = StandardScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
# Step 6: Plot histograms after standardization
plt.figure(figsize=(12, 8))
for i, col in enumerate(numerical_columns, 1):
plt.subplot(2, 3, i)
df[col].hist(bins=20, edgecolor='black')
plt.title(f'Histogram of {col} (Standardized)')
plt.xlabel(col)
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
# Step 7: Plot boxplots after standardization
plt.figure(figsize=(12, 8))
for i, col in enumerate(numerical_columns, 1):
plt.subplot(2, 3, i)
sns.boxplot(x=df[col])
plt.title(f'Boxplot of {col} (Standardized)')
plt.xlabel(col)
plt.tight_layout()
plt.show()
ii) Write the python code to
a. Create an array with values ranging from 100 to 125
b. Find the number of rows and columns in the array
c. Find the mean of the array
d. Square each element of the array and display it
Solution:
import numpy as np
# Step 1: Create an array with values ranging from 100 to 125
array = np.arange(100, 126)
# Step 2: Find the number of rows and columns in the array (for a 1D array, it's just the number of
elements)
rows, cols = array.shape[0], 1 # Array is 1D, so number of rows is the size of the array and cols is 1
# Step 3: Find the mean of the array
mean_value = np.mean(array)
# Step 4: Square each element of the array and display it
squared_array = np.square(array)
# Output the results
print("Array:", array)
print("Number of Rows:", rows)
print("Number of Columns:", cols)
print("Mean of the Array:", mean_value)
print("Squared Array:", squared_array)""")

    elif num == 14:
        print("""14. i)Write Python code to plot amazonstock.csv and applestock.csv dataset’s close attribute to
observer trends between them in single lineplot, add relevant legend, label the axis and give title.
Solution:
import pandas as pd
import matplotlib.pyplot as plt
# Step 1: Load the datasets
amazon_df = pd.read_csv('amazonstock.csv')
apple_df = pd.read_csv('applestock.csv')
# Step 2: Extract the 'Close' attribute
amazon_close = amazon_df['Close']
apple_close = apple_df['Close']
# Step 3: Plot the data
plt.figure(figsize=(10, 6))
# Plot Amazon stock close price
plt.plot(amazon_df['Date'], amazon_close, label='Amazon', color='blue')
# Plot Apple stock close price
plt.plot(apple_df['Date'], apple_close, label='Apple', color='red')
# Step 4: Add labels and title
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Amazon vs Apple Stock Close Price Trends')
plt.legend()
# Display the plot
plt.xticks(rotation=45) # Rotate the x-axis labels for better readability
plt.tight_layout() # Adjust layout to prevent label overlap
plt.show()
ii) Write a Pandas program
a. to convert a dictionary to a Pandas series. {'a': 100, 'b': 200, 'c': 300, 'd': 400, 'e': 800}
b. convert series to datafram
c. crate new attribute and insert value for them
d. display the column names
e. change value 200 to 500
Solution:
import pandas as pd
# Step 1: Convert a dictionary to a Pandas Series
data_dict = {'a': 100, 'b': 200, 'c': 300, 'd': 400, 'e': 800}
series = pd.Series(data_dict)
# Step 2: Convert the Series to a DataFrame
df = series.to_frame(name='Value')
# Step 3: Create a new attribute and insert values
df['New_Attribute'] = ['X', 'Y', 'Z', 'W', 'V']
# Step 4: Display the column names
print("Column Names:", df.columns)
# Step 5: Change value 200 to 500 in the 'Value' column
df['Value'] = df['Value'].replace(200, 500)
# Display the updated DataFrame
print("\nUpdated DataFrame:")
print(df)""")

    elif num == 15:
        print("""15. Write a Pandas code:
a. to create pandas for the dictionary
school= { 'school_code': ['s001','s002','s003','s001','s002','s004'],
'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill',
'David Parkes'],
'date_of_birth':['15/05/2002','17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/0
9/1997'],
'weight': [35, 32, 33, 30, 31, 32]}
b. to display the default index and set a column as an Index in a given dataframe.
c. to convert index of a given dataframe into a column.
d. to create a dataframe and set a title or name of the index column.
e. to split the following dataframe into groups based on school code. Also check the type of
GroupBy object.
Solution:
import pandas as pd
# Step 1: Create a DataFrame from the given dictionary
school = {
'school_code': ['s001', 's002', 's003', 's001', 's002', 's004'],
'class': ['V', 'V', 'VI', 'VI', 'V', 'VI'],
'name': ['Alberto Franco', 'Gino Mcneill', 'Ryan Parkes', 'Eesha Hinton', 'Gino Mcneill', 'David
Parkes'],
'date_of_birth': ['15/05/2002', '17/05/2002', '16/02/1999', '25/09/1998', '11/05/2002', '15/09/1997'],
'weight': [35, 32, 33, 30, 31, 32]
}
df = pd.DataFrame(school)
# Step 2: Display the default index (RangeIndex)
print("DataFrame with Default Index:")
print(df)
print("\n")
# Step 3: Set 'school_code' column as the index
df.set_index('school_code', inplace=True)
print("DataFrame with 'school_code' as the index:")
print(df)
print("\n")
# Step 4: Convert the index back to a column
df_reset = df.reset_index()
print("DataFrame after resetting the index into a column:")
print(df_reset)
print("\n")
# Step 5: Set a name for the index column
df_reset.set_index('school_code', inplace=True)
df_reset.index.name = 'School_Index'
print("DataFrame with Index Column Named:")
print(df_reset)
print("\n")
# Step 6: Group the DataFrame by 'school_code' and display the group type
grouped = df_reset.groupby('school_code')
print("Type of GroupBy object:", type(grouped))
print("\nGroups based on 'school_code':")
for school_code, group in grouped:
print(f"\nGroup for {school_code}:")
print(group)""")

    elif num == 16:
        print("""16. Write a Pandas program
a. Crate a dataset for the dictionary
exam_data = {'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael',
'Matthew', 'Laura', 'Kevin', 'Jonas'],
'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']}
b. to calculate the median of all students' scores. Data is stored in a dataframe.
c. to change the name 'James' to 'John' in name column of the DataFrame.
d. to to select the rows where number of attempts in the examination is less than 1 and score
greater than 14.
e. to sort the data frame first by 'name', then by 'score' in ascending order.
Solution:
import pandas as pd
import numpy as np
# Step 1: Create a DataFrame from the given dictionary
exam_data = {
'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin',
'Jonas'],
'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']
}
df = pd.DataFrame(exam_data)
# Step 2: Calculate the median of all students' scores (excluding NaN values)
median_score = df['score'].median()
print(f"Median of all students' scores: {median_score}\n")
# Step 3: Change the name 'James' to 'John' in the 'name' column
df['name'] = df['name'].replace('James', 'John')
print("DataFrame after changing 'James' to 'John':")
print(df, "\n")
# Step 4: Select rows where number of attempts is less than 1 and score greater than 14
# Since attempts can't be less than 1, we'll select attempts >= 1 and score > 14 for the condition.
filtered_rows = df[(df['attempts'] >= 1) & (df['score'] > 14)]
print("Rows where attempts >= 1 and score > 14:")
print(filtered_rows, "\n")
# Step 5: Sort the DataFrame first by 'name', then by 'score' in ascending order
sorted_df = df.sort_values(by=['name', 'score'], ascending=[True, True])
print("DataFrame sorted by 'name' and 'score' in ascending order:")
print(sorted_df)""")

    elif num == 17:
        print("""17. Load the dataset adult.csv and perform below operation:
a. Make column name codeable and display it
b. create a multi Index based on “race” and “sex” and display its count
c. display the content using wide form and long form
d. calculate the mean and median age of people with preschool education
e. display the Capital Gain of individuals whose education is less than 10 years
Solution:
import pandas as pd
# Step 1: Load the dataset
df = pd.read_csv('adult.csv')
# Step 2: Make column names codeable (cleaning column names)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
# Display the cleaned column names
print("Cleaned Column Names:")
print(df.columns)
print("\n")
# Step 3: Create a Multi-Index based on 'race' and 'sex', and display its count
df.set_index(['race', 'sex'], inplace=True)
print("Multi-Index DataFrame (race, sex):")
print(df.groupby(['race', 'sex']).size())
print("\n")
# Step 4: Display content in wide form and long form
# Wide form is the default, so let's display the first 5 rows of the DataFrame
print("Wide Form (first 5 rows of original DataFrame):")
print(df.head())
print("\n")
# Long form: use pd.melt() to unpivot the data
long_form = pd.melt(df.reset_index(), id_vars=['race', 'sex'], var_name='attribute',
value_name='value')
print("Long Form (melted DataFrame):")
print(long_form.head())
print("\n")
# Step 5: Calculate the mean and median age of people with preschool education
preschool_education = df[df['education'] == 'Preschool']
mean_age_preschool = preschool_education['age'].mean()
median_age_preschool = preschool_education['age'].median()
print(f"Mean age of people with preschool education: {mean_age_preschool}")
print(f"Median age of people with preschool education: {median_age_preschool}")
print("\n")
# Step 6: Display Capital Gain of individuals whose education is less than 10 years
# Assuming 'education' values that are less than 10 years would be '10th', '11th', '12th', 'HS-grad', etc.
education_less_than_10 = df[df['education'].isin(['10th', '11th', '12th', 'HS-grad'])]
capital_gain_less_than_10 = education_less_than_10[['capital_gain']]
print("Capital Gain of individuals whose education is less than 10 years:")
print(capital_gain_less_than_10)""")

    elif num == 18:
        print("""18. Write a python cod to unpack the ReadingDateTime feature of Temperature_data.csv into date
and time and then remove time attribute, and then integrate Temperature_data2.csv
Solution:
import pandas as pd
# Step 1: Load the Temperature_data.csv dataset
temperature_data = pd.read_csv('Temperature_data.csv')
# Step 2: Unpack the ReadingDateTime feature into separate date and time columns
# Convert 'ReadingDateTime' to datetime type
temperature_data['ReadingDateTime'] = pd.to_datetime(temperature_data['ReadingDateTime'])
# Extract date and time from the 'ReadingDateTime' column
temperature_data['Date'] = temperature_data['ReadingDateTime'].dt.date
temperature_data['Time'] = temperature_data['ReadingDateTime'].dt.time
# Step 3: Remove the time attribute (drop the 'Time' column)
temperature_data = temperature_data.drop(columns=['Time'])
# Step 4: Load the Temperature_data2.csv dataset
temperature_data2 = pd.read_csv('Temperature_data2.csv')
# Step 5: Integrate the two datasets (assuming both datasets have a common key like 'Date')
# Merge the two datasets based on the 'Date' column (adjust the key if necessary)
merged_data = pd.merge(temperature_data, temperature_data2, on='Date', how='inner')
# Display the integrated DataFrame
print("Integrated DataFrame:")
print(merged_data.head())""")

    elif num == 19:
        print("""19. Write a python program to unpack the column Datetime in airdata.csv and diagonise the missing
value based on all categorical attribute using bar plot.
Solution:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Step 1: Load the airdata.csv dataset
airdata = pd.read_csv('airdata.csv')
# Step 2: Unpack the 'Datetime' column into separate 'Date' and 'Time' columns
# Convert the 'Datetime' column to datetime type
airdata['Datetime'] = pd.to_datetime(airdata['Datetime'])
# Extract 'Date' and 'Time' from 'Datetime'
airdata['Date'] = airdata['Datetime'].dt.date
airdata['Time'] = airdata['Datetime'].dt.time
# Step 3: Diagnose missing values for all categorical attributes
# Identify categorical columns in the dataset
categorical_columns = airdata.select_dtypes(include=['object', 'category']).columns
# Create a bar plot to show missing values for each categorical attribute
missing_values = airdata[categorical_columns].isnull().sum()
missing_values = missing_values[missing_values > 0] # Only show columns with missing values
# Plotting missing values using bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x=missing_values.index, y=missing_values.values, palette='viridis')
plt.title('Missing Values in Categorical Columns')
plt.xlabel('Categorical Columns')
plt.ylabel('Number of Missing Values')
plt.xticks(rotation=45)
plt.show()""")

    elif num == 20:
        print("""20. Load MFGEmployees dataset and perform the following
a. replace zero as nan
b. remove duplicates
c. find the missing value in each column and overall count.
d. apply mean, median and mode to replace the missing value
Solution:
import pandas as pd
import numpy as np
# Step 1: Load the MFGEmployees dataset
mfg_data = pd.read_csv('MFGEmployees.csv')
# Step 2: Replace zeros with NaN
mfg_data.replace(0, np.nan, inplace=True)
# Step 3: Remove duplicates
mfg_data.drop_duplicates(inplace=True)
# Step 4: Find missing values in each column and overall count
missing_values_per_column = mfg_data.isnull().sum()
total_missing_values = missing_values_per_column.sum()
# Display missing values and overall count
print("Missing values per column:")
print(missing_values_per_column)
print(f"Total missing values in the dataset: {total_missing_values}")
# Step 5: Apply mean, median, and mode to replace missing values
# For numerical columns, we apply different strategies to replace missing values
for column in mfg_data.select_dtypes(include=['float64', 'int64']).columns:
if mfg_data[column].isnull().sum() > 0:
# Replacing missing values with mean, median, and mode
mean_value = mfg_data[column].mean()
median_value = mfg_data[column].median()
mode_value = mfg_data[column].mode()[0] # Mode returns a series, we take the first value
print(f"Replacing missing values in '{column}':")
print(f"Mean: {mean_value}, Median: {median_value}, Mode: {mode_value}")
# Option 1: Replacing missing values with mean
mfg_data[column].fillna(mean_value, inplace=True)
# Option 2: Alternatively, you can choose median or mode to fill missing values
# mfg_data[column].fillna(median_value, inplace=True)
# mfg_data[column].fillna(mode_value, inplace=True)
# Display the cleaned dataset
print("Cleaned dataset:")
print(mfg_data.head())""")

    elif num == 21:
        print("""21. Write a python program to detect univariate outliers in all numeric columns in populations and
deal it by removing data objects with outliers
Solution:
import pandas as pd
# Step 1: Load the dataset
populations = pd.read_csv('populations.csv')
# Step 2: Detect outliers using IQR for all numeric columns
numeric_columns = populations.select_dtypes(include=['float64', 'int64']).columns
# Function to remove outliers using IQR
def remove_outliers(df, column):
Q1 = df[column].quantile(0.25)
Q3 = df[column].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
# Remove rows where the column value is outside the bounds
return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
# Apply the function to all numeric columns to remove outliers
for column in numeric_columns:
populations = remove_outliers(populations, column)
# Step 3: Display the cleaned dataset
print("Cleaned dataset (after removing outliers):")
print(populations.head())""")

    elif num == 22:
        print("""22. Write a python program to detect the bivariate outlier between weight and age of response.csv
dataset and replace with median value.
import pandas as pd
import numpy as np
from scipy.stats import zscore
# Step 1: Load the dataset
df = pd.read_csv('response.csv')
# Step 2: Calculate Z-scores for weight and age columns
df['z_weight'] = zscore(df['weight'])
df['z_age'] = zscore(df['age'])
# Step 3: Detect outliers
# Set the threshold for outlier detection (commonly 3 for Z-scores)
threshold = 3
# Identify outliers where the Z-score is above or below the threshold
outliers_weight = df['z_weight'].abs() > threshold
outliers_age = df['z_age'].abs() > threshold
# Combine the two conditions (outlier in either weight or age)
outliers = outliers_weight | outliers_age
# Step 4: Replace outliers with the median of the respective columns
df.loc[outliers, 'weight'] = df['weight'].median()
df.loc[outliers, 'age'] = df['age'].median()
# Drop the Z-score columns as they are no longer needed
df.drop(columns=['z_weight', 'z_age'], inplace=True)
# Step 5: Display the cleaned dataset
print("Cleaned dataset (after replacing bivariate outliers):")
print(df.head())""")

    elif num == 23:
        print("""23. Create a dataframe emp.csv with columns rollno, emp_name, branch, salary with atleast five
entries and create another dataframe empdetails.csv with columns dateofbirth, address, and
mobilenumber for the employees in emp.csv. Apply data integration technique to integrate
empdetails.csv into emp.csv dataset. Plot all numeric columns using boxplot in single graph
Solution:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Step 1: Create emp.csv DataFrame
data_emp = {
'rollno': [101, 102, 103, 104, 105],
'emp_name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
'branch': ['IT', 'HR', 'Finance', 'IT', 'HR'],
'salary': [60000, 45000, 70000, 50000, 55000]
}
emp_df = pd.DataFrame(data_emp)
# Save to emp.csv
emp_df.to_csv('emp.csv', index=False)
# Step 2: Create empdetails.csv DataFrame
data_empdetails = {
'emp_name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
'dateofbirth': ['1990-05-10', '1985-09-20', '1988-02-15', '1992-11-10', '1989-07-12'],
'address': ['123 St, City A', '456 Ave, City B', '789 Rd, City C', '101 Blvd, City D', '202 Ln, City E'],
'mobilenumber': ['123-456-7890', '987-654-3210', '555-123-4567', '444-333-2222', '999-888-7777']
}
empdetails_df = pd.DataFrame(data_empdetails)
# Save to empdetails.csv
empdetails_df.to_csv('empdetails.csv', index=False)
# Step 3: Perform Data Integration (Merge empdetails.csv into emp.csv)
# Merge on 'emp_name' column
integrated_df = pd.merge(emp_df, empdetails_df, on='emp_name')
# Step 4: Plot all numeric columns using a boxplot
# Select only numeric columns for plotting
numeric_cols = integrated_df.select_dtypes(include=[np.number]).columns
# Plot boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(data=integrated_df[numeric_cols])
plt.title('Boxplot of Numeric Columns')
plt.show()
# Display the integrated DataFrame
print("Integrated DataFrame:")
print(integrated_df)""")

    elif num == 24:
        print("""24. Consider Churn.csv dataset normalize the dataset numerical values and then apply random forest
to identify the relative importance of each attribute in the classification of customer churn. Plot the
result using bar plot.
Solution:
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
# Step 1: Load the Churn dataset
df = pd.read_csv('Churn.csv')
# Step 2: Identify numerical columns and normalize them
# Assuming the target variable is 'Churn' and the rest are features
numerical_cols = df.select_dtypes(include=[np.number]).columns
X = df[numerical_cols].drop('Churn', axis=1, errors='ignore') # Drop target if it's a numerical column
y = df['Churn'] if 'Churn' in df.columns else None
# Step 3: Normalize the numerical columns
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Step 4: Train a Random Forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_scaled, y)
# Step 5: Get the feature importances
importances = rf.feature_importances_
# Step 6: Create a DataFrame for better visualization
feature_importance_df = pd.DataFrame({
'Feature': X.columns,
'Importance': importances
})
# Step 7: Sort the feature importance in descending order
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
# Step 8: Plot the feature importances using a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
plt.title('Feature Importance - Random Forest Classifier')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.show()""")

    elif num == 25:
        print("""25. Load Toyocorolla.csv and perform below operation:
a. normalization price attribute
b. standardize the Quarterly_Tax attribute
c. convert the Fuel_Type attributes to numerical using rank transformation
d. apply log transformation to Age_08_04 attribute
Solution:
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
# Step 1: Load the dataset
df = pd.read_csv('Toyocorolla.csv')
# Step 2: Normalize the 'price' attribute using Min-Max scaling
scaler = MinMaxScaler()
df['price_normalized'] = scaler.fit_transform(df[['price']])
# Step 3: Standardize the 'Quarterly_Tax' attribute using StandardScaler
scaler_tax = StandardScaler()
df['Quarterly_Tax_standardized'] = scaler_tax.fit_transform(df[['Quarterly_Tax']])
# Step 4: Convert 'Fuel_Type' to numerical values using rank transformation
df['Fuel_Type_rank'] = df['Fuel_Type'].rank(method='dense')
# Step 5: Apply log transformation to 'Age_08_04' attribute
# Ensure all values are positive to apply log transformation
df['Age_08_04_log'] = np.log(df['Age_08_04'] + 1) # Adding 1 to avoid log(0) issues
# Display the modified dataframe
print(df.head())""")

    elif num == 26:
        print("""26. Load the WHReport dataset and perform the following
a. Make the column title codable
b. Find the number of missing values in each column, total missing value count and remove
the missing data objects
c. Find min and max of each attribute and then normalize the dataset.
d. Plot all the numeric column using histogram.
Solution:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
# Step 1: Load the WHReport dataset
df = pd.read_csv('WHReport.csv')
# Step 2: Make column titles codable (replace spaces with underscores and lowercase)
df.columns = df.columns.str.replace(' ', '_').str.lower()
# Step 3: Find the number of missing values in each column and total missing value count
missing_values_per_column = df.isnull().sum()
total_missing_values = missing_values_per_column.sum()
# Print the missing values per column and total missing value count
print("Missing values per column:")
print(missing_values_per_column)
print(f"\nTotal missing values: {total_missing_values}")
# Step 4: Remove rows with missing data
df_cleaned = df.dropna()
# Step 5: Find min and max of each attribute and normalize the dataset
min_max_values = df_cleaned.describe().loc[['min', 'max']]
# Normalize the dataset using Min-Max scaling
scaler = MinMaxScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df_cleaned), columns=df_cleaned.columns)
# Step 6: Plot all the numeric columns using histograms
numeric_cols = df_normalized.select_dtypes(include=[np.number]).columns
plt.figure(figsize=(12, 10))
for i, col in enumerate(numeric_cols, 1):
plt.subplot(2, 3, i) # Adjust the number of rows and columns as per the number of numeric
columns
sns.histplot(df_normalized[col], kde=True, bins=20)
plt.title(f'Histogram of {col}')
plt.xlabel(col)
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
# Display the min-max values for reference
print("\nMin and Max values of the cleaned dataset:")
print(min_max_values)""")

    elif num == 27:
        print("""27. i)Draw histogram of all the numerical columns of WH Report.csv dataset in plot, give title for
each of them, resize the visuals and save them.
Solution:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Step 1: Load the WHReport dataset
df = pd.read_csv('WHReport.csv')
# Step 2: Identify the numerical columns in the dataset
numeric_cols = df.select_dtypes(include=['number']).columns
# Step 3: Plot histograms for each numerical column
plt.figure(figsize=(12, 10)) # Resize the plot for better readability
for i, col in enumerate(numeric_cols, 1):
plt.subplot(2, 3, i) # Adjust the number of rows and columns as per the number of numeric
columns
sns.histplot(df[col], kde=True, bins=20) # Plot histogram with kernel density estimate (KDE)
plt.title(f'Histogram of {col}')
plt.xlabel(col)
plt.ylabel('Frequency')
# Step 4: Adjust layout for neatness
plt.tight_layout()
# Step 5: Save the plot as a PNG image
plt.savefig('WHReport_histograms.png')
# Display the plot
plt.show()
ii) Write the python code to
a. Create an array with values ranging from 10 to 35.
b. Reverse the array
c. Find the number of rows and columns in the array
d. Find the mean of the array
e. Square each element of the array and display it
Solution:
import numpy as np
# Step 1: Create an array with values ranging from 10 to 35
arr = np.arange(10, 36) # Values from 10 to 35 (inclusive)
# Step 2: Reverse the array
arr_reversed = arr[::-1]
# Step 3: Find the number of rows and columns in the array
# For a 1D array, the number of rows will be the length of the array and columns will be 1
rows, cols = arr_reversed.shape[0], 1 # Since it's a 1D array, it has 1 column by default
# Step 4: Find the mean of the array
mean_val = np.mean(arr_reversed)
# Step 5: Square each element of the array and display it
squared_arr = arr_reversed ** 2
# Print results
print("Original Array:", arr)
print("Reversed Array:", arr_reversed)
print("Number of Rows:", rows)
print("Number of Columns:", cols)
print("Mean of the Array:", mean_val)
print("Squared Array:", squared_arr)""")

    elif num == 28:
        print("""28.i)Write a python code to discover the pattern between amazonstock.csv and applestock.csv dataset
using Matplotlib visualizations, Label the axis, modify the markers and give a title for the plot.
Solution:
import pandas as pd
import matplotlib.pyplot as plt
# Load the datasets
amazon_stock = pd.read_csv('amazonstock.csv')
apple_stock = pd.read_csv('applestock.csv')
# Convert date columns to datetime objects for accurate plotting on the x-axis
amazon_stock['Date'] = pd.to_datetime(amazon_stock['Date'])
apple_stock['Date'] = pd.to_datetime(apple_stock['Date'])
# Plotting Amazon and Apple "Close" prices
plt.figure(figsize=(14, 8))
# Amazon stock plot
plt.plot(amazon_stock['Date'], amazon_stock['Close'], label='Amazon Close Price', marker='o',
color='blue', markersize=4)
# Apple stock plot
plt.plot(apple_stock['Date'], apple_stock['Close'], label='Apple Close Price', marker='x', color='green',
markersize=4)
# Labeling the axes
plt.xlabel("Date")
plt.ylabel("Close Price")
# Adding a title
plt.title("Comparison of Amazon and Apple Stock Close Prices")
# Adding a legend
plt.legend()
# Displaying the plot
plt.show()
ii) Write the python program for the following
a. Create an array with 12 element between the limits 50 to 70
b. Reshape array to 4x3 matrix
c. Display the last two rows and columns
d. Find the dimension and type of data
e. Create a one dimension with 5 elements all filled with ones.
Solution:
import numpy as np
# Step 1: Create an array with 12 elements between the limits 50 to 70
arr = np.linspace(50, 70, 12)
# Step 2: Reshape the array to a 4x3 matrix
matrix = arr.reshape(4, 3)
# Step 3: Display the last two rows and columns
last_two_rows_cols = matrix[-2:, -2:]
# Step 4: Find the dimension and type of data
dimension = matrix.ndim
data_type = matrix.dtype
# Step 5: Create a one-dimensional array with 5 elements all filled with ones
ones_array = np.ones(5)
# Display results
print("Original Array:", arr)
print("4x3 Matrix:\n", matrix)
print("Last Two Rows and Columns:\n", last_two_rows_cols)
print("Dimension of Matrix:", dimension)
print("Data Type of Matrix:", data_type)
print("One-dimensional Array of Ones:", ones_array)""")

    elif num == 29:
        print("""29. i)Write python code to draw boxplot of all the numerical columns of churn.csv dataset, give title
for each of them. Show visualization before normalization and after normalization of the dataset.
Solution:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
# Load the dataset
data = pd.read_csv('churn.csv')
# Separate numerical columns
numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
# Visualize boxplots before normalization
plt.figure(figsize=(15, 8))
plt.suptitle('Boxplots of Numerical Columns Before Normalization', fontsize=16)
for i, col in enumerate(numerical_cols, 1):
plt.subplot(2, (len(numerical_cols) + 1) // 2, i) # Arrange plots in two rows
sns.boxplot(y=data[col])
plt.title(col)
plt.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust layout to fit title
plt.show()
# Normalize the numerical columns using MinMaxScaler
scaler = MinMaxScaler()
data_normalized = data.copy()
data_normalized[numerical_cols] = scaler.fit_transform(data[numerical_cols])
# Visualize boxplots after normalization
plt.figure(figsize=(15, 8))
plt.suptitle('Boxplots of Numerical Columns After Normalization', fontsize=16)
for i, col in enumerate(numerical_cols, 1):
plt.subplot(2, (len(numerical_cols) + 1) // 2, i)
sns.boxplot(y=data_normalized[col])
plt.title(col)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
ii) Write the python code to
a. Create an array with values ranging from 10 to 35.
b. Reverse the array
c. Add 5 to each element of array
d. Create 3x3 array with all values filled with zero
Solution:
import numpy as np
# Step 1: Create an array with values ranging from 10 to 35
arr = np.arange(10, 36)
# Step 2: Reverse the array
arr_reversed = arr[::-1]
# Step 3: Add 5 to each element of the array
arr_plus_5 = arr + 5
# Step 4: Create a 3x3 array with all values filled with zero
zero_array = np.zeros((3, 3))
# Display results
print("Original Array:", arr)
print("Reversed Array:", arr_reversed)
print("Array with 5 Added to Each Element:", arr_plus_5)
print("3x3 Array Filled with Zeros:\n", zero_array)""")

    elif num == 30:
        print("""30.Write a Pandas program
f. Crate a dataset for the dictionary
exam_data = {'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew',
'Laura', 'Kevin', 'Jonas'],
'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']}
g. to calculate the mean of all students' scores. Data is stored in a dataframe.
h. to change the name 'James' to 'Suresh' in name column of the DataFrame.
i. to to select the rows where number of attempts in the examination is less than 2 and score
greater than 15.
j. to sort the data frame first by 'name' in descending order, then by 'score' in ascending order.
Solution:
import pandas as pd
import numpy as np
# Step 1: Create a DataFrame from the dictionary
exam_data = {
'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin',
'Jonas'],
'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']
}
df = pd.DataFrame(exam_data)
# Step 2: Calculate the mean of all students' scores
mean_score = df['score'].mean()
print("Mean Score of All Students:", mean_score)
# Step 3: Change the name 'James' to 'Suresh' in the name column
df['name'] = df['name'].replace('James', 'Suresh')
# Step 4: Select rows where the number of attempts is less than 2 and score is greater than 15
filtered_df = df[(df['attempts'] < 2) & (df['score'] > 15)]
print("\nRows with attempts < 2 and score > 15:\n", filtered_df)
# Step 5: Sort the DataFrame by 'name' in descending order and then by 'score' in ascending order
sorted_df = df.sort_values(by=['name', 'score'], ascending=[False, True])
print("\nSorted DataFrame:\n", sorted_df)""")

    elif num == 31:
        print("""31. Draw horizontal boxplot of all the numerical columns of adult.csv dataset in plot, set the figure
size, give title for each of them.
Write a Pandas program
a. to convert a dictionary to a Pandas series. {'a': 10, 'b': 20, 'c': 30, 'd': 40, 'e': 80}
b. convert series to dataframe
c. display the column names
d. change value 200 to 500
e. sort the values reverse order
Solution:
import pandas as pd
import numpy as np
# Step 1: Create a DataFrame from the dictionary
exam_data = {
'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin',
'Jonas'],
'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']
}
df = pd.DataFrame(exam_data)
# Step 2: Calculate the mean of all students' scores
mean_score = df['score'].mean()
print("Mean Score of All Students:", mean_score)
# Step 3: Change the name 'James' to 'Suresh' in the name column
df['name'] = df['name'].replace('James', 'Suresh')
# Step 4: Select rows where the number of attempts is less than 2 and score is greater than 15
filtered_df = df[(df['attempts'] < 2) & (df['score'] > 15)]
print("\nRows with attempts < 2 and score > 15:\n", filtered_df)
# Step 5: Sort the DataFrame by 'name' in descending order and then by 'score' in ascending order
sorted_df = df.sort_values(by=['name', 'score'], ascending=[False, True])
print("\nSorted DataFrame:\n", sorted_df)""")

    elif num == 32:
        print("""32. Consider Temperature_data.csv and Temperature_data1.csv. Identify the challenge and fix it and
then integrate the dataset.
Solution:
import pandas as pd
# Step 1: Load the Datasets
temp_data = pd.read_csv('Temperature_data.csv')
temp_data1 = pd.read_csv('Temperature_data1.csv')
# Step 2: Check for column name mismatches, data types, or missing values
print("Temperature_data.csv Columns:", temp_data.columns)
print("Temperature_data1.csv Columns:", temp_data1.columns)
# If column names differ, we need to rename them accordingly.
# Checking the column names and data types
print("\nTemperature_data.csv Info:")
print(temp_data.info())
print("\nTemperature_data1.csv Info:")
print(temp_data1.info())
# Step 3: Standardize Column Names (if needed)
# Renaming columns if necessary (example given in case there are column name mismatches)
temp_data.columns = temp_data.columns.str.strip().str.lower()
temp_data1.columns = temp_data1.columns.str.strip().str.lower()
# Step 4: Check for Missing Values and Duplicates
print("\nMissing Values in Temperature_data.csv:\n", temp_data.isnull().sum())
print("\nMissing Values in Temperature_data1.csv:\n", temp_data1.isnull().sum())
# Handling missing values (example: forward fill)
temp_data.fillna(method='ffill', inplace=True)
temp_data1.fillna(method='ffill', inplace=True)
# Removing duplicate rows if they exist
temp_data.drop_duplicates(inplace=True)
temp_data1.drop_duplicates(inplace=True)
# Step 5: Identify common column(s) for merging
# For example, if 'date' column is present in both, we will merge on it.
# Step 6: Merge the datasets
# Using an 'inner' join on the 'date' column if it exists in both dataframes; otherwise, we can merge
on indices.
merged_data = pd.merge(temp_data, temp_data1, how='inner', on='date')
# Step 7: Display or save the merged dataset
print("\nMerged DataFrame:\n", merged_data.head())
# Optionally, save the merged dataset to a new CSV file
merged_data.to_csv("Merged_Temperature_Data.csv", index=False)""")