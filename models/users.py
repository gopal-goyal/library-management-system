class User:
    def __init__(self, user_id, name, borrowed_books=[], library=None):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = borrowed_books  # List to track borrowed books
        self.library = library  # Reference to Library class object
