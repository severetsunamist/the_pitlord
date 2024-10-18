from argparse import Action as Action_argparse
from webapp.bot.models import PlayerModel, HeroModel, BattleModel, RoundModel, ActionModel
from webapp.bot.bot_main import bot
class Battle:
    heroes = list()
    rounds = list()
    battle_db: BattleModel
    cur_round = 0



    class Round:
        def __init__(self, battle, number):
            self.number = number
            self.actions = list()
            self.db_round = RoundModel(battle=battle)
            self.db_round.save()


    class ActionClass:
        def __init__(self, action_number, playing_hero, victim, damage=10, heal=0):
            self.action_number = action_number
            self.playing_hero = playing_hero
            self.victim = victim
            self.damage = damage
            self.heal = heal
            # self.effects = list() /// EffectModel TODO LATER
            new_action = ActionModel().objects.create(
                number=action_number,
                subject=playing_hero,
                object=victim,
                damage=damage,
                heal=heal
            )
            new_action.save()


    def __init__(self, character):
        self.battle_db, _ = BattleModel.objects.get_or_create(queued=True) # There will be a Battle Object for each player?
        self.character = character
        print('Battle created. Queue is pending')

        if not self.battle_db.hero_1:
            print('Hero 1')
            self.battle_db.hero_1 = character.char
            self.battle_db.save()

        elif not self.battle_db.hero_2:
            print('Hero 2')
            self.battle_db.hero_2 = character.char
            self.battle_db.queued = False
            self.battle_db.current_round += 1
            self.battle_db.save()

        character.char.hero_stage = "FIGHT"
        character.char.save()
        bot.send_message(character.char.hero_owner.tg_id, "You are queued for a battle! It won't take too long")
        self.next_round()

            # cur_round = RoundModel.objects.create(battle=self.battle_db, number=self.battle_db.current_round)
            # cur_round.save()
        # self.db_battle = BattleModel()
        # self.db_battle.save()
        # print('Battle started')
        # queue_round = self.Round(number=0, battle=self)
        # self.rounds.append(queue_round)


    def make_action(self, playing_hero, victim, damage, heal, action_type):
        cur_round = self.rounds[-1]
        made_action = cur_round.ActionClass(action_number=len(cur_round.actions)-1, playing_hero=playing_hero, victim=victim, damage=damage, heal=heal)
        cur_round.append(made_action)
        if action_type == "hit":
            bot.send_message(playing_hero.hero_owner.tg_id, f"You hit {victim.nickname} by {damage}")
            bot.send_message(victim.hero_owner.tg_id, f"{playing_hero.nickname} hits you by {damage}")


    def add_hero(self, hero):
        if hero not in self.heroes:
            self.heroes.append(hero)


    def next_round(self):
        self.cur_round += 1
        next_round = self.Round(self.cur_round, self)
        next_round.save()
        self.rounds.append(next_round)
        for each in self.heroes:
            bot.send_message(self.character.char.hero_owner.tg_id, f"Round {self.cur_round}") # Change character.char with each?



    def try_end_battle(self):
        count_alive = 0
        winner_player = None
        for hero in self.heroes:
            if hero.alive:
                count_alive += 1
                winner_player = hero.hero_owner
        if count_alive == 1:
            for hero in self.heroes:
                if winner_player == hero:
                    bot.send_message(chat_id=hero.hero_owner.tg_id, text="You have won! Kill more become the pitlord")
                else:
                    bot.send_message(chat_id=hero.hero_owner.tg_id, text="You are dead! in a pit...")
        elif count_alive == 0:
            for hero in self.heroes:
                bot.send_message(chat_id=hero.hero_owner.tg_id, text="All dead, such a pity...")
        else:

            self.next_round()

