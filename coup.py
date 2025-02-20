import random


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


class Game:
    def __init__(self, players):
        self.players = [Player(name) for name in players]
        self.deck = ['Duke', 'Assassin', 'Captain',
                     'Ambassador', 'Contessa'] * 3
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
        while True:
            print(
                f"{player.name}'s turn. Coins: {player.coins}, Influence: {player.influence}, Cards: {player.cards}")
            action = input(
                "Choose an action (income, coup, tax, assassinate, exchange, steal): ").strip().lower()
            if action == 'income':
                player.gain_coins(2)
                break
            elif action == 'coup':
                if player.coins < 7:
                    print("Not enough coins to perform a coup.")
                    continue
                target = self.choose_target(player)
                target.lose_influence()
                player.lose_coins(7)
                break
            elif action == 'tax':
                if 'Duke' in player.cards:
                    player.gain_coins(3)
                    break
                else:
                    print("You need a Duke to perform this action.")
            elif action == 'assassinate':
                if 'Assassin' in player.cards:
                    if player.coins < 3:
                        print("Not enough coins to assassinate.")
                        continue
                    target = self.choose_target(player)
                    target.lose_influence()
                    player.lose_coins(3)
                    break
                else:
                    print("You need an Assassin to perform this action.")
            elif action == 'exchange':
                if 'Ambassador' in player.cards:
                    self.exchange_cards(player)
                    break
                else:
                    print("You need an Ambassador to perform this action.")
            elif action == 'steal':
                if 'Captain' in player.cards:
                    target = self.choose_target(player)
                    if target.coins == 0:
                        print("Target has no coins to steal.")
                        continue
                    stolen_coins = min(2, target.coins)
                    target.lose_coins(stolen_coins)
                    player.gain_coins(stolen_coins)
                    break
                else:
                    print("You need a Captain to perform this action.")
            else:
                print("Invalid action. Please choose a valid action.")

    def choose_target(self, player):
        while True:
            available_targets = [
                p.name for p in self.players if p != player and p.influence > 0]
            print(f"Available targets: {', '.join(available_targets)}")
            target_name = input("Choose a target: ").strip()
            target = next((p for p in self.players if p.name ==
                          target_name and p != player and p.influence > 0), None)
            if target:
                if target.influence > 0:
                    return target
                else:
                    print(f"{target.name} has no influence remaining.")
            else:
                print("Invalid target. Please choose a valid player.")

    def exchange_cards(self, player):
        new_cards = [self.deck.pop(), self.deck.pop()]
        player.cards = new_cards


if __name__ == "__main__":
    player_names = [name.strip() for name in input(
        "Enter player names separated by commas: ").strip().split(',')]
    game = Game(player_names)
    game.start()
