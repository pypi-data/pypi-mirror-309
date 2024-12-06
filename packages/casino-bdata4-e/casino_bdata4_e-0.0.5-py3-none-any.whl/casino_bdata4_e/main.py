from casino_bdata4_e.roulette import RouletteGame
from casino_bdata4_e.cards import Blackjack, Poker
from casino_bdata4_e.bingo import BingoGame 
from casino_bdata4_e.dice import DiceGame

def main_menu():
    """
    Displays the main casino menu and handles user selection.
    """
    print("Welcome to the casino!")
    print("1. Play Roulette")
    print("2. Play Card Games")
    print("3. Play Bingo")
    print("4. Play Dice Games")
    print("5. Exit")

    option = input("Select an option: ")

    if option == "1":
        play_roulette()
    elif option == "2":
        play_card_games()
    elif option == "3":
        play_bingo()  # Actualización para usar la clase
    elif option == "4":
        play_dice_games()
    elif option == "5":
        print("Thank you for playing. See you next time!")
    else:
        print("Invalid option, please try again.")
        main_menu()

def play_roulette():
    """
    Starts a roulette game.
    """
    print("Starting Roulette...")
    game = RouletteGame()
    game.play()


def play_card_games():
    """
    Displays the menu for card games and handles user selection.
    """
    print("Select the card game you want to play:")
    print("1. Blackjack")
    print("2. Poker")
    print("3. Return to Main Menu")

    option = input("Select an option: ")

    if option == "1":
        play_blackjack()
    elif option == "2":
        play_poker()
    elif option == "3":
        main_menu()
    else:
        print("Invalid option, please try again.")
        play_card_games()

def play_blackjack():
    """
    Starts a game of Blackjack.
    """
    print("Starting Blackjack...")
    game = Blackjack()
    game.play()

def play_poker():
    """
    Starts a game of Poker with 2 players.
    """
    print("Starting Poker...")
    game = Poker(players=2)
    game.play()

def play_bingo():
    """
    Starts a bingo game.
    """
    print("Starting Bingo...")
    game = BingoGame() 
    game.play()  

def play_dice_games():
    """
    Starts a dice game.
    """
    print("Starting the Dice Game...")
    game = DiceGame()
    game.play()

if __name__ == "__main__":
    main_menu()
