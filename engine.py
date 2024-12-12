from fastapi import FastAPI

app = FastAPI()

class User:
    def __init__(self, name, email, id = 0):
        self.name = name
        self.email = email
        self.id = id
        self.borrowed_books = []

class Book:
    def __init__(self, title, year, genre, id = 0):
        self.available = True
        self.title = title
        self.year = year
        self.genre = genre
        self.id = id


class BookRepository:
    def __init__(self):
        self.books = []
        self.increment_id = 0
    def add_book(self, book):
        book.id = self.increment_id
        self.increment_id += 1
        self.books.append(book)

    def delete_book(self, book):
        self.books.remove(book)

    def get_all_book(self):
        return self.books


book_rep = BookRepository()

@app.get('/books')
def get_all_books():
    return book_rep.get_all_book()

@app.get('/book/')
def add_book(title, year, genre):
    book_rep.add_book(Book(title, year, genre))
    return "ADDED"
