import csv
from models.users import User
from models.book import Book
from models.transaction import Transaction
import os
from datetime import datetime

# Define the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE DIR: {BASE_DIR}")

# Dfine paths to CSV files in the "data" folder
BOOKS_FILE = os.path.join(BASE_DIR, "data", "books.csv")
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "data", "transactions.csv")
USERS_FILE = os.path.join(BASE_DIR, "data", "users.csv")

class LibrarySystem:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.transactions = []
        self.load_users()
        self.load_books()
        self.load_transactions()
        self.transaction_counter = 1000
        if self.transactions:
            self.transaction_counter = max(t.transaction_id for t in self.transactions) + 1

    # USER LEVEL OPERATIONS
    def load_users(self):
        try:
            with open(USERS_FILE, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    user_id, name, borrowed_books = row
                    borrowed_books = [int(b) for b in borrowed_books.split("|") if b]  # Convert to list
                    self.users[int(user_id)] = User(int(user_id), name, borrowed_books, self)
        except FileNotFoundError:
            with open(USERS_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["UserID", "Name", "BorrowedBooks"])  # Create header

    def add_user(self, user_id, name):
        if user_id in self.users:
            return f"User with ID {user_id} already exists."
        
        self.users[user_id] = User(user_id, name, [], self)
        self.save_users()  # Rewrite entire file instead of appending
        return f"User {name} added successfully."

    def delete_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]  # Remove from dictionary
            self.save_users()  # Rewrite entire file after deletion
            return f"User {user_id} deleted successfully."
        else:
            return "User not found."

    def save_users(self):
        """ Rewrite the entire users.csv file with updated user list. """
        with open(USERS_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["UserID", "Name", "BorrowedBooks"])  # Header
            for user in self.users.values():
                borrowed_books_str = "|".join(map(str, user.borrowed_books))  # Convert list to string
                writer.writerow([user.user_id, user.name, borrowed_books_str])

    # BOOK LEVEL OPERATIONS
    def load_books(self):
        """ Load books from books.csv, skipping empty lines """
        try:
            with open(BOOKS_FILE, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) == 4:  # Ensure row has all required values
                        book_id, title, author, available = row
                        self.books[int(book_id)] = Book(int(book_id), title, author, available == "Yes")
        except FileNotFoundError:
            with open(BOOKS_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["BookID", "Title", "Author", "Available"])  # Create header


    def add_book(self, book_id, title, author):
        """ Add a new book to the system """
        if book_id in self.books:
            return f"Book with ID {book_id} already exists."

        self.books[book_id] = Book(book_id, title, author)
        self.save_books()
        return f"Book '{title}' added successfully."

    def delete_book(self, book_id):
        """ Remove a book from the system only if it's not borrowed """
        
        # Check if the book exists
        if book_id not in self.books:
            return "Book not found."

        # Check if the book is borrowed by any user
        for user in self.users.values():
            if book_id in user.borrowed_books:
                return f"Cannot delete book {book_id} as it is currently borrowed by {user.name}."

        # If not borrowed, delete it
        del self.books[book_id]
        self.save_books()
        return f"Book {book_id} deleted successfully."


    def save_books(self):
        """ Save updated book data to books.csv """
        with open(BOOKS_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["BookID", "Title", "Author", "Available"])
            for book in self.books.values():
                writer.writerow([book.book_id, book.title, book.author, "Yes" if book.is_available else "No"])

    def borrow_book(self, user_id, book_id):
        """ Allow a user to borrow a book if available """
        if user_id not in self.users:
            return "User not found."
        if book_id not in self.books:
            return "Book not found."

        user = self.users[user_id]
        book = self.books[book_id]

        if book_id in user.borrowed_books:
            return f"{user.name} has already borrowed '{book.title}'."
        
        if not book.is_available:
            return f"Book '{book.title}' is currently unavailable."

        # Generate new transaction ID
        transaction_id = self.transaction_counter
        self.transaction_counter += 1

        # Get the current timestamp
        date = datetime.now().strftime("%I:%M %p")

        # Update book status and user's borrowed books
        book.is_available = False
        user.borrowed_books.append(book_id)

        # Save updated book and user data
        self.save_books()
        self.save_users()

        # Log the transaction
        transaction = Transaction(transaction_id, user_id, book_id, "borrowed", date)
        self.transactions.append(transaction)
        self.save_transaction()

        return f"Transaction {transaction_id}: {user.name} borrowed '{book.title}' successfully."
    
    def return_book(self, user_id, book_id):
        """ Allow a user to return a borrowed book """
        if user_id not in self.users:
            return "User not found."
        
        if book_id not in self.books:
            return "Book not found."

        book = self.books[book_id]
        user = self.users[user_id]

        if book_id not in user.borrowed_books:
            return f"{user.name} has not borrowed '{book.title}'."

        # Generate new transaction ID
        transaction_id = self.transaction_counter
        self.transaction_counter += 1

         # Get the current timestamp
        date = datetime.now().strftime("%I:%M %p")

        # Update book status and remove from user's borrowed books list
        book.is_available = True
        user.borrowed_books.remove(book_id)

        # Save updated book and user data
        self.save_books()
        self.save_users()

        # Log the transaction
        transaction = Transaction(transaction_id, user_id, book_id, "Returned", date)
        self.transactions.append(transaction)
        self.save_transaction()

        return f"Transaction {transaction_id}: {user.name} returned '{book.title}' successfully."

    # TRANSACTION LEVEL OPERATIONS
    def load_transactions(self):
        """ Load transaction history from transactions.csv """
        self.transactions = []  # Reset transactions list
        try:
            with open(TRANSACTIONS_FILE, mode="r") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                for row in reader:
                    if row:  # Ensure row is not empty
                        transaction = Transaction(
                            transaction_id=int(row[0]),
                            user_id=int(row[1]),
                            book_id=int(row[2]),
                            transaction_type=row[3],
                            date=row[4]
                        )
                        self.transactions.append(transaction)  # Store as a Transaction object
        except FileNotFoundError:
            with open(TRANSACTIONS_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["TransactionID", "UserID", "BookID", "TransactionType", "Date"])  # Create header

    def show_transactions(self):
        for transaction in self.transactions:
            print(f"Transaction {transaction.transaction_id}: User {transaction.user_id} {transaction.transaction_type} Book {transaction.book_id} on {transaction.date}")

    
    def save_transaction(self):
        """ Save transaction history to transactions.csv """
        with open(TRANSACTIONS_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["TransactionID", "UserID", "BookID", "TransactionType", "Date"])
            writer.writerows([
                [t.transaction_id, t.user_id, t.book_id, t.transaction_type, t.date]  # Convert object to list
                for t in self.transactions
            ])


    