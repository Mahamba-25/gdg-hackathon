def stations_name(file_path):
    # Initialize an empty list to hold the station dictionaries
    station = []

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        # Read the header line to skip it
        header = file.readline().strip().split(',')

        # Process each subsequent line
        for line in file:
            # Strip whitespace and split the line by commas
            data = line.strip().split(',')

            # Create a dictionary for the station with the relevant fields
            station_dict = {
                'stop_id': data[0],
                'address': data[3]  # This is where the station name is located
            }

            # Append the dictionary to the list
            station.append(station_dict)
    print("stations_name.py return stations success")
    return station