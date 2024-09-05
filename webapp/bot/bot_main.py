import asyncio
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings

bot = AsyncTeleBot(settings.TG_BOT_TOKEN, parse_mode='HTML') # HTML parse mode not always works with MarkDown

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    w_message = "Welcome! Everything works as expected so far"
    await bot.send_message(message.chat.id, w_message)

@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)