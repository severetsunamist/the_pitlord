from django.core.management.base import BaseCommand
from bot.models import PlayerModel

class Command(BaseCommand):
    help = 'Clearing DB'

    def handle(self, *args, **options):
        print("DB is cleared")
        PlayerModel.objects.all().delete()