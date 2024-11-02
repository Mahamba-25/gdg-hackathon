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
