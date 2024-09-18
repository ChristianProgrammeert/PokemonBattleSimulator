from types import NoneType

import requests
import random


def get_pokemon_info(pokemon_name, all_moves=False):
    """Get information about a Pokémon from the PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
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
        #Increase the HP stat by 110
        #because the base HP stat is too low
        pokemon_info["stats"]["hp"] = 2 * pokemon_info["stats"]["hp"]
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

def display_pokemon_info(pokemon):
    if pokemon:
        print(f"\nName: {pokemon['name']}")
        print(f"Type(s): {', '.join(pokemon['types']).capitalize()}")
        print("Available Moves:")

        print("Base Stats:")
        for stat_name, stat_value in pokemon["stats"].items():
            print(f"  {stat_name}:".replace("-", " ").capitalize(),stat_value)

        print("\nLearnable Moves: ", end="")
        print(", ".join([move["move"]["name"].replace("-", " ").capitalize() for move in pokemon["moves"]]))

    else:
        print("Pokémon not found!")

#what offensive type is effective against what defensive type
type_effectiveness_chart = {
    "Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
               "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0, "Dragon": 1, "Dark": 1,
               "Steel": 0.5, "Fairy": 1},
    "Fire": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1, "Ice": 2, "Fighting": 1, "Poison": 1,
             "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 0.5, "Dark": 1,
             "Steel": 2, "Fairy": 1},
    "Water": {"Normal": 1, "Fire": 2, "Water": 0.5, "Grass": 0.5, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
              "Ground": 2, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 0.5, "Dark": 1,
              "Steel": 1, "Fairy": 1},
    "Grass": {"Normal": 1, "Fire": 0.5, "Water": 2, "Grass": 0.5, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 0.5,
              "Ground": 2, "Flying": 0.5, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1, "Dragon": 0.5, "Dark": 1,
              "Steel": 0.5, "Fairy": 1},
    "Electric": {"Normal": 1, "Fire": 1, "Water": 2, "Grass": 0.5, "Electric": 0.5, "Ice": 1, "Fighting": 1,
                 "Poison": 1, "Ground": 0, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 0.5,
                 "Dark": 1, "Steel": 1, "Fairy": 1},
    "Ice": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1, "Ice": 0.5, "Fighting": 1, "Poison": 1,
            "Ground": 2, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 1,
            "Steel": 0.5, "Fairy": 1},
    "Fighting": {"Normal": 2, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 2, "Fighting": 1, "Poison": 0.5,
                 "Ground": 1, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dragon": 1, "Dark": 2,
                 "Steel": 2, "Fairy": 0.5},
    "Poison": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 0.5,
               "Ground": 0.5, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0.5, "Dragon": 1, "Dark": 1,
               "Steel": 0, "Fairy": 2},
    "Ground": {"Normal": 1, "Fire": 2, "Water": 1, "Grass": 0.5, "Electric": 2, "Ice": 1, "Fighting": 1, "Poison": 2,
               "Ground": 1, "Flying": 0, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1,
               "Steel": 2, "Fairy": 1},
    "Flying": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 0.5, "Ice": 1, "Fighting": 2, "Poison": 1,
               "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 1, "Dark": 1,
               "Steel": 0.5, "Fairy": 1},
    "Psychic": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 2, "Poison": 2,
                "Ground": 1, "Flying": 1, "Psychic": 0.5, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 0,
                "Steel": 0.5, "Fairy": 1},
    "Bug": {"Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 2, "Electric": 1, "Ice": 1, "Fighting": 0.5, "Poison": 0.5,
            "Ground": 1, "Flying": 0.5, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 0.5, "Dragon": 1, "Dark": 2,
            "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Normal": 1, "Fire": 2, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 2, "Fighting": 0.5, "Poison": 1,
             "Ground": 0.5, "Flying": 2, "Psychic": 1, "Bug": 2, "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1,
             "Steel": 0.5, "Fairy": 1},
    "Ghost": {"Normal": 0, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
              "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 0.5,
              "Steel": 1, "Fairy": 1},
    "Dragon": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1,
               "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 1,
               "Steel": 0.5, "Fairy": 0},
    "Dark": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 0.5, "Poison": 1,
             "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 0.5,
             "Steel": 1, "Fairy": 0.5},
    "Steel": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 1, "Electric": 0.5, "Ice": 2, "Fighting": 1, "Poison": 1,
              "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1,
              "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 2, "Poison": 0.5,
              "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 2,
              "Steel": 0.5, "Fairy": 1}
}
