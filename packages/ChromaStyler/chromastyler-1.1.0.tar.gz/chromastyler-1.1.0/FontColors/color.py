# ChromaStyler/color.py
import os
import ctypes

def just_fix_windows_console():
    if os.name == 'nt':
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        
        # Retrieve the current console mode
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            # Enable virtual terminal processing (ANSI support)
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

class Color:
    black       =  "\x1b[30m"
    darkred     =  "\x1b[31m"
    darkgreen   =  "\x1b[32m"
    darkyellow  =  "\x1b[33m"
    darkblue    =  "\x1b[34m"
    purple      =  "\x1b[35m"
    darkcyan    =  "\x1b[36m"
    reset       =  "\x1b[37m"
    grey        =  "\x1b[90m"
    red         =  "\x1b[91m"
    green       =  "\x1b[92m"
    yellow      =  "\x1b[93m"
    blue        =  "\x1b[94m"
    pink        =  "\x1b[95m"
    cyan        =  "\x1b[96m"
    white       =  "\x1b[97m"