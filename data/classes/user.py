class User:
    @staticmethod
    def enter(player, types, game_field, list_of_players):
        if types == "wall":
            if player.player_type:
                return player.action[1]
        elif types == "move":
            if player.player_type:
                return player.action[1]
        elif types == "choose":
            if player.player_type:
                player.action = User.get_action_from_opponent()
                return player.action[0]
        elif types == "playAgain":
            if player.player_type:
                return input() # - перша лаба
    
    @staticmethod
    def ask_game_mode(text=None):
        state = input("Input your side: ")
        if text is None:
            return "2" if state.lower() == "black" else "3"
        else:
            return text