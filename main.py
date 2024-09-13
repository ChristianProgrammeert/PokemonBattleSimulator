import math
import random

from pokemon_data import get_pokemon_info, display_pokemon_info
from helper import print_move, decrease_pp, give_nickname, choose_move, calculate_damage

def main():


    print("Welcome to the Pokémon Battle Simulator!")
    while True:
        choice = input("Do you want to \n1. Start a Pokémon battle \n2. Add Pokémon to your Pokédex \n3. Check Type Effectiveness \n4. Exit\nChoice-number: ")
        if choice == "1":

            #todo: implement file to open last searched pokemon in pokedex
            #with open(filepath) as file:
            #file = open(filepath, "r")
            #    last_searched = file.read()
            #file.write(pokemon_name\n)
            #or
            #file.append(pokemon_name\n)

            #try and except for fout afhandelingen
            #Value errors voor keuzes
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
                break
            if pokemon_2 is None:
                print("Could not find the opposing pokémon")
                break

            if multiplayer:
                nickname = input("Player 1, would you like to give your Pokémon a nickname?: ")
                nickname_2 = input("Player 2, would you like to give your Pokémon a nickname?: ")
                pokemon_2 = give_nickname(pokemon_2, nickname_2)
            else:
                nickname = input("Would you like to give your Pokémon a nickname?: ")

            pokemon_1 = give_nickname(pokemon_1, nickname)

            # The battle is active while 1 of the 2 Pokémon has not fainted yet (hp > 0)
            print(f"{pokemon_1['name']} vs. {pokemon_2['name']}")
            print("Let the battle begin!")
            while (pokemon_1["stats"]["hp"] > 0) and (pokemon_2["stats"]["hp"] > 0):
                print(
                    f"\n{pokemon_1["name"]} current HP: {pokemon_1["stats"]["hp"]} & {pokemon_2["name"]} current HP: {pokemon_2["stats"]["hp"]}")
                # Choosing of moves (you pick a move and the opponent gets a random moves selected from their 4 moves)

                move_1 = choose_move(pokemon_1)

                if multiplayer:
                    move_2 = choose_move(pokemon_2)
                else:
                    move_2 = random.choice(pokemon_2["moves"])



                # Question 1: How much damage is done?
                # The damage is calculated based on the move used and the defending Pokémon's stats and several other factors.
                damage_1, message_1 = calculate_damage(pokemon_1, move_1, pokemon_2)
                damage_2, message_2 = calculate_damage(pokemon_2, move_2, pokemon_1)

                # Question 2: How much HP is left?
                # The HP of the defending Pokémon is decreased by the damage done by the attacking Pokémon
                pokemon_1["stats"]["hp"] -= damage_2
                pokemon_2["stats"]["hp"] -= damage_1

                # Question 3: What happens to the PP of the move used?
                # decrease the pp of the moves used.
                pokemon_1 = decrease_pp(pokemon_1, move_1)
                pokemon_2 = decrease_pp(pokemon_2, move_2)

                # Question 4: Who goes first?
                # Based on the speed stat, the Pokémon with the higher speed stat goes first, this move is printed first
                if pokemon_1["stats"]["speed"] > pokemon_2["stats"]["speed"]:
                    print_move(pokemon_1, move_1)
                    print(message_1)
                    print_move(pokemon_2, move_2)
                    print(message_2)
                else:
                    print_move(pokemon_2, move_2)
                    print(message_2)
                    print_move(pokemon_1, move_1)
                    print(message_1)

            if pokemon_1["stats"]["hp"] <= 0:
                print(f"{pokemon_1["name"]} has fainted! {pokemon_2["name"]} wins!")
                print(f"Remaining HP: {pokemon_2["name"]}: {pokemon_2["stats"]["hp"]}")
            else:
                print(f"{pokemon_2["name"]} has fainted! {pokemon_1["name"]} wins!")
                print(f"Remaining HP: {pokemon_1["name"]}: {pokemon_1["stats"]["hp"]}")
        elif choice == "2":
            pokemon_name = input("Welcome to the pokédex where you can see types, moves & stats every Pokémon: \nEnter the name of the Pokémon you want to see: ")
            pokemon = get_pokemon_info(pokemon_name, True)
            if pokemon:
                display_pokemon_info(pokemon)
            else:
                print(f"Could not find information about {pokemon_name}")
        elif choice == "3":
            #Pokemon type effectiveness checker
            type_1 = input("Enter the type: ")
        elif choice == "4":
            break
        else:
            print("Invalid choice, please try again")






if __name__ == "__main__":
    main()







