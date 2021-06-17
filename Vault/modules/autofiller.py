#!/usr/bin/python
import time
import pyautogui

# Autofills given credentials
def autofill_credentials(service_name, username, password):
    if service_name in ["facebook", "fb", "facebook.com", "face book"]:
        pyautogui.hotkey('alt', 'tab')
        pyautogui.write(username, interval = 0.05)
        pyautogui.hotkey('tab')
        pyautogui.write(password, interval = 0.05)
        pyautogui.hotkey('tab')
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
    elif service_name in ["gmail", "google", "gmail.com", "google mail"]:
        pyautogui.hotkey('alt', 'tab')
        pyautogui.write(username, interval = 0.05)
        pyautogui.hotkey('tab')        
        pyautogui.hotkey('tab')
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        time.sleep(2)
        pyautogui.write(password, interval = 0.05)
        pyautogui.hotkey('tab')
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
    elif service_name in ["yahoo", "ymail", "yahoo.com", "yahoo mail"]:
        pyautogui.hotkey('alt', 'tab')
        pyautogui.write(username, interval = 0.05)
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        time.sleep(2)
        pyautogui.write(password, interval = 0.05)
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
    else:
        pyautogui.hotkey('alt', 'tab')
        pyautogui.write(username, interval = 0.05)
        pyautogui.hotkey('tab')
        pyautogui.write(password, interval = 0.05)
        pyautogui.hotkey('tab')
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')