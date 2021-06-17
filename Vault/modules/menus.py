#!/usr/bin/python
from termcolor import colored

from .platform_checker import get_clear_screen_command

import random
import os


# Checks whether or not you're a robot
def prove_you_are_not_a_robot():
	os.system(get_clear_screen_command())
	failed_attempts = 0
	while failed_attempts < 3:		
		matrix = [" ", " ", " ",
				" ", " ", " ",
				" ", " ", " ",]
		randomized_place = random.randint(0,8)
		matrix.insert(randomized_place, "x")
		print(colored("Please prove that you're not a robot\n\n", "cyan"))
		print(colored(f" -----------------------------------", "cyan"))
		print(colored(f"|1          |2          |3          |", "cyan"))
		print(colored(f"|     {matrix[0]}     |     {matrix[1]}     |     {matrix[2]}     |", "cyan"))
		print(colored(f"|           |           |           |", "cyan"))
		print(colored(f" -----------------------------------", "cyan"))
		print(colored(f"|4          |5          |6          |", "cyan"))
		print(colored(f"|     {matrix[3]}     |     {matrix[4]}     |     {matrix[5]}     |", "cyan"))
		print(colored(f"|           |           |           |", "cyan"))
		print(colored(f" -----------------------------------", "cyan"))
		print(colored(f"|7          |8          |9          |", "cyan"))
		print(colored(f"|     {matrix[6]}     |     {matrix[7]}     |     {matrix[8]}     |", "cyan"))
		print(colored(f"|           |           |           |", "cyan"))
		print(colored(f" -----------------------------------", "cyan"))
		try:
			response = input(colored("\n\nIn what square is the (x) located?\n > ", "yellow"))
			response = int(response)
			if response not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
				os.system(get_clear_screen_command())
				failed_attempts += 1
				print(colored(f"Failed attempts : {failed_attempts}\nIncorrect, please try again.\n", "red"))
				continue
			elif matrix[response-1] != "x":				
				os.system(get_clear_screen_command())
				failed_attempts += 1
				print(colored(f"Failed attempts : {failed_attempts}\nIncorrect, please try again.\n", "red"))
				continue
			else:
				print(colored("Success!", "green"))
				return
		except Exception:
			os.system(get_clear_screen_command())
			failed_attempts += 1
			print(colored(f"Failed attempts : {failed_attempts}\nIncorrect, please try again.\n", "red"))
			continue
	os.system(get_clear_screen_command())
	print(colored("Too many failed attempts, exiting...", "green"))
	os._exit(0)


# Prints the logo
def print_logo():
    print(colored(r"    __      __         _ _           .----.     ", "green"))
    print(colored(r"    \ \    / /        | | |         / /  \ \    ", "green"))
    print(colored(r"     \ \  / /_ _ _   _| | |_       _| |__| |_   ", "green"))
    print(colored(r"      \ \/ / _` | | | | | __|    .' |_   |_| '. ", "green"))
    print(colored(r"       \  / (_| | |_| | | |_     '.__________.' ", "green"))
    print(colored(r"        \/ \__,_|\__,_|_|\__|    |            | ", "green"))
    print(colored(r"                                 '.__________.' ", "green"))
    print(colored(r"                                                  v 1.00", "magenta"))
    print(colored("\nVault - Free Offline Password Manager made by Osama A. Al-Amarneh\n\n", "cyan"))


# Prints main menu
def print_menu():
    print(colored("(1) View all passwords", "blue"))
    print(colored("(2) Fetch and copy a specific password", "blue"))
    print(colored("(3) Add a new password to the database", "blue"))
    print(colored("(4) Update an existing password", "blue"))
    print(colored("(5) Delete a password from the database", "red"))
    print(colored("(6) Delete all passwords from the database", "red"))
    print(colored("(7) Delete all passwords, master password, and key file", "red"))
    print(colored("(e) Exit", "yellow"))


# Prints greeting message for master password
def print_master_password_greeting_message():
    print(colored("To start, you'll have to create a master password... \nBe careful not to lose it as it cannot be changed, and is only recoverable with a backup key.\n", "cyan"))
    print(colored("According to OWASP password standards 2021 your master password must contain the following :", "magenta"))
    print(colored("* An uppercase character\n* A lowercase character\n* A digit\n* A special character\n* Length has to be 8 or more characters\n", "magenta"))


# Prints greeting message for backup key
def print_key_greeting_message():
	print(colored("\nLastly, you'll have to provide me with a backup key in case you forget your password.", "cyan"))
	print(colored("\nA \"Key.txt\" file will be created in your current directory, and you can only use the backup key when the key file exists.", "magenta"))
	print(colored("It's advised that you keep your backup key file on an external storage when you don't need it.\n", "magenta"))



# Prints table's column names
def print_column_names():
    print(colored("No.\tName\t\tUsername/Email\t\t\tPassword\n---\t----\t\t--------------\t\t\t--------", "yellow"))


# Returns appropriate tab count for name based on length
def get_name_tab_count(name):
    if len(name) < 8:
        name_tab_count = 2
    else:
        name_tab_count = 1
    return name_tab_count


# Returns appropriate tab count for username based on length
def get_username_tab_count(username):
    if len(username) >= 24:
        username_tab_count = 0
    elif len(username) >= 16:
        username_tab_count = 1
    elif len(username) >= 8:
        username_tab_count = 2
    else:
        username_tab_count = 3
    return username_tab_count

