"""
bookstore_cli.py - command-line interface for "The Data Shelf" bookstore.

Connects to bookstore.db (SQLite) and lets the user browse and manage books.
Every query that uses a value typed by the user is parameterized with ?.

Run with: python3 bookstore_cli.py
"""

import os
import sqlite3

DB_NAME = "bookstore.db"

# ---------------------------------------------------------------------------
# SQL queries (Part 3). User-supplied values are always passed as ? params.
# ---------------------------------------------------------------------------

# READ
SQL_ALL_CATEGORIES = """
    SELECT categoryId, categoryName, categoryImage
    FROM category
    ORDER BY categoryId
"""

SQL_ALL_BOOKS = """
    SELECT b.bookId, b.title, b.author, c.categoryName, b.price, b.readNow
    FROM book AS b
    JOIN category AS c ON b.categoryId = c.categoryId
    ORDER BY b.bookId
"""

SQL_BOOKS_IN_CATEGORY = """
    SELECT b.bookId, b.title, b.author, c.categoryName, b.price, b.readNow
    FROM book AS b
    JOIN category AS c ON b.categoryId = c.categoryId
    WHERE c.categoryId = ?
    ORDER BY b.title
"""

SQL_SEARCH_BY_TITLE = """
    SELECT b.bookId, b.title, b.author, c.categoryName, b.price, b.readNow
    FROM book AS b
    JOIN category AS c ON b.categoryId = c.categoryId
    WHERE b.title LIKE ?
    ORDER BY b.title
"""

SQL_CATEGORY_NAME = "SELECT categoryName FROM category WHERE categoryId = ?"

SQL_BOOK_BY_ID = "SELECT bookId, title, price FROM book WHERE bookId = ?"

# CREATE
SQL_INSERT_BOOK = """
    INSERT INTO book (categoryId, title, author, isbn, price, image, readNow)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""

# UPDATE
SQL_UPDATE_PRICE = "UPDATE book SET price = ? WHERE bookId = ?"

# DELETE
SQL_DELETE_BOOK = "DELETE FROM book WHERE bookId = ?"

# EXTRA FEATURE: number of books in each category.
# LEFT JOIN keeps categories that currently have zero books.
SQL_COUNT_PER_CATEGORY = """
    SELECT c.categoryId, c.categoryName, COUNT(b.bookId) AS numBooks
    FROM category AS c
    LEFT JOIN book AS b ON b.categoryId = c.categoryId
    GROUP BY c.categoryId, c.categoryName
    ORDER BY c.categoryId
