#!/usr/bin/python
from Crypto.Cipher import AES
from getpass import getpass
from termcolor import colored

from modules.animations import db_found_animation, db_not_found_animation
from modules.autofiller import autofill_credentials
from modules.encryptions import sha256_hash_1000, sha256_hash_500, md5_hash_1000, aes_encrypt, aes_decrypt
from modules.menus import print_logo, print_menu, print_master_password_greeting_message, print_key_greeting_message, print_column_names, get_name_tab_count, get_username_tab_count, prove_you_are_not_a_robot
from modules.password import Password, generate_random_password, check_for_owasp_standards
from modules.platform_checker import check_platform, get_clear_screen_command

import os
import time
import string
import random
import hashlib
import sqlite3
import threading
import pyperclip
import pyautogui


# Clears console screen
def clear_screen():
    os.system(get_clear_screen_command())


# Starts inactivity timer
def start_timer():
    platform = check_platform()
    if platform == "Windows":
        def timer_start():
            while True:
                time.sleep(1)
                check_if_idle_windows()
        thread1 = threading.Thread(target=timer_start)
        thread1.start()

    elif platform == "Linux":
        def timer_start():
            while True:
                time.sleep(1)
                check_if_idle_linux()
        thread1 = threading.Thread(target=timer_start)
        thread1.start()


# Checks if the user is idle on Windows
def check_if_idle_windows():
    import win32api
    idle_time = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
    if idle_time > 50:
        os.system("cls")
        print(colored("You have been logged out due to inactivity.", "red"))
        time.sleep(0.2)
        os._exit(0)


# Checks if the user is idle on Linux
def check_if_idle_linux():
    import subprocess
    idle_time = int(subprocess.getoutput('xprintidle')) / 1000 # Requires xprintidle (sudo apt install xprintidle)
    if idle_time > 50:
        os.system("clear")
        print(colored("You have been logged out due to inactivity.", "red"))
        time.sleep(0.2)
        os._exit(0)


# Opens connection to DB
def open_connection():
    global conn, cursor
    conn = sqlite3.connect('Vault.db')
    cursor = conn.cursor()


# Clears clipboard after 10 seconds
def clear_clipboard():    
    def clear_clipboard():        
        time.sleep(10)
        pyperclip.copy("")
    thread2 = threading.Thread(target=clear_clipboard)
    thread2.start()


# Closes connection to DB
def close_connection():
    conn.close()


# Closes connection to the database and the application itself
def close_application():
    clear_screen()
    print(colored("Saving changes and exiting...", "green"))
    close_connection()
    time.sleep(0.2)
    os._exit(0)


# Fetches master password tuple
def get_stored_master_password_tuple():
    cursor.execute("SELECT * FROM masterpw")
    hashed_master_password_tuple = cursor.fetchone()
    return hashed_master_password_tuple


# Fetches master password hash
def get_stored_master_password():    
    hashed_master_password_tuple = get_stored_master_password_tuple()
    hashed_master_password = hashed_master_password_tuple[0]
    return hashed_master_password


