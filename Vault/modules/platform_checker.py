#!/usr/bin/python
import os


# Checks what OS you're using
def check_platform():
    if os.name == "nt":
        platform = "Windows"
    else:
        platform = "Linux"
    return platform


# Chooses appropraite command to clear screen based on OS
def get_clear_screen_command():
    platform = check_platform()
    if platform == "Windows":
        command = "cls"
    else:
        command = "clear"
    return command