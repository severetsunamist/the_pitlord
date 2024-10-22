from django.core.management.base import BaseCommand
from bot.models import PlayerModel
import asyncio

from bot.bot_main import tgbot

class Command(BaseCommand):
    help = 'Lunching bot'

    def handle(self, *args, **options):
        print("DB is cleared")
        PlayerModel.objects.all().delete()

        print("Bot is running")
        asyncio.run(tgbot.infinity_polling())