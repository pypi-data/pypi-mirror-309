#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import sys
from colorama import Fore, Style, init
import requests
import threading
import keyboard
import os
import argparse
import pyfiglet

# Initialize colorama for cross-platform color support
init()

# Define the current version of the package
CURRENT_VERSION = "1.7"

def check_for_updates():
    try:
        # Query PyPI for the latest version of the package
        response = requests.get(f"https://pypi.org/pypi/runtexts/json")
        response.raise_for_status()  # Raise an exception for a bad response
        data = response.json()

        latest_version = data["info"]["version"]

        if latest_version != CURRENT_VERSION:
            print(Fore.YELLOW + f"\nA new version ({latest_version}) of 'runtexts' is available! Please update using:" + Style.RESET_ALL)
            print(Fore.CYAN + "pip install --upgrade runtexts" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "\nYou are using the latest version of 'runtexts'." + Style.RESET_ALL)
            print(Fore.GREEN + "made by Maruf Ovi." + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"\nError checking for updates: {e}" + Style.RESET_ALL)

def get_user_inputs():
    print(Fore.CYAN + "\n--- Message Configuration ---" + Style.RESET_ALL)
    message = input(Fore.GREEN + "Enter the message to send: " + Style.RESET_ALL)
    
    while True:
        times_input = input(Fore.GREEN + "How many times to send the message (or type 'infinity' for endless): " + Style.RESET_ALL).strip()
        if times_input.lower() == "infinity":
            times = float("inf")  # Use infinity as the signal for an endless loop
            break
        else:
            try:
                times = int(times_input)
                break  # Exit loop if input is valid
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a number or type 'infinity'." + Style.RESET_ALL)
    
    while True:
        try:
            delay = float(input(Fore.GREEN + "Enter delay between each message (in seconds): " + Style.RESET_ALL))
            break  # Exit loop if input is valid
        except ValueError:
            print(Fore.RED + "Invalid input for 'delay'. Please enter a valid number." + Style.RESET_ALL)
    
    return message, times, delay

def send_texts(message, times, delay, mode):
    print(Fore.YELLOW + "\nStarting in 3 seconds. Switch to the target window..." + Style.RESET_ALL)
    time.sleep(3)  # Give user time to switch to the target application
    
    count = 0  # Keep track of the number of messages sent
    while count < times:
        if mode == "bot":
            pyautogui.typewrite(message)  # No delay (like a bot)
        elif mode == "human":
            pyautogui.typewrite(message, interval=0.1)  # Add delay for human-like typing
        pyautogui.press("enter")
        time.sleep(delay)
        count += 1
        # Stop if not in infinite mode
        if times == float("inf"):
            count = 0  # Reset count to loop infinitely

    print(Fore.YELLOW + "\nCompleted sending messages." + Style.RESET_ALL)

