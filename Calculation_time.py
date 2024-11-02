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
