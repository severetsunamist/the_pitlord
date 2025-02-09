
from django.db import models
from django.utils.translation.trans_real import deactivate
from .random_text.utils import CLASSES, STAGES


class PlayerModel(models.Model):
    tg_id = models.PositiveBigIntegerField('Telegram account id', unique=True)
    level = models.PositiveSmallIntegerField('Level', default=1, null=False, blank=False)

    exp = models.PositiveBigIntegerField('Experience', default=0, null=False, blank=False)
    next_lvl_exp = models.PositiveBigIntegerField('Next Lvl Experience', default=300, null=False, blank=False)

    hero = models.ForeignKey('HeroModel', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Current hero")

    battles = models.PositiveIntegerField('Total battles', default=0, null=False, blank=False)
    wins = models.PositiveIntegerField('Wins', default=0, null=False, blank=False)
    deaths = models.PositiveIntegerField('Deaths', default=0, null=False, blank=False)
    draws = models.PositiveIntegerField('Draws', default=0, null=False, blank=False)

    def __str__(self):
        return f'Player LVL {self.level} tgID: {self.tg_id}'

    class Meta:
        verbose_name = "Player's tg account"
        verbose_name_plural = "Players' tg accounts"


class HeroModel(models.Model):
    hero_owner = models.ForeignKey(PlayerModel, on_delete=models.CASCADE, verbose_name='Player', related_name='tg_account')
    hero_stage = models.CharField('Current stage', choices=STAGES, max_length=6, default='ENTER', null=False, blank=False)
    hero_finished_round = models.BooleanField("Finished round", default=False)
    hero_is_alive = models.BooleanField('Alive', default=True, null=False)
    hero_class = models.CharField('Class', max_length=20)
    nickname = models.CharField('Name', max_length=20)
    hero_str = models.SmallIntegerField('STR', default=5)
    hero_agl = models.SmallIntegerField('AGL', default=5)
    hero_int = models.SmallIntegerField('INT', default=5)
    hero_free_stats = models.SmallIntegerField('FREE STATS', default=3)

    hero_max_hp = models.SmallIntegerField('Max HP', default=50)
    hero_max_ap = models.SmallIntegerField('Max AP', default=50)
    hero_max_mp = models.SmallIntegerField('Max MP', default=50)
    hero_cur_hp = models.SmallIntegerField('Current HP', default=hero_max_hp.default)
    hero_cur_ap = models.SmallIntegerField('Current AP', default=hero_max_ap.default)
    hero_cur_mp = models.SmallIntegerField('Current MP', default=hero_max_mp.default)

    hero_armor = models.SmallIntegerField('Armor', default=0, null=False)
    hero_magic_resist = models.SmallIntegerField('Magic Resistance', default=0, null=False)
    hero_crit_resist = models.FloatField('Crit Resistance', default=0.0, null=False)
    hero_pierce_resist = models.FloatField('Pierce Resistance', default=0.0, null=False)
    hero_block_resist = models.FloatField('Block Resistance', default=0.0, null=False)
    hero_react_resist = models.FloatField('React Resistance', default=0.0, null=False)
    hero_dodge_resist = models.FloatField('Dodge Resistance', default=0.0, null=False)
    hero_inventory = models.BooleanField(default=True)

    exp_gained = models.PositiveIntegerField('Experience gained', default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.hero_class} {self.nickname} LVL {self.hero_owner.level} - {self.hero_owner.tg_id}'

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Heroes"


class BattleModel(models.Model):
    queued = models.BooleanField('Queued', default=True, null=False, blank=False)
    started = models.DateTimeField('Date started', default=None, null=True, blank=False) # TODO ADD DEFAULT
    is_finished = models.BooleanField('Finished', default=False, null=False, blank=False)
    finished = models.DateTimeField('Date finished', null=True, blank=True)

    current_round = models.PositiveSmallIntegerField('Current round', default=0, null=False, blank=False)
    total_rounds = models.PositiveSmallIntegerField('Total rounds', null=True, blank=True)

    hero_1 = models.ForeignKey(HeroModel, on_delete=models.CASCADE, null=True, default=None, verbose_name='Hero 1', related_name='hero_1')
    hero_2 = models.ForeignKey(HeroModel, on_delete=models.CASCADE, null=True, default=None, verbose_name='Hero 2', related_name='hero_2')
    # hero_3 = models.ForeignKey(HeroModel, on_delete=models.CASCADE, null=True, default=None, verbose_name='Hero 3', related_name='hero_3')

    # def __str__(self):
    #     return f'{self.pk} {self.started} {self.hero_1.nickname} vs {self.hero_2.nickname} vs {self.hero_3.nickname}'

    class Meta:
        verbose_name = 'Battle'
        verbose_name_plural = 'Battles'


class RoundModel(models.Model):
    battle = models.ForeignKey(BattleModel, on_delete=models.CASCADE, verbose_name='Battle')
    number = models.PositiveSmallIntegerField('Number', default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.pk} {self.battle} Round {self.number}'

    class Meta:
        verbose_name = 'Round'
        verbose_name_plural = 'Rounds'


class ActionModel(models.Model):
    round = models.ForeignKey(RoundModel, on_delete=models.CASCADE, verbose_name='Round')
    number = models.PositiveSmallIntegerField('Number', default=1, blank=False, null=False)
    subject = models.ForeignKey(HeroModel, on_delete=models.CASCADE, verbose_name='Subject', related_name='actor')
    object = models.ForeignKey(HeroModel, on_delete=models.CASCADE, verbose_name='Object', related_name='victim')
    damage = models.SmallIntegerField('Damage', default=0, blank=False, null=False)
    heal = models.SmallIntegerField('Heal', default=0, blank=False, null=False)
    # effect_applied = models.ForeignKey('EffectModel', on_delete=models.CASCADE)  //// EffectModel TODO LATER

    def __str__(self):
        return f'{self.round} Action {self.number}'

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

