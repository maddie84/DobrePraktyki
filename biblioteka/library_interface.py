# from library_catalog import LibraryCatalog
# from observer import LibraryCatalog as ObserverCatalog, User

# class LibraryInterface:
#     def __init__(self):
#         self.catalog = LibraryCatalog()

#     def add_book(self, book):
#         self.catalog.add_book(book)

#     def find_book(self, title):
#         return self.catalog.find_book(title)

# # Test Facade
# if __name__ == "__main__":
#     library = LibraryInterface()
#     library.add_book({"title": "Book G", "author": "Author 7"})
#     print(library.find_book("Book G"))

from library_catalog import LibraryCatalog
from observer import LibraryCatalog as ObserverCatalog
from user_factory import UserFactory
from iterator import BookIterator


class LibraryInterface:
    def __init__(self):
        # Singleton katalogu książek
        self.catalog = LibraryCatalog()
        # Katalog z obsługą powiadomień
        self.observer_catalog = ObserverCatalog()
        # Lista użytkowników
        self.users = []

    # Dodawanie książek
    def add_book(self, book):
        self.catalog.add_book(book)
        self.observer_catalog.add_book(book)

    # Wyszukiwanie książek
    def find_book(self, title):
        return self.catalog.find_book(title)

    # Dodawanie użytkownika
    def add_user(self, name, user_type):
        user = UserFactory.create_user(name, user_type)
        self.users.append(user)
        self.observer_catalog.subscribe(user)
        return user

    # Wyświetlanie wszystkich książek
    def list_books(self):
        book_iterator = BookIterator(self.catalog.get_books())
        for book in book_iterator:
            print(book)

    # Wyświetlanie użytkowników
    def list_users(self):
        for user in self.users:
            print(user)


# Test Facade
if __name__ == "__main__":
    library = LibraryInterface()

    # Dodanie użytkowników
    library.add_user("Alice", "student")
    library.add_user("Bob", "teacher")

    # Dodanie książek
    library.add_book({"title": "Book X", "author": "Author 10"})
    library.add_book({"title": "Book Y", "author": "Author 11"})

    # Wyszukiwanie książki
    print("\nSearching for 'Book X':", library.find_book("Book X"))

    # Wyświetlanie książek
    print("\nListing all books:")
    library.list_books()

    # Wyświetlanie użytkowników
    print("\nListing all users:")
    library.list_users()
