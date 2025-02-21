from ollama import chat
from ollama import ChatResponse
from models import Turn


def get_action_from_model(player, players=[], keep_alive="5s"):
    player_names = [p.name for p in players if p != player]
    messages = player.game_history + [
        {'role': 'user',
            'content': f"{player.name}, it's your turn. You have {player.coins} coins and {player.influence} influence with cards: {player.cards}. Choose one action from the following:\nassassinate (requires Assassin, requires and costs 3 coins, choose a target to lose influence)\nexchange (requires Ambassador, exchange cards with the deck)\nsteal (requires Captain, steal up to 2 coins from a target)\nincome (gain 2 coins)\ncoup (costs 7 coins, choose a target to lose influence, if you have more than 10 coins you must coup)\ntax (requires Duke, gain 3 coins).\n You must also choose a target. The available targets are: {player_names}.\nRespond with a JSON object with the keys 'action' and 'target'."}
    ]
    response: ChatResponse = chat(
        model='deepseek-r1:1.5b', messages=messages, keep_alive=keep_alive, format=Turn.model_json_schema())
    action = Turn.model_validate_json(response.message.content).action
    target = Turn.model_validate_json(response.message.content).target
    if target:
        target = next((p for p in players if p.name == target), None)
    else:
        target = None
    return action, target


def take_turn(game, player):
    player.clear_error_history()
    player.add_to_game_history(
        f"{player.name}'s turn. Coins: {player.coins}, Influence: {player.influence}, Cards: {player.cards}", role="user")
    while True:

        if player.error_history.__len__() > 8:
            player.clear_error_history()

        action, target = get_action_from_model(player, game.players)
        player.add_to_game_history(
            f"Action chosen: {action}, Target chosen: {target.name if target else 'None'}", role="assistant")

        if action == 'income':
            player.gain_coins(2)
            break
        elif action == 'coup':
            if player.coins < 7:
                player.add_to_error_history(
                    "Not enough coins to perform a coup.", role="user")
                continue
            if not target:
                player.add_to_error_history(
                    "You must choose a target.", role="user")
                continue
            if target and target not in game.players:
                player.add_to_error_history(
                    "Invalid target. Please choose a valid target.", role="user")
                continue
            target.lose_influence()
            player.lose_coins(7)
            break
        elif action == 'tax':
            if 'Duke' in player.cards:
                player.gain_coins(3)
                break
            else:
                player.add_to_error_history(
                    "You need a Duke to perform this action.", role="user")
        elif action == 'assassinate':
            if 'Assassin' in player.cards:
                if player.coins < 3:
                    player.add_to_error_history(
                        "Not enough coins to assassinate.", role="user")
                    continue
                if not target:
                    player.add_to_error_history(
                        "You must choose a target.", role="user")
                    continue
                if target and target not in game.players:
                    player.add_to_error_history(
                        "Invalid target. Please choose a valid target.", role="user")
                    continue
                target.lose_influence()
                player.lose_coins(3)
                break
            else:
                player.add_to_error_history(
                    "You need an Assassin to perform this action.", role="user")
        elif action == 'exchange':
            if 'Ambassador' in player.cards:
                game.exchange_cards(player)
                break
            else:
                player.add_to_error_history(
                    "You need an Ambassador to perform this action.", role="user")
        elif action == 'steal':
            if 'Captain' in player.cards:
                if not target:
                    player.add_to_error_history(
                        "You must choose a target.", role="user")
                    continue
                if target and target not in game.players:
                    player.add_to_error_history(
                        "Invalid target. Please choose a valid target.", role="user")
                    continue
                if target.coins == 0:
                    player.add_to_error_history(
                        "Target has no coins to steal.", role="user")
                    continue
                stolen_coins = min(2, target.coins)
                target.lose_coins(stolen_coins)
                player.gain_coins(stolen_coins)
                break
            else:
                player.add_to_error_history(
                    "You need a Captain to perform this action.", role="user")
        else:
            player.add_to_error_history(
                "Invalid action. Please choose a valid action.", role="user")
