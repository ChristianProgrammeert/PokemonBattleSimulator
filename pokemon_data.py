from types import NoneType

import requests
import random

def get_pokemon_info(pokemon_name, all_moves=False):
    """Get information about a Pokémon from the PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        damaging_moves = []
        #Get only damaging moves (physical or special)
        for move in pokemon_data["moves"]:
            move_info = get_damaging_moves(move["move"]["name"])
            if move_info:
                damaging_moves.extend(move_info)
        if not all_moves:
            # Get 4 unique damaging moves to choose from.
            damaging_moves = random.sample(damaging_moves, 4)

        pokemon_info = {
            "name": pokemon_data["name"].replace("-", " ").capitalize(),
            #"abilities": random.choices([ability["ability"]["name"] for ability in pokemon_data["abilities"]]),
            "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]],
            "moves": damaging_moves,
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]}
        }
        return pokemon_info
    else:
        return None

def get_damaging_moves(move_name):
    """Get information about a move from the PokéAPI."""
    url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        move_data = response.json()
        #Some moves have a power of None which means they don't deal damage
        #We only want moves that deal damage so we filter those out.
        if type(move_data["power"]) is not NoneType and move_data["power"] > 0:
            move_info = {
                "name": move_data["name"].replace("-", " ").capitalize(),
                "power": move_data["power"],
                "damage_class": move_data["damage_class"]["name"],
                "type": move_data["type"]["name"],
                "current_pp": int(move_data["pp"]),
                "max_pp": int(move_data["pp"])
            }
            return [move_info]
    return []

def display_pokemon_info(pokemon):
    if pokemon:
        print(f"\nName: {pokemon['name']}")
        #print(f"Abilities: {', '.join(pokemon['abilities'])}")
        print(f"Type(s): {', '.join(pokemon['types']).capitalize()}")
        print("Available Moves:")

        print("Base Stats:")
        for stat_name, stat_value in pokemon["stats"].items():
            print(f"  {stat_name}:".replace("-", " ").capitalize(),{stat_value})

        print("Learnable Moves:")
        for move in pokemon["moves"].Items():
            print(move["name"].capitalize())

    else:
        print("Pokémon not found!")


type_effectiveness_chart = {
    "normal": {
        "fighting": 2,
        "normal": 1,
        "ghost": 0,
    },
    "fire": {
        "water": 2,
        "rock": 2,
        "ground": 2,
        "fire": 0.5,
        "grass": 2,
        "ice": 2,
        "bug": 2,
        "steel": 2,
        "fairy": 1,
    },
    "water": {
        "electric": 2,
        "grass": 2,
        "fire": 2,
        "water": 0.5,
        "ice": 1,
        "steel": 1,
    },
    "electric": {
        "ground": 0,
        "electric": 0.5,
        "flying": 2,
        "steel": 1,
    },
    "grass": {
        "fire": 2,
        "ice": 2,
        "poison": 2,
        "flying": 2,
        "bug": 2,
        "water": 2,
        "electric": 0.5,
        "grass": 0.5,
        "ground": 2,
    },
    "ice": {
        "fire": 2,
        "fighting": 2,
        "rock": 2,
        "steel": 2,
        "ice": 0.5,
    },
    "fighting": {
        "flying": 2,
        "psychic": 2,
        "fairy": 2,
        "bug": 0.5,
        "rock": 2,
        "dark": 2,
    },
    "poison": {
        "ground": 2,
        "psychic": 2,
        "grass": 2,
        "fighting": 0.5,
        "poison": 0.5,
        "bug": 1,
        "fairy": 2,
    },
    "ground": {
        "water": 2,
        "grass": 2,
        "ice": 2,
        "poison": 2,
        "rock": 2,
        "electric": 0,
    },
    "flying": {
        "electric": 2,
        "ice": 2,
        "rock": 2,
        "grass": 2,
        "fighting": 0.5,
        "bug": 2,
        "ground": 0,
    },
    "psychic": {
        "bug": 2,
        "ghost": 2,
        "dark": 2,
        "fighting": 2,
        "psychic": 0.5,
    },
    "bug": {
        "fire": 2,
        "flying": 2,
        "rock": 2,
        "grass": 2,
        "fighting": 0.5,
        "ground": 2,
    },
    "rock": {
        "water": 2,
        "grass": 2,
        "fighting": 2,
        "ground": 2,
        "steel": 2,
        "normal": 0.5,
        "fire": 2,
        "poison": 0.5,
        "flying": 2,
    },
    "ghost": {
        "ghost": 2,
        "dark": 2,
        "poison": 0.5,
        "bug": 1,
        "normal": 0,
        "fighting": 0,
    },
    "dragon": {
        "ice": 2,
        "dragon": 2,
        "fairy": 0,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
    },
    "dark": {
        "fighting": 2,
        "bug": 2,
        "fairy": 2,
        "ghost": 2,
        "dark": 0.5,
        "psychic": 0,
    },
    "steel": {
        "fire": 2,
        "fighting": 2,
        "ground": 2,
        "normal": 0.5,
        "grass": 0.5,
        "ice": 2,
        "flying": 0.5,
        "psychic": 0.5,
        "bug": 0.5,
        "rock": 2,
        "dragon": 0.5,
        "steel": 0.5,
        "fairy": 2,
        "poison": 0,
    },
    "fairy": {
        "poison": 2,
        "steel": 2,
        "fighting": 0.5,
        "bug": 0.5,
        "dark": 2,
        "dragon": 0,
    }
}