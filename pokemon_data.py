from types import NoneType

import requests
import random

def get_pokemon_info(pokemon_name, all_moves=False):
    """Get information about a Pokémon from the PokéAPI."""
    #Make a request to the PokéAPI (set all capital letters to lowercase and replace spaces with dashes to get the right formatting)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower().replace(' ', '-')}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        moves = []
        #Get only damaging moves (physical or special)
        if not all_moves:
            # Shuffle the list of moves
            random.shuffle(pokemon_data["moves"])
            # Get 4 unique damaging moves to choose from.
            for move in pokemon_data["moves"]:
                move_info = get_damaging_moves(move["move"]["name"])
                if move_info:
                    moves.extend(move_info)
                # If we have 4 moves we can stop the loop
                if len(moves) == 4:
                    break
        else:
            moves = pokemon_data["moves"]

        pokemon_info = {
            "name": pokemon_data["name"].replace("-", " ").capitalize(),
            "gender": random.choice(["♂", "♀"]),
            "types": [type_data["type"]["name"].capitalize() for type_data in pokemon_data["types"]],
            "moves": moves,
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]},
            "shiny": False
        }
        # #Increase the HP stat by 110
        # #because the base HP stat is too low
        # pokemon_info["stats"]["hp"] = 2 * pokemon_info["stats"]["hp"]
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
                "type": move_data["type"]["name"].capitalize(),
                "current_pp": int(move_data["pp"]),
                "max_pp": int(move_data["pp"])
            }
            return [move_info]
    return []

