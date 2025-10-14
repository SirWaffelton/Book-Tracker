import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

BOOKS_FILE = "book_tracker.json"


want_to_read = []
have_read = []


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
            book = {
                "name": book_name,
                "author": book_author,
                "time": formatted,
                "id": id,
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
    print("4. Save to JSON")
    print("5. Load from JSON")
    print("6. Exit")

    choice = input("What would you like to do?\n>")

    if choice in ("1", "2", "3", "4", "5", "6"):
        if choice == "1":
            add_book()
        elif choice == "2":
            list_books()
        elif choice == "3":
            web_books()
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
