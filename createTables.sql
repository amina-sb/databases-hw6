-- createTables.sql
-- Schema for "The Data Shelf" bookstore.
-- Run with: sqlite3 bookstore.db < createTables.sql

PRAGMA foreign_keys = ON;

-- Drop child table first so the foreign key does not block the drop.
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS category;

CREATE TABLE category (
    categoryId    INTEGER PRIMARY KEY,
    categoryName  TEXT    NOT NULL UNIQUE,
    categoryImage TEXT    NOT NULL
);

CREATE TABLE book (
    bookId     INTEGER PRIMARY KEY,
    categoryId INTEGER NOT NULL,
    title      TEXT    NOT NULL,
    author     TEXT    NOT NULL,
    isbn       TEXT    NOT NULL UNIQUE CHECK (length(isbn) = 13),
    price      REAL    NOT NULL CHECK (price >= 0),
    image      TEXT    NOT NULL,
    readNow    INTEGER NOT NULL DEFAULT 0 CHECK (readNow IN (0, 1)),
    FOREIGN KEY (categoryId) REFERENCES category (categoryId)
);
