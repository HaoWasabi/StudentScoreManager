import sys
import signal
from utils.terminal_handler import TerminalHandler

class BaseCLI:
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        TerminalHandler.clear()
        self.run()
        
    def signal_handler(self, signum, frame):
        print("Goodbye!")
        sys.exit(0)
        
    def run(self):
        pass