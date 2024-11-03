import pandas as pd

# Convert 'First_GPS_Datetime' and 'Last_GPS_Datetime' columns to datetime format
data['First_GPS_Datetime'] = pd.to_datetime(data['First_GPS_Datetime'])
data['Last_GPS_Datetime'] = pd.to_datetime(data['Last_GPS_Datetime'])

# Calculate the time difference in minutes and create the 'total_time_taken' column
data['total_time_taken'] = (data['Last_GPS_Datetime'] - data['First_GPS_Datetime']).dt.total_seconds() / 60.0

# Create a new DataFrame with aggregated total_time_taken for each trip number
new_data = data.groupby('Trip_No')['total_time_taken'].sum().reset_index()

# Merge the aggregated data back to the original DataFrame based on 'Trip_No'
data = pd.merge(data, new_data, on='Trip_No', how='left', suffixes=('', '_per_trip'))

# Keep all columns except 'total_time_taken' (you can add more columns to exclude)
columns_to_exclude = ['total_time_taken']
columns_to_keep = [col for col in data.columns if col not in columns_to_exclude]
data = data[columns_to_keep]

data

# To check which bus has the most data

# Group the data by Bus_Registration_No and count the number of rows for each registration number
registration_counts = data['Bus_Registration_No'].value_counts()

# Find the registration number with the largest number of rows
max_registration_number = registration_counts.idxmax()

# Get the count for the registration number with the largest number of rows
max_registration_count = registration_counts.max()

# Output the result
print(f"The registration number with the largest number of rows is: {max_registration_number}")
print(f"The count of rows for this registration number is: {max_registration_count}")

# Assing target and features
y=filtered_data['total_time_taken_per_trip']
X=filtered_data.drop('total_time_taken_per_trip',axis=1)

# Split dataset to train and test using Holdout method
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize the features (optional but can be beneficial for some models)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)