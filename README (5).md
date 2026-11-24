# The Data Shelf - Bookstore Part I

**Name:** Amina Salamatolla (as20312)

## About the bookstore

The Data Shelf is a small bookstore for students learning to work with data. It sells real books in four categories: **Programming**, **Databases**, **Statistics** and **Machine Learning**. There are 16 books in total, 4 per category. Each book has a title, author, ISBN-13, price, image filename and a `readNow` flag (1 = recommended to read now).

## Files

| File | Purpose |
|---|---|
| `createTables.sql` | Creates the `category` and `book` tables (primary keys, foreign key, `NOT NULL`, `UNIQUE` and `CHECK` constraints) |
| `insertRows.sql` | Inserts 4 categories and 16 books |
| `bookstore.db` | The SQLite database built from the two SQL files |
| `bookstore_cli.py` | Python command-line program for browsing and managing books |

## Database design

- `category(categoryId PK, categoryName UNIQUE, categoryImage)`
- `book(bookId PK, categoryId FK -> category, title, author, isbn UNIQUE, price, image, readNow)`
- All columns are `NOT NULL`. `price` must be at least 0, `readNow` must be 0 or 1 and `isbn` must be 13 characters.
- Foreign keys are enabled with `PRAGMA foreign_keys = ON;` in the SQL files and on every Python connection, because SQLite turns them off by default.

## Create the database

From this folder, run:

```bash
sqlite3 bookstore.db < createTables.sql
sqlite3 bookstore.db < insertRows.sql
```

`createTables.sql` drops the tables first, so you can run both commands again to reset the data.

If the `sqlite3` shell is not installed, use Python instead:

```bash
python3 -c "import sqlite3; c = sqlite3.connect('bookstore.db'); [c.executescript(open(f).read()) for f in ('createTables.sql', 'insertRows.sql')]; c.close()"
```

## Run the program

```bash
python3 bookstore_cli.py
```

Menu options:

1. View all categories
2. View all books
3. View books in a category (uses a `JOIN`)
4. Search books by title keyword
5. Add a new book
6. Update a book's price
7. Delete a book (asks for confirmation)
8. **Count books per category** (extra feature, uses `LEFT JOIN` and `GROUP BY`)
9. Quit

## Notes

- Every query that uses input from the user is parameterized with `?`. No SQL is built with string concatenation or f-strings. For the title search, the `%` wildcards are added to the parameter value, not to the SQL.
- All SQL queries are defined as constants at the top of `bookstore_cli.py`.
- Invalid input is handled without crashing: non-numbers, negative prices, unknown ids, a category that doesn't exist, a duplicate ISBN and a bad `readNow` value.
