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