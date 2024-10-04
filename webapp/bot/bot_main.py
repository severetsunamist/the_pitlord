from django.conf import settings
import asyncio

from django.core.management import call_command
from telebot import TeleBot
from telebot import types
from .models import PlayerModel, HeroModel, BattleModel, RoundModel
from .random_text.utils import random_class, random_nickname
from .visuals import stage_imgs, stage_text, class_imgs
from .visuals.class_imgs import classes_urls
from .visuals.hero_text_repr import hero_text_repr, HeroData


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
    print(character)
    markup = types.InlineKeyboardMarkup()
    stat_choices = [types.InlineKeyboardButton("+STR", callback_data="add_str"),
                    types.InlineKeyboardButton("+AGL", callback_data="add_agl"),
                    types.InlineKeyboardButton("+INT", callback_data="add_int")]

    for i in stat_choices:
        markup.add(i)

    if call.data == 'enter':
        print("Pit is entered")
        character.char.hero_stage = "STATS"
        character.char.save()
        bot.send_photo(call.message.chat.id,
                             photo=classes_urls[character.hero_class],
                             caption=hero_text_repr(account, character),
                             reply_markup=markup
                             )


    if (call.data == 'add_str' or call.data == 'add_agl' or call.data == 'add_int') and character.free_stats > 0:
        if call.data == 'add_str':
            character.char.hero_free_stats -= 1
            character.char.hero_str += 1
            character.char.hero_max_hp += 10
            character.char.hero_cur_hp += 10
            character.char.save()
            print(f"STR is added to {character.hero_nickname}")
        if call.data == 'add_agl':
            character.char.hero_free_stats -= 1
            character.char.hero_agl += 1
            character.char.hero_max_ap += 10
            character.char.hero_cur_ap += 10
            character.char.save()
            print(f"AGL is added to {character.hero_nickname}")
        if call.data == 'add_int':
            character.char.hero_free_stats -= 1
            character.char.hero_int += 1
            character.char.hero_max_mp += 10
            character.char.hero_cur_mp += 10
            character.char.save()
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
            character.char.hero_stage = "READY"
            character.char.save()
            bot.edit_message_caption(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                caption=hero_text_repr(account, character),
                reply_markup=markup
            )

    if call.data == "fight":
        battle, _ = BattleModel.objects.get_or_create(queued=True)
        print('Battle created. Queue is pending')
        if not battle.hero_1:
            print('Hero 1')
            battle.hero_1 = character.char
            battle.save()
        # elif not battle.hero_2:
        #     print('Hero 2')
        #     battle.hero_2 = character.char
        #     battle.save()
        elif not battle.hero_2:
            print('Hero 2')
            battle.hero_2 = character.char
            battle.queued = False
            battle.current_round += 1
            battle.save()
            cur_round = RoundModel.objects.create(battle=battle, number=battle.current_round)
            cur_round.save()
        character.char.hero_stage = "FIGHT"
        character.char.save()
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

                if call.message.chat.id == players[0]:
                    enemy_player = players[1]
                else:
                    enemy_player = players[0]

                markup = types.InlineKeyboardMarkup()
                stat_choices = [types.InlineKeyboardButton("Hit enemy", callback_data="hit"),
                                types.InlineKeyboardButton("Block", callback_data="block"),
                                types.InlineKeyboardButton("Use physical skill", callback_data="skill"),
                                types.InlineKeyboardButton("Use magic spell", callback_data="spell")]
                for i in stat_choices:
                    markup.add(i)

                enemy_hero = HeroData(enemy_player)
                bot.send_photo(chat_id,
                               photo=classes_urls[enemy_hero.hero_class],
                               caption=hero_text_repr(account, enemy_hero),
                               reply_markup=markup
                               )




@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