# Creates master password
def create_master_password_and_backup_key():
    global master_password_md5_hash
    while True:
        print_master_password_greeting_message()
        master_password = getpass(colored("Enter your master password : ", "blue"))
        # If password is empty
        if master_password == "":
            clear_screen()
            print(colored("Password can't be empty, let's try again.\n", "yellow"))
            continue
        # If password does not meet the standards
        if check_for_owasp_standards(master_password) == False:
            clear_screen()
            print(colored("Password does not meet the standards, let's try again.\n", "yellow"))
            continue
        master_password_confirmation = getpass(colored("Confirm your master password : ", "blue"))
        # If passwords match and meet the standards
        if master_password == master_password_confirmation:
            master_password_sha256_hash_pre_salting = sha256_hash_1000(master_password)
            salt = "-" * len(master_password)
            salted_master_password = master_password + salt
            master_password_md5_hash = md5_hash_1000(sha256_hash_500(salted_master_password))
            master_password_sha256_hash = sha256_hash_1000(salted_master_password)

            backup_key = get_backup_key(master_password_sha256_hash_pre_salting)
            backup_key_md5_hash = md5_hash_1000(backup_key)
            aes_encrypted_master_password = aes_encrypt(master_password, backup_key_md5_hash)
            with conn:
                cursor.execute("INSERT INTO masterpw VALUES (:password)", {'password' : master_password_sha256_hash})

            with open("Key.txt", "wb") as key_file:
                key_file.write(aes_encrypted_master_password)

            print(colored("Master password and backup key saved successfully!", "green"))
            time.sleep(0.2)
            clear_screen()
            break
        # If passwords do not match
        else:
            clear_screen()
            print(colored("Passwords do not match, please try again.\n", "yellow"))
            continue


# Creates a backup key
def get_backup_key(master_password_sha256_hash_to_compare):
    while True:
        print_key_greeting_message()
        backup_key = input(colored("Enter your backup key : ", "blue"))
        backup_key_sha256_hash = sha256_hash_1000(backup_key)
        # If the backup key is the same as the master password
        if backup_key_sha256_hash == master_password_sha256_hash_to_compare:
            clear_screen()
            print(colored("Backup key can't be the same as the master password, let's try again.\n", "yellow"))
            continue
        # If the backup key is empty
        elif not backup_key:
            clear_screen()
            print(colored("Backup key can't be empty, let's try again.\n", "yellow"))
            continue
        # If the backup key is shorter than 6 characters
        elif len(backup_key) < 6:
            clear_screen()
            print(colored("Length has to be 6 or more, let's try again.\n", "yellow"))
            continue
        backup_key_confirmation = input(colored("Confirm your backup key : ", "blue"))
        # If keys match and meet the standards
        if backup_key == backup_key_confirmation:
            return backup_key
        # If keys do not match
        else:
            clear_screen()
            print(colored("Backup keys do not match, please try again.\n", "yellow"))
            continue


# Confirms master password for addition, extraction, and deletion of passwords
def confirm_master_password():
    failed_attempts = 0
    while failed_attempts < 10:
        print(colored("\n\t* Enter \"key\" if you have forgotten your master password. *\n", "magenta"))
        master_password = getpass(colored("Enter your master password to continue : ", "yellow"))
        salt = "-" * len(master_password)
        salted_master_password = master_password + salt
        master_password_md5_hash = md5_hash_1000(sha256_hash_500(salted_master_password))
        master_password_sha256_hash = sha256_hash_1000(salted_master_password)
        if master_password_sha256_hash == get_stored_master_password():
            print(colored("Success!", "green"))
            time.sleep(0.1)
            clear_screen()
            return master_password_md5_hash
        elif master_password.lower() == "key":
            master_password = confirm_backup_key()
            clear_screen()
            if not master_password:
                print(colored("The backup key file \"Key.txt\" does not exist, please make sure you move it to the current directory.", "yellow"))
            else:
                print(colored(f"Your master password is : {master_password}", "green"))
            continue   
        else:
            clear_screen()
            failed_attempts += 1
            print(colored(f"Failed attempts : {failed_attempts} \nMaster password is incorrect, please try again.", "red"))
    if failed_attempts == 10:
        close_application()


# Confirms backup key
def confirm_backup_key():
    failed_attempts = 0
    clear_screen()
    if not os.path.isfile("Key.txt"):
        return None
    else:
        while failed_attempts < 5:
            backup_key = getpass(colored("\nEnter your backup key to continue : ", "yellow"))
            try:
                with open("Key.txt", "rb") as key_file:
                    aes_encrypted_master_password = key_file.read()
                backup_key_md5_hash = md5_hash_1000(backup_key)
                unencrypted_master_password = aes_decrypt(aes_encrypted_master_password, backup_key_md5_hash)
                return unencrypted_master_password
            except Exception:
                clear_screen()                
                failed_attempts += 1
                print(colored(f"Failed attempts : {failed_attempts} \nBackup key is incorrect, please try again.", "red")) 
        if failed_attempts == 5:
            close_application()



