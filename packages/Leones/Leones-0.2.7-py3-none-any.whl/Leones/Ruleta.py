import random

class RouletteGame():
    def __init__(self, banca):
        """
        Initializes the roulette game with an initial bank defined by the player.
        """
        self.roulette_numbers = list(range(1, 37)) + [0]
        self.colors = {
            0: "green",
            **{n: "red" if n % 2 != 0 else "black" for n in range(1, 37)}
        }
        self.call_bets = {
            "1": [1, 6, 9, 14, 17, 20, 31, 34],
            "2": [0, 2, 3, 4, 7, 12, 15, 18, 19, 22, 25, 26, 28, 29, 32, 35],
            "3": [5, 8, 10, 11, 13, 16, 23, 24, 27, 30, 33, 36]
        }
        self.banca = banca

    def spin_roulette(self):
        """
        Simulates spinning the roulette.
        """
        result_number = random.choice(self.roulette_numbers)
        result_color = self.colors[result_number]
        return result_number, result_color

    def place_bets(self, bets):
        """
        Processes the user's bets, calculates winnings or losses,
        and updates the bank.
        """
        result_number, result_color = self.spin_roulette()
        total_bet = 0
        total_payout = 0

        for bet in bets:
            bet_type = bet.get("type")
            bet_value = bet.get("value")
            bet_amount = bet.get("amount")
            split_amount = bet.get("split", False)

            if bet_type == "number":
                if split_amount:
                    total_bet += bet_amount
                else:
                    total_bet += bet_amount * len(bet_value)

                if result_number in bet_value:
                    if split_amount:
                        amount_per_number = bet_amount / len(bet_value)
                        total_payout += amount_per_number * 36
                    else:
                        total_payout += bet_amount * 36
            elif bet_type == "color":
                total_bet += bet_amount
                if result_color == bet_value:
                    total_payout += bet_amount * 2
            elif bet_type == "parity":
                total_bet += bet_amount
                if result_number != 0 and ((bet_value == "even" and result_number % 2 == 0) or
                                           (bet_value == "odd" and result_number % 2 != 0)):
                    total_payout += bet_amount * 2
            elif bet_type == "call_bets":
                total_bet += bet_amount
                if result_number in self.call_bets.get(bet_value, []):
                    amount_per_number = bet_amount / len(self.call_bets[bet_value])
                    total_payout += amount_per_number * 36

        net_gain = total_payout - total_bet
        self.banca += net_gain  
        result_summary = {
            "result_number": result_number,
            "result_color": result_color,
            "total_bet": total_bet,
            "total_payout": total_payout,
            "net_gain": net_gain
        }

        return result_summary

    def get_bets_from_user(self):
        """
        Asks the user for their bets and ensures they are valid
        based on the available bank amount.
        """
        while True:
            bets = []
            num_bets = input("How many bets would you like to place? (or type 'no bet' to exit): ").strip().lower()

            if num_bets == "no bet":
                print("Thanks for playing. See you next time!")
                return self.banca

            try:
                num_bets = int(num_bets)
            except ValueError:
                print("Invalid input. You must enter a number or 'no bet'. Please try again.")
                continue

            total_bet = 0
            for i in range(num_bets):
                bet_type = input("Type of bet (number, color, parity, call_bets): ").strip().lower()
                if bet_type not in ["number", "color", "parity", "call_bets"]:
                    print("Invalid bet type. Please try again.")
                    continue

                if bet_type == "number":
                    bet_value = input("Number(s) to bet on (0-36), separated by commas: ").strip().lower()
                    bet_value = [int(n.strip()) for n in bet_value.split(",") if n.strip().isdigit()]
                    if not bet_value or not all(0 <= n <= 36 for n in bet_value):
                        print("Invalid numbers. Please try again.")
                        continue

                    split_amount = input("Do you want to split the amount among the selected numbers? (yes/no): ").strip().lower()
                    if split_amount not in ["yes", "no"]:
                        print("Invalid response. Please try again.")
                        continue
                    split_amount = (split_amount == "yes")

                elif bet_type == "color":
                    bet_value = input("Color to bet on (red/black): ").strip().lower()
                    if bet_value not in ["red", "black"]:
                        print("Invalid color. Please try again.")
                        continue

                elif bet_type == "parity":
                    bet_value = input("Parity to bet on (even/odd): ").strip().lower()
                    if bet_value not in ["even", "odd"]:
                        print("Invalid parity. Please try again.")
                        continue

                elif bet_type == "call_bets":
                    bet_value = input("Special bet (orphelins(1), voisins_du_zero(2), tiers_du_cylindre(3)): ").strip().lower()
                    if bet_value not in self.call_bets:
                        print("Invalid special bet. Please try again.")
                        continue

                bet_amount = input("Amount to bet (in euros): ").strip()
                try:
                    bet_amount = float(bet_amount)
                except ValueError:
                    print("Invalid amount. Please try again.")
                    continue

                if total_bet + bet_amount > self.banca:
                    print("Your total bets exceed the available bank. Adjust your bets.")
                    break  

                total_bet += bet_amount
                bets.append({
                    "type": bet_type,
                    "value": bet_value,
                    "amount": bet_amount,
                    "split": split_amount if bet_type == "number" else False
                })

            if total_bet <= self.banca:
                return bets
            else:
                print("Your total bets exceed the available bank. Please try again.")

    def play_game(self):
        """
        Manages the main flow of the game. Verifies the bank and allows continued play.
        """
        while True:
            print(f"\nYour current bank is: {self.banca} euros")
            if self.banca <= 0:
                print("You have run out of money in the bank. Game over. Thanks for playing!")
                return self.banca

            bets = self.get_bets_from_user()
            if bets is None:
                break  

            result_summary = self.place_bets(bets)

            print(f"\nRoulette result: Number {result_summary['result_number']} ({result_summary['result_color']})")
            print(f"Total bet: {result_summary['total_bet']} euros")
            print(f"Total payout: {result_summary['total_payout']} euros")
            print(f"Net gain: {result_summary['net_gain']} euros\n")

            while True:
                play_again = input("Do you want to play again? (yes/no): ").strip().lower()
                if play_again == "yes":
                    break  
                elif play_again == "no":
                    print("Thanks for playing! See you next time!")
                    return self.banca
                else:
                    print("Invalid input. Please type 'yes' or 'no'.")


if __name__ == '__main__': 
    banca = 1000
    roulette_game = RouletteGame(banca)
    roulette_game.play_game()
