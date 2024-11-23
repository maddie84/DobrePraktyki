class LibraryCatalog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.books = []
        return cls._instance

    def add_book(self, book):
        self.books.append(book)

    def get_books(self):
        return self.books

    def find_book(self, title):
        return next((book for book in self.books if book['title'] == title), None)

# Test Singleton
if __name__ == "__main__":
    catalog1 = LibraryCatalog()
    catalog2 = LibraryCatalog()

    catalog1.add_book({"title": "Book A", "author": "Author 1"})
    catalog2.add_book({"title": "Book B", "author": "Author 2"})

    print("Books in catalog1:", catalog1.get_books())
    print("Books in catalog2:", catalog2.get_books())
    print("Singleton test:", catalog1 is catalog2)  # Should print True
    