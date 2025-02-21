from ollama import chat
from ollama import ChatResponse
from models import Turn


def get_action_from_model(player, players=[], keep_alive="5s"):
    player_names = [p.name for p in players if p != player]
    messages = [
        {'role': 'user',
            'content': f"{player.name}, it's your turn. You have {player.coins} coins and {player.influence} influence with cards: {player.cards}. Choose one action from the following:\nincome (gain 2 coins)\ncoup (costs 7 coins, choose a target to lose influence)\ntax (requires Duke, gain 3 coins)\nassassinate (requires Assassin, requires and costs 3 coins, choose a target to lose influence)\nexchange (requires Ambassador, exchange cards with the deck)\nsteal (requires Captain, steal up to 2 coins from a target). You must also choose a target if applicable. The available targets are: {player_names}. Respond with a JSON object with the keys 'action' and 'target'."}
    ]
    response: ChatResponse = chat(
        model='deepseek-r1:1.5b', messages=messages, keep_alive=keep_alive, format=Turn.model_json_schema())
    action = Turn.model_validate_json(response.message.content).action
    target = Turn.model_validate_json(response.message.content).target
    # print raw response
    print(response.message.content)
    if target:
        target = next((p for p in players if p.name == target), None)
    else:
        target = None
    return action, target


def take_turn(game, player):
    while True:
        print(
            f"{player.name}'s turn. Coins: {player.coins}, Influence: {player.influence}, Cards: {player.cards}")
        action, target = get_action_from_model(player, game.players)
        print(f"Action chosen by {player.name}: {action}")
        print(
            f"Target chosen by {player.name}: {target.name if target else 'None'}")

        if action == 'income':
            player.gain_coins(2)
            break
        elif action == 'coup':
            if player.coins < 7:
                print("Not enough coins to perform a coup.")
                continue
            if not target:
                print("You must choose a target.")
                continue
            if target and target not in game.players:
                print("Invalid target. Please choose a valid target.")
                continue
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
                if not target:
                    print("You must choose a target.")
                    continue
                if target and target not in game.players:
                    print("Invalid target. Please choose a valid target.")
                    continue
                target.lose_influence()
                player.lose_coins(3)
                break
            else:
                print("You need an Assassin to perform this action.")
        elif action == 'exchange':
            if 'Ambassador' in player.cards:
                game.exchange_cards(player)
                break
            else:
                print("You need an Ambassador to perform this action.")
        elif action == 'steal':
            if 'Captain' in player.cards:
                if not target:
                    print("You must choose a target.")
                    continue
                if target and target not in game.players:
                    print("Invalid target. Please choose a valid target.")
                    continue
                if target.coins == 0:
                    print("Target has no coins to steal.")
                    continue
                stolen_coins = min(2, target.coins)
                target.lose_coins(stolen_coins)
                player.gain_coins(stolen_coins)
            else:
                print("You need a Captain to perform this action.")
        else:
            print("Invalid action. Please choose a valid action.")