# Checks for vault
def check_for_database():
    global master_password_md5_hash
    # If vault does not exist
    if not os.path.isfile("Vault.db"):
        open_connection()
        db_not_found_animation()
        with conn:
            cursor.execute("""CREATE TABLE masterpw(
                password text not null
                )""")
        with conn:
            cursor.execute("""CREATE TABLE passwords(
                name text not null unique,
                username text not null,
                password text not null
                )""")
        create_master_password_and_backup_key()        
    # If vault exists
    else:
        open_connection()
        db_found_animation()
        # If vault exists but there is no master password
        if get_stored_master_password_tuple() == None:
            create_master_password_and_backup_key()
        # If vault exists and contains a master password
        else:            
            master_password_md5_hash = confirm_master_password()


# Prints the menu and takes input from user
def get_choice():
    global master_password_md5_hash
    while True:
        print_logo()
        print_menu()
        try:
            choice = input(colored(" > ", "green"))
            if choice not in ["e","E","1","2","3","4","5","6","7"]:
                clear_screen()
                print(colored("Invalid choice, please try again.", "red"))
                continue
            elif choice == "1":
                view_all_passwords(master_password_md5_hash)
            elif choice == "2":
                fetch_password_by_name(master_password_md5_hash)
            elif choice == "3":
                create_and_add_password_to_db(master_password_md5_hash)
            elif choice == "4":
                update_password_by_name(master_password_md5_hash)
            elif choice == "5":
                master_password_md5_hash = confirm_master_password()
                delete_password_by_name(master_password_md5_hash)
            elif choice == "6":
                confirm_master_password()
                delete_all_passwords()
            elif choice == "7":
                confirm_master_password()
                delete_passwords_and_master_password()
            elif choice in ["e","E"]:
                close_application()
        except Exception:            
            print(colored("Invalid choice, please try again.", "red"))


# Views all stored passwords
def view_all_passwords(master_password_md5_hash):
    clear_screen()
    cursor.execute("SELECT rowid, * FROM passwords")
    password_list = cursor.fetchall()
    # If there are no passwords
    if not password_list:
        print(colored("There are no passwords in the database!", "red"))
    # If there are passwords
    else:
        print_column_names()
        for password_tuple in password_list:
            id_number = password_tuple[0]
            name = aes_decrypt(password_tuple[1], master_password_md5_hash)
            username = aes_decrypt(password_tuple[2], master_password_md5_hash)
            password = aes_decrypt(password_tuple[3], master_password_md5_hash)
            name_tab_count = get_name_tab_count(name)
            username_tab_count = get_username_tab_count(username)
            print(colored(f"{id_number}\t" 
            + f"{name}" + "\t" * name_tab_count 
            + f"{username}" + "\t" * username_tab_count 
            + f"\t{password}", "magenta"))
        print()


