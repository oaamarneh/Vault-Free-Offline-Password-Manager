#!/usr/bin/python
from termcolor import colored

import string
import random


# Creates a password object
class Password:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password


# Generates a random password with given length
def generate_random_password():
	while True:
		try:
			length = int(input(colored("\nEnter the length of the password : ", "cyan")))
			if length < 8:
				print(colored("Password length can't be less than 8", "yellow"))
				continue
			else:
				password = ""
				uppercase_letters = string.ascii_uppercase
				lowercase_letters = string.ascii_lowercase
				digits = string.digits 
				special_characters = "!@#$%^&*()-_"
				for _ in range(length):
					password += random.choice(random.choice([uppercase_letters, lowercase_letters, digits, special_characters]))
				print(colored(password, "magenta"))
				while True:
					choice = input(colored("Are you happy with this password? (Y/N) > ", "blue"))
					if choice not in ["N", "n", "Y", "y"]:
						print(colored("Invalid choice, please try again.", "red"))
						continue
					elif choice in ["N", "n"]:
						break
					else:
						return password
		except ValueError:
			print(colored("Invalid choice, please try again.", "red"))
		except Exception:
			print(colored("Invalid choice, please try again.", "red"))


# Checks if password meets OWASP standards
def check_for_owasp_standards(password):
	uppercase_letters = string.ascii_uppercase
	lowercase_letters = string.ascii_lowercase
	digits = string.digits
	special_characters = "!@#$%^&*()-_"

	length_is_over_8 = False        	
	contains_uppercase_letter = False
	contains_lowercase_letter = False
	contains_digit = False
	contains_special_character = False
	Checklist = []

	if len(password) >= 8 :		
		length_is_over_8 = True
	Checklist.append(length_is_over_8)

	for character in password:
		if character in uppercase_letters:
			contains_uppercase_letter = True
			break
	Checklist.append(contains_uppercase_letter)

	for character in password:
		if character in lowercase_letters:
			contains_lowercase_letter = True
			break
	Checklist.append(contains_lowercase_letter)

	for character in password:
		if character in digits:
			contains_digit = True
			break
	Checklist.append(contains_digit)

	for character in password:
		if character in special_characters:
			contains_special_character = True
			break
	Checklist.append(contains_special_character)
	
	if False in Checklist:
		return False
	else:
		return True
