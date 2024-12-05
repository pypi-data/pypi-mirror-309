# font-colors/color.py
from colorama import Fore, just_fix_windows_console

# Fix console issues on Windows
just_fix_windows_console()

class Color:
    blue        =  Fore.LIGHTBLUE_EX
    yellow      =  Fore.LIGHTYELLOW_EX
    white       =  Fore.LIGHTWHITE_EX
    red         =  Fore.LIGHTRED_EX
    green       =  Fore.LIGHTGREEN_EX
    pink        =  Fore.LIGHTMAGENTA_EX
    purple      =  Fore.MAGENTA
    cyan        =  Fore.LIGHTCYAN_EX
    darkcyan    =  Fore.CYAN
    darkblue    =  Fore.BLUE
    darkyellow  =  Fore.YELLOW
    grey        =  Fore.WHITE
    darkred     =  Fore.RED
    darkgreen   =  Fore.GREEN