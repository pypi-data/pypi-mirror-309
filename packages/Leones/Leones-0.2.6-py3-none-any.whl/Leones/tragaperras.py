import random
import time

class SlotMachine:
    """
    A class representing a slot machine game.

    Attributes:
        name (str): The name of the slot machine.
        symbols (list): A list of symbols that appear on the reels.
        rewards (dict): A dictionary mapping symbols to their respective rewards.
        rtp (float): Return to player percentage.
        bet_cost (float): Minimum bet cost to play.
        banca (float): The total amount of money available to the player.
    """

    def __init__(self, name, symbols, rewards, rtp, bet_cost):
        """
        Initializes a new SlotMachine instance.

        Args:
            name (str): The name of the slot machine.
            symbols (list): List of symbols on the reels.
            rewards (dict): Dictionary of rewards for each symbol.
            rtp (float): Return to Player percentage.
            bet_cost (float): The cost of one spin.
            banca (float): The total amount of money the player has available.
        """
        self.name = name
        self.symbols = symbols
        self.rewards = rewards
        self.rtp = rtp
        self.bet_cost = bet_cost

    def spin_reels(self):
        """
        Spins the reels and returns a random combination of three symbols.

        Returns:
            list: A list of three randomly selected symbols from the machine.
        """
        return [random.choice(self.symbols) for _ in range(3)]

    def calculate_reward(self, reels, bet):
        """
        Calculates the reward based on matching symbols and the bet amount.

        Args:
            reels (list): The list of symbols displayed on the reels.
            bet (float): The amount of money bet on the spin.

        Returns:
            float: The calculated reward based on the symbols.
        """
        if reels[0] == reels[1] == reels[2]:  # Check if all three symbols are the same
            symbol = reels[0]
            return self.rewards.get(symbol, 0) * bet
        return 0

    def play_game(self, banca):
        self.banca = banca
        """
        Starts a round of the slot machine game.

        Returns:
            float: The remaining money after the game.
        """
        print(f"\n🎰 Welcome to the '{self.name}' slot machine 🎰")
        print(f"Initial balance: {self.banca}€")

        last_bet = None  # No last bet for the first round

        while self.banca >= self.bet_cost:
            try:
                # Prompt user for their bet
                bet_input = input(f"How much do you want to bet? (0 to quit, minimum {self.bet_cost}): ")

                if bet_input == "":
                    if last_bet is None:
                        print(f"You must enter a minimum bet of {self.bet_cost}€. Please try again.")
                        continue
                    else:
                        bet = last_bet  # Use the last bet if no new value is entered
                else:
                    bet = float(bet_input)

                if bet == 0:
                    print("Thanks for playing. See you next time!")
                    break
                if bet < self.bet_cost:
                    print(f"The minimum bet is {self.bet_cost}€. Please try again.")
                    continue
                if bet > self.banca:
                    print("You don't have enough funds. Please try a lower amount.")
                    continue

                # Update the last bet placed
                last_bet = bet

            except ValueError:
                print("Please enter a valid number.")
                continue

            self.banca -= bet
            print("Spinning... ")
            time.sleep(1)

            # Spin the reels
            reels = self.spin_reels()
            print(" | ".join(reels))

            # Calculate the reward based on the symbols and bet
            reward = self.calculate_reward(reels, bet)
            if reward > 0:
                print(f"🎉 You won {reward:.2f}€! 🎉")
                self.banca += reward + bet
            else:
                print("You didn't win this time. Try again.")

            print(f"Current balance: {self.banca}€")

        if self.banca < self.bet_cost:
            print("You're out of funds or don't have enough for the minimum bet. Game over.")
        return self.banca
    

# Function to create and play the slot machine
def casino(money, machine_config):
    """
    Creates and plays a slot machine based on the given configuration.

    Args:
        money (float): The initial amount of money the player has.
        machine_config (dict): Configuration for the slot machine.

    Returns:
        float: The remaining money after playing.
    """
    slot_machine = SlotMachine(**machine_config)
    return slot_machine.play_game(money)