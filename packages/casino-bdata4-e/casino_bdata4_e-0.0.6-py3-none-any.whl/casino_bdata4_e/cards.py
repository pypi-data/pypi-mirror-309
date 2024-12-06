import random

SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:
    """
    Represents a playing card with a suit and a value.
    """
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    """
    Represents a deck of 52 playing cards.
    The deck is shuffled upon creation.
    """
    def __init__(self):
        self.cards = [Card(suit, value) for suit in SUITS for value in VALUES]
        random.shuffle(self.cards)

    def deal_card(self):
        """
        Deals a single card from the deck.
        Returns None if the deck is empty.
        """
        return self.cards.pop() if self.cards else None

    def __len__(self):
        """
        Returns the number of remaining cards in the deck.
        """
        return len(self.cards)


class Blackjack:
    """
    Simulates a game of Blackjack.
    The player competes against the dealer (house).
    """
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []

    def calculate_hand_value(self, hand):
        """
        Calculates the total value of a hand in Blackjack.
        Adjusts the value of Aces (11 or 1) as needed.
        """
        value = 0
        aces = 0
        for card in hand:
            # Use the value of the card to determine its score
            if card.value == 'A':
                aces += 1
                value += 11  # Initially count Ace as 11
            elif card.value in ['K', 'Q', 'J']:
                value += 10  # Face cards (King, Queen, Jack) are worth 10
            elif card.value == '10':
                value += 10  # '10' is worth 10
            else:
                value += int(card.value)  # Other cards are worth their numerical value

        # Adjust the value of Aces if the total value exceeds 21
        while value > 21 and aces > 0:
            value -= 10  # Treat one Ace as 1 instead of 11
            aces -= 1

        return value

    def play(self):
        """
        Starts a game of Blackjack, with the player making decisions.
        The dealer follows standard Blackjack rules.
        """
        print("Welcome to Blackjack!")
        
        # Deal the initial two cards to the player and dealer
        for _ in range(2):
            self.player_hand.append(self.deck.deal_card())
            self.dealer_hand.append(self.deck.deal_card())

        # Show the player's initial hand
        player_value = self.calculate_hand_value(self.player_hand)
        print("Your initial hand:", [str(card) for card in self.player_hand])
        print("Current hand value:", player_value)

        # Player's turn
        while True:
            if player_value >= 21:
                break
            action = input("Do you want to hit (h) or stand (s)? ").lower()
            if action == 'h':
                card = self.deck.deal_card()
                self.player_hand.append(card)
                player_value = self.calculate_hand_value(self.player_hand)
                
                # Show current state of the player's hand
                print("New card:", card)
                print("Your hand:", [str(card) for card in self.player_hand])
                print("Current hand value:", player_value)

                if player_value > 21:
                    print("You went over 21. You lost!")
                    return
            elif action == 's':
                print("You stand with a value of:", player_value)
                break
            else:
                print("Invalid option. Try again.")
        
        # Dealer's turn
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        print("Dealer's initial hand:", [str(card) for card in self.dealer_hand])
        print("Current dealer hand value:", dealer_value)
        
        while dealer_value < 17:
            card = self.deck.deal_card()
            self.dealer_hand.append(card)
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            print("Dealer hits:", card)
            print("Dealer's hand now:", [str(card) for card in self.dealer_hand])
            print("Current dealer hand value:", dealer_value)

        # Results
        print("\nFinal results:")
        print("Your hand:", [str(card) for card in self.player_hand], "with a value of:", player_value)
        print("Dealer's hand:", [str(card) for card in self.dealer_hand], "with a value of:", dealer_value)

        if player_value > 21:
            print("You went over 21. The dealer wins.")
        elif dealer_value > 21 or player_value > dealer_value:
            print("Congratulations, you won!")
        elif player_value < dealer_value:
            print("The dealer wins.")
        else:
            print("It's a tie.")



class Poker:
    """
    Simulates a simplified Poker game with multiple players and a dealer.
    """
    def __init__(self, players=2):
        self.deck = Deck()
        self.players = {f'Player {i+1}': [] for i in range(players)}
        self.players["Dealer"] = []  # Add the dealer as another player

    def deal_hands(self):
        """
        Deals 5 cards to each player and the dealer.
        """
        for player in self.players:
            self.players[player] = [self.deck.deal_card() for _ in range(5)]

    def show_hands(self):
        """
        Shows the current hands of all players and the dealer.
        """
        for player, hand in self.players.items():
            print(f"{player}: {', '.join(str(c) for c in hand)}")

    def calculate_hand_strength(self, hand):
        """
        Simulates a function to calculate the strength of a poker hand. This is a simplified example.
        """
        # This is just a basic example. You can add more advanced poker hand ranking logic.
        values = [card.value for card in hand]
        if 'A' in values:
            return 1  # Hand with Ace (just to illustrate)
        elif 'K' in values:
            return 2  # Hand with King
        elif 'Q' in values:
            return 3  # Hand with Queen
        return 0  # Basic hands

    def play(self):
        """
        Simulates a round of Poker with player and dealer decisions.
        """
        self.deal_hands()
        self.show_hands()

        # Player's turn
        print("\nYour turn:")
        decision = input("Do you want to stand (s) or bet (b)? ").lower()
        while decision not in ['s', 'b']:
            print("Invalid option. You must type 's' to stand or 'b' to bet.")
            decision = input("Do you want to stand (s) or bet (b)? ").lower()
        
        if decision == 'b':
            print("You bet.")
        else:
            print("You stand.")

        # Dealer's turn (simple decision based on hand strength)
        print("\nDealer's turn:")
        strength = self.calculate_hand_strength(self.players["Dealer"])
        if strength >= 1:
            print("The dealer bets.")
        else:
            print("The dealer stands.")

        # Final results
        print("\nResults:")
        print("Your hand:", [str(card) for card in self.players["Player 1"]])  # Convert Card objects to strings
        print("Dealer's hand:", [str(card) for card in self.players["Dealer"]])

        # Simulate winner (you can adjust this with more advanced poker rules)
        if strength >= 1:  # Dealer wins if they have an Ace or higher
            print("The dealer wins!")
        else:
            print("You won!")
