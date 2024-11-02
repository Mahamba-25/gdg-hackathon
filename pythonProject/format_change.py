# Create new column
import pandas as pd

# Convert 'First_GPS_Datetime' and 'Last_GPS_Datetime' colums to datetime format
data['First_GPS_Datetime'] = pd.to_datetime(data['First_GPS_Datetime'])
data['Last_GPS_Datetime'] = pd.to_datetime(data['Last_GPS_Datetime'])

data['total_time'] = data['Last_GPS_Datetime'] - data['First_GPS_Datetime']

new_data = data.groupby('Trid_No')['total_time'].sum().reset_index()

data = pd.merge(data, new_data, on='Trid_No', how='left', suffixes=('', '_per_trip'))

columns