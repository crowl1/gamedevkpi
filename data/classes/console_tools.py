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