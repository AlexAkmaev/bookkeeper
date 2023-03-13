import sqlite3
import pytest
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from pprint import pprint


class Book:
    def __init__(self, title: str, author: str, year: int, pages: int):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        else:
            return self.title == other.title and self.author == other.author and self.year == other.year and self.pages == other.pages


def get_repo():
    return SQLiteRepository[Book](
        db_path=":memory:",
        table_name="books",
        columns={"title": "TEXT", "author": "TEXT", "year": "INTEGER", "pages": "INTEGER"},
        entity_type=Book,
    )


def test_add():
    repo = get_repo()
    book = Book(title='Test Book', author='Test Author', year=2021, pages=200)
    pk = repo.add(book)
    assert isinstance(pk, int)
    retrieved_book = repo.get(pk)
    assert retrieved_book == book


def test_update():
    repo = get_repo()
    book = Book('The Lord of the Rings', 'J.R.R. Tolkien', 1954, 1178)
    pk = repo.add(book)
    book.title = 'The Hobbit'
    repo.update(book)
    updated_book = repo.get(pk)
    assert updated_book.title == 'The Hobbit'
    assert updated_book.author == 'J.R.R. Tolkien'
    assert updated_book.year == 1954
    assert updated_book.pages == 1178


def test_get_all():
    repo = get_repo()
    book1 = Book('The Lord of the Rings', 'J.R.R. Tolkien', 1954, 1178)
    book2 = Book('The Hobbit', 'J.R.R. Tolkien', 1937, 310)
    repo.add(book1)
    repo.add(book2)
    books = repo.get_all()
    assert len(books) == 2
    assert books[0].title == 'The Lord of the Rings'
    assert books[0].author == 'J.R.R. Tolkien'
    assert books[0].year == 1954
    assert books[0].pages == 1178
    assert books[1].title == 'The Hobbit'
    assert books[1].author == 'J.R.R. Tolkien'
    assert books[1].year == 1937
    assert books[1].pages == 310

    books = repo.get_all({'title': 'The Lord of the Rings'})

    assert len(books) == 1

def test_get():
    repo = get_repo()

    book = Book(title='Test Book', author='Test Author', year=2021, pages=200)
    pk = repo.add(book)
    retrieved_book = repo.get(pk)
    assert retrieved_book == book

    expect_none = repo.get(pk + 1)
    assert expect_none is None


def test_delete():
    repo = get_repo()

    # Add a book
    book = Book("Book1", "Author1", 2021, 100)
    pk = repo.add(book)

    # Delete the book
    repo.delete(pk)

    # Check that the book is deleted
    assert repo.get(pk) is None

    # Check that the book is not in the list of all books
    all_books = repo.get_all()
    assert book not in all_books
