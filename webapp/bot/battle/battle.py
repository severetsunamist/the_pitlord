from argparse import Action as Action_argparse
from bot.models import PlayerModel, HeroModel, BattleModel, RoundModel, ActionModel


class Battle:
    heroes = list()
    rounds = list()
    model: BattleModel
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


    def __init__(self, your_hero, tgbot):
        self.model, _ = BattleModel.objects.get_or_create(queued=True) # There will be a Battle Object for each player?
        self.your_hero = your_hero
        self.tgbot = tgbot
        print('Battle created. Queue is pending')
        first_round, _ = RoundModel.objects.get_or_create(battle=self.model, number=1)
        first_round.save()
        print(f"Queue round created {first_round}")
        if not self.model.hero_1:
            print('Hero 1')
            self.model.hero_1 = your_hero
            self.model.save()
            self.heroes.append(your_hero)

        elif not self.model.hero_2:
            print('Hero 2')
            self.model.hero_2 = your_hero
            self.heroes.append(your_hero)
            self.model.queued = False
            self.model.current_round += 1
            self.model.save()
            

        your_hero.hero_stage = "FIGHT"
        your_hero.save()
        tgbot.send_message(your_hero.hero_owner.tg_id, "You are queued for a battle! It won't take too long")
        self.next_round()
        print(f"1st round created")

            # cur_round = RoundModel.objects.create(battle=self.model, number=self.model.current_round)
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
            tgbot.send_message(playing_hero.hero_owner.tg_id, f"You hit {victim.nickname} by {damage}")
            tgbot.send_message(victim.hero_owner.tg_id, f"{playing_hero.nickname} hits you by {damage}")


    def add_hero(self, hero):
        if hero not in self.heroes:
            self.heroes.append(hero)


    def next_round(self):
        round_finished_counter = 0

        for hero in self.heroes:
            if hero.hero_finished_round:
                round_finished_counter += 1

        if round_finished_counter == 2:
            for hero in self.heroes:
                hero.hero_finished_round = False
                hero.hero_cur_ap += int(hero.hero_max_ap / 2)
                if hero.hero_cur_ap > hero.hero_max_ap:
                    hero.hero_cur_ap = hero.hero_max_ap
                hero.hero_cur_mp += int(hero.hero_max_mp / 2)
                if hero.hero_cur_mp > hero.hero_max_mp:
                    hero.hero_cur_mp = hero.hero_max_mp
                hero.save()
            self.cur_round += 1
            next_round = self.Round(self.cur_round, self)
            next_round.save()
            self.rounds.append(next_round)
            for each in self.heroes:
                self.tgbot.send_message(self.your_hero.hero_owner.tg_id, f"Round {self.cur_round}") # Change your_hero with each?



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
                    tgbot.send_message(chat_id=hero.hero_owner.tg_id, text="You have won! Kill more become the pitlord")
                else:
                    tgbot.send_message(chat_id=hero.hero_owner.tg_id, text="You are dead! in a pit...")
        elif count_alive == 0:
            for hero in self.heroes:
                tgbot.send_message(chat_id=hero.hero_owner.tg_id, text="All dead, such a pity...")
        else:
            self.next_round()

