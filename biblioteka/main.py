from library_interface import LibraryInterface
from data_adapter import BookDataAdapter

# Facade
library = LibraryInterface()

# Adapter
json_data = '[{"title": "Book A", "author": "Author 1"}]'
xml_data = """
<books>
    <book><title>Book B</title><author>Author 2</author></book>
</books>
"""
csv_data = "title,author\nBook C,Author 3"

# Adapter
books_from_json = BookDataAdapter.parse_json(json_data)
books_from_xml = BookDataAdapter.parse_xml(xml_data)
books_from_csv = BookDataAdapter.parse_csv(csv_data)

# Facade (korzysta z Singleton)
for book in books_from_json + books_from_xml + books_from_csv:
    library.add_book(book)

# Factory
library.add_user("Alice", "student") 
library.add_user("Bob", "teacher")
library.add_user("Charlie", "librarian")

# Observer
library.add_book({"title": "Book D", "author": "Author 4"})
library.add_book({"title": "Book E", "author": "Author 5"})

# Facade (korzysta z Singleton)
print("\nSearching for 'Book D':", library.find_book("Book D"))

# Facade (korzysta z Iterator)
print("\nListing all books:")
library.list_books()  # Iterator: przechodzenie po kolekcji książek

# Facade
print("\nListing all users:")
library.list_users()
