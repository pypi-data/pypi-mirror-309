import time
from Leones.variables import machine_configs, show_welcome_banner
from Leones.Ruleta import RouletteGame
from Leones.blackjack import Blackjack
from Leones.higher_lower import HigherOrLowerGame
from Leones.tragaperras import SlotMachine


class CasinoMontepinar:

    def __init__(self):
        self.__balance = 0  # Private account balance
        self.total_deposits = 0  # Total deposits accumulated

    def deposit(self, amount):
        """Allows the user to deposit money into their account."""
        if amount > 0:
            self.__balance += amount
            self.total_deposits += amount
            print(f"You have deposited {amount}€. Your current balance is {self.__balance}€.")
        else:
            print("The deposit amount must be greater than 0.")

    def withdraw(self, amount):
        """Allows the user to withdraw money if sufficient balance is available."""
        if amount > self.__balance:
            print("Error: You don't have enough balance to withdraw that amount.")
        elif amount <= 0:
            print("The withdrawal amount must be greater than 0.")
        else:
            self.__balance -= amount
            print(f"You have withdrawn {amount}€. Your current balance is {self.__balance}€.")

    def current_balance(self):
        """Returns the current account balance."""
        return self.__balance

    def display_game_menu(self):
        """Displays the available games in an engaging format."""
        time.sleep(0.5)
        print("\n🎮 Available Games 🎮")
        print("1️⃣ Blackjack")
        print("2️⃣ Roulette")
        print("3️⃣ Higher or Lower")
        print("4️⃣ Slot Machine")
        print("0️⃣ Exit the casino")
        time.sleep(0.5)

    def play_casino(self):
        """Main function to start the casino."""
        time.sleep(0.5)
        name = input("Please enter your name: ")
        time.sleep(0.5)
        try:
            age = int(input("Enter your age: "))
        except ValueError:
            print("Age must be an integer number.")
            return

        if age < 18:
            print("Sorry, you must be at least 18 years old to play. Come back when you're older!")
            return

        show_welcome_banner()
        print(f"Let's get started, {name}! You have a starting balance of {self.current_balance()}€.")
        time.sleep(0.5)

        # Main casino loop
        while True:
            if self.current_balance() <= 0:
                print("Welcome back to the main menu of Casino Montepinar.")
                print("💸 You have no available balance. Please make a deposit to continue playing.")
                try:
                    amount = float(input("Enter the amount you want to deposit: "))
                    self.deposit(amount)
                except ValueError:
                    print("Please enter a valid number.")
                    continue

            self.display_game_menu()
            choice = input("Select the number of the game you want to play: ").strip()

            if choice == "0":
                print("🎲 Thank you for visiting Casino Montepinar. See you next time! 🎲")
                break

            starting_balance = self.current_balance()
            ending_balance = starting_balance

            if choice == "1":
                game = Blackjack(starting_balance)
                ending_balance = game.play_game()

            elif choice == "2":
                game = RouletteGame(starting_balance)
                ending_balance = game.play_game()

            elif choice == "3":
                game = HigherOrLowerGame(starting_balance)
                ending_balance = game.play_game()

            elif choice == "4":
                try:
                    print("\n🔧 Slot Machine Configurations:")
                    print("1️⃣ No Jackpot")
                    print("2️⃣ Jackpot")
                    print("3️⃣ Super Jackpot")
                    machine = int(input("Select the machine (1, 2, 3): "))
                    selected_machine = machine_configs[machine - 1]

                    slot_machine = SlotMachine(**selected_machine)
                    ending_balance = slot_machine.play_game(starting_balance)
                except (ValueError, IndexError):
                    print("Invalid selection. Returning to the main menu.")
                    continue
            else:
                print("❌ Invalid option. Please select a game from the menu.")
                continue

            self.__balance = ending_balance
            # self.total_deposits += starting_balance - ending_balance

            # Ask if the player wants to continue playing
            print(f"\nYour current balance is {self.current_balance()}€.")
            continue_playing = input("Do you want to keep playing in the casino? (y/n): ").strip().lower()
            if continue_playing != "y":
                print("🎲 Thank you for visiting Casino Montepinar. See you next time! 🎲")
                break

    def calculate_balance(self):
        """Calculates the total winnings or losses."""
        net_balance = self.__balance - self.total_deposits
        if net_balance > 0:
            print(f"💰 Congratulations! You have won a total of {net_balance:.2f}€.")
        elif net_balance < 0:
            print(f"💸 Sorry, you have lost a total of {-net_balance:.2f}€.")
        else:
            print("⚖️ You have neither gains nor losses. You're even.")
        print(f"Your remaining balance is {self.__balance}€.")
        print("Thank you for playing at Casino Montepinar!")


if __name__ == "__main__":
    casino = CasinoMontepinar()
    casino.deposit(1000)  # Initial deposit
    casino.play_casino()
    casino.calculate_balance()
