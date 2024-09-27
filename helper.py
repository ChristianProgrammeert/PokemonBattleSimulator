import math
import random

from api_call import get_pokedex_info
from type_chart import type_effectiveness_chart

def give_nickname(pokemon, nickname):
    """Give a Pokémon a nickname"""
    if nickname.lower() != "no":
        pokemon["name"] = nickname + " (" + pokemon["name"] + ")"
    return pokemon

def shiny_chance(pokemon):
    """The chance of a Pokémon being shiny which is 1 in 4096"""
    if random.randint(1, 4096) == 1:
        print(f"{pokemon['name']} is shiny!")
        pokemon["name"] = pokemon["name"] + " ✨"

def choose_move(pokemon):
    """Choose a move for the Pokémon"""
    print(f"\n{pokemon['name']} {pokemon['gender']} moves: ")
    for i in range(len(pokemon["moves"])):
        print(
            f"|{i + 1}. {pokemon['moves'][i]['name']}/{pokemon['moves'][i]['damage_class']} {pokemon['moves'][i]['type']} type move [{pokemon['moves'][i]['power']} damage] [{pokemon['moves'][i]['current_pp']}/{pokemon['moves'][i]['max_pp']} pp]| ")
    move = input(f"Choose a move for {pokemon['name']} {pokemon['gender']}: ")
    # I've chosen switch case here to because there are 4 moves and every case more than three you don't want to use if else
    switcher = {
        "1": pokemon["moves"][0],
        "2": pokemon["moves"][1],
        "3": pokemon["moves"][2],
        "4": pokemon["moves"][3]
    }

    # The move is selected based on the user's input
    # If the input is not valid, a random move is selected
    move = switcher.get(move, random.choice(pokemon["moves"]))
    return move

def decrease_pp(pokemon, move):
    """Decrease the PP of the move used by the Pokémon"""
    for i in range(len(pokemon["moves"])):
        if move["name"] == pokemon["moves"][i]["name"]:
            pokemon["moves"][i]["current_pp"] -= 1
    return pokemon

def get_pokedex():
    """Get the user's Pokédex (text file)"""

    # Read the pokedex file
    # First time this will not find a pokedex file because it has not been created yet
    #in this case the pokedex will be an empty list to iterate through
    pokedex = []
    try:
        with open("pokedex.txt", "r") as file:
            #remove the newline character from the file
            #this is so the pokemon name can be compared to the pokemon in the pokedex correctly
            pokedex = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        #return empty list if the file is empty (so you can still iterate through it)
        return pokedex
    #return the pokedex list
    return pokedex

def add_to_pokedex(pokemon):
    """Add a Pokémon to the user's Pokédex (text file)"""
    pokedex = get_pokedex()
    #Check if the Pokémon is already in the Pokédex
    #if this is not the case create a Pokédex file if this has not been created yet and add the Pokémon
    if pokemon['name'] in pokedex:
        print(f"{pokemon['name']} is already in your pokedex")
    else:
        try:
            with open("pokedex.txt", "a") as file:
                file.write(f"{pokemon['name']}\n")
                print(f"{pokemon['name']} is added to your pokédex\n")
        except IOError as e:
            print(f"Er is een fout opgetreden bij het opslaan van {pokemon['name']} in de pokedex: {e}\n")

def check_pokedex():
    """Check if the user has a pokédex and if so, ask the user to choose a Pokémon from the pokédex"""
    pokedex = get_pokedex()

    if pokedex:
        print("Pokémon in your pokédex:", end=" ")
        for pokemon in pokedex:
            # print a list of pokemon which is comma seperated except for the last one
            print(f"{pokemon}", end=", " if pokemon != pokedex[-1] else "\n")
            # Prompt the user to choose a Pokémon from the Pokédex or choose one themselves
        print("You can choose a Pokémon from your Pokédex or pick one of the 1,164 Pokémon available.")

def display_pokemon_info(pokemon):
    """Display information about a Pokémon"""
    if pokemon:
        print(f"\nName: {pokemon['name']}")
        print(f"Type(s): {', '.join(pokemon['types']).capitalize()}\n")
        print(get_pokedex_info(pokemon["name"]))

        print("\nBase Stats:")
        for stat_name, stat_value in pokemon["stats"].items():
            print(f"  {stat_name}:".replace("-", " ").capitalize(),stat_value)

        print("\nAvailable Moves: ", end="")
        print(", ".join([move["move"]["name"].replace("-", " ").capitalize() for move in pokemon["moves"]]))

    else:
        print("Pokémon not found!")

