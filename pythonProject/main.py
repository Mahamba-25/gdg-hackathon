import pandas as pd
from huggingface_hub import metadata_save

import config as cfg
import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from pythonProject.stations_name import stations_name

import Datasets
from predict import predict_bus_arrival_time
from datetime import datetime
bot = telebot.TeleBot(cfg.Telegram_BOT_API)

# Global variable to hold the stations
stations = []


# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    # Send a welcome message with options
    bot.send_message(message.chat.id, f"- Привет, {message.from_user.first_name}!😄 ")
    global stations  # Use global variable
    stations = stations_name("Datasets/name_of_station")
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
                'address': data[3],  # This is where the station name is located
                'route_id': data[4],  # Add the correct index for route_id
                'direction': data[5],
                # Add the correct index for direction
            }

            # Append the dictionary to the list
            station.append(station_dict)
    return station



@bot.message_handler(commands=['button'])
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
    bot.send_message(message.chat.id, "Я помогу узнать время, когда автобус приедет на вашу остановку. Пожалуйста, выберите название остановки. _Например: Wales park._", reply_markup=markup, parse_mode='Markdown')

from datetime import datetime

@bot.message_handler(func=lambda message: message.text in [stations[i]['address'] for i in range(len(stations))])
def handle_bus_stop_selection(message):
    try:
        selected_bus_stop = message.text

        # Get the current hour and day of the week
        now = datetime.now()
        hour = now.hour  # Текущий час (0-23)
        day_of_week = now.weekday()  # Текущий день недели (0=Понедельник, 6=Воскресенье)
        dwell_time = 30  # Пример времени ожидания в секундах

        # Find the route_id and direction for the selected bus stop
        stop_info = next((s for s in stations if s['address'] == selected_bus_stop), None)

        if stop_info:
            route_id = stop_info['route_id']
            direction_x = stop_info['direction']

            # Call the prediction function
            predicted_arrival_time = predict_bus_arrival_time(
                bus_stop=selected_bus_stop,
                route_id=route_id,
                direction_x=direction_x,
                hour=hour,
                day_of_week=day_of_week,
                dwell_time=dwell_time
            )

            # Convert predicted arrival time from decimal hours to hours and minutes
            total_hours = int(predicted_arrival_time[0])  # Получить целую часть (часы)
            total_minutes = int((predicted_arrival_time[0] - total_hours) * 60)  # Преобразовать десятичную часть в минуты

            # Create a user-friendly message
            if total_hours > 0:
                time_message = f"{total_hours} час{'а' if total_hours == 1 else 'ов'} и {total_minutes} минут{'а' if total_minutes == 1 else 'ы'}"
            else:
                time_message = f"{total_minutes} минут{'а' if total_minutes == 1 else 'ы'}"

            # Send the formatted arrival time to the user
            bot.send_message(message.chat.id, f"Предполагаемое время прибытия на {selected_bus_stop}: {time_message}.")
        else:
            bot.send_message(message.chat.id, "Автобусная остановка не найдена.")
    except Exception as e:
        print(f"Error: {e}")  # Log the error to the console
        bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса.")


bot.polling()