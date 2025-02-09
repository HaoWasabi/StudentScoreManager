import os

class TerminalHandler:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')