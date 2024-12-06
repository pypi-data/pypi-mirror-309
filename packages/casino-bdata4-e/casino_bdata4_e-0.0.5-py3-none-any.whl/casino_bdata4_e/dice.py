import random

class DiceError(Exception):
    """Base exception for errors related to the dice game."""
    pass

class InvalidDiceError(DiceError):
    """Exception raised when the bet is invalid."""
    pass

class DiceGame:
    @staticmethod
    def roll_die():
        """
        Simulates the rolling of a six-sided die.
        
        Returns:
            int: A random number between 1 and 6.
        """
        return random.randint(1, 6)

    def specific_number(self):
        """
        Allows the player to bet on a specific number (between 1 and 6) to match the die roll.
        If the rolled number matches the bet, the player wins.
        """
        try:
            bet = int(input("Place your bet on a number between 1 and 6: "))
            if bet < 1 or bet > 6:
                raise InvalidDiceError("Invalid bet number. It must be between 1 and 6.")
            rolled_number = self.roll_die()
            if rolled_number == bet:
                print(f"Congratulations! You won. The rolled number was {rolled_number}.")
            else:
                print(f"Sorry, you didn't win this time. The rolled number was {rolled_number}.")
        except ValueError:
            print("Error: You must enter a number.")
        except InvalidDiceError as e:
            print(e)

    def high_or_low(self):
        """
        Allows the player to bet on whether the rolled number will be high (4-6) or low (1-3).
        """
        try:
            high_or_low = input("Bet on High (4-6) or Low (1-3): ").strip().lower()
            if high_or_low not in ['high', 'low']:
                raise InvalidDiceError("Invalid option. You must choose 'high' or 'low'.")
            rolled_number = self.roll_die()
            if (high_or_low == 'high' and rolled_number > 3) or (high_or_low == 'low' and rolled_number <= 3):
                print(f"Congratulations! You won. The rolled number is {high_or_low}.")
            else:
                print(f"Sorry, you didn't win this time. The rolled number is {'high' if rolled_number > 3 else 'low'}.")
        except InvalidDiceError as e:
            print(e)

    def even_or_odd(self):
        """
        Allows the player to bet on whether the rolled number will be even or odd.
        """
        try:
            even_or_odd = input("Bet on Even or Odd: ").strip().lower()
            if even_or_odd not in ['even', 'odd']:
                raise InvalidDiceError("Invalid option. You must choose 'even' or 'odd'.")
            rolled_number = self.roll_die()
            if (even_or_odd == 'even' and rolled_number % 2 == 0) or (even_or_odd == 'odd' and rolled_number % 2 == 1):
                print(f"Congratulations! You won. The rolled number is {'even' if rolled_number % 2 == 0 else 'odd'}.")
            else:
                print(f"Sorry, you didn't win this time. The rolled number is {'even' if rolled_number % 2 == 0 else 'odd'}.")
        except InvalidDiceError as e:
            print(e)

    def target_sum(self):
        """
        Allows the player to bet on a specific sum (between 2 and 12) of two dice rolls.
        """
        try:
            target = int(input("Place your bet on a sum (2-12): "))
            if target < 2 or target > 12:
                raise InvalidDiceError("Invalid number. It must be between 2 and 12.")
            die1 = self.roll_die()
            die2 = self.roll_die()
            total = die1 + die2
            print(f"You rolled {die1} and {die2}. Total sum: {total}")
            if total == target:
                print("Congratulations! You won.")
            else:
                print("Sorry, you didn't win this time.")
        except ValueError:
            print("Error: You must enter a number.")
        except InvalidDiceError as e:
            print(e)

    def greater_less_equal(self):
        """
        Allows the player to bet on whether the second roll will be 'greater', 'less' or 'equal' to the first roll.
        """
        try:
            die1 = self.roll_die()
            print(f"The first die is: {die1}")
            choice = input("Do you think the next roll will be 'greater', 'less', or 'equal'? ").strip().lower()
            if choice not in ['greater', 'less', 'equal']:
                raise InvalidDiceError("Invalid option. You must choose 'greater', 'less', or 'equal'.")
            die2 = self.roll_die()
            print(f"The second die is: {die2}")
            if (choice == 'greater' and die2 > die1) or (choice == 'less' and die2 < die1) or (choice == 'equal' and die2 == die1):
                print("Congratulations! You won.")
            else:
                print("Sorry, you didn't win this time.")
        except InvalidDiceError as e:
            print(e)
    
    def exact_or_approximate(self):
        """
        Allows the player to bet on an exact or close sum between two dice rolls.
        """
        try:
            target = int(input("Place your bet on a sum (2-12): "))
            if target < 2 or target > 12:
                raise InvalidDiceError("Invalid number. It must be between 2 and 12.")
            
            die1 = self.roll_die()
            die2 = self.roll_die()
            total = die1 + die2
            print(f"You rolled {die1} and {die2}. Total sum: {total}")
            
            if total == target or abs(total - target) == 1:
                print("Congratulations! You won.")
            else:
                print("Sorry, you didn't win this time.")
        except ValueError:
            print("Error: You must enter a number.")
        except InvalidDiceError as e:
            print(e)

    def ladder(self):
        """
        The player accumulates points by rolling numbers in ascending order.
        """
        try:
            points = 0
            previous = 0
            while True:
                die = self.roll_die()
                print(f"You rolled a {die}")
                
                if die > previous:
                    points += 1
                    previous = die
                    print(f"You've climbed the ladder! You have {points} points.")
                    continue_game = input("Do you want to continue? (y/n): ").strip().lower()
                    if continue_game != 'y':
                        break
                else:
                    print("You failed! The ladder is broken.")
                    points = 0
                    break
            
            print(f"Game over. You accumulated {points} points.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def three_dice_greater(self):
        """
        The player bets on whether the largest number rolled between three dice will be even or odd.
        """
        try:
            choice = input("Bet on the highest number: will it be 'even' or 'odd'? ").strip().lower()
            if choice not in ['even', 'odd']:
                raise InvalidDiceError("Invalid option. You must choose 'even' or 'odd'.")
            
            die1 = self.roll_die()
            die2 = self.roll_die()
            die3 = self.roll_die()
            print(f"You rolled {die1}, {die2}, and {die3}")
            
            highest = max(die1, die2, die3)
            print(f"The highest number is {highest}")
            
            if (choice == 'even' and highest % 2 == 0) or (choice == 'odd' and highest % 2 == 1):
                print("Congratulations! You won.")
            else:
                print("Sorry, you didn't win this time.")
        except InvalidDiceError as e:
            print(e)

    def play(self):
        """
        Main function to display the available betting options and allow the player to choose a bet.
        """
        options = {
            1: self.specific_number,
            2: self.high_or_low,
            3: self.even_or_odd,
            4: self.target_sum,
            5: self.greater_less_equal,
            6: self.exact_or_approximate,
            7: self.ladder,
            8: self.three_dice_greater
        }
        print("Welcome to the dice game. What would you like to bet on?")
        print("1. Specific Number (1-6)")
        print("2. High or Low (1-3 is low, 4-6 is high)")
        print("3. Even or Odd")
        print("4. Target Sum (bet on a specific sum between 2 and 12 from two dice rolls)")
        print("5. Greater, Less, or Equal on two rolls")
        print("6. Exact or Approximate (bet on a specific or close sum between two dice rolls)")
        print("7. Ladder (accumulate points by rolling numbers in ascending order)")
        print("8. Three Dice Greater (bet on whether the largest number rolled is even or odd)")

        try:
            option = int(input("Select an option (1-8): "))
            if option in options:
                options[option]()
            else:
                raise InvalidDiceError("Invalid option. You must select a number between 1 and 8.")
        except ValueError:
            print("Error: You must enter a number.")
        except InvalidDiceError as e:
            print(e)


   