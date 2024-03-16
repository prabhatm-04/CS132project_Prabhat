import json
from datetime import datetime, timedelta

class LibraryManager:
    def __init__(self):
        self.books = []
        self.patrons = []
        self.transactions = []

    def add_new_book(self, book):
        """Add a new book to the library."""
        self.books.append(book)

    def remove_book(self, book):
        """Remove a book from the library."""
        if book in self.books:
            self.books.remove(book)
        else:
            print("Book not found in the library.")

    def register_patron(self, patron):
        """Register a new patron."""
        self.patrons.append(patron)

    def remove_patron(self, patron):
        """Remove a patron from the library records."""
        if patron in self.patrons:
            self.patrons.remove(patron)
        else:
            print("Patron not found in the library records.")

    def process_transaction(self, transaction):
        """Process a transaction in the library."""
        self.transactions.append(transaction)
        if transaction.book in self.books and transaction.patron in self.patrons:
            transaction.checkout_book()
        else:
            print("Invalid transaction: Book or patron not found.")

    def search_books_by_title(self, title):
        """Search for books by title."""
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        return found_books

    def generate_library_reports(self):
        """Generate reports for the library."""
        pass

    def save_library_data(self, file_name):
        """Save library data to a file."""
        data = {
            'books': [book.to_dict() for book in self.books],
            'patrons': [patron.to_dict() for patron in self.patrons],
            'transactions': [transaction.to_dict() for transaction in self.transactions]
        }
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def load_library_data(self, file_name):
        """Load library data from a file."""
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                self.books = [Book(**book_data) for book_data in data['books']]
                self.patrons = [Patron(**patron_data) for patron_data in data['patrons']]
                self.transactions = [Transaction(**transaction_data) for transaction_data in data['transactions']]
        except FileNotFoundError:
            print("File not found.")

class PatronRegistry:
    def __init__(self, name, id, contact_info):
        self.name = name
        self.id = id
        self.contact_info = contact_info
        self.borrowed_books = []

    def display_patron_details(self):
        """Display details of the patron."""
        print(f"Name: {self.name}")
        print(f"ID: {self.id}")
        print(f"Contact Information: {self.contact_info}")

    def borrow_book(self, book):
        """Add a book to the list of borrowed books."""
        if book.quantity > 0:
            self.borrowed_books.append(book)
            book.quantity -= 1
        else:
            print("Book is out of stock.")

    def return_book(self, book):
        """Remove a book from the list of borrowed books."""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.quantity += 1

    def get_patron_info(self):
        """Retrieve patron information."""
        return {
            'name': self.name,
            'id': self.id,
            'contact_info': self.contact_info,
            'borrowed_books': [book.to_dict() for book in self.borrowed_books]
        }


class BookCatalog:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity

    def display_book_details(self):
        """Display details of the book."""
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.isbn}")
        print(f"Quantity: {self.quantity}")

    def update_book_quantity(self, new_quantity):
        """Update the quantity of the book."""
        self.quantity = new_quantity

    def get_book_info(self):
        """Retrieve book information."""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'quantity': self.quantity
        }


class LibraryTransaction:
    def __init__(self, book, patron, due_date=None):
        self.book = book
        self.patron = patron
        self.due_date = due_date

    def checkout_book(self):
        """Handle the checkout process."""
        if self.book.quantity > 0:
            self.book.quantity -= 1
            self.due_date = datetime.now() + timedelta(days=14)  # Due in 14 days
        else:
            print("Sorry, the book is out of stock.")

    def return_book(self):
        """Handle the return process."""
        if self.book in self.patron.borrowed_books:
            self.book.quantity += 1
            self.due_date = None
        else:
            print("This book was not borrowed by the patron.")

    def calculate_fine(self):
        """Calculate any possible fines."""
        pass

    def get_transaction_info(self):
        """Retrieve transaction information."""
        return {
            'book': self.book.to_dict(),
            'patron': self.patron.get_patron_info(),
            'due_date': str(self.due_date)
        }


# Sample usage:
def main():
    library_manager = LibraryManager()

    # Input book details
    titlebook = input("Input the title of the book: ")
    authorbook = input("Input the author of the book: ")
    isbnbook = input("Enter the ISBN code of the book: ")
    qtbook = int(input("Enter the quantity of books taken: "))

    # Create a book object
    book1 = BookCatalog(titlebook, authorbook, isbnbook, qtbook)

    # Input patron details
    patronname = input("Enter patron name: ")
    patronID = input("Enter patron ID: ")
    patroncontact = input("Enter patron contact information: ")

    # Create a patron object
    patron1 = PatronRegistry(patronname, patronID, patroncontact)

    # Create a transaction object and add book and patron to the library
    transaction1 = LibraryTransaction(book1, patron1)
    library_manager.add_new_book(book1)
    library_manager.register_patron(patron1)

    # Handle the transaction (checkout book)
    library_manager.process_transaction(transaction1)

    # Save data to a file
    library_manager.save_library_data('library_data.json')

    # Load data from a file
    library_manager.load_library_data('library_data.json')

    # Perform transactions
    transaction1 = LibraryTransaction(book1, patron1)
    library_manager.process_transaction(transaction1)

if __name__ == "__main__":
    main()
