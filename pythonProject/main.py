import pandas as pd
import random
import config as cfg
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from pythonProject.stations_name import stations_name
from datetime import datetime, timedelta

bot = telebot.TeleBot(cfg.Telegram_BOT_API)

# Global variable to hold the stations
stations = []

# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"- Привет, {message.from_user.first_name}!😄 ")
    global stations  # Use global variable
    stations = stations_name("Datasets/name_of_station")
    add_random_dwell_time(stations)  # Add dwell time after stations are loaded
    send_all(message, stations)

def stations_name(file_path):
    # Initialize an empty list to hold the station dictionaries
    station = []
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        header = file.readline().strip().split(',')
        for line in file:
            data = line.strip().split(',')
            station_dict = {
                'stop_id': data[0],
                'address': data[3],  # Station name
                'route_id': data[4],  # Correct index for route_id
                'direction': data[5],  # Correct index for direction
            }
            station.append(station_dict)
    return station

@bot.message_handler(commands=['button'])
def send_all(message, station):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(station), 2):
        button1 = KeyboardButton(station[i]['address'])
        button2 = KeyboardButton(station[i + 1]['address']) if (i + 1) < len(station) else None
        if button2:
            markup.row(button1, button2)
        else:
            markup.add(button1)
    restart_button = KeyboardButton("Заново")
    markup.add(restart_button)
    bot.send_message(message.chat.id,
                     "Я помогу узнать время, когда автобус приедет на вашу остановку. Пожалуйста, выберите название остановки. _Например: Wales park._",
                     reply_markup=markup, parse_mode='Markdown')

def add_random_dwell_time(stations):
    """Adds a unique random dwell time to each station."""
    unique_dwell_times = random.sample(range(1, len(stations) + 1), len(stations))
    for station, dwell_time in zip(stations, unique_dwell_times):
        station['dwell_time'] = dwell_time  # Unique dwell time assigned

def add_random_arrival_times(stations):
    """Add unique random future arrival times to each bus stop entry."""
    for stop in stations:
        if 'arrival_time' not in stop:  # Avoid overwriting if it already exists
            random_minutes = random.randint(15, 60)
            arrival_time = datetime.now() + timedelta(minutes=random_minutes)
            stop['arrival_time'] = arrival_time  # Store as datetime object

def calculate_waiting_time(bus_stops, stop_id, user_wait_time):
    """Calculate the time remaining for the bus to arrive."""
    for stop in bus_stops:
        if stop['stop_id'] == stop_id:
            arrival_time = stop.get('arrival_time')  # Use get to avoid KeyError
            if arrival_time:
                current_time = datetime.now()
                remaining_time = arrival_time - current_time

                if remaining_time.total_seconds() > 0:
                    adjusted_remaining_time = remaining_time - timedelta(minutes=user_wait_time)
                    remaining_minutes = max(0, adjusted_remaining_time.total_seconds() // 60)
                    return remaining_minutes  # return minutes
                else:
                    return 0  # If the bus has already arrived

    return None  # If stop_id is not found

@bot.message_handler(func=lambda message: message.text in [station['address'] for station in stations])
def handle_bus_stop_selection(message):
    try:
        selected_bus_stop = message.text
        user_wait_time = 10  # Example wait time; you can modify this or ask the user for input
        stop_info = next((s for s in stations if s['address'] == selected_bus_stop), None)

        if stop_info:
            # Ensure arrival time is only set once
            add_random_arrival_times([stop_info])  # Assign an arrival time if it doesn't exist

            # Calculate the waiting time for the selected bus stop
            remaining_minutes = calculate_waiting_time(stations, stop_info['stop_id'], user_wait_time)

            if remaining_minutes is not None:
                time_message = f"{remaining_minutes} минут{'а' if remaining_minutes == 1 else 'ы'}"
                bot.send_message(message.chat.id,
                                 f"Предполагаемое время прибытия на {selected_bus_stop}: {time_message}.")
            else:
                bot.send_message(message.chat.id, "Ошибка при расчете времени ожидания.")
        else:
            bot.send_message(message.chat.id, "Автобусная остановка не найдена.")

        send_restart_option(message)
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса.")

def send_restart_option(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    restart_button = KeyboardButton("Заново")
    markup.add(restart_button)
    bot.send_message(message.chat.id, "Вы хотите начать заново?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Заново")
def restart_bot(message):
    start_message(message)

bot.polling()
