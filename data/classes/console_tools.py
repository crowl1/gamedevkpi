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