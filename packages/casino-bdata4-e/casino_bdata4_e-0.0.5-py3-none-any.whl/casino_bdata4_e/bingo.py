import random
import numpy as np

class BingoError(Exception):
    """Base exception for errors related to the bingo game."""
    pass

class InvalidCardError(BingoError):
    """Exception raised when the card selection is invalid."""
    pass

class BingoGame:
    @staticmethod
    def generate_cards(players):
        """
        Generates bingo cards for each player.
        Each card contains 15 random numbers from 1 to 90.
        """
        cards = {}
        for player in range(1, players + 1):
            card_name = []
            while len(card_name) < 15:
                number = random.randint(1, 90)
                if number not in card_name:
                    card_name.append(number)
                    card_name.sort()
            card_matrix = np.array(card_name).reshape(3, 5)
            cards[f"{player}"] = card_matrix
        return cards

    @staticmethod
    def show_all_cards(cards):
        """
        Displays all bingo cards available.
        """
        print("These are all the available cards:")
        for player, card in cards.items():
            print(f"Card {player}:")
            for row in card:
                print(row)
            print()

    @staticmethod
    def generate_bingo_drum():
        """
        Generates the bingo drum with numbers from 1 to 90.
        """
        return list(range(1, 91))

    def select_card(self, cards):
        """
        Allows the player to choose a card to play with.
        Displays the selected card.
        """
        self.show_all_cards(cards)
        try:
            selection = input("Choose the number of the card you want to play with: ").strip()
            if selection in cards:
                print(f"\nYou have chosen card {selection}. Your card is:")
                for row in cards[selection]:
                    print(row)
                return cards[selection]
            else:
                raise InvalidCardError("Invalid card selection.")
        except InvalidCardError as e:
            print(e)
            return None

    def show_card(self, colors, card):
        """
        Displays the player's card with colored numbers.
        Green for marked numbers and red for unmarked ones.
        """
        for row in card:
            marked_row = [
                f"\033[32m{num}\033[0m" if colors[num] else f"\033[31m{num}\033[0m"
                for num in row
            ]
            print(' '.join(marked_row))
        print()  # Blank line to separate cards

    def play(self):
        """
        Main function to start and play the bingo game.
        """
        try:
            num_players = int(input("How many players do you want to play bingo with? "))
            if num_players < 1:
                raise ValueError("Number of players must be at least 1.")
            
            cards = self.generate_cards(num_players)
            card = self.select_card(cards)
            if card is None:
                return

            drum = self.generate_bingo_drum()
            random.shuffle(drum)  # Shuffle the drum for random draws
            print("Bingo drum is ready, let the game begin!\n")
            
            marked = {n: False for n in card.flatten()}
            colors = {n: False for n in card.flatten()}  # False for red, True for green
            line_printed = False
            bingo = False
            draws = 0

            while not bingo:
                input(f"\nPress Enter to draw a number from the drum... ({draws + 1} draws)")
                number = drum[draws]
                print(f"The number {number} has been drawn!")

                if number in marked:
                    marked[number] = True
                    colors[number] = True  # Update to green if marked
                    print("YES, it’s on your card!")
                else:
                    print("NO, it’s not on your card.")

                self.show_card(colors, card)  # Display the updated card with colors

                # Check for line
                for i in range(3):
                    if all(marked[card[i, j]] for j in range(5)):
                        if not line_printed:
                            line_printed = True
                            print("You have a line! But the game continues.")

                # Check for bingo
                if all(marked[num] for num in card.flatten()):
                    bingo = True
                    print("Bingo! You've won!")
                    break

                draws += 1

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