def get_stab(pokemon, move):
    """Check if the Pokémon has STAB (Same Type Attack Bonus)"""
    for pokemon_type in pokemon["types"]:
        if pokemon_type == move["type"]:
            return 1.5
    return 1

def get_type_effectiveness(move, defending_pokemon):
    """Get the effectiveness of the move against the defending Pokémon"""
    # 2 is super effective, 0.5 is not very effective, 1 is neutral damage & 0 is no effect.
    type_1_effectiveness = type_effectiveness_chart[move["type"]].get(defending_pokemon["types"][0], 1)
    # if the defending Pokémon has two types, get the effectiveness of the move against the second type.
    if len(defending_pokemon["types"]) > 1:
        type_2_effectiveness = type_effectiveness_chart[move["type"]].get(defending_pokemon["types"][1], 1)
    else:
        # If the Pokémon has no second type, set the type_2_effectiveness to 1.
        type_2_effectiveness = 1

    return type_1_effectiveness, type_2_effectiveness


def get_damage_class(attacking_pokemon, move, defending_pokemon):
    """Get the damage class of the move"""
    # initialize attack and defence based on the move's damage class.
    defense = defending_pokemon["stats"]["defense"]
    if move["damage_class"] == "special":
        defense = defending_pokemon["stats"]["special-defense"]
    attack = attacking_pokemon["stats"]["attack"]
    if move["damage_class"] == "special":
        attack = attacking_pokemon["stats"]["special-attack"]
    # If either attack or damage are greater than 255, both are divided by 4 and rounded down.
    if attack > 255 or defense > 255:
        attack = math.floor(attack / 4)
        defense = math.floor(defense / 4)
    return attack, defense


def apply_type_effectiveness(total_damage, type_1_effectiveness, type_2_effectiveness, defending_pokemon):
    """Apply the type effectiveness to the damage and create a message based on the effectiveness"""
    # If the Pokémon has only one type.
    if len(defending_pokemon["types"]) == 1:
        # If the type of a move is super effective against a type of its target, the damage is doubled as in the case of a Fire-type move used against a Grass Pokémon.
        if type_1_effectiveness == 2:
            total_damage = math.floor(total_damage * 2)
            message = "It's super effective!"
        # If the type of a move is not very effective against a type of its target, the damage is halved as in the case of a Water-type move used against a Grass Pokémon.
        elif type_1_effectiveness == 0.5:
            total_damage = math.floor(total_damage / 2)
            message = "It's not very effective!"
        # If the type of a move has no effect against a type of its target, the move has no effect on the target Pokémon as in the case of a Ground-type move used against a Flying Pokémon.
        elif type_1_effectiveness == 0:
            total_damage = 0
            message = "It has no effect on the Pokémon."
        # In every other case the move deals regular damage.
        else:
            message = "It deals regular damage!"
    # If the Pokémon has two types.
    else:
        # If the type of a move is super effective against both of the opponent's types (such as a Ground-type move used against a Steel/Rock Pokémon), then the move does 4 times  the damage.
        if type_1_effectiveness == 2 and type_2_effectiveness == 2:
            total_damage = math.floor(total_damage * 4)
            message = "It's super effective!"
        # If the type of a move is not very effective against both of the opponent's types (such as a Fighting-type move used against a Psychic/Flying Pokémon), then the move only does 1/4 of the damage.
        elif type_1_effectiveness == 0.5 and type_2_effectiveness == 0.5:
            total_damage = math.floor(total_damage / 4)
            message = "It's not very effective!"
        # If the type of a move is super effective against one of the opponent's types but not very effective against the other (such as a Grass-type move used against a Water/Flying Pokémon), then the move deals regular damage.
        elif type_1_effectiveness == 2 and type_2_effectiveness == 0.5:
            total_damage = math.floor(total_damage)
            message = "It deals regular damage!"
        # If the type of move is completely ineffective against one of the opponent's types, then the move does no damage regardless of how the Pokémon’s other type would be affected (as in an Electric-type move used against a Water/Ground Pokémon).
        elif type_1_effectiveness == 0 or type_2_effectiveness == 0:
            total_damage = 0
            message = "It has no effect on the Pokémon."
        # In every other case the move deals regular damage.
        else:
            message = "It deals regular damage!"
    return total_damage, message