# Views a specific password
def fetch_password_by_name(master_password_md5_hash):
    clear_screen()
    cursor.execute("SELECT rowid, * FROM passwords")
    password_list = cursor.fetchall()
    # If there are no passwords
    if not password_list:
        print(colored("There are no passwords in the database!", "red"))
    # If there are passwords
    else:
        name = input(colored("\nWhat's the name of the service/website you want to fetch the password for?\n : ", "blue")).lower()
        print()
        name = aes_encrypt(name, master_password_md5_hash)
        cursor.execute("SELECT rowid, * FROM passwords WHERE name=:name", {'name': name})
        password_tuple = cursor.fetchone()
        # If the input password does not exist
        if not password_tuple:
            clear_screen()
            print(colored("Password is not in the database, please try again.", "red"))
        # If the input password exists
        else:
            clear_screen()
            print_column_names()
            id_number = password_tuple[0]
            name = aes_decrypt(password_tuple[1], master_password_md5_hash)
            username = aes_decrypt(password_tuple[2], master_password_md5_hash)
            password = aes_decrypt(password_tuple[3], master_password_md5_hash)
            name_tab_count = get_name_tab_count(name)
            username_tab_count = get_username_tab_count(username)                     
            print(colored(f"{id_number}\t" 
            + f"{name}" + "\t" * name_tab_count 
            + f"{username}" + "\t" * username_tab_count 
            + f"\t{password}", "magenta"))
            while True:
                try:
                    clipboard_choice = input(colored("\nDo you want to autofill your credentials? (Y/N) \n* Make sure your browser is open and the username field is selected \n* This may not work on all sites\n > ", "blue"))
                    if clipboard_choice not in ("n", "N", "y", "Y"):
                        print(colored("Invalid choice, please try again.", "red"))
                        continue
                    elif clipboard_choice in ("y", "Y"):
                        clear_screen()
                        thread2 = threading.Thread(target=autofill_credentials, args=(name, username, password))
                        thread2.start()
                        return
                    else:
                        break
                except Exception:
                    print(colored("Invalid choice, please try again.", "red"))
            while True:
                try:
                    clipboard_choice = input(colored("\nDo you want to copy this password to your clipboard? (Y/N) \n > ", "blue"))
                    if clipboard_choice not in ("n", "N", "y", "Y"):
                        print(colored("Invalid choice, please try again.", "red"))
                        continue
                    elif clipboard_choice in ("y", "Y"):
                        pyperclip.copy(password)
                        clear_screen()
                        print(colored("Password has been copied to the clipboard for 10 seconds.", "green"))
                        clear_clipboard()
                        return
                    else:
                        clear_screen()
                        break
                except Exception:                    
                    print(colored("Invalid choice, please try again.", "red"))


# Creates a password object
def create_and_add_password_to_db(master_password_md5_hash):
    while True:
        name = input(colored("\nName of the service/website : ", "cyan")).lower()
        name = aes_encrypt(name, master_password_md5_hash)
        cursor.execute("SELECT rowid, * FROM passwords WHERE name=:name", {'name': name})
        # If name is empty
        if not name:
            print(colored("\nPassword name can't be empty, please try again.", "red"))
            continue
        # If there isn't a duplicate password
        elif not cursor.fetchone():        	
        	break
        # If there is duplicate password
        else:
        	print(colored("\nPassword already exists, please try again.", "red"))
        	continue
    while True:
        username = input(colored("\nUsername/Email : ", "cyan")).lower()
        # If the username is empty
        if not username:
            print(colored("\nUsername can't be empty, please try again.", "red"))
            continue
        else:
            username = aes_encrypt(username, master_password_md5_hash)
            break
    while True:
        random_password_choice = input(colored("\nDo you want to generate a random password? (Y/N) > ", "yellow"))
        if random_password_choice not in ["N", "n", "Y", "y"]:
            print(colored("\nInvalid choice, please try again.", "red"))
            continue
        elif random_password_choice in ["N", "n"]:
            password = input(colored("Password : ", "cyan"))
            if password == "":
                print(colored("\nPassword can't be empty, please try again.", "red"))
                continue
            else:
                break
        else:
            password = generate_random_password()
            break
    password = aes_encrypt(password, master_password_md5_hash)          
    new_password = Password(name, username, password)
    add_password_to_db(new_password)
    


# Adds a password to the DB
def add_password_to_db(new_password):
    with conn:
        cursor.execute("INSERT INTO passwords VALUES (:name, :username, :password)",
            {'name': new_password.name,
            'username': new_password.username,
            'password': new_password.password})
    clear_screen()
    print(colored("Password successfully added to the database!\n", "green"))


