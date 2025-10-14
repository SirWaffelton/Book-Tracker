import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

BOOKS_FILE = "book_tracker.json"


want_to_read = []
have_read = []
goal_list = []

def add_goal():
    while True:
        goal_type = input("What's the goal type? (1. Read X books in Y time | 2. Try New Genre [X] amount]) ")
        try:
            goal_type_int = int(goal_type)
            if goal_type_int in (1, 2):
                break
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter a number, 1 or 2 (more goal types to be added maybe).")

    if goal_type_int == 1:
        book_amount = input("How many books would you like to read?\n>")
        timeframe = input("How long will this goal last (Eg: 1 Week, 2 Months): ")
        id = len(goal_list) + 1
        goal_1 = {"id": id, "amount": book_amount, "timeframe": timeframe}
        goal_list.append(goal_1)

    elif goal_type_int == 2:
        # Define genre options
        non_fiction_genres = [
            "Autobiography", "Self Help", "Biography", "History", "Science", "Philosophy"
        ]
        fiction_genres = [
            "Science Fiction", "Dystopia", "Fantasy", "Mystery", "Romance", "Thriller"
        ]
        
        print("Select a genre category:")
        print("1. Non-Fiction")
        print("2. Fiction")
        
        while True:
            category_choice = input("Enter 1 or 2 for the category: ")
            if category_choice == "1":
                genres_list = non_fiction_genres
                break
            elif category_choice == "2":
                genres_list = fiction_genres
                break
            else:
                print("Please enter a valid option: 1 or 2.")
        
        print("Available genres:")
        for idx, g in enumerate(genres_list, start=1):
            print(f"{idx}. {g}")
        
        while True:
            genre_choice = input("Select a genre by number: ")
            try:
                genre_idx = int(genre_choice)
                if 1 <= genre_idx <= len(genres_list):
                    selected_genre = genres_list[genre_idx - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(genres_list)}")
            except ValueError:
                print("Invalid input, please enter a number.")
        
        amount = input(f"How many {selected_genre} books would you like to read? ")
        
        id = len(goal_list) + 1
        goal_2 = {
            "id": id,
            "goal_type": "Try New Genre",
            "genre": selected_genre,
            "amount": amount
        }
        goal_list.append(goal_2)

def view_goals():
    if not goal_list:
        print("No goals to display. SET SOME!!!!")
        return

    print("--" * 20)
    for goal in goal_list:
        print(f"Goal ID: {goal["id"]}")
        
        if "goal_type" in goal and goal["goal_type"] == "Try New Genre":
            print(f"Type: {goal["goal_type"]}")
            print(f"Genre: {goal["genre"]}")
            print(f"Amount: {goal["amount"]}")
        
        else:
            print("Type: Read X books in Y Time")
            print(f"Amount(x): {goal["amount"]}")
            print(f"Timeframe: {goal["timeframe"]}")

        print('-' * 20)
        
        manage_choice = input("Would you like to delete/manage any of your goals? (y or n): ").lower()
        if manage_choice not in ("y", 'yes', "no", "n"):
            print("Please enter a valid ")
            return
            manage_goals()

def goal_choice():

    print("-" * 15 + "Goal Menu" + "-" * 15)

    while True:
        print("1. Create New Goal")
        print("2. View Goals")
        print(" -- Manage Goals")
        print(" -- Delete Goal[s]")
        print("3. Cancel")
        
        choice = input("What would you like to do?\n")
            
        if choice == "1":
            add_goal()
        elif choice == "2":
            view_goals()
            manage_goals()
        elif choice.lower() in ("3", "q", "quit"):
            print("Bye bye")
            break

def web_books():
    url = "http://books.toscrape.com/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
        print(title)
    else:
        print("Failed to retrieve the page")


def add_book():
    while True:
        book_name = input("Enter book name: ")
        book_author = input("Enter author name: ")
        genre = input("Whats the Genre of this book (seperate with commas): ")
        if "," in genre:
            genres = [item.strip() for item in genre.split(',')]
        else:
            genre = [genre.strip()]
        dt_created = datetime.now()
        formatted = dt_created.strftime("%d/%m/%Y, %H:%M:%S")

        list_option = (
            input(
                "Which list do you want to place this in:\n(Options: 1. Want To Read, 2. Have Read)\n>"
            )
            .strip()
            .lower()
        )

        if list_option in ("1", "want to read"):
            id = len(want_to_read) + 1
            if genres:
                book = {
                "name": book_name,
                "author": book_author,
                "time": formatted,
                "id": id,
                'genres':genres
            }
            elif genre:
                book = {
                "name": book_name,
                "author": book_author,
                "time": formatted,
                "id": id,
                'genre':genre
            }
                
            want_to_read.append(book)
            yes_or_no = input("Do you want to continue? ('y' or 'n')").lower()
            if yes_or_no in ("y", "yes"):
                continue
            elif yes_or_no in ("n", "no"):
                break
            else:
                print("Invalid selection")

        elif list_option in ("2", "have read"):
            id = len(have_read) + 1
            book = {
                "name": book_name,
                "author": book_author,
                "time": formatted,
                "id": id,
            }
            have_read.append(book)
            yes_or_no = input("Do you want to continue? ('y' or 'n')").lower()
            if yes_or_no in ("y", "yes"):
                continue
            elif yes_or_no in ("n", "no"):
                break
            else:
                print("Invalid selection")
        else:
            print("Invalid decision")


def list_books():
    print("1. Want to Read | 2. Have Read")
    list_option = input("What list would you like to view? ").strip().lower()

    global want_to_read
    global have_read

    if not want_to_read and not have_read:
        print("No books to list")
    else:
        if list_option in ("1", "want to read"):
            print("-" * 20)
            for i in want_to_read:
                print(f"{i['id']}. {i['name']} - {i['author']}")
                print("Description to be added")
                print(f"Date Added | {i['time']}")
                print("-" * 20)
        elif list_option in ("2", "have read"):
            print("-" * 20)
            for i in have_read:
                print(f"{i['id']}. {i['name']} - {i['author']}")
                print("Description to be added")
                print(f"Date Added | {i['time']}")
                print("-" * 20)
        else:
            print("Invalid list selection")


while True:
    print("Welcome to Book Tracker:")
    print("\n ---Menu---\n")
    print("1. Add book to list")
    print("2. Display List")
    print("3. Find Books and Prices")
    print("4. Goals")
    print("5. JSON CONTROLS")
    print("6. Exit")

    choice = input("What would you like to do?\n>")

    if choice in ("1", "2", "3", "4", "5", "6"):
        if choice == "1":
            add_book()
        elif choice == "2":
            list_books()
        elif choice == "3":
            web_books()
        elif choice == "4":
            goal_choice()
        elif choice == "5":
            print("Bye Bye")
            break
"""
make reading goals for amount of books to read including timeframe



web-scrape catalogs of book titles in certain genres to make a search system


want-to-read:
    select a genre (Non-Fiction---Autobiography, Self Help, etc | Fiction---Science Fiction, Dystopia, Fantasy, etc)
    Look up books from those genres
    search barnes and nobles for link to buy book
    
have read:
    ask for and create json file containing book name, author, date finished, rating out of 5
    
    allows to open subfolder "reviewed":
        add actual review of book within 1000 characters
        displays ratings and review with name of book and author and time of review made
    
"""
