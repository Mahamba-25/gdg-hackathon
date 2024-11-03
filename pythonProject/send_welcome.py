import config as cfg
bot = telebot.TeleBot(cfg.Telegram_BOT_API)

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
    stations = stations_name("Datasets/name_of_station")
    send_all(message, stations)