import random
import config as cfg
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

bot = telebot.TeleBot(cfg.Telegram_BOT_API)

# Global variable to hold the stations
stations = []

# Load and process stations only once
def initialize_stations(file_path):
    global stations
    stations = load_stations(file_path)
    add_random_dwell_time(stations)
    add_random_arrival_time(stations)

# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"- Привет, {message.from_user.first_name}!😄 ")
    initialize_stations("Datasets/name_of_station")  # Initialize stations
    send_all_stations(message)

def load_stations(file_path):
    """Load station data from a CSV file into a list of dictionaries."""
    station_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        header = file.readline().strip().split(',')
        for line in file:
            data = line.strip().split(',')
            station_dict = {
                'stop_id': data[0],
                'address': data[3],  # Station name
                'route_id': data[4],  # Correct index for route_id
                'direction': data[5],  # Correct index for direction
                'dwell_time': 0,  # Placeholder for dwell time
                'arrival_time': None,  # Placeholder for arrival time
            }
            station_list.append(station_dict)
    return station_list

def send_all_stations(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(stations), 2):
        button1 = KeyboardButton(stations[i]['address'])
        button2 = KeyboardButton(stations[i + 1]['address']) if (i + 1) < len(stations) else None
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

def add_random_arrival_time(stations):
    """Add a unique random future arrival time to each bus stop entry only once."""
    for station in stations:
        random_minutes = random.randint(15, 60)
        station['arrival_time'] = datetime.now() + timedelta(minutes=random_minutes)

def calculate_waiting_time(arrival_time):
    """Calculate the time remaining for the bus to arrive."""
    current_time = datetime.now()
    remaining_time = arrival_time - current_time

    if remaining_time.total_seconds() > 0:
        return max(0, remaining_time.total_seconds() // 60)  # return minutes
    return 0  # If the bus has already arrived

@bot.message_handler(func=lambda message: message.text in [station['address'] for station in stations])
def handle_bus_stop_selection(message):
    try:
        selected_bus_stop = message.text
        stop_info = next((s for s in stations if s['address'] == selected_bus_stop), None)

        if stop_info:
            remaining_minutes = calculate_waiting_time(stop_info['arrival_time'])
            time_message = f"{remaining_minutes} минут{'а' if remaining_minutes == 1 else 'ы'}"
            bot.send_message(message.chat.id,
                             f"Предполагаемое время прибытия на {selected_bus_stop}: {time_message}.")
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
    # Do not reinitialize the stations
    send_all_stations(message)

bot.polling(none_stop=True)
