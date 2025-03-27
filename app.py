from services.library import LibrarySystem
from datetime import datetime

current_time = datetime.now().strftime("%I:%M %p")

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
    print(library.borrow_book(1, 101, 1001, current_time))  # Piyush borrows your first year in Code
    print(library.borrow_book(2, 102, 1002, current_time))  # Saloni borrows Concepts of Physics
    print(library.borrow_book(1, 103, 1003, current_time))  # Book not in Database
    print(library.borrow_book(2, 101, 1004, current_time))  # Book not available
    print(library.return_book(2, 102, 1005, current_time))  # Saloni returns Concepts of Physics
    print(library.borrow_book(1, 102, 1006, current_time))  # Piyush borrows Concepts of Physics
    print(library.return_book(1, 101, 1007, current_time))  # Piyush returns your first year in Code
    print(library.return_book(1, 102, 1008, current_time))  # Piyush returns Concepts of Physics
    
    # Display Transactions
    print("\nTransaction History:")
    library.show_transactions()