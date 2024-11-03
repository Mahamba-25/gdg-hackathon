import pandas as pd
from huggingface_hub import metadata_save

import config as cfg
import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from pythonProject.stations_name import stations_name

import Datasets

bot = telebot.TeleBot(cfg.Telegram_BOT_API)

# Global variable to hold the stations
stations = []


# Define a handler for the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    # Send a welcome message with options
    bot.send_message(message.chat.id, f"- Привет, {message.from_user.first_name}!😄 ")
    bot.send_message(
        message.chat.id,
        "Я помогу узнать время, когда автобус приедет на вашу остановку. Пожалуйста, выберите название остановки. _Например: Wales park._",
        parse_mode='Markdown'
    )
    global stations  # Use global variable
    stations = stations_name("Datasets/name_of_station")


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Kandy":
        bot.send_message(message.chat.id, "Kandy")


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

    bot.send_message(message.chat.id, "- Отлично! Теперь выберите из списка номер вашего автобуса. Например, 17. ",
                     reply_markup=markup)


bot.polling()