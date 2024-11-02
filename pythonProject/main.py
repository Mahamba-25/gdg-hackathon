import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = '8188039347:AAFOEPZFYEy5zSPirE0E-IQUSvfdcaS3M9w'
bot = telebot.TeleBot(API_KEY)

# Global variable to hold the stations
stations = []


# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Send a welcome message with options
    bot.send_message(message.chat.id, f"- Привет, {message.from_user.first_name}!😄 ")
    bot.send_message(
        message.chat.id,
        "Я помогу узнать время, когда автобус приедет на вашу остановку. Пожалуйста, выберите название остановки. _Например: Wales park._",
        parse_mode='Markdown'
    )
    global stations  # Use global variable
    stations = stations_name("name_of_station")
    send_all(message, stations)


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
    return station


def send_all(message, station):
    # Create a keyboard with buttons split into two columns
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(0, len(station), 2):
        button1 = KeyboardButton(station[i]['address'])
        # Ensure there's a second button if there's an odd number of stations
        button2 = KeyboardButton(station[i + 1]['address']) if (i + 1) < len(station) else None

        if button2:
            markup.row(button1, button2)  # Add two buttons in a row
        else:
            markup.add(button1)  # Add single button if it's the last one

    bot.send_message(message.chat.id, "- Отлично! Теперь выберите из списка номер вашего автобуса. Например, 17. ",
                     reply_markup=markup)


bot.polling()
