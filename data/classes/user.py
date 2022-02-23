from data.classes.coordinate import Coordinate
from data.classes.game import AI
ai = AI(None, None)


class User:
    @staticmethod
    def enter(player, types, game_field=None, list_of_players=None) -> str:
        if types == "wall":
            if player.player_type:
                return player.action[1]
            elif not player.player_type:
                return ai.get_wall()
        elif types == "move":
            if player.player_type:
                return player.action[1]
            elif not player.player_type:
                return ai.move(player)
        elif types == "choose":
            if player.player_type:
                player.action = User.get_action_from_opponent()
                return player.action[0]
            elif not player.player_type:
                return ai.choose(player, game_field, list_of_players)
        elif types == "playAgain":
            if player.player_type:
                return "1"
                # return input() #1 - друга лаба, input() - перша лаба

    @staticmethod
    def to_our_coordinates(temp) -> str:
        if temp[0] == "move" or temp[0] == "jump":
            temp[0] = "1"
            temp[1] = Coordinate((int(temp[1][1])*2 - 2),
                                 (ord(temp[1][0].lower()) - 96)*2 - 2)
        elif temp[0] == "wall":
            temp[0] = '2'
            if temp[1][2] == 'h':
                x = ((ord(temp[1][0].lower()) - 96 - 18) * 2) - 1
                y = ((int(temp[1][1])) * 2) - 1
                temp[1] = f"{y} {x - 1} {y} {x + 1}"
            else:
                x = ((ord(temp[1][0].lower()) - 96 - 18) * 2) - 1
                y = ((int(temp[1][1])) * 2) - 1
                temp[1] = f"{y - 1} {x} {y + 1} {x}"
        return temp

    @staticmethod
    def ask_game_mode(text=None) -> str:
        state = input("Input your side: ")
        if text is None:
            if state.lower() == "black":
                return "2"
            else:
                return "3"
        else:
            return text

    @staticmethod
    def get_action_from_opponent():
        temp = input().split(" ")
        return User.to_our_coordinates(temp)

    @staticmethod
    def play() -> str:
        return "1"
        # return input() #1 - друга лаба, input() - перша лаба
