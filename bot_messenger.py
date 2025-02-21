import telebot
import json

# خواندن تنظیمات از فایل config.json
with open("config.json", "r") as file:
    config = json.load(file)

bot = telebot.TeleBot(config["bot_token"])
admins = config["admin_ids"]
allowed_users = config["allowed_users"]

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in admins:
        bot.send_message(message.chat.id, "سلام مدیر! پیام خود را ارسال کنید.")
    else:
        bot.send_message(message.chat.id, "شما مجاز به استفاده از ربات نیستید.")

@bot.message_handler(func=lambda message: True)
def forward_message(message):
    if message.from_user.id in allowed_users or message.from_user.id in admins:
        for admin_id in admins:
            bot.forward_message(admin_id, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "پیام شما ارسال شد!")
    else:
        bot.send_message(message.chat.id, "شما مجاز به ارسال پیام نیستید.")

bot.polling()
