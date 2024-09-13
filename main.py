from helper import print_move, decrease_pp, give_nickname, choose_move
from pokemon_data import get_pokemon_info
import random

def main():
    multiplayer = False
    game_mode = input("Do you want to play singleplayer or multiplayer: ")
    if game_mode.lower() == "multiplayer":
        multiplayer = True
    if multiplayer:
        your_pokemon = input("Player 1, enter your Pokémon's name: ")
        opposing_pokemon = input("Player 2, enter your Pokémon's name: ")
    else:
        your_pokemon = input("Enter your Pokémon's name: ")
        opposing_pokemon = input("Enter the opposing Pokémon's name: ")

    pokemon_1 = get_pokemon_info(your_pokemon)
    pokemon_2 = get_pokemon_info(opposing_pokemon)
    if pokemon_1 is None:
        print("Could not find your Pokémon")
        exit()
    if pokemon_2 is None:
        print("Could not find the opposing pokémon")
        exit()

    if multiplayer:
        nickname = input("Player 1, would you like to give your Pokémon a nickname?: ")
        nickname_2 = input("Player 2, would you like to give your Pokémon a nickname?: ")
        pokemon_2 = give_nickname(pokemon_2, nickname_2)
    else:
        nickname = input("Would you like to give your Pokémon a nickname?: ")

    pokemon_1 = give_nickname(pokemon_1, nickname)

    # display_pokemon_info(pokemon_1)
    # display_pokemon_info(pokemon_2)

    # todo: battle simulation
    # The battle is active while of of the 2 pokemon has not fainted yet (hp > 0)
    print(f"{pokemon_1['name']} vs. {pokemon_2['name']}")
    print("Let the battle begin!")
    while (pokemon_1["stats"]["hp"] > 0) and (pokemon_2["stats"]["hp"] > 0):
        print(
            f"{pokemon_1["name"]} current HP: {pokemon_1["stats"]["hp"]} & {pokemon_2["name"]} current HP: {pokemon_2["stats"]["hp"]}")
        # Choosing of moves (you pick a move and the opponent gets a random moves selected from their 4 moves)

        move_1 = choose_move(pokemon_1)

        if multiplayer:
            move_2 = choose_move(pokemon_2)
        else:
            move_2 = random.choice(pokemon_2["moves"])

        # Question 1: Who goes first?
        # Based on the speed stat, the Pokémon with the higher speed stat goes first.
        if pokemon_1["stats"]["speed"] > pokemon_2["stats"]["speed"]:
            print_move(pokemon_1, move_1)
            print_move(pokemon_2, move_2)
        else:
            print_move(pokemon_2, move_2)
            print_move(pokemon_1, move_1)

        pokemon_1 = decrease_pp(pokemon_1, move_1)
        pokemon_2 = decrease_pp(pokemon_2, move_2)



        # Calculate damage based on type, stab, stats & a random factor
        # Question 2: How is damage calculated?
        # According to the official way the Pokémon company does it, damage is calculated using the following formula:
        # Modifier = STAB(1.5) * Type-effectiveness(0, 0.25, or 0.5 or 1) * Random(0.85 to 1)
        # Damage = (((2 * 100 / 5 + 2) * Move-Power * Attack(physical or special) / Defence(physical or special) / 50 + 2) * Modifier
        # The damage is then rounded down to the nearest 10
if __name__ == "__main__":
    main()







