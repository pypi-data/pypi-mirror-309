import random
import time
# import numpy as np
from src.Leones.variables import valores_numericos, crear_mazo


class HigherOrLowerGame:
    """
    A class to represent the Higher or Lower card game.

    Attributes:
        cartas_posibles (list): The full deck of cards.
        valores_numericos (dict): Numeric values corresponding to each card.
        cartas_juego_actual (list): The remaining cards in the current game.
        dinero_ganado (int): The total winnings accumulated by the player.
        cartas_elegidas (list): Cards already drawn during the game.
        banca (int): The total money the player has to bet.
    """
    
    def __init__(self, banca):
        """
        Initializes the game with a deck of cards and their values.

        Args:
            banca (int): Initial amount of money the player has to bet.
        """
        self.cartas_posibles = crear_mazo()
        self.cartas_posibles.append('Joker')
        self.valores_numericos = valores_numericos
        self.cartas_juego_actual = self.cartas_posibles[:]
        self.dinero_ganado = 0
        self.cartas_elegidas = []
        self.banca = banca
    
    def mostrar_cartas(self):
        """
        Displays the current deck of cards in rows for better visualization.
        """
        cartas_por_fila = 13
        print("Cards in the deck:")
        for i in range(0, len(self.cartas_posibles), cartas_por_fila):
            print("  ".join(self.cartas_posibles[i:i + cartas_por_fila]))
        print()

    def iniciar_apuesta(self):
        """
        Prompts the player to place their initial bet.
        """
        while True:
            try:
                apuesta = int(input(f'Enter your bet amount (minimum 1€, maximum {self.banca}€): '))
                if 1 <= apuesta <= self.banca:
                    self.apuesta = apuesta
                    print(f'Initial bet: {self.apuesta}€')
                    break
                else:
                    print(f"You must bet between 1€ and {self.banca}€. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def obtener_carta(self):
        """
        Draws a random card from the current deck and removes it from the game.

        Returns:
            str: The card that was drawn.
        """
        carta = random.choice(self.cartas_juego_actual)
        self.cartas_juego_actual.remove(carta)
        self.cartas_elegidas.append(carta)
        return carta
    
    def jugar_turno(self):
        """
        Executes a single turn of the game.

        Returns:
            bool: True if the player wins the turn, False otherwise.
        """
        if len(self.cartas_elegidas) == 0:
            carta = self.obtener_carta()
            print(f'The starting card is: {carta}')
            time.sleep(.2)
        else:
            carta = self.cartas_elegidas[-1]
        
        eleccion_usuario = input('Choose higher or lower (h/l): ')
        segunda_carta = self.obtener_carta()
        print(f'The next card is: {segunda_carta}')
        time.sleep(.2)
        
        if segunda_carta == 'Joker':
            self.banca -= self.apuesta
            print('The Joker has appeared! You lost.')
            print(f'Your current balance is: {self.banca}€')
            return False
        
        if self.verificar_resultado(eleccion_usuario, carta, segunda_carta):
            print('You won!')
            self.banca += self.apuesta
            print(f'Your current balance is: {self.banca}€')
            return True
        else:
            self.banca -= self.apuesta
            print('You lost.')
            print(f'Your current balance is: {self.banca}€')
            return False

    def verificar_resultado(self, eleccion, carta, segunda_carta):
        """
        Checks if the player's prediction is correct.

        Args:
            eleccion (str): The player's choice ('h' for higher, 'l' for lower).
            carta (str): The current card.
            segunda_carta (str): The next card drawn.

        Returns:
            bool: True if the prediction is correct, False otherwise.
        """
        valor_carta = self.valores_numericos[carta.split('\x1b')[0]]
        valor_segunda = self.valores_numericos[segunda_carta.split('\x1b')[0]]
        
        if eleccion == 'h':
            return valor_segunda > valor_carta
        elif eleccion == 'l':
            return valor_segunda < valor_carta
        else:
            print('Invalid choice.')
            return False
    
    def reiniciar_juego(self):
        """
        Prompts the player to restart the game with a new bet.

        Returns:
            bool: True if the player chooses to restart, False otherwise.
        """
        if self.banca <= 0:
            print("You have no money left. Game over!")
            return False
        
        respuesta = input('Do you want to bet again? (y/n): ')
        if respuesta.lower() == 'y':
            self.cartas_juego_actual = self.cartas_posibles[:]
            self.cartas_elegidas = []
            self.iniciar_apuesta()
            return True
        else:
            print('Game over. Thanks for playing!')
            return False
    
    def play_game(self):
        """
        Starts and manages the main game loop.
        """
        print('The Higher or Lower game begins!')
        print(f"Your starting balance is: {self.banca}€")
        self.mostrar_cartas()
        self.iniciar_apuesta()
        
        while True:
            if not self.jugar_turno():
                if not self.reiniciar_juego():
                    return self.banca
            else:
                if self.banca < 1:
                    print("You have no money left. Game over!")
                    return self.banca
                respuesta = input('If you want to keep playing, enter your new bet; otherwise, press any key to exit: ')
                try: 
                    self.apuesta = float(respuesta)
                    if self.apuesta > self.banca:
                        print(f"You cannot bet more than what you have ({self.banca}€).")
                        self.reiniciar_juego()
                except ValueError:
                    print(f'Your total winnings are: {self.banca}€')
                    print('Game over. Thanks for playing!')
                    return self.banca


if __name__ == "__main__":
    # Initial bank
    game = HigherOrLowerGame(1000)
    bank = game.play_game()
    print(bank)