from models import Game

if __name__ == "__main__":
    player_names = [name.strip() for name in input(
        "Enter player names separated by commas: ").strip().split(',')]
    game = Game(player_names)
    game.start()
