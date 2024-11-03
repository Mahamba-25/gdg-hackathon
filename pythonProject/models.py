import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
import joblib  # Import joblib for saving the model

# Load the datasets
bus_stop_data = pd.read_csv("Datasets/bus_stop")  # Ensure the correct filename with extension
stop_data = pd.read_csv("Datasets/name_of_station")  # Ensure the correct filename with extension

# Convert data types if necessary
bus_stop_data['bus_stop'] = bus_stop_data['bus_stop'].astype(str)
stop_data['stop_id'] = stop_data['stop_id'].astype(str)

# Merge bus_stop_data with stop_data
data = pd.merge(bus_stop_data, stop_data, left_on="bus_stop", right_on="stop_id", how="inner")
print("Shape after merging bus_stop_data with stop_data:", data.shape)

# Feature engineering
data['arrival_time'] = pd.to_datetime(data['arrival_time'], format='%H:%M:%S', errors='coerce')
data['hour'] = data['arrival_time'].dt.hour
data['day_of_week'] = pd.to_datetime(data['date'], format='%Y-%m-%d', errors='coerce').dt.dayofweek

# Check available columns before selecting features
print("Columns in data for feature selection:")
print(data.columns)  # Debugging print

# Select features and target
features = data[['bus_stop', 'route_id', 'direction_x', 'hour', 'day_of_week', 'dwell_time_in_seconds']]
target = data['hour'] + (data['arrival_time'].dt.minute / 60)

# Convert categorical variables to numeric
features = pd.get_dummies(features, columns=['bus_stop', 'route_id', 'direction_x'], drop_first=True)

# Save the features to a file
joblib.dump(features.columns.tolist(), 'features.pkl')

# Check shape of features and target
print("Shape of features before train-test split:", features.shape)
print("Shape of target before train-test split:", target.shape)

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model
model = GradientBoostingRegressor()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, predictions))

# Save the model
joblib.dump(model, 'bus_arrival_model.pkl')  # Save the model to a file

print("Model saved as 'bus_arrival_model.pkl'")
