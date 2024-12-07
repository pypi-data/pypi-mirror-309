import random
from variables import valores_numericos, crear_mazo


class Blackjack:
    """
    A class to represent the Blackjack game.
    
    Attributes:
        banca (float): The total money available for betting.
    """

    def __init__(self, banca):
        """
        Initializes the game with a player's bank.

        Args:
            banca (float): Initial bank amount.
        """
        self.banca = banca

    def calcular_valor(self, mano):
        """
        Calculates the total value of a hand of cards.

        Args:
            mano (list): List of cards in hand.

        Returns:
            int: Total value of the hand.
        """
        total = 0
        ases = 0
        for carta in mano:
            numero = carta.split("\033")[0]
            valor = valores_numericos[numero]
            total += valor
            if numero == 'A':
                ases += 1
        while total > 21 and ases:
            total -= 10
            ases -= 1
        return total

    def mostrar_mano(self, mano_jugador, mano_dealer, revelar_dealer=False):
        """
        Displays the player's and dealer's cards on the screen.
        """
        print("\nDealer's Hand:")
        if revelar_dealer:
            print("  ".join(mano_dealer), "- Value:", self.calcular_valor(mano_dealer))
        else:
            print(mano_dealer[0], "X")  # Shows dealer's first card and hides the second

        print("\nYour Hand:")
        print("  ".join(mano_jugador), "- Value:", self.calcular_valor(mano_jugador))

    def turno_jugador(self, mazo, mano_jugador, mano_dealer, apuesta):
        """
        Manages the player's turn.
        """
        while True:
            self.mostrar_mano(mano_jugador, mano_dealer)
            if self.calcular_valor(mano_jugador) > 21:
                print("Bust! You lose the bet.")
                return -apuesta  # Player loses the bet

            accion = input("Do you want to [H]it, [D]ouble, or [S]tand?: ").strip().upper()
            
            if accion == 'H':  # Hit
                mano_jugador.append(mazo.pop())
            elif accion == 'D':  # Double
                if apuesta * 2 > self.banca:
                    print("You don't have enough funds to double the bet.")
                    continue
                apuesta *= 2
                self.n_cartas = len(mano_jugador)
                mano_jugador.append(mazo.pop())
                break
            elif accion == 'S':  # Stand
                self.n_cartas = len(mano_jugador)
                break
            else:
                print("Invalid option, try again.")

        return apuesta

    def turno_dealer(self, mazo, mano_dealer):
        """
        Manages the dealer's turn.
        """
        while self.calcular_valor(mano_dealer) < 17:
            mano_dealer.append(mazo.pop())
        return self.calcular_valor(mano_dealer)

    def evaluar_resultado(self, valor_jugador, valor_dealer, apuesta):
        """
        Evaluates the outcome of the game by comparing the hands of the player and the dealer.
        """
        if valor_jugador > 21:
            return -apuesta
        elif valor_dealer > 21  or valor_jugador > valor_dealer:
            return apuesta * 1.5 if (valor_jugador == 21 and self.n_cartas == 2) else apuesta
        elif valor_jugador == valor_dealer:
            return 0  # Tie
        else:
            return -apuesta

    def bienvenida(self):
        """
        Prints a decorative message explaining the rules of the game to the player.
        """
        print("\n✦✦✦✦ Welcome to Blackjack ✦✦✦✦✦\n")
        print("Objective: Get a card value as close to 21 as possible without going over.")
        print(" - Blackjack (A + 10) increases the reward by 50%.")
        print(" - Ace is worth 11 or 1 as appropriate.")
        print("Good luck and bet wisely!")

    def play_game(self):
        """
        Executes the main cycle of the blackjack game.
        """
        self.bienvenida()
        
        while self.banca > 0:
            try:
                print(f"Your current bank: {self.banca}€")
                apuesta = float(input("Enter your initial bet or type 0 to exit: "))
                if apuesta <= 0:
                    print("Thanks for playing! See you next time!")
                    return self.banca
                if apuesta > self.banca:
                    print("You cannot bet more than what you have in your bank.")
                    continue
            except ValueError:
                print("Please enter a valid number for the bet.")
                continue

            mazo = crear_mazo()
            random.shuffle(mazo)

            # Deal
            mano_jugador = [mazo.pop(), mazo.pop()]
            mano_dealer = [mazo.pop(), mazo.pop()]

            apuesta_final = self.turno_jugador(mazo, mano_jugador, mano_dealer, apuesta)
            if apuesta_final < 0:
                self.banca += apuesta_final
                continue

            print("\nThe dealer reveals their hand...")
            valor_dealer = self.turno_dealer(mazo, mano_dealer)

            self.mostrar_mano(mano_jugador, mano_dealer, revelar_dealer=True)
            
            valor_jugador = self.calcular_valor(mano_jugador)
            resultado = self.evaluar_resultado(valor_jugador, valor_dealer, apuesta_final)
            
            if resultado > 0:
                print(f"You win! Winnings: {resultado}€")
            elif resultado < 0:
                print(f"You lose. Loss: {abs(resultado)}€")
            else:
                print("It's a tie. Your bet is returned.")

            self.banca += resultado

        if self.banca <= 0:
            print("You're out of money. Game over!")
            return self.banca


if __name__ == '__main__':
    Blackjack = Blackjack(1000)
    banca = Blackjack.play_game()
    print(banca)