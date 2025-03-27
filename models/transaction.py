class Transaction:
    def __init__(self, transaction_id, user_id, book_id, transaction_type, date):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.book_id = book_id
        self.transaction_type = transaction_type  # 'borrow' or 'return'
        self.date = date

    def __str__(self):
        return f"Transaction {self.transaction_id}: {self.user_id.name} {self.type}ed {self.book_id.title} on {self.date}"