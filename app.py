from services.library import LibrarySystem
from datetime import datetime


if __name__ == "__main__":
    
    # Initialize Library System
    library = LibrarySystem()
    
    # Add and deleteUsers
    print(library.add_user(1, "Piyush"))
    print(library.add_user(2, "Saloni"))
    print(library.add_user(3, "Vipin"))
    print(library.delete_user(3))
    
    
    # # Add and delete Books
    print(library.add_book(101, "Your First Year in Code", "Isaac Lyman"))
    print(library.add_book(102, "Concepts of Physics", "H.C. Verma"))
    print(library.add_book(103, "The Great Gatsby", "F. Scott Fitzgerald"))
    print(library.delete_book(103))
    
    # Borrow and Return Books
    print(library.borrow_book(2, 102))  # Saloni borrows Concepts of Physics
    print(library.borrow_book(1, 101))  # Piyush borrows your first year in Code
    print(library.borrow_book(1, 103))  # Book not in Database
    print(library.borrow_book(2, 101))  # Book not available
    print(library.return_book(2, 102))  # Saloni returns Concepts of Physics
    print(library.borrow_book(1, 102))  # Piyush borrows Concepts of Physics
    print(library.return_book(1, 101))  # Piyush returns your first year in Code
    print(library.return_book(1, 102))  # Piyush returns Concepts of Physics
    
    # Display Transactions
    print("\nTransaction History:")
    library.show_transactions()