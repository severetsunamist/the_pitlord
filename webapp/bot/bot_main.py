from django.conf import settings
import asyncio

from django.core.management import call_command
from telebot import TeleBot
from telebot import types
from .models import PlayerModel, HeroModel, BattleModel, RoundModel, ActionModel
from .random_text.utils import random_class, random_nickname
from .visuals import stage_imgs, stage_text, class_imgs, markups
from .visuals.class_imgs import classes_urls
from .visuals.hero_text_repr import hero_text_repr, HeroData
from random import randint


bot = TeleBot(settings.TG_BOT_TOKEN, parse_mode='HTML') # HTML parse mode not always works with MarkDown


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    player, player_created = PlayerModel.objects.get_or_create(tg_id=message.chat.id)
    player.save()
    hero, hero_created = HeroModel.objects.get_or_create(hero_owner=player)
    if hero_created:
        print("New hero created")
    else:
        print("Old hero downloaded")
    if not hero.hero_class and not hero.nickname:
        hero.hero_class = random_class()
        hero.nickname = random_nickname()
    hero.save()

    welcome_message = "Welcome! Everything works as expected so far"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Enter the pit", callback_data='enter'))

    bot.send_message(message.chat.id, welcome_message)



    bot.send_photo(message.chat.id,
                         photo=stage_imgs.stages['welcome'],
                         caption=stage_text.stage_text['welcome'],
                         reply_markup=markup
                         )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    account = call.message.chat.id
    character = HeroData(account)
    your_hero = character.char
    print(character)
    markup = types.InlineKeyboardMarkup()
    stat_choices = [types.InlineKeyboardButton("+STR", callback_data="add_str"),
                    types.InlineKeyboardButton("+AGL", callback_data="add_agl"),
                    types.InlineKeyboardButton("+INT", callback_data="add_int")]

    for i in stat_choices:
        markup.add(i)

    if call.data == 'enter':
        print("Pit is entered")
        if your_hero.hero_stage == "ENTER":
            your_hero.hero_stage = "STATS"
            your_hero.save()
        bot.send_photo(call.message.chat.id,
                             photo=classes_urls[character.hero_class],
                             caption=hero_text_repr(account, character),
                             reply_markup=markup
                             )


    if (call.data == 'add_str' or call.data == 'add_agl' or call.data == 'add_int') and character.free_stats > 0:
        if call.data == 'add_str':
            your_hero.hero_free_stats -= 1
            your_hero.hero_str += 1
            your_hero.hero_max_hp += 10
            your_hero.hero_cur_hp += 10
            your_hero.save()
            print(f"STR is added to {character.hero_nickname}")
        if call.data == 'add_agl':
            your_hero.hero_free_stats -= 1
            your_hero.hero_agl += 1
            your_hero.hero_max_ap += 10
            your_hero.hero_cur_ap += 10
            your_hero.save()
            print(f"AGL is added to {character.hero_nickname}")
        if call.data == 'add_int':
            your_hero.hero_free_stats -= 1
            your_hero.hero_int += 1
            your_hero.hero_max_mp += 10
            your_hero.hero_cur_mp += 10
            your_hero.save()
            print(f"INT is added to {character.hero_nickname}")

        character = HeroData(account)
        bot.edit_message_caption(
                            chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            caption=hero_text_repr(account, character),
                            reply_markup=markup
                        )

        print(f'Free stats: {character.free_stats}')
        if character.free_stats == 0:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Fight", callback_data="fight"))
            if your_hero.hero_stage == "STATS":
                your_hero.hero_stage = "READY"
                your_hero.save()
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                caption=hero_text_repr(account, character),
                reply_markup=markup
            )
    if your_hero.hero_stage == "FIGHT":
        pass

    if call.data == "fight":
        battle, _ = BattleModel.objects.get_or_create(queued=True)
        print('Battle created. Queue is pending')
        if not battle.hero_1:
            print('Hero 1')
            battle.hero_1 = your_hero
            battle.save()
        # elif not battle.hero_2:
        #     print('Hero 2')
        #     battle.hero_2 = your_hero
        #     battle.save()
        elif not battle.hero_2:
            print('Hero 2')
            battle.hero_2 = your_hero
            battle.queued = False
            battle.current_round += 1
            battle.save()
            cur_round = RoundModel.objects.create(battle=battle, number=battle.current_round)
            cur_round.save()
        if your_hero.hero_stage == "READY":
            your_hero.hero_stage = "FIGHT"
            your_hero.save()
        bot.send_message(call.message.chat.id, "You are queued for a battle! It won't take too long")

        # if not battle.queued:
        #     print("Battle queued == False")
        #     battle_queue = [battle.hero_1.hero_owner.tg_id, battle.hero_2.hero_owner.tg_id]
        #     for chat_id in battle_queue:
        #         print(chat_id)
        #         bot.send_message(chat_id, "Fight started")

        if not battle.queued:
            players = [battle.hero_1.hero_owner.tg_id, battle.hero_2.hero_owner.tg_id]
            for chat_id in players:
                bot.send_photo(chat_id, photo=stage_imgs.stages['battle'], caption="Battle begins.\nChoose your next move carefully!", reply_markup=None)

            next_round = True
            while battle.hero_1.hero_is_alive and battle.hero_2.hero_is_alive and next_round:
                next_round = False
                for chat_id in players:
                    if chat_id == players[0]:
                        enemy_player_tg_id = players[1]

                    else:
                        enemy_player_tg_id = players[0]

                    markup = markups.action_markup(your_hero)

                    enemy_hero = HeroData(enemy_player_tg_id)
                    bot.send_photo(chat_id,
                                   photo=classes_urls[enemy_hero.hero_class],
                                   caption=hero_text_repr(account, enemy_hero),
                                   reply_markup=markup
                                   )
                    print("123123123")
    if call.data == 'hit':
        your_hero = HeroModel.objects.get(hero_owner=PlayerModel.objects.get(tg_id=call.message.chat.id))

        try:
            battle = BattleModel.objects.get(hero_1=your_hero)
            enemy_hero = battle.hero_2
        except: # ANOTHER TRY NEEDED?
            battle = BattleModel.objects.get(hero_2=your_hero)
            enemy_hero = battle.hero_1
        if your_hero.hero_cur_ap >= 30:
            actions_in_round = []
            round_objects = RoundModel.objects.filter(battle=battle)
            num = round_objects.count()
            dealt_damage = randint(4, 12)
            your_hero.hero_cur_ap -= 35
            your_hero.save()
            action = ActionModel(round=RoundModel.objects.get(number=num), subject=your_hero, object=enemy_hero, damage=dealt_damage)
            actions_in_round.append(action)
            action.save()
            if not enemy_hero.hero_cur_hp <= 0:
                enemy_hero.hero_cur_hp -= dealt_damage
                enemy_hero.save()


            # if your_hero.hero_cur_ap < 30:
            #     for act in actions_in_round:
            #         act.save()

            if call.message.chat.id == battle.hero_1.hero_owner.tg_id:
                bot.send_message(call.message.chat.id, text=f'You hit {action.object.nickname} by {action.damage}')
                bot.send_message(battle.hero_2.hero_owner.tg_id, text=f'{action.subject.nickname} hits you by {action.damage}')
            elif call.message.chat.id == battle.hero_2.hero_owner.tg_id:
                bot.send_message(call.message.chat.id, text=f'You hit {action.object.nickname} by {action.damage}')
                bot.send_message(battle.hero_1.hero_owner.tg_id, text=f'{action.subject.nickname} hits you by {action.damage}')

            markup = markups.action_markup(your_hero)

            character = HeroData(enemy_hero.hero_owner.tg_id)
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                caption=hero_text_repr(account, character),
                reply_markup=markup
            )
            # bot.edit_message_media(media=classes_urls[enemy_hero.hero_class], chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)
            print('triggers 01')










@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