def calculate_damage(attacking_pokemon, move, defending_pokemon):
    """Pokémon's way of damage calculation based on several factors"""

    #The damage calculation is based on the following formula with the following variables:
    # STAB = Same Type Attack Bonus
    # Type-effectiveness = how effective the move is against the defending pokemon
    # Random = random factor between 217 and 255 divided by 255
    # Move-Power = the power of the move
    # Attack = the attacking pokemon's attack (physical or special) stat
    # Defence = the defending pokemon's defence (physical or special) stat
    # Damage = (((2 * 100 / 5 + 2) * move_power * Attack (physical or special) / Defence(physical or special) / 50 + 2)
    #Apply STAB if applicable to the damage at this point (damage += stab_bonus)
    #damage = damage * type_1_effectiveness * type_2_effectiveness
    #Apply Type effectiveness to the damage based on the defending pokemon's type(s)
    #Halve the damage to make the game more balanced
    # The damage is calculated as a float and is then rounded down to the nearest 10

    # initialize STAB to 1
    stab = get_stab(attacking_pokemon, move)

    #A random integer between 217 and to 255, divided by 255.
    random_number = random.randint(217, 255) / 255

    #get the type effectiveness of the move against the defending pokemon
    type_1_effectiveness, type_2_effectiveness = get_type_effectiveness(move, defending_pokemon)

    # If the move has no effect on one of the types, it deals no damage
    #This step is done before the damage calculation
    if type_1_effectiveness == 0 or type_2_effectiveness == 0:
        message = "It has no effect on the Pokémon."
        return 0, message

    #Get the attack and defense stats based on the move's damage class
    attack, defense = get_damage_class(attacking_pokemon, move, defending_pokemon)

    # calculate the initial damage
    damage = ((2 * 100 / 5 + 2) * move["power"] * attack / defense / 50 + 2)

    # Apply STAB if applicable
    if stab == 1.5:
        # STAB is recognized as an addition of the damage calculated thus far divided by 2, rounded down.
        # It is then added to the damage calculated thus far.
        stab_bonus = math.floor(damage / 2)
        damage += stab_bonus

    #Before using the random number if the calculated damage thus far is 1, random is always 1.
    if damage >= 1:
        random_number = 1

    damage = damage * type_1_effectiveness * type_2_effectiveness * random_number

    #Apply Type effectiveness to the damage:
    damage, message = apply_type_effectiveness(damage, type_1_effectiveness, type_2_effectiveness, defending_pokemon)

    #Halve the damage to make the game more balanced
    damage = damage / 2
    #The damage is rounded down to the nearest 10
    damage = int(math.floor(damage / 10.0) * 10)
    #If the damage has exceeded the defending Pokémon's HP, make it equal to the defending Pokémon's HP
    if damage > defending_pokemon["stats"]["hp"]:
        #If the damage is greater than the defending Pokémon's HP make it equal to the defending Pokémon's HP
        damage = defending_pokemon["stats"]["hp"]
    if damage == 0:
        message = "The move missed!"
    return damage, message

def perform_attack(attacking_pokemon, defending_pokemon, move):
    """Perform an attack on a Pokémon"""
    # How much damage is done?
    # The damage is calculated based on the move used and the defending Pokémon's stats and several other factors.
    damage, message = calculate_damage(attacking_pokemon, move, defending_pokemon)
    # How much HP is left?
    # The HP of the defending Pokémon is decreased by the damage done by the attacking Pokémon
    defending_pokemon["stats"]["hp"] -= damage
    # What happens to the PP of the move used?
    # decrease the pp of the moves used.
    attacking_pokemon = decrease_pp(attacking_pokemon, move)
    # Print the move
    print(f"\n{attacking_pokemon['name']} used: {move['name']}")
    #The corresponding message is printed
    print(message)
    #The damage done and the HP left of the defending Pokémon is printed
    print(f"{defending_pokemon['name']} took {damage} damage and has {defending_pokemon['stats']['hp']} HP left.")
    #return the attacking and defending Pokémon with their updated hp and decreased move pp
    return attacking_pokemon, defending_pokemon