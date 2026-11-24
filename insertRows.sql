-- insertRows.sql
-- Sample data for "The Data Shelf": 4 categories, 16 books (4 per category).
-- Run after createTables.sql: sqlite3 bookstore.db < insertRows.sql

PRAGMA foreign_keys = ON;

INSERT INTO category (categoryId, categoryName, categoryImage) VALUES
(1, 'Programming',      'programming-category.jpg'),
(2, 'Databases',        'databases-category.jpg'),
(3, 'Statistics',       'statistics-category.jpg'),
(4, 'Machine Learning', 'machine-learning-category.jpg');

INSERT INTO book (bookId, categoryId, title, author, isbn, price, image, readNow) VALUES
-- Programming
(1,  1, 'Fluent Python', 'Luciano Ramalho', '9781492056355', 59.99, 'fluent-python.jpg', 1),
(2,  1, 'Automate the Boring Stuff with Python', 'Al Sweigart', '9781593279929', 39.95, 'automate-boring-stuff.jpg', 1),
(3,  1, 'Clean Code', 'Robert C. Martin', '9780132350884', 44.99, 'clean-code.jpg', 0),
(4,  1, 'The Pragmatic Programmer', 'David Thomas and Andrew Hunt', '9780135957059', 49.99, 'pragmatic-programmer.jpg', 0),

-- Databases
(5,  2, 'Designing Data-Intensive Applications', 'Martin Kleppmann', '9781449373320', 54.99, 'designing-data-intensive.jpg', 1),
(6,  2, 'Learning SQL', 'Alan Beaulieu', '9781492057611', 49.99, 'learning-sql.jpg', 1),
(7,  2, 'Database System Concepts', 'Abraham Silberschatz', '9780078022159', 189.99, 'database-system-concepts.jpg', 0),
(8,  2, 'Fundamentals of Database Systems', 'Ramez Elmasri and Shamkant B. Navathe', '9780133970777', 174.99, 'fundamentals-db-systems.jpg', 0),

-- Statistics
(9,  3, 'Naked Statistics', 'Charles Wheelan', '9780393347777', 17.95, 'naked-statistics.jpg', 1),
(10, 3, 'The Signal and the Noise', 'Nate Silver', '9780143125082', 20.00, 'signal-and-noise.jpg', 0),
(11, 3, 'How to Lie with Statistics', 'Darrell Huff', '9780393310726', 13.95, 'how-to-lie-with-statistics.jpg', 1),
(12, 3, 'Practical Statistics for Data Scientists', 'Peter Bruce, Andrew Bruce and Peter Gedeck', '9781492072942', 59.99, 'practical-statistics.jpg', 0),

-- Machine Learning
(13, 4, 'Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow', 'Aurelien Geron', '9781098125974', 79.99, 'hands-on-ml.jpg', 1),
(14, 4, 'Deep Learning', 'Ian Goodfellow, Yoshua Bengio and Aaron Courville', '9780262035613', 80.00, 'deep-learning.jpg', 0),
(15, 4, 'The Elements of Statistical Learning', 'Trevor Hastie, Robert Tibshirani and Jerome Friedman', '9780387848570', 89.99, 'elements-of-statistical-learning.jpg', 0),
(16, 4, 'Pattern Recognition and Machine Learning', 'Christopher M. Bishop', '9780387310732', 94.99, 'pattern-recognition-ml.jpg', 0);
