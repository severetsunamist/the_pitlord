from django.contrib import admin

from .models import PlayerModel, HeroModel, BattleModel, RoundModel, ActionModel

admin.site.register(PlayerModel)
admin.site.register(BattleModel)
admin.site.register(HeroModel)
admin.site.register(RoundModel)
admin.site.register(ActionModel)