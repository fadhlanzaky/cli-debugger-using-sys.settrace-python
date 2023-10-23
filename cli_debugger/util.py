import os

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

class FormatPrint(Bcolors):
    def __init__(self) -> None:
        super().__init__()
    
    def header(self, string):
        return self.HEADER + string + self.ENDC
    
    def line(self, string):
        return self.OKBLUE + string + self.ENDC
    
    def warning(self, string):
        return self.WARNING + string + self.ENDC
    
    def fail(self, string):
        return self.FAIL + string + self.ENDC
    
    def underline(self, string):
        return self.UNDERLINE + string + self.ENDC
    

def clear_cli():
    # clear all print/text on terminal
    os.system('cls' if os.name == 'nt' else 'clear')