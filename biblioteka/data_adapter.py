import json
import xml.etree.ElementTree as ET
import csv


class BookDataAdapter:
    @staticmethod
    def parse_json(data):
        return json.loads(data)

    @staticmethod
    def parse_xml(data):
        root = ET.fromstring(data)
        books = []
        for book in root.findall("book"):
            books.append(
                {"title": book.find("title").text, "author": book.find("author").text}
            )
        return books

    @staticmethod
    def parse_csv(data):
        books = []
        reader = csv.DictReader(data.splitlines())
        for row in reader:
            books.append({"title": row["title"], "author": row["author"]})
        return books


# Test Adapter
if __name__ == "__main__":
    json_data = '[{"title": "Book C", "author": "Author 3"}]'
    xml_data = """
    <books>
        <book><title>Book D</title><author>Author 4</author></book>
    </books>
    """
    csv_data = "title,author\nBook E,Author 5"

    print("JSON Data:", BookDataAdapter.parse_json(json_data))
    print("XML Data:", BookDataAdapter.parse_xml(xml_data))
    print("CSV Data:", BookDataAdapter.parse_csv(csv_data))
