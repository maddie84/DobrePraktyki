class BookIterator:
    def __init__(self, books):
        self.books = books
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        else:
            raise StopIteration

# Test Iterator
if __name__ == "__main__":
    books = [
        {"title": "Book H", "author": "Author 8"},
        {"title": "Book I", "author": "Author 9"}
    ]
    book_iterator = BookIterator(books)
    for book in book_iterator:
        print(book)
