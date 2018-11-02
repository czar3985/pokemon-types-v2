# INITIAl_ENTRIES.PY populates the database with all the possible pokemon
# types, the first three pokemon entries and their corresponding details

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Pokemon, Category, Type, Move, User
from view_model import get_type_id, get_move_id

engine = create_engine('sqlite:///pokemon.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a 'staging zone' for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create first user
user_kanto_admin = User(name='KantoAdmin', email='pixie.czar@gmail.com')
session.add(user_kanto_admin)
session.commit()
print('Added first user')

# Types
type_bug = Type(name='Bug')
type_dark = Type(name='Dark')
type_ground = Type(name='Ground')
type_dragon = Type(name='Dragon')
type_ice = Type(name='Ice')
type_electric = Type(name='Electric')
type_normal = Type(name='Normal')
type_fairy = Type(name='Fairy')
type_fighting = Type(name='Fighting')
type_psychic = Type(name='Psychic')
type_rock = Type(name='Rock')
type_flying = Type(name='Flying')
type_steel = Type(name='Steel')
type_ghost = Type(name='Ghost')
type_fire = Type(name='Fire')
type_grass = Type(name='Grass')
type_poison = Type(name='Poison')
type_water = Type(name='Water')

session.add(type_bug)
session.add(type_dark)
session.add(type_ground)
session.add(type_dragon)
session.add(type_ice)
session.add(type_electric)
session.add(type_normal)
session.add(type_fairy)
session.add(type_fighting)
session.add(type_psychic)
session.add(type_rock)
session.add(type_flying)
session.add(type_steel)
session.add(type_ghost)
session.add(type_fire)
session.add(type_grass)
session.add(type_poison)
session.add(type_water)

session.commit()
print('Added all possible types')

# Categories
category_lizard = Category(name='Lizard')
category_seed = Category(name='Seed')
category_tiny_turtle = Category(name='Tiny Turtle')

session.add(category_lizard)
session.add(category_seed)
session.add(category_tiny_turtle)

session.commit()
print('Added initial categories')

# Moves
move_aqua_tail = Move(name='Aqua Tail')
move_bubble = Move(name='Bubble')
move_bite = Move(name='Bite')
move_double_edge = Move(name='Double-Edge')
move_dragon_rage = Move(name='Dragon Rage')
move_ember = Move(name='Ember')
move_fire_fang = Move(name='Fire Fang')
move_fire_spin = Move(name='Fire Spin')
move_flame_burst = Move(name='Flame Burst')
move_flamethrower = Move(name='Flamethrower')
move_growl = Move(name='Growl')
move_growth = Move(name='Growth')
move_hydro_pump = Move(name='Hydro Pump')
move_inferno = Move(name='Inferno')
move_iron_defense = Move(name='Iron Defense')
move_leech_seed = Move(name='Leech Seed')
move_poison_powder = Move(name='Poison Powder')
move_protect = Move(name='Protect')
move_rain_dance = Move(name='Rain Dance')
move_rapid_spin = Move(name='Rapid Spin')
move_razor_leaf = Move(name='Razor Leaf')
move_scary_face = Move(name='Scary Face')
move_scratch = Move(name='Scratch')
move_seed_bomb = Move(name='Seed Bomb')
move_skull_bash = Move(name='Skull Bash')
move_slash = Move(name='Slash')
move_sleep_powder = Move(name='Sleep Powder')
move_smokescreen = Move(name='Smokescreen')
move_sweet_scent = Move(name='Sweet Scent')
move_synthesis = Move(name='Synthesis')
move_tackle = Move(name='Tackle')
move_tail_whip = Move(name='Tail Whip')
move_take_down = Move(name='Take Down')
move_vine_whip = Move(name='Vine Whip')
move_water_gun = Move(name='Water Gun')
move_water_pulse = Move(name='Water Pulse')
move_withdraw = Move(name='Withdraw')
move_worry_seed = Move(name='Worry Seed')

session.add(move_aqua_tail)
session.add(move_bubble)
session.add(move_bite)
session.add(move_double_edge)
session.add(move_dragon_rage)
session.add(move_ember)
session.add(move_fire_fang)
session.add(move_fire_spin)
session.add(move_flame_burst)
session.add(move_flamethrower)
session.add(move_growl)
session.add(move_growth)
session.add(move_hydro_pump)
session.add(move_inferno)
session.add(move_iron_defense)
session.add(move_leech_seed)
session.add(move_poison_powder)
session.add(move_protect)
session.add(move_rain_dance)
session.add(move_rapid_spin)
session.add(move_razor_leaf)
session.add(move_scary_face)
session.add(move_scratch)
session.add(move_seed_bomb)
session.add(move_skull_bash)
session.add(move_slash)
session.add(move_sleep_powder)
session.add(move_smokescreen)
session.add(move_sweet_scent)
session.add(move_synthesis)
session.add(move_tackle)
session.add(move_tail_whip)
session.add(move_take_down)
session.add(move_vine_whip)
session.add(move_water_gun)
session.add(move_water_pulse)
session.add(move_withdraw)
session.add(move_worry_seed)

session.commit()
print('Added initial moves')

# Pokemon

# BULBASAUR
bulbasaur_type_id_list = []
bulbasaur_type_id_list.append(get_type_id('Grass', session))
bulbasaur_type_id_list.append(get_type_id('Poison', session))

bulbasaur_weakness_id_list = []
bulbasaur_weakness_id_list.append(get_type_id('Fire', session))
bulbasaur_weakness_id_list.append(get_type_id('Flying', session))
bulbasaur_weakness_id_list.append(get_type_id('Ice', session))
bulbasaur_weakness_id_list.append(get_type_id('Psychic', session))

bulbasur_move_id_list = []
bulbasur_move_id_list.append(get_move_id('Tackle', session))
bulbasur_move_id_list.append(get_move_id('Growl', session))
bulbasur_move_id_list.append(get_move_id('Leech Seed', session))
bulbasur_move_id_list.append(get_move_id('Vine Whip', session))
bulbasur_move_id_list.append(get_move_id('Poison Powder', session))
bulbasur_move_id_list.append(get_move_id('Sleep Powder', session))
bulbasur_move_id_list.append(get_move_id('Take Down', session))
bulbasur_move_id_list.append(get_move_id('Razor Leaf', session))
bulbasur_move_id_list.append(get_move_id('Sweet Scent', session))
bulbasur_move_id_list.append(get_move_id('Growth', session))
bulbasur_move_id_list.append(get_move_id('Double-Edge', session))
bulbasur_move_id_list.append(get_move_id('Worry Seed', session))
bulbasur_move_id_list.append(get_move_id('Synthesis', session))
bulbasur_move_id_list.append(get_move_id('Seed Bomb', session))

bulbasaur_evolution_id_list = []
bulbasaur_evolution_id_list.append(2)

bulbasaur = Pokemon(pokedex_id=1,
                    name='Bulbasaur',
                    description=('Bulbasaur can be seen napping in bright '
                                 'sunlight. There is a seed on its back. By '
                                 'soaking up the sun\'s rays, the seed grows '
                                 'progressively larger.'),
                    image=('https://assets.pokemon.com/assets/cms2/img/'
                           'pokedex/full/001.png'),
                    height=28,
                    weight=15.2,
                    is_mythical=False,
                    is_legendary=False,
                    evolution_before=None,
                    evolution_after_list=bulbasaur_evolution_id_list,
                    type_list=bulbasaur_type_id_list,
                    weakness_list=bulbasaur_weakness_id_list,
                    move_list=bulbasur_move_id_list,
                    category=category_seed,
                    user=user_kanto_admin)

# CHARMANDER
charmander_type_id_list = []
charmander_type_id_list.append(get_type_id('Fire', session))

charmander_weakness_id_list = []
charmander_weakness_id_list.append(get_type_id('Ground', session))
charmander_weakness_id_list.append(get_type_id('Rock', session))
charmander_weakness_id_list.append(get_type_id('Water', session))

charmander_move_id_list = []
charmander_move_id_list.append(get_move_id('Scratch', session))
charmander_move_id_list.append(get_move_id('Growl', session))
charmander_move_id_list.append(get_move_id('Ember', session))
charmander_move_id_list.append(get_move_id('Smokescreen', session))
charmander_move_id_list.append(get_move_id('Dragon Rage', session))
charmander_move_id_list.append(get_move_id('Scary Face', session))
charmander_move_id_list.append(get_move_id('Fire Fang', session))
charmander_move_id_list.append(get_move_id('Flame Burst', session))
charmander_move_id_list.append(get_move_id('Slash', session))
charmander_move_id_list.append(get_move_id('Flamethrower', session))
charmander_move_id_list.append(get_move_id('Fire Spin', session))
charmander_move_id_list.append(get_move_id('Inferno', session))

charmander_evolution_id_list = []
charmander_evolution_id_list.append(5)

charmander = Pokemon(pokedex_id=4,
                     name='Charmander',
                     description=('The flame that burns at the tip of its '
                                  'tail is an indication of its emotions. The '
                                  'flame wavers when Charmander is enjoying '
                                  'itself. If the Pokemon becomes enraged, '
                                  'the flame burns fiercely.'),
                     image=('https://assets.pokemon.com/assets/cms2/img/'
                            'pokedex/full/004.png'),
                     height=24,
                     weight=15.2,
                     is_mythical=False,
                     is_legendary=False,
                     evolution_before=None,
                     evolution_after_list=charmander_evolution_id_list,
                     type_list=charmander_type_id_list,
                     weakness_list=charmander_weakness_id_list,
                     move_list=charmander_move_id_list,
                     category=category_lizard,
                     user=user_kanto_admin)

# SQUIRTLE
squirtle_type_id_list = []
squirtle_type_id_list.append(get_type_id('Water', session))

squirtle_weakness_id_list = []
squirtle_weakness_id_list.append(get_type_id('Electric', session))
squirtle_weakness_id_list.append(get_type_id('Grass', session))

squirtle_move_id_list = []
squirtle_move_id_list.append(get_move_id('Tackle', session))
squirtle_move_id_list.append(get_move_id('Tail Whip', session))
squirtle_move_id_list.append(get_move_id('Water Gun', session))
squirtle_move_id_list.append(get_move_id('Withdraw', session))
squirtle_move_id_list.append(get_move_id('Bubble', session))
squirtle_move_id_list.append(get_move_id('Bite', session))
squirtle_move_id_list.append(get_move_id('Rapid Spin', session))
squirtle_move_id_list.append(get_move_id('Protect', session))
squirtle_move_id_list.append(get_move_id('Water Pulse', session))
squirtle_move_id_list.append(get_move_id('Aqua Tail', session))
squirtle_move_id_list.append(get_move_id('Skull Bash', session))
squirtle_move_id_list.append(get_move_id('Iron Defense', session))
squirtle_move_id_list.append(get_move_id('Rain Dance', session))
squirtle_move_id_list.append(get_move_id('Hydro Pump', session))

squirtle_evolution_id_list = []
squirtle_evolution_id_list.append(8)

squirtle = Pokemon(pokedex_id=7,
                   name='Squirtle',
                   description=('Squirtle\'s shell is not merely used for '
                                'protection. The shell\'s rounded shape and '
                                'the grooves on its surface help minimize '
                                'resistance in water, enabling this Pokemon '
                                'to swim at high speeds.'),
                   image=('https://assets.pokemon.com/assets/cms2/img/'
                          'pokedex/full/007.png'),
                   height=20,
                   weight=19.8,
                   is_mythical=False,
                   is_legendary=False,
                   evolution_before=None,
                   evolution_after_list=squirtle_evolution_id_list,
                   type_list=squirtle_type_id_list,
                   weakness_list=squirtle_weakness_id_list,
                   move_list=squirtle_move_id_list,
                   category=category_tiny_turtle,
                   user=user_kanto_admin)
session.add(bulbasaur)
session.add(charmander)
session.add(squirtle)

session.commit()

print('Added initial pokemon entries')
