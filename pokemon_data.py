import requests
import random

def get_pokemon_info(pokemon_name):
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
        #Get 4 random damaging moves to choose from.
        random_moves = random.choices(damaging_moves, k=4)
        pokemon_info = {
            "name": pokemon_data["name"].replace("-", " ").capitalize(),
            #"abilities": random.choices([ability["ability"]["name"] for ability in pokemon_data["abilities"]]),
            "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]],
            "moves": random_moves,
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
        if move_data["damage_class"]["name"] in ["physical", "special"]:
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
        print(f"Type(s): {', '.join(pokemon['types'])}")
        print("Moves:")
        for move in pokemon["moves"]:
            print(f"  Name: {move['name']}")
            print(f"    Power: {move['power']}")
            print(f"    Damage Class: {move['damage_class']}")
            print(f"    Type: {move['type']}")
            print(f"    PP: {move['pp']}")
        print("Base Stats:")
        for stat_name, stat_value in pokemon["base_stats"].items():
            print(f"  {stat_name}: {stat_value}")
    else:
        print("Pokémon not found!")