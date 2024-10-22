from telebot import types

def action_markup(your_hero):
    markup = types.InlineKeyboardMarkup()
    action_choices = list()
    if your_hero.hero_cur_ap >= 35:
        action_choices.append(types.InlineKeyboardButton("🗡 Hit enemy", callback_data="hit"))
    if your_hero.hero_cur_ap >= 20:
        action_choices.append(types.InlineKeyboardButton("🛡 Block", callback_data="block"))
    if your_hero.hero_cur_mp >= 40:
        action_choices.append(types.InlineKeyboardButton("🔥 Use spell", callback_data="spell"))
    action_choices.append(types.InlineKeyboardButton("End round", callback_data="end_round"))
    for i in action_choices:
        markup.add(i)
    return markup