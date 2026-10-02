"""
You're building a small REST API for a bookstore using Python and Flask. Implement the endpoints for a `books` resource:

- `GET /books` returns all books
- `GET /books/<id>` returns one book, or a 404 if it doesn't exist
- `POST /books` creates a book from a JSON body like `{"title": "Dune", "author": "Frank Herbert"}` and returns the created book

Use an in-memory dictionary for storage (no database needed).
"""

from flask import Flask, request, jsonify, abort
from pydantic import BaseModel, ValidationError
from werkzeug.exceptions import HTTPException

# Book schema
class Book(BaseModel):
    title: str
    author: str

# Create the web application
app = Flask(__name__)

# Keep track of the book indexes
book_index = 0

# In-memory storage
books = dict()

# Error handler for status code 422
@app.errorhandler(422)
def handle_422_error(error):
    # Retrieve custom description passed during abort()
    description = error.description if hasattr(error, 'description') else 'Unprocessable Entity'

    return jsonify({
        "error": "Unprocessable Entity",
        "message": description
    }), 422

@app.errorhandler(HTTPException)
def handle_http_error(error):
    return jsonify(error=error.name, message=error.description), error.code

# Handles GET and POST for Books
@app.route('/books', methods=['GET', 'POST'])
def booksAPI():
    global book_index
    if request.method == 'POST':
        try:
            book = Book(**request.get_json())
        except ValidationError as error:
            return jsonify(error.errors()), 422

        books[book_index] = book.model_dump()

        created = {'id': book_index, 'book': books[book_index]}

        book_index += 1

        return created, 201

    else:
        return books

# Handles GET for a single book
@app.get('/books/<int:id>')
def getBookAPI(id: int):
  book = books.get(id)
  if book is None:
      abort(404, description=f"No book with id {id}")
  return jsonify({"id": id, "book": books[id]})