"""

BOOK_HEADERS = ["ID", "Title", "Author", "Category", "Price", "Read Now"]


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_divider() -> None:
    print("\n" + "-" * 60)


def pause() -> None:
    input("\nPress Enter to continue...")


def shorten(text: str, width: int) -> str:
    """Cut long text so table columns stay aligned."""
    return text if len(text) <= width else text[: width - 3] + "..."


def print_table(headers: list, rows: list, max_width: int = 40) -> None:
    """Print rows as a simple aligned text table."""
    if not rows:
        print("No results found.")
        return

    cells = [[shorten(str(value), max_width) for value in row] for row in rows]
    widths = [
        max(len(headers[i]), *(len(row[i]) for row in cells))
        for i in range(len(headers))
    ]

    print("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
    print("  ".join("-" * w for w in widths))
    for row in cells:
        print("  ".join(value.ljust(w) for value, w in zip(row, widths)))


def format_books(rows: list) -> list:
    """Turn raw book rows into display rows (price as $, readNow as Yes/No)."""
    return [
        (book_id, title, author, category, f"${price:.2f}", "Yes" if read_now else "No")
        for book_id, title, author, category, price, read_now in rows
    ]


# ---------------------------------------------------------------------------
# Input helpers (return None when the input is invalid)
# ---------------------------------------------------------------------------

def prompt_int(message: str):
    try:
        return int(input(message).strip())
    except ValueError:
        print("Please enter a whole number.")
        return None


def prompt_price(message: str):
    try:
        price = float(input(message).strip())
    except ValueError:
        print("Please enter a number, for example 24.99.")
        return None
    if price < 0:
        print("Price cannot be negative.")
        return None
    return round(price, 2)


def prompt_text(message: str):
    text = input(message).strip()
    if not text:
        print("This field cannot be empty.")
        return None
    return text


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------

def view_categories(cursor: sqlite3.Cursor) -> None:
    cursor.execute(SQL_ALL_CATEGORIES)
    print_divider()
    print("Categories\n")
    print_table(["ID", "Category", "Image"], cursor.fetchall())


def view_books(cursor: sqlite3.Cursor) -> None:
    cursor.execute(SQL_ALL_BOOKS)
    print_divider()
    print("All books\n")
    print_table(BOOK_HEADERS, format_books(cursor.fetchall()))


def view_books_in_category(cursor: sqlite3.Cursor) -> None:
    category_id = prompt_int("Enter a category id: ")
    if category_id is None:
        return

    cursor.execute(SQL_CATEGORY_NAME, (category_id,))
    category = cursor.fetchone()
    print_divider()
    if category is None:
        print(f"No category with id {category_id}.")
        return

    cursor.execute(SQL_BOOKS_IN_CATEGORY, (category_id,))
    print(f"Books in {category[0]}\n")
    print_table(BOOK_HEADERS, format_books(cursor.fetchall()))


def search_by_title(cursor: sqlite3.Cursor) -> None:
    keyword = prompt_text("Enter a title keyword: ")
    if keyword is None:
        return

    # The % wildcards go into the parameter value, not into the SQL string.
    cursor.execute(SQL_SEARCH_BY_TITLE, (f"%{keyword}%",))
    print_divider()
    print(f"Books with '{keyword}' in the title\n")
    print_table(BOOK_HEADERS, format_books(cursor.fetchall()))


def add_book(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    category_id = prompt_int("Enter category id: ")
    if category_id is None:
        return
    title = prompt_text("Enter title: ")
    if title is None:
        return
    author = prompt_text("Enter author: ")
    if author is None:
        return
    isbn = input("Enter 13-digit ISBN: ").strip().replace("-", "")
    if not (isbn.isdigit() and len(isbn) == 13):
        print("ISBN must be exactly 13 digits.")
        return
    price = prompt_price("Enter price: ")
    if price is None:
        return
    image = prompt_text("Enter image filename: ")
    if image is None:
        return
    read_now = prompt_int("Enter readNow (0 = no, 1 = yes): ")
    if read_now not in (0, 1):
        print("readNow must be 0 or 1.")
        return

    print_divider()
    try:
        cursor.execute(
            SQL_INSERT_BOOK,
            (category_id, title, author, isbn, price, image, read_now),
        )
        connection.commit()
        print(f"Book added with id {cursor.lastrowid}.")
    except sqlite3.IntegrityError as error:
        connection.rollback()
        message = str(error)
        if "FOREIGN KEY" in message:
            print(f"No category with id {category_id}. Book not added.")
        elif "isbn" in message:
            print(f"A book with ISBN {isbn} already exists. Book not added.")
        else:
            print("Database error:", message)


def update_price(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    book_id = prompt_int("Enter book id: ")
    if book_id is None:
        return

    cursor.execute(SQL_BOOK_BY_ID, (book_id,))
    book = cursor.fetchone()
    if book is None:
        print_divider()
        print(f"No book with id {book_id}.")
        return

    print(f"'{book[1]}' currently costs ${book[2]:.2f}.")
    new_price = prompt_price("Enter the new price: ")
    if new_price is None:
        return

    cursor.execute(SQL_UPDATE_PRICE, (new_price, book_id))
    connection.commit()
    print_divider()
    print(f"Price updated to ${new_price:.2f}.")


def delete_book(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    book_id = prompt_int("Enter book id to delete: ")
    if book_id is None:
        return

    cursor.execute(SQL_BOOK_BY_ID, (book_id,))
    book = cursor.fetchone()
    if book is None:
        print_divider()
        print(f"No book with id {book_id}.")
        return

    confirm = input(f"Delete '{book[1]}'? (y/n): ").strip().lower()
    print_divider()
    if confirm != "y":
        print("Delete cancelled.")
        return

    cursor.execute(SQL_DELETE_BOOK, (book_id,))
    connection.commit()
    print("Book deleted.")


def count_books_per_category(cursor: sqlite3.Cursor) -> None:
    """Extra feature: how many books are in each category."""
    cursor.execute(SQL_COUNT_PER_CATEGORY)
    print_divider()
    print("Books per category\n")
    print_table(["ID", "Category", "Books"], cursor.fetchall())


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def print_menu() -> None:
    print_divider()
    print("The Data Shelf - Main Menu")
    print("1. View all categories")
    print("2. View all books")
    print("3. View books in a category")
    print("4. Search books by title")
    print("5. Add a new book")
    print("6. Update a book price")
    print("7. Delete a book")
    print("8. Count books per category")
    print("9. Quit")


def main() -> None:
    if not os.path.exists(DB_NAME):
        print(f"Could not find {DB_NAME}. Create it first (see README.md).")
        return

    connection = sqlite3.connect(DB_NAME)
    # Foreign keys are off by default in SQLite and must be enabled per connection.
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    print_divider()
    print("Welcome to The Data Shelf!")
    print("Books on programming, databases, statistics and machine learning.")

    actions = {
        "1": lambda: view_categories(cursor),
        "2": lambda: view_books(cursor),
        "3": lambda: view_books_in_category(cursor),
        "4": lambda: search_by_title(cursor),
        "5": lambda: add_book(connection, cursor),
        "6": lambda: update_price(connection, cursor),
        "7": lambda: delete_book(connection, cursor),
        "8": lambda: count_books_per_category(cursor),
    }

    try:
        while True:
            print_menu()
            choice = input("\nChoose an option (1-9): ").strip()

            if choice == "9":
                print_divider()
                print("Goodbye!")
                break

            action = actions.get(choice)
            if action is None:
                print("Invalid option. Please enter a number from 1 to 9.")
            else:
                action()
            pause()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
