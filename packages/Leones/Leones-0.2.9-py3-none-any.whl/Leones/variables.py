valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
valores_numericos = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

machine_configs = [
                {"name": "No Jackpot", "symbols": ["🍒", "🔔", "🍋"], "rewards": {"🍒": 5, "🔔": 10, "🍋": 3}, "rtp": 0.99, "bet_cost": 0.20},
                {"name": "Jackpot", "symbols": ["🍒", "🔔", "🍋", "🍉", "⭐"], "rewards": {"🍒": 10, "🔔": 15, "🍋": 5, "🍉": 20, "⭐": 30}, "rtp": 0.97, "bet_cost": 0.25},
                {"name": "Super Jackpot", "symbols": ["🍒", "🔔", "🍋", "🍉", "⭐", "🍇", "💎", "🍊", "🍍", "🍈", "🔑"],
                "rewards": {"🍒": 20, "🔔": 25, "🍋": 10, "🍉": 30, "⭐": 40, "🍇": 50, "💎": 100, "🍊": 15, "🍍": 12, "🍈": 8, "🔑": 75},
                "rtp": 0.95, "bet_cost": 0.30}
        ]

def crear_mazo():
    """
    Create a deck of cards with 52 cards and with four different suits (♠, ♥, ♦, ♣) (no jokers).
    Return a list with the cards.
    """
    negro = "\033[90m"
    rojo = "\033[31m"
    reset = "\033[0m"
    return list(
        [f"{numero}{negro}\u2664{reset}" for numero in valores] +   # Spades ♤ in black
        [f"{numero}{rojo}\u2661{reset}" for numero in valores] +    # Hearts  ♡ in red
        [f"{numero}{rojo}\u2662{reset}" for numero in valores] +    # Diamonds ♢ in red
        [f"{numero}{negro}\u2667{reset}" for numero in valores]     # Clubs ♧ in black
    )

def show_welcome_banner():
    banner = r"""
    ┌───────────────────────────────────────────────────────────────────┐
    │                                                                   │
    │  █     █ █████ █      █████ █████ ██   ██ █████    █████ █████    │
    │  █     █ █     █      █     █   █ █ █ █ █ █          █   █   █    │
    │  █  █  █ ████  █      █     █   █ █  █  █ █████      █   █   █    │
    │  █ █ █ █ █     █      █     █   █ █     █ █          █   █   █    │
    │   █   █  █████ ██████ █████ █████ █     █ █████      █   █████    │
    │                                                                   │
    │                  █████ ████ ███  █ ██    █ ████                   │
    │                  █     █  █ █    █ █ █   █ █  █                   │
    │                  █     ████ ████ █ █  █  █ █  █                   │
    │                  █     █  █    █ █ █   █ █ █  █                   │
    │                  █████ █  █ ████ █ █    ██ ████                   │
    │                                                                   │
    │  ██   ██ █████ ██    █ █████ █████ ██████ █ ██    █ ████ █████    │
    │  █ █ █ █ █   █ █ █   █   █   █     █    █ █ █ █   █ █  █ █   █    │
    │  █  █  █ █   █ █  █  █   █   █████ ██████ █ █  █  █ ████ █████    │
    │  █     █ █   █ █   █ █   █   █     █      █ █   █ █ █  █ ███      │
    │  █     █ █████ █    ██   █   █████ █      █ █    ██ █  █ ██ ██    │
    │                                                                   │
    └───────────────────────────────────────────────────────────────────┘
    """
    print(banner)