# Updates a password in the DB
def update_password_by_name(master_password_md5_hash):
    clear_screen()
    cursor.execute("SELECT rowid, * FROM passwords")
    password_list = cursor.fetchall()
    # If there are no passwords
    if not password_list:
        print(colored("There are no passwords in the database!", "red"))
    # If there are passwords
    else:
        view_all_passwords(master_password_md5_hash)
        name = input(colored("\nWhat's the name of the service/website you want to change the password for?\n : ", "blue")).lower()
        encrypted_name = aes_encrypt(name, master_password_md5_hash)
        # Check if input password exists in the database
        cursor.execute("SELECT rowid, * FROM passwords WHERE name=:name", {'name': encrypted_name})
        password_tuple = cursor.fetchone()
        # If input password does not exist
        if not password_tuple:
            clear_screen()
            print(colored("Password does not exist in the database, please try again.", "red"))
        # If input password exists
        else:
            clear_screen()
            print_column_names()
            id_number = password_tuple[0]
            name = aes_decrypt(password_tuple[1], master_password_md5_hash)
            username = aes_decrypt(password_tuple[2], master_password_md5_hash)
            password = aes_decrypt(password_tuple[3], master_password_md5_hash)
            name_tab_count = get_name_tab_count(name)
            username_tab_count = get_username_tab_count(username)          
            print(colored(f"{id_number}\t" 
            + f"{name}" + "\t" * name_tab_count 
            + f"{username}" + "\t" * username_tab_count 
            + f"\t{password}", "magenta"))
            while True:
                try:
                    response = input(colored("\nAre you sure you want to modify this password? (Y/N) > ", "yellow"))
                    if response not in ["y", "Y", "n", "N"]:                    
                        print(colored("Invalid choice, please try again.", "red"))
                        continue
                    elif response in ["n", "N"]:
                        clear_screen()
                        return
                    else:
                        # Checking new password name
                        while True:
                            new_name = input(colored("\nNew name : ", "cyan")).lower()
                            encrypted_new_name = aes_encrypt(new_name, master_password_md5_hash)
                            cursor.execute("SELECT rowid, * FROM passwords WHERE name=:name", {'name': encrypted_new_name})
                            # If the new name is empty
                            if not new_name:
                                print(colored("\nPassword name can't be empty, please try again.", "red"))
                                continue
                            # If the new name is the same name of the password being changed
                            elif new_name == name:
                            	break
                            # If the new name is an existing password name
                            elif cursor.fetchone():
                                print(colored("\nPassword name already exists, please try again.", "red"))
                                continue
                            # If the new name is not empty and does not break uniqueness of the database
                            else:
                            	break
                        # Checking new username
                        while True:
                            new_username = input(colored("\nNew username/email : ", "cyan")).lower()
                            # If the new username is empty
                            if not new_username:
                                print(colored("\nUsername can't be empty, please try again.", "red"))
                            # If the new username is not empty
                            else:
                                new_username = aes_encrypt(new_username, master_password_md5_hash)
                                break            
                        while True:
                            random_password_choice = input(colored("Do you want to generate a random password? (Y/N) > ", "yellow"))
                            if random_password_choice not in ["N", "n", "Y", "y"]:
                                print(colored("\nInvalid choice, please try again.", "red"))
                                continue
                            elif random_password_choice in ["N", "n"]:
                                new_password = input(colored("New password : ", "cyan"))
                                break
                            else:
                                new_password = generate_random_password()
                                break
                        new_password = aes_encrypt(new_password, master_password_md5_hash)
                        with conn:
                            cursor.execute("""UPDATE passwords SET name=:name, username=:username, password=:password
                                WHERE rowid = :id""", 
                                {'name': encrypted_new_name,
                                'username': new_username,
                                'password': new_password,
                                'id': id_number})
                        clear_screen()
                        print(colored("Password updated successfully!", "green"))
                        break
                except Exception:                    
                    print(colored("Invalid choice, please try again.", "red"))


