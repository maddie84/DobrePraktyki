from user_factory import User


class LibraryCatalog:
    def __init__(self):
        self.books = []
        self.subscribers = []

    def subscribe(self, user):
        self.subscribers.append(user)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

    def add_book(self, book):
        self.books.append(book)
        self.notify(f"New book added: {book['title']}")


# Test Observer
if __name__ == "__main__":
    from user_factory import UserFactory

    catalog = LibraryCatalog()
    user1 = UserFactory.create_user("Alice", "student")
    user2 = UserFactory.create_user("Bob", "teacher")

    catalog.subscribe(user1)
    catalog.subscribe(user2)

    catalog.add_book({"title": "Book D", "author": "Author 4"})
