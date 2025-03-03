from bot.models import PlayerModel, HeroModel

class HeroData:
    def __init__(self, acc):
        self.account = PlayerModel.objects.get(tg_id=acc)
        self.char = HeroModel.objects.get(hero_owner=self.account.id)
        self.hero_class = self.char.hero_class
        self.next_lvl_exp = self.account.next_lvl_exp
        self.exp = self.account.exp
        self.free_stats = self.char.hero_free_stats
        self.hero_max_hp = self.char.hero_max_hp
        self.hero_cur_hp = self.char.hero_cur_hp
        self.hero_max_ap = self.char.hero_max_ap
        self.hero_cur_ap = self.char.hero_cur_ap
        self.hero_max_mp = self.char.hero_max_mp
        self.hero_cur_mp = self.char.hero_cur_mp
        self.level = self.account.level + self.char.exp_gained
        self.hero_nickname = self.char.nickname
        self.hero_str = self.char.hero_str
        self.hero_agl = self.char.hero_agl
        self.hero_int = self.char.hero_int
        self.hero_dmg_min = 0
        self.hero_dmg_max = 0
        self.hero_armor = 0



def hero_text_repr(account, character):
    exp_bar = ''
    hp_bar = ''
    ap_bar = ''
    mp_bar = ''
    exp_chunck = character.next_lvl_exp / 13
    exp_chuncks_filled = int(character.exp / exp_chunck)
    for i in range(exp_chuncks_filled):
        exp_bar += '🟧'
    for y in range(13 - exp_chuncks_filled):
        exp_bar += '◽️'

    hp_chunck = character.hero_max_hp / 13
    hp_chuncks_filled = round(character.hero_cur_hp / hp_chunck)
    for i in range(hp_chuncks_filled):
        hp_bar += '🟥'
    for y in range(13 - hp_chuncks_filled):
        hp_bar += '⬜️'

    ap_chunck = character.hero_max_ap / 13
    ap_chuncks_filled = round(character.hero_cur_ap / ap_chunck)
    for i in range(ap_chuncks_filled):
        ap_bar += '🟩'
    for y in range(13 - ap_chuncks_filled):
        ap_bar += '⬜️'

    mp_chunck = character.hero_max_mp / 13
    mp_chuncks_filled = round(character.hero_cur_mp / mp_chunck)
    for i in range(mp_chuncks_filled):
        mp_bar += '🟪'
    for y in range(13 - mp_chuncks_filled):
        mp_bar += '⬜️'
    hero_template = f'''
{exp_bar}
EXP 🔸 {character.exp} / {character.next_lvl_exp}
LVL 🔹 {character.level} 
{character.hero_nickname}
〰〰〰〰〰〰〰〰〰〰〰〰〰
{hp_bar}
{character.hero_cur_hp}/{character.hero_max_hp} HP
{ap_bar}
{character.hero_cur_ap}/{character.hero_max_ap} AP
{mp_bar}
{character.hero_cur_mp}/{character.hero_max_mp} MP

STR🔴{character.hero_str}      AGL🟢{character.hero_agl}      INT🟣{character.hero_int}
〰〰〰〰〰〰〰〰〰〰〰〰〰
DMG🔺3 - 15     ARM🔰2
'''
    return hero_template

    

def battle_text_repr(you, enemy):
    def render_bars(character):
        hp_bar = ''
        ap_bar = ''
        mp_bar = ''

        hp_chunck = character.hero_max_hp / 13
        hp_chuncks_filled = round(character.hero_cur_hp / hp_chunck)
        for i in range(hp_chuncks_filled):
            hp_bar += '🟥'
        for y in range(13 - hp_chuncks_filled):
            hp_bar += '⬜️'

        ap_chunck = character.hero_max_ap / 13
        ap_chuncks_filled = round(character.hero_cur_ap / ap_chunck)
        for i in range(ap_chuncks_filled):
            ap_bar += '🟩'
        for y in range(13 - ap_chuncks_filled):
            ap_bar += '⬜️'

        mp_chunck = character.hero_max_mp / 13
        mp_chuncks_filled = round(character.hero_cur_mp / mp_chunck)
        for i in range(mp_chuncks_filled):
            mp_bar += '🟪'
        for y in range(13 - mp_chuncks_filled):
            mp_bar += '⬜️'
        return hp_bar, ap_bar, mp_bar


    enemy_hp_bar, enemy_ap_bar, enemy_mp_bar = render_bars(enemy)
    your_hp_bar, your_ap_bar, your_mp_bar = render_bars(you)

    battle_template = f'''

<b>☠ENEMY☠</b> <i>{enemy.hero_nickname}</i>

STR🔴{enemy.hero_str}      AGL🟢{enemy.hero_agl}      INT🟣{enemy.hero_int}

{enemy_hp_bar}
{enemy.hero_cur_hp}/{enemy.hero_max_hp} HP
{enemy_ap_bar}
{enemy.hero_cur_ap}/{enemy.hero_max_ap} AP
{enemy_mp_bar}
{enemy.hero_cur_mp}/{enemy.hero_max_mp} MP

🔺🔻🔺🔻🔺🔻<b>VS</b>🔺🔻🔺🔻🔺🔻

<b>⚔HERO⚔</b> <i>{you.hero_nickname}</i>

STR🔴{you.hero_str}      AGL🟢{you.hero_agl}      INT🟣{you.hero_int}

{your_hp_bar}
{you.hero_cur_hp}/{you.hero_max_hp} HP
{your_ap_bar}
{you.hero_cur_ap}/{you.hero_max_ap} AP
{your_mp_bar}
{you.hero_cur_mp}/{you.hero_max_mp} MP

'''
    return battle_template