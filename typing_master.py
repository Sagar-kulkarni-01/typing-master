import json
import random
import time
import sys

WORD_FILE = "words.json"
LEADERBOARD_FILE = "leaderboard.json"
QUIT_KEY = "Ctrl + Q"

def update_leaderboard(username, wpm, category):
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            leaderboard_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard_data = {"leaderboard": []}

    leaderboard = leaderboard_data.get("leaderboard", [])

    leaderboard_entry = {
        "username": username,
        "wpm": wpm,
        "category": category
    }

    leaderboard.append(leaderboard_entry)
    leaderboard_data["leaderboard"] = leaderboard

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard_data, f, indent=4)

def show_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                leaderboard_data = json.load(f)
            except json.JSONDecodeError:
                print("Error decoding JSON. Leaderboard file may be empty.")
                return

        leaderboard = leaderboard_data.get("leaderboard", [])

        if not isinstance(leaderboard, list):
            print("Invalid leaderboard format.")
            return

        if not leaderboard:
            print("Leaderboard is empty.")
        else:
            print("Leaderboard")
            print("-" * 50)
            print("Username\tWPM\t\tCategory")
            print("-" * 50)
            for entry in leaderboard:
                print(f"{entry.get('username', 'Unknown')}\t\t{entry.get('wpm', 0):.2f}\t\t{entry.get('category', 'Unknown')}")
            print("-" * 50)
    except FileNotFoundError:
        print(f"Leaderboard file ({LEADERBOARD_FILE}) not found.")

def load_words_from_json(category):
    try:
        with open(WORD_FILE, "r") as f:
            words = json.load(f)
            return words.get(category, [])
    except FileNotFoundError:
        print(f"Error: {WORD_FILE} not found. Please provide a JSON file with words.")
        sys.exit(1)

def get_user_input(prompt):
    print(prompt)
    try:
        user_input = input()
    except KeyboardInterrupt:
        print(f"\nYou pressed {QUIT_KEY}. Quitting the game.")
        sys.exit(0)
    return user_input

def main():
    print("Welcome to Terminal Typing Master!")

    username = get_user_input("Enter your username: ")

    while True:
        print("\nMenu")
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")

        option = get_user_input("Choose an option: ")

        if option == "1":
            print("\nSelect a category:")
            print("1. Python")
            print("2. Java")
            print("3. C")
            print("4. C#")
            print("5. Rust")
            print("6. Ruby")
            print("7. JavaScript")
            print("8. Go")
            print("9. TypeScript")
            print("10. C++")

            category_number = get_user_input("Enter the number corresponding to your chosen category: ")

            categories = {
                "1": "Python",
                "2": "Java",
                "3": "C",
                "4": "C#",
                "5": "Rust",
                "6": "Ruby",
                "7":"JavaScript",
                "8":"Go",
                "9":"TypeScript",
                "10":"C++"
            }

            category = categories.get(category_number)
            if not category:
                print("Invalid category number. Please try again.")
                continue

            words = load_words_from_json(category)

            print(f"\nCategory: {category}")
            print(f"Words: {' '.join(words)}")

            input("Press Enter when you are ready to start typing...")
            start_time = time.time()

            typed_words = get_user_input("\nType the words exactly as shown. Press Enter when done. "
                                         f"Press {QUIT_KEY} to quit at any time: ").split()

            end_time = time.time()
            time_taken = end_time - start_time
            words_typed = len(typed_words)
            wpm = int(words_typed / (time_taken / 60)) if time_taken > 0 else 0

            print(f"\nWords Typed: {words_typed}")
            print(f"Time Taken: {int(time_taken)} seconds")
            print(f"Words Per Minute (WPM): {wpm}")

            update_leaderboard(username, wpm, category)

        elif option == "2":
            show_leaderboard()

        elif option == "3":
            print("Thank you for playing!")
            sys.exit(0)

if __name__ == "__main__":
    main()