def create_gui():
    global window, message_entry, times_entry, delay_entry, typing_mode_var

    # Create the main window
    window = tk.Tk()
    window.title("RunTexts GUI")
    window.geometry("600x500")  # Larger window size for better layout
    window.configure(bg="#f0f0f0")  # Set background color

    # Header Label
    header_label = tk.Label(window, text="RunTexts Message Sender", font=("Arial", 18, "bold"), bg="#f0f0f0")
    header_label.pack(pady=20)

    # Message input
    message_label = tk.Label(window, text="Enter the message to send:", font=("Arial", 12), bg="#f0f0f0")
    message_label.pack(pady=5)
    message_entry = tk.Entry(window, width=50, font=("Arial", 14))
    message_entry.pack(pady=10)

    # Times input
    times_label = tk.Label(window, text="How many times to send the message (or 'infinity'):", font=("Arial", 12), bg="#f0f0f0")
    times_label.pack(pady=5)
    times_entry = tk.Entry(window, width=50, font=("Arial", 14))
    times_entry.pack(pady=10)

    # Delay input
    delay_label = tk.Label(window, text="Delay between each message (in seconds):", font=("Arial", 12), bg="#f0f0f0")
    delay_label.pack(pady=5)
    delay_entry = tk.Entry(window, width=50, font=("Arial", 14))
    delay_entry.pack(pady=10)

    # Typing mode selection
    typing_mode_label = tk.Label(window, text="Select Typing Mode:", font=("Arial", 12), bg="#f0f0f0")
    typing_mode_label.pack(pady=5)

    typing_mode_var = tk.StringVar(value="1")  # Default to "bot"

    bot_radio = tk.Radiobutton(window, text="Bot (Fast Typing)", variable=typing_mode_var, value="1", font=("Arial", 12), bg="#f0f0f0")
    bot_radio.pack(pady=5)

    human_radio = tk.Radiobutton(window, text="Human (Slow Typing)", variable=typing_mode_var, value="2", font=("Arial", 12), bg="#f0f0f0")
    human_radio.pack(pady=5)

    # Frame for buttons to manage layout better
    button_frame = tk.Frame(window, bg="#f0f0f0")
    button_frame.pack(pady=20)

    run_button = tk.Button(button_frame, text="Run", command=on_run_button_click, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", width=15)
    run_button.grid(row=0, column=0, padx=10)

    edit_button = tk.Button(button_frame, text="Edit Configuration", command=on_edit_button_click, font=("Arial", 12, "bold"), bg="#FF9800", fg="white", relief="raised", width=15)
    edit_button.grid(row=0, column=1, padx=10)

    # Start listening for the "Esc" key to exit the program
    window.after(100, listen_for_esc_key)

    # Run the GUI event loop
    window.mainloop()

def listen_for_esc_key():
    if keyboard.is_pressed('esc'):
        print("Exiting program...")
        window.quit()

    # Check again after 100ms
    window.after(100, listen_for_esc_key)

def on_run_button_click():
    message = message_entry.get()
    try:
        times_input = times_entry.get().strip()
        if times_input.lower() == "infinity":
            times = float("inf")  # Use infinity as the signal for an endless loop
        else:
            times = int(times_input)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for times.")
        return

    try:
        delay = float(delay_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for delay.")
        return

    mode = "bot" if typing_mode_var.get() == "1" else "human"

    # Start sending messages in a new thread
    threading.Thread(target=send_texts, args=(message, times, delay, mode), daemon=True).start()

def on_edit_button_click():
    message, times, delay = get_user_inputs()
    # Repeat the typing mode selection and update accordingly
    while True:
        print(Fore.CYAN + "\n--- Typing Mode Selection ---" + Style.RESET_ALL)
        print(Fore.BLUE + "Press '1' for bot (fast typing)")
        print("Press '2' for human (slow typing)" + Style.RESET_ALL)
        typing_choice = input(Fore.GREEN + "Choose typing mode: " + Style.RESET_ALL).strip()

        if typing_choice == "1":
            typing_mode = "bot"
            break
        elif typing_choice == "2":
            typing_mode = "human"
            break
        else:
            print(Fore.RED + "Invalid choice. Please select '1' or '2'." + Style.RESET_ALL)

    send_texts(message, times, delay, typing_mode)

def run_cli():
    # Get user inputs: message, times, and delay
    message, times, delay = get_user_inputs()

    while True:
        # Ask for typing mode selection after basic configurations
        print(Fore.CYAN + "\n--- Typing Mode Selection ---" + Style.RESET_ALL)
        print(Fore.BLUE + "Press '1' for bot (fast typing)")
        print("Press '2' for human (slow typing)" + Style.RESET_ALL)
        typing_choice = input(Fore.GREEN + "Choose typing mode: " + Style.RESET_ALL).strip()

        if typing_choice == "1":
            typing_mode = "bot"
            break
        elif typing_choice == "2":
            typing_mode = "human"
            break
        else:
            print(Fore.RED + "Invalid choice. Please select '1' or '2'." + Style.RESET_ALL)

    # Now provide the confirmation options before running
    while True:
        print(Fore.CYAN + "\n--- Confirmation ---" + Style.RESET_ALL)
        print(Fore.BLUE + "1 - Run the script with the selected configuration" + Style.RESET_ALL)
        print(Fore.YELLOW + "2 - Edit the configuration" + Style.RESET_ALL)
        print(Fore.RED + "3 - Exit" + Style.RESET_ALL)

        confirmation_choice = input(Fore.GREEN + "Choose an option: " + Style.RESET_ALL).strip()

        if confirmation_choice == "1":
            # Run the script with the selected settings
            send_texts(message, times, delay, typing_mode)
            break  # Exit the loop after running the script
        
        elif confirmation_choice == "2":
            # Allow the user to edit the configuration (input settings again)
            on_edit_button_click()
            break  # Exit the loop to return to the editing options

        elif confirmation_choice == "3":
            # Exit the program
            print(Fore.YELLOW + "\nExiting CLI mode..." + Style.RESET_ALL)
            break  # Exit the loop and end the program
        
        else:
            print(Fore.RED + "Invalid choice. Please choose 1, 2, or 3." + Style.RESET_ALL)



def main():
    try:
        # Create ASCII art for the welcome message
        ascii_art = pyfiglet.figlet_format("RunTexts!")
        print(Fore.CYAN + ascii_art + Style.RESET_ALL)

        # Ask the user to choose the mode
        print(Fore.CYAN + "1 - Use CLI")
        print("2 - Use GUI")
        print("3 - Check for updates")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            run_cli()
        elif choice == '2':
            create_gui()
        elif choice == '3':
            check_for_updates()
        else:
            print("Invalid option. Exiting...")

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print(Fore.YELLOW + "\nProgram terminated by user (Ctrl+C)." + Style.RESET_ALL)
        sys.exit(0)  # Exit the program gracefully

if __name__ == "__main__":
    main()
