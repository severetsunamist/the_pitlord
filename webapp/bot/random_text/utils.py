def random_nickname():
    firsts = ['Bold', 'Tough', 'Sharp', 'Sneaky', 'Holly', 'Divine', 'Bloody', 'Evil', 'Creepy', 'Awesome', 'Serious',
              'Hip', 'Crazy', 'Mad', 'Agent', 'Liquid', 'Silver', 'Glorious', 'Wild', 'Old', 'Elder', 'Quick', 'Uncle']
    seconds = ['John', 'Bill', 'Will', 'Danny', 'Sam', 'Max', 'Joe', 'Bart', 'Rick', 'Ken', 'Richard', 'Bob', 'Ben', 'Victor',
               'George', 'Benedict', 'Karl', 'Tonny', 'Tom', 'Harry', 'Fedor', 'Charlie', 'Mark', 'Konstantin', 'Oliver']

    nickname = f'{random.choice(firsts)} {random.choice(seconds)}'
    return nickname
def random_class():
    all_classes = ['Paladin', 'Wizard', 'Druid', 'Shaman', 'Knight', 'Necromancer', 'Assassin', 'Archer',
                   'Sourcer', 'Bard', 'Headsman', 'Undertaker', 'Monk']
    return random.choice(all_classes)

CLASSES = [
    ('Paladin', 'Paladin'),
    ('Knight', 'Knight'),
    ('Assassin', 'Assassin'),
    ('Necromancer', 'Necromancer'),
    ('Archer', 'Archer'),
    ('Druid', 'Druid'),
    ('Shaman', 'Shaman'),
    ('Sorcerer', 'Sorcerer'),
    ('Wizard', 'Wizard'),
    ('Monk', 'Monk'),
    ('Headsman', 'Headsman'),
    ('Undertaker', 'Undertaker'),
    ('Bard', 'Bard')
]
STAGES = [
    ('STATS', 'STATS'),
    ('ITEMS', 'ITEMS'),
    ('READY', 'READY'),
    ('FIGHT', 'FIGHT'),
    ('REWARD', 'REWARD'),
]