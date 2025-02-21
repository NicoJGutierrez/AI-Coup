import random
from pydantic import BaseModel


class Turn(BaseModel):
    action: str
    target: str = None


class Player:
    def __init__(self, name):
        self.name = name
        self.coins = 2
        self.cards = []

    @property
    def influence(self):
        return len(self.cards)

    def lose_influence(self):
        if self.cards:
            self.cards.pop()

    def gain_coins(self, amount):
        self.coins += amount

    def lose_coins(self, amount):
        self.coins -= amount

    def __str__(self):
        return f"{self.name}"


class Game:
    def __init__(self, players):
        self.players = [Player(name) for name in players]
        self.deck = ['Duke', 'Assassin', 'Captain', 'Ambassador'] * 3
        random.shuffle(self.deck)
        self.deal_cards()

    def deal_cards(self):
        for player in self.players:
            player.cards = [self.deck.pop(), self.deck.pop()]

    def start(self):
        while len([p for p in self.players if p.influence > 0]) > 1:
            for player in self.players:
                if player.influence > 0:
                    self.take_turn(player)
                    if len([p for p in self.players if p.influence > 0]) == 1:
                        break
        winner = [p for p in self.players if p.influence > 0][0]
        print(f"{winner.name} wins the game!")

    def take_turn(self, player):
        from actions import take_turn  # Importar la función desde actions.py
        take_turn(self, player)

    def choose_target(self, player, action="none"):
        from actions import choose_target  # Importar la función desde actions.py
        return choose_target(self, player, action)

    def exchange_cards(self, player):
        new_cards = [self.deck.pop(), self.deck.pop()]
        player.cards = new_cards
