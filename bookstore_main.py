from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Bookstore API",
    description="A simple API to manage a bookstore inventory",
    version="1.0.0"
)

# In-memory database
books_db = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "price": 12.99,
        "stock": 10
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "price": 14.99,
        "stock": 5
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "price": 9.99,
        "stock": 15
    }
]

# Pydantic model for creating a new book
class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, le=10000)
    stock: int = Field(ge=0, le=1000)

# Pydantic model for updating an existing book
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0, le=10000)
    stock: Optional[int] = Field(None, ge=0, le=1000)

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Bookstore API"}

# Get all books
@app.get("/books")
def get_books():
    return books_db

# Search books by title or author
@app.get("/books/search")
def search_books(q: str, author: Optional[str] = None):
    results = []

    for book in books_db:
        if (
            q.lower() in book["title"].lower()
            or q.lower() in book["author"].lower()
        ):
            if author:
                if author.lower() in book["author"].lower():
                    results.append(book)
            else:
                results.append(book)

    return results

# Get a book by ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

# Add a new book
@app.post("/books")
def add_book(book: BookCreate):

    # Check if the book already exists
    for existing_book in books_db:
        if (
            existing_book["title"].lower() == book.title.lower()
            and existing_book["author"].lower() == book.author.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Book already exists"
            )

    # Generate a new ID
    new_id = max([b["id"] for b in books_db]) + 1 if books_db else 1

    # Create the new book
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "stock": book.stock
    }

    books_db.append(new_book)

    return {
        "message": "Book added successfully",
        "book": new_book
    }

# Update an existing book
@app.put("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):

    for index, book in enumerate(books_db):
        if book["id"] == book_id:

            if book_update.title is not None:
                books_db[index]["title"] = book_update.title

            if book_update.author is not None:
                books_db[index]["author"] = book_update.author

            if book_update.price is not None:
                books_db[index]["price"] = book_update.price

            if book_update.stock is not None:
                books_db[index]["stock"] = book_update.stock

            return {
                "message": "Book updated successfully",
                "book": books_db[index]
            }

    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            deleted_book = books_db.pop(index)

            return {
                "message": "Book deleted successfully",
                "book": deleted_book
            }

    raise HTTPException(status_code=404, detail="Book not found")