import pandas as pd
import joblib

# Load the trained model and feature names
model = joblib.load('bus_arrival_model.pkl')
# Load the feature names used during training
original_feature_columns = joblib.load('features.pkl')

def predict_bus_arrival_time(bus_stop, route_id, direction_x, hour, day_of_week, dwell_time):
    # Prepare new data for prediction
    new_data = {
        'bus_stop': [bus_stop],
        'route_id': [route_id],
        'direction_x': [direction_x],
        'hour': [hour],
        'day_of_week': [day_of_week],
        'dwell_time_in_seconds': [dwell_time]
    }

    # Create a DataFrame from the new data
    new_data_df = pd.DataFrame(new_data)

    # Convert categorical variables to numeric (one-hot encoding)
    new_data_df = pd.get_dummies(new_data_df, columns=['bus_stop', 'route_id', 'direction_x'], drop_first=True)

    # Align new data with training data features
    # Create columns for one-hot encoding that may not exist in new data
    for col in original_feature_columns:
        if col not in new_data_df.columns:
            new_data_df[col] = 0  # Add missing columns with a value of 0

    # Reorder the new DataFrame to match the original feature order
    new_data_df = new_data_df[original_feature_columns]

    # Make predictions
    predictions = model.predict(new_data_df)

    # Print the predicted values
    return predictions

# Example usage
predicted_arrival_time = predict_bus_arrival_time(
    bus_stop='Bus Stop A',   # Replace with the desired bus stop
    route_id='Route 1',      # Replace with the desired route ID
    direction_x='North',      # Replace with the correct direction
    hour=10,                 # Example hour
    day_of_week=2,           # Example day of the week (0=Monday, 6=Sunday)
    dwell_time=30            # Example dwell time in seconds
)

print("Predicted arrival time (in hours):", predicted_arrival_time)
