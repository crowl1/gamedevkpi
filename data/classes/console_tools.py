import os


class Tools:
    @staticmethod
    def clear_console():
        '''
        очищення консолі
        '''
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
        pass


def game_mode_selection():
    '''
    перша лаба, вибір для гравця
    '''
    print("1)PvP\n2)PvB\n3)BvB")
    pass


def send_wall(wall):
    if wall.coordinates_start.x == wall.coordinates_end.x:
        print(
            f"wall {chr(int(wall.coordinates_middle.y / 2 + 96 + 19)).capitalize()}{int((wall.coordinates_middle.x + 1) / 2)}h")
    else:
        print(
            f"wall {chr(int(wall.coordinates_middle.y / 2 + 96 + 19)).capitalize()}{int((wall.coordinates_middle.x + 1) / 2)}v")


def print_field(field):
    '''
    перша лаба, принт в консоль карти
    '''
    a = 1
    if a == 0:
        num_horizontal = "    "
        count = 0
        for item in field[0]:
            if count < 10:
                num_horizontal += f"{count}  "
                count += 1
            else:
                num_horizontal += f"{count} "
                count += 1
        print(num_horizontal)

        num_horizontal = "     "
        count = 0
        for item in field[0]:
            if item == 0 or item == 1 or item == 2:
                num_horizontal += f"{count}"
                count += 1
            else:
                num_horizontal += "     "
        print(num_horizontal)

        count_1 = 0
        count_2 = 0
        for row in field:
            if row[0] == 0 or row[0] == 1 or row[0] == 2:
                if count_2 < 10:
                    print(f"{count_2}  {count_1}{row}")
                    count_1 += 1
                    count_2 += 1
                else:
                    print(f"{count_2} {count_1}{row}")
                    count_1 += 1
                    count_2 += 1

            else:
                if count_2 < 10:
                    print(f"{count_2}   {row}")
                    count_2 += 1
                else:
                    print(f"{count_2}  {row}")
                    count_2 += 1
    else:
        for index, i in enumerate(field):
            for index2, j in enumerate(i):
                symbols = ['0', 'X', 'M', ' ', '#', '+']
                if j == 5:
                    print("\033[33m {}".format(symbols[j]), end="")
                elif j == 3:
                    print("\033[37m {}".format(symbols[j]), end="")
                elif j == 0:
                    print("\033[32m {}".format(symbols[j]), end="")
                elif j == 1:
                    print("\033[31m {}".format(symbols[j]), end="")
                elif j == 2:
                    print("\033[31m {}".format(symbols[j]), end="")
                elif j == 4:
                    print("\033[33m {}".format(symbols[j]), end="")
            print()


def send_move(player):
    print(
        f"move {chr(int(player.current_position.y / 2 + 96) + 1).capitalize()}{int(player.current_position.x / 2) + 1}")


def send_jump(player):
    print(
        f"jump {chr(int(player.current_position.y / 2 + 96) + 1).capitalize()}{int(player.current_position.x / 2) + 1}")


def print_places_to_move(places):
    '''
    перша лаба
    '''
    count = 1
    for place in places:
        print(f"{count} - {place.x} {place.y}")
        count += 1
    print("Введіть 'back' щоб повернутися назад")


def choose_action_message(player):
    '''
    перша лаба
    '''
    print(f"{player.player_number} виберідь, будь ласка, дію.\n1 - Походити героєм.\n2 - Поставити стіну.")


def place_the_wall_message():
    '''
    перша лаба
    '''
    print("Введіть початкові та кінцеві координати стіни (наприклад, '0 1 2 1') або введіть 'back', щоб повернутися до вибору ")
