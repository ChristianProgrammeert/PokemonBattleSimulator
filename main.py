import random

from pokemon_data import get_pokemon_info
from helper import print_move, decrease_pp, give_nickname, choose_move, calculate_damage, shiny_chance, add_to_pokedex, \
    display_pokemon_info, check_pokedex, perform_attack
from type_chart import type_effectiveness_chart

def main():
    print("Welcome to the Pokémon Battle Simulator!")
    while True:
        choice = input(
            "Do you want to: \n1. Start a Pokémon battle \n2. Add Pokémon to your Pokédex \n3. Check Type Effectiveness \n4. Exit\nChoice-number: ")
        if choice == "1":
            multiplayer = False
            pokemon = []
            nicknames = []

            game_mode = input("Do you want to play: 1. singleplayer or 2. multiplayer:\nChoice-number:  ")
            if game_mode == "2":
                multiplayer = True

            check_pokedex()

            #
            for i in range(2):
                #Change the input message based on the game mode
                if multiplayer:
                    name = input(f"Player {i + 1}, enter your Pokémon's name: ")
                    # Ask the players if they want to give their Pokémon a nickname
                    nicknames.append(input(f"Player {i + 1}, would you like to give your Pokémon a nickname?: "))
                else:
                    name = input("Enter Pokémon's name: ")
                    #give only your Pokémon a nickname
                    if i == 0:
                        nicknames.append(input(f"Would you like to give {name} a nickname?: "))
                #Get the Pokémon information from the PokéAPI
                pokemon.append(get_pokemon_info(name))
                shiny_chance(pokemon[i])
                if pokemon[i] is None:
                    print(f"Could not find {name}")
                    break
                #If the index is 0 and the length of the nicknames list is 1, give the nickname to the first Pokémon
                if i == 0 and len(nicknames) == 1:
                    #give the first Pokémon a nickname, because the other pokemon is not user controlled.
                    pokemon[0] = give_nickname(pokemon[0], nicknames[0])
                elif len(nicknames) > 1:
                    #give all Pokémon a nickname
                    pokemon[i] = give_nickname(pokemon[i], nicknames[i])

            # The battle is active while 1 of the 2 Pokémon has not fainted yet (hp > 0)
            #The pokemon battle is not created dynamically, it is hardcoded to be 2 players
            print(f"{pokemon[0]['name']} {pokemon[0]['gender']} vs. {pokemon[1]['name']} {pokemon[1]['gender']}")
            print("Let the battle begin!")
            while (pokemon[0]["stats"]["hp"] > 0) and (pokemon[1]["stats"]["hp"] > 0):
                print(
                    f"\n{pokemon[0]["name"]} {pokemon[0]['gender']} current HP: {pokemon[0]["stats"]["hp"]} & {pokemon[1]["name"]} {pokemon[1]['gender']} current HP: {pokemon[1]["stats"]["hp"]}")
                # Choose a move for each Pokémon
                move_a = choose_move(pokemon[0])
                # If the gamemode is multiplayer, the second player chooses a move
                # Otherwise, a random move is chosen
                if multiplayer:
                    move_b = choose_move(pokemon[1])
                else:
                    move_b = random.choice(pokemon[1]["moves"])

                #Who goes first?
                # Based on the speed stat, the Pokémon with the higher speed stat goes first, this move is printed first

                if pokemon[0]["stats"]["speed"] > pokemon[1]["stats"]["speed"]:
                    #The first pokémon is faster so it performs a move first
                    pokemon[0], pokemon[1] = perform_attack(pokemon[0], pokemon[1], move_a)
                    # Check if the second Pokémon can still attack
                    if pokemon[1]["stats"]["hp"] > 0:
                        pokemon[1], pokemon[0] = perform_attack(pokemon[1], pokemon[0], move_b)
                    else:
                        #If the second Pokémon has fainted, the battle is over and the first Pokémon wins
                        print(f"{pokemon[1]["name"]} has fainted! {pokemon[0]["name"]} wins!\n")
                        break
                else:
                    #The second pokémon is faster so it performs a move first
                    pokemon[1], pokemon[0] = perform_attack(pokemon[1], pokemon[0], move_b)
                    # Check if the first Pokémon can still attack
                    if pokemon[0]["stats"]["hp"] > 0:
                        pokemon[0], pokemon[1] = perform_attack(pokemon[0], pokemon[1], move_a)
                    else:
                        #If the first Pokémon has fainted, the battle is over and the second Pokémon wins
                        print(f"{pokemon[0]["name"]} has fainted! {pokemon[1]["name"]} wins!\n")
                        break

        elif choice == "2":
            #Pokedex
            pokemon_name = input(
                "Welcome to the pokédex where you can see types, moves, stats & evolutions of every Pokémon. "
                "\nAfter which you can add the Pokémon to your Pokédex to use in battle! "
                "\nEnter the name of the Pokémon you want to see: ")
            pokemon = get_pokemon_info(pokemon_name, True)
            if pokemon:
                display_pokemon_info(pokemon)
                choice = input(f"Do you wanna add {pokemon['name']} to your pokedex? (y/n): ")
                if choice.lower() == "y":
                    add_to_pokedex(pokemon)
                else:
                    print(f"{pokemon['name']} is not added to your pokedex")
            else:
                print(f"Could not find information about {pokemon_name}")

        elif choice == "3":
            #Pokémon type effectiveness checker
            pokemon_type = input("Enter the Pokémon type: ")
            #capitalize the first letter of the pokemon type
            pokemon_type = pokemon_type.capitalize()
            if pokemon_type not in type_effectiveness_chart.keys():
                print(f"{pokemon_type} is not a valid Pokémon type\n")
                continue
            #show all types which this type is effective against
            print(f"Type effectiveness of {pokemon_type} type:")
            for key, value in type_effectiveness_chart.items():
                if pokemon_type in value and value[pokemon_type] == 2:
                    print(f"    {key} type is super-effective against {pokemon_type} type")
                elif pokemon_type in value and value[pokemon_type] == 0.5:
                    print(f"    {key} type is not very effective against {pokemon_type} type")
                elif pokemon_type in value and value[pokemon_type] == 0:
                    print(f"    {key} type has no effect against {pokemon_type} type")
            #print a new line
            print()
        elif choice == "4":
            #exit with a pokemon greeting
            print("Thank you for playing the Pokémon Battle Simulator! Gotta catch 'em all!")
            break
        else:
            print("Invalid choice, please try again\n")


if __name__ == "__main__":
    main()
