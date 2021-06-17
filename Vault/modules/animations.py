#!/usr/bin/python
from termcolor import colored

from .platform_checker import get_clear_screen_command

import os
import time


# An animation for passwords database creating
def db_not_found_animation():
    os.system(get_clear_screen_command())
    print(colored("Database not found, creating database...", "yellow"))
    time.sleep(0.3)
    os.system(get_clear_screen_command())


# An animation for connecting to the passwords database
def db_found_animation():
    os.system(get_clear_screen_command())
    print(colored("Database found, connecting...", "green"))
    time.sleep(0.3)
    os.system(get_clear_screen_command()) 