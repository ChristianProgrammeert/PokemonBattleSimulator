import math
import random

from pokemon_data import type_effectiveness_chart


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
    print(f"{pokemon['name']} {pokemon['gender']} moves: ")
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


def print_move(pokemon, move):
    """Print the move used by the Pokémon"""
    print(f"\n{pokemon['name']} used: {move['name']}")


def decrease_pp(pokemon, move):
    """Decrease the PP of the move used by the Pokémon"""
    for i in range(len(pokemon["moves"])):
        if move["name"] == pokemon["moves"][i]["name"]:
            pokemon["moves"][i]["current_pp"] -= 1
    return pokemon

def add_to_pokedex(pokemon):
    # Read the pokedex file
    # First time this will not find a pokedex file because it has not been created yet
    #in this case the pokedex will be an empty list to iterate through
    try:
        with open("pokedex.txt", "r") as file:
            #remove the newline character from the file
            #this is so the pokemon name can be compared to the pokemon in the pokedex correctly
            pokedex = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        pokedex = []

    #Check if the pokemon is already in the pokedex
    #if this is not the case create a pokedex file if this has not been created yet and add the pokemon
    if pokemon['name'] in pokedex:
        print(f"{pokemon['name']} is already in your pokedex")
    else:
        try:
            with open("pokedex.txt", "a") as file:
                file.write(f"{pokemon['name']}\n")
                print(f"{pokemon['name']} is added to your pokédex\n")
        except IOError as e:
            print(f"Er is een fout opgetreden bij het opslaan van {pokemon['name']} in de pokedex: {e}\n")


def calculate_damage(attacking_pokemon, move_1, defending_pokemon):
    """Pokémon's way of damage calculation based on several factors"""

    #The damage calculation is based on the following formula with the following variables:
    # STAB = Same Type Attack Bonus
    # Type-effectiveness = how effective the move is against the defending pokemon
    # Random = random factor between 0.85 and 1
    # Move-Power = the power of the move
    # Attack = the attacking pokemon's attack (physical or special) stat
    # Defence = the defending pokemon's defence (physical or special) stat
    # Modifier = STAB * Type-effectiveness * Random
    # Damage = (((2 * 100 / 5 + 2) * move_power * Attack (physical or special) / Defence(physical or special) / 50 + 2) * Modifier
    # The damage is calculated as a float and is then rounded down to the nearest 10
    # The damage is then subtracted from the opponent's HP

    # initialize damage message
    message = ""
    # initialize STAB to 1
    stab = 1
    # if the move's type is the same as the attacking Pokémon's type(s), STAB is 1.5
    for pokemon_type in attacking_pokemon["types"]:
        if pokemon_type == move_1["type"]:
            stab = 1.5
            break

    #A random integer between 217 and to 255, divided by 255.
    random_number = random.randint(217, 255) / 255
    # get the type effectiveness of the move against the Pokémon
    # 2 is super effective, 0.5 is not very effective, 0 is no effect
    # default to 1 (neutral damage) if the type is not in the specific type dictionary

    type_1_effectiveness = type_effectiveness_chart[move_1["type"]].get(defending_pokemon["types"][0], 1)
    # if the defending Pokémon has two types, get the effectiveness of the move against the second type
    if len(defending_pokemon["types"]) > 1:
        type_2_effectiveness = type_effectiveness_chart[move_1["type"]].get(defending_pokemon["types"][1], 1)
    else:
        #else, set the second type to 1
        type_2_effectiveness = 1

    # If the move has no effect on one of the types, it deals no damage
    if type_1_effectiveness == 0 or type_2_effectiveness == 0:
        message = "It has no effect on the Pokémon."
        return 0, message

    # initialize attack and defence based on the move's damage class
    defense = defending_pokemon["stats"]["defense"]
    if move_1["damage_class"] == "special":
        defence = defending_pokemon["stats"]["special-defense"]
    attack = attacking_pokemon["stats"]["attack"]
    if move_1["damage_class"] == "special":
        attack = attacking_pokemon["stats"]["special-attack"]
    # If either attack or damage are greater than 255, both are divided by 4 and rounded down.
    if attack > 255 or defense > 255:
        attack = math.floor(attack / 4)
        defense = math.floor(defense / 4)

    # calculate the damage
    print(f"STAB: {stab}")
    print(f"Random: {random_number}")
    print(f"Move Power: {move_1['power']}")
    print(f"Attack: {attack}")
    print(f"Defence: {defense}")
    damage = ((2 * 100 / 5 + 2) * move_1["power"] * attack / defense / 50 + 2)
    # Apply STAB if applicable
    if stab == 1.5:
        # STAB is recognized as an addition of the damage calculated thus far divided by 2, rounded down, then added to the damage calculated thus far.
        stab_bonus = math.floor(damage / 2)
        damage += stab_bonus

    damage = damage * type_1_effectiveness * type_2_effectiveness
    #Before using the random number if the calculated damage thus far is 1, random is always 1.
    if damage == 1:
        random_number = 1

    total_damage = damage * type_1_effectiveness * type_2_effectiveness * random_number / 2

    print(f"Damage: {damage}")
    print(f"Modifier: {total_damage}")

    #If the Pokémon has only one type.
    if len(defending_pokemon["types"]) == 1:
        #If the type of a move is super effective against a type of its target, the damage is doubled;
        if type_1_effectiveness == 2:
            total_damage = math.floor(total_damage * 2)
            message = "It's super effective!"
        #If the type of a move is not very effective against a type of its target, the damage is halved;
        elif type_1_effectiveness == 0.5:
            total_damage = math.floor(total_damage / 2)
            message = "It's not very effective!"
        #If the type of a move has no effect against a type of its target, the move has no effect;
        elif type_1_effectiveness == 0:
            total_damage = 0
            message = "It has no effect on the Pokémon."
        #In every other case the move deals regular damage.
        else:
            message = "It deals regular damage!"
    #If the Pokémon has two types.
    else:
        #If the type of a move is super effective against both of the opponent's types (such as a Ground-type move used against a Steel/Rock Pokémon), then the move does 4 times  the damage.
        if type_1_effectiveness == 2 and type_2_effectiveness == 2:
            total_damage = math.floor(total_damage * 4)
            message = "It's super effective!"
        #If the type of a move is not very effective against both of the opponent's types (such as a Fighting-type move used against a Psychic/Flying Pokémon), then the move only does 1/4 of the damage.
        elif type_1_effectiveness == 0.5 and type_2_effectiveness == 0.5:
            total_damage = math.floor(total_damage / 4)
            message = "It's not very effective!"
        #If the type of a move is super effective against one of the opponent's types but not very effective against the other (such as a Grass-type move used against a Water/Flying Pokémon), then the move deals regular damage.
        elif type_1_effectiveness == 2 and type_2_effectiveness == 0.5:
            total_damage = math.floor(total_damage)
            message = "It deals regular damage!"
        #If the type of move is completely ineffective against one of the opponent's types, then the move does no damage regardless of how the Pokémon’s other type would be affected (as in an Electric-type move used against a Water/Ground Pokémon).
        elif type_1_effectiveness == 0 or type_2_effectiveness == 0:
            total_damage = 0
            message = "It has no effect on the Pokémon."
        # In every other case the move deals regular damage.
        else:
            message = "It deals regular damage!"

    total_damage = int(math.floor(total_damage / 10.0) * 10)
    print(f"Total Damage: {total_damage}")
    return total_damage, message
