import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = '8188039347:AAFOEPZFYEy5zSPirE0E-IQUSvfdcaS3M9w'
bot = telebot.TeleBot(API_KEY)


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


# Run the bot
bot.polling()
