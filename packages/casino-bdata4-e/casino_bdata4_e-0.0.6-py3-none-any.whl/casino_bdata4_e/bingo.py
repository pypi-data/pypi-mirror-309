import random
import numpy as np

class BingoGame:
    """
    A class to represent a Bingo game.
    This class handles the creation of Bingo cards, game logic, and player interaction.
    """

    def __init__(self, num_players):
        """
        Initializes the Bingo game with a given number of players.
        
        :param num_players: The number of players participating in the game.
        """
        self.num_players = num_players
        self.cards = self.generate_cards()
        self.bombo = self.generate_bombo()
        self.card_colors = {}
        self.current_card = None

    def generate_cards(self):
        """
        Generates Bingo cards for each player.
        
        :return: A dictionary where the keys are player numbers and the values are 3x5 matrices representing Bingo cards.
        """
        cards = {}
        for player in range(1, self.num_players + 1):
            card = []
            while len(card) < 15:
                number = random.randint(1, 90)
                if number not in card:
                    card.append(number)
                    card.sort()
            matrix_3x5 = np.array(card).reshape(3, 5)
            cards[f"{player}"] = matrix_3x5
        return cards

    def show_all_cards(self):
        """
        Displays all the Bingo cards.
        """
        print("Here are all the available cards:")
        for player, card in self.cards.items():
            print(f"Card {player}:")
            for row in card:
                print(row)
            print()

    def show_card_with_colors(self, colors, card):
        """
        Shows the player's Bingo card with marked numbers displayed in colors.
        
        :param colors: A dictionary where keys are the numbers on the card and values are Booleans indicating whether the number is marked.
        :param card: The Bingo card to display.
        """
        for row in card:
            colored_row = [
                f"\033[32m{num}\033[0m" if colors[num] else f"\033[31m{num}\033[0m"
                for num in row
            ]
            print(' '.join(colored_row))
        print()  # Blank line for separation

    def select_player_card(self):
        """
        Prompts the player to choose a Bingo card and displays it.
        
        :return: The selected Bingo card.
        """
        self.show_all_cards()
        selection = input("Choose the card number you want to play with: ")
        if selection in self.cards:
            print(f"\nYou have chosen card {selection}. Your card is:")
            for row in self.cards[selection]:
                print(row)
            return self.cards[selection]
        else:
            print("Invalid card.")
            return None

    def generate_bombo(self):
        """
        Generates a shuffled list of Bingo numbers (from 1 to 90).
        
        :return: A list of unique numbers from 1 to 90.
        """
        bombo = []
        while len(bombo) < 90:
            number = random.randint(1, 90)
            if number not in bombo:
                bombo.append(number)
        return bombo

    def play(self):
        """
        Starts the Bingo game and handles the gameplay loop, including number drawing, card marking, and checking for bingo.
        """
        while True:
            try:
                num_players = int(input("How many people do you want to play Bingo with? "))
                if num_players >= 1:
                    break
                else:
                    print("Please enter a number greater than or equal to 1.")
            except ValueError:
                print("Please enter a valid number.")

        self.num_players = num_players
        self.cards = self.generate_cards()
        self.current_card = self.select_player_card()
        if self.current_card is None:
            return

        print("Bombo is ready, the game starts now!\n")
        marked = {n: False for n in self.current_card.flatten()}
        line_printed = False
        bingo = False
        draws = 0
        self.card_colors = {n: False for n in self.current_card.flatten()}  # False for red, True for green

        while not bingo:
            input(f"\nPress Enter to draw a number from the bombo... ({draws + 1} draws)")
            number = self.bombo[draws]
            if number in marked:
                marked[number] = True
                self.card_colors[number] = True  # Updates to green if marked
                print(f"Number {number} has been drawn -> It IS on your card!!")
            else:
                print(f"Number {number} has been drawn -> It is NOT on your card.")

            self.show_card_with_colors(self.card_colors, self.current_card)  # Display the updated card with colors

            for i in range(3):
                if all(marked[self.current_card[i, j]] for j in range(5)):
                    if not line_printed:
                        line_printed = True
                        print("You have a line! But the game continues.")
                    break

            if all(marked[num] for num in self.current_card.flatten()):
                bingo = True
                print("Bingo! You have won!")
                break

            for player, other_card in self.cards.items():
                marked_other = {n: False for n in other_card.flatten()}
                for i in range(draws + 1):
                    number = self.bombo[i]
                    if number in marked_other:
                        marked_other[number] = True

                for i in range(3):
                    if all(marked_other[other_card[i, j]] for j in range(5)):
                        if not line_printed:
                            print("--------------------------------------------------")
                            print(f"Player {player} has a line! But the game continues.".upper())
                            print("--------------------------------------------------")
                            line_printed = True
                        break

                if all(marked_other[num] for num in other_card.flatten()):
                    print("--------------------------------------------------")
                    print(f"Player {player} has bingo! The game ends.".upper())
                    return

            draws += 1

