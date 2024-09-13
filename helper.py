import random

def give_nickname(pokemon, nickname):
    if nickname.lower() != "no":
        pokemon["name"] = nickname + " (" + pokemon["name"] + ")"
    return pokemon

def choose_move(pokemon):
    print(f"{pokemon['name']} moves: ")
    for i in range(len(pokemon["moves"])):
        print(
            f"|{i + 1}. {pokemon['moves'][i]['name']}/{pokemon['moves'][i]['damage_class']} move [{pokemon['moves'][i]['power']} damage] [{pokemon['moves'][i]['current_pp']}/{pokemon['moves'][i]['max_pp']} pp]| ")
    move = input(f"Choose a move for {pokemon['name']}: ")
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
    print(f"\n{pokemon['name']} used: {move['name']}")

def decrease_pp(pokemon, move):
    for i in range(len(pokemon["moves"])):
            if move["name"] == pokemon["moves"][i]["name"]:
                pokemon["moves"][i]["current_pp"] -= 1
    return pokemon