# Deletes a password from the database
def delete_password_by_name(master_password_md5_hash):
    clear_screen()
    cursor.execute("SELECT rowid, * FROM passwords")
    password_list = cursor.fetchall()
    # If there are no passwords
    if not password_list:
        print(colored("There are no passwords in the database!", "red"))
    # If there are passwords
    else:
        view_all_passwords(master_password_md5_hash)
        name = input(colored("\nWhat's the name of the service/website you want to delete the password for?\n : ", "blue")).lower()
        encrypted_name = aes_encrypt(name, master_password_md5_hash)
        cursor.execute("SELECT rowid, * FROM passwords WHERE name=:name", {'name': encrypted_name})
        password_tuple = cursor.fetchone()
        # If input password does not exist
        if not password_tuple:
            clear_screen()
            print(colored("Password does not exist in the database, please try again.", "red"))
        # If input password exists
        else:
            clear_screen()
            print_column_names()
            id_number = password_tuple[0]
            name = aes_decrypt(password_tuple[1], master_password_md5_hash)
            username = aes_decrypt(password_tuple[2], master_password_md5_hash)
            password = aes_decrypt(password_tuple[3], master_password_md5_hash)
            name_tab_count = get_name_tab_count(name)
            username_tab_count = get_username_tab_count(username)           
            print(colored(f"{id_number}\t" 
            + f"{name}" + "\t" * name_tab_count 
            + f"{username}" + "\t" * username_tab_count 
            + f"\t{password}", "magenta"))
            while True:
                try:
                    response = input(colored("\nAre you sure you want to delete this password? (Y/N) > ", "yellow"))
                    if response not in ["y", "Y", "n", "N"]:                    
                        print(colored("Invalid choice, please try again.", "red"))
                        continue
                    else:
                        if response in ["n", "N"]:
                            clear_screen()
                            return
                        else:
                            with conn:
                                cursor.execute("""DELETE FROM passwords WHERE name=:name""", {'name': encrypted_name})
                            clear_screen()
                            print(colored("Password deleted successfully!", "green"))
                            break
                except Exception:                    
                    print(colored("Invalid choice, please try again.", "red"))


# Deletes stored passwords
def delete_all_passwords():
    while True:
                try:
                    choice = input(colored("\nAre you sure you want to delete all passwords? (Y/N) > ", "red"))
                    if choice not in ("n", "N", "y", "Y"):
                        print(colored("Invalid choice, please try again.", "red"))
                        continue
                    elif choice in ("y", "Y"):
                        with conn:
                            cursor.execute("DELETE FROM passwords")
                        clear_screen()
                        print(colored("Your saved passwords have been deleted.", "green"))                        
                        break
                    else:
                        clear_screen()
                        break
                except Exception:                    
                    print(colored("Invalid choice, please try again.", "red"))


# Deletes passwords and master password databases
def delete_passwords_and_master_password():    
    while True:
                try:
                    choice = input(colored("\nAre you sure you want to delete all passwords, master password, and key file? (Y/N) > ", "red"))
                    if choice not in ("n", "N", "y", "Y"):
                        print(colored("Invalid choice, please try again.", "red"))
                        continue
                    elif choice in ("y", "Y"):
                        close_connection()
                        os.remove("Vault.db")
                        os.remove("Key.txt")
                        print(colored("Your saved passwords, master password, and key file have been deleted..", "green"))
                        time.sleep(0.2)
                        os._exit(0)
                        break
                    else:
                        clear_screen()
                        break
                except Exception:
                    clear_screen()                    
                    print(colored("Invalid choice, please try again.", "red"))


# Main function
def main():
    start_timer()
    prove_you_are_not_a_robot()
    check_for_database()
    get_choice()


if __name__ == "__main__":
    main()                                  