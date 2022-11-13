from datetime import date, datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError
from models.book import Book, BookSchema
from models.author import Author, AuthorSchema
from controllers.auth_controller import authorize
from init import db


books_bp = Blueprint('books', __name__, url_prefix='/books')


# Route for displaying all books in database
@books_bp.route('/')
def get_all_books():
    # Select all books
    stmt = db.select(Book)
    books = db.session.scalars(stmt)
    # Return bookshcema of books selected with stmt
    return BookSchema(many=True, exclude=['author_id']).dump(books)


# Route for displaying a signle book based on its id
@books_bp.route('/<int:book_id>/')
def get_one_book(book_id):
    # Select books in database filtered by the id in the url
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        # Return bookshcema of books selected with stmt
        return BookSchema(exclude=['author_id']).dump(book)
    else:
        return {'error': f'Book not found with id {book_id}'}, 404


# Route for searching for books based on their title or author
@books_bp.route("/search/")
def search_books():
    if request.json.get('title'):
        # Select books filtered by title match
        stmt = db.select(Book).filter_by(title=request.json['title'].title())  # title() ensures upper/lower cases match that in databse
        # Assign selection to a variable
        books = db.session.scalars(stmt)
        # Return BookSchema of books selected with stmt
        return BookSchema(many=True, exclude=['author_id']).dump(books)
    elif request.json.get('author'):
        # Select books filtered by author match
        stmt = db.select(Author).filter_by(name=request.json['author'].title())  # title() ensures upper/lower cases match that in databse
        # Assign selection to a variable
        author = db.session.scalars(stmt)
        # Return BookSchema of books selected with stmt
        return AuthorSchema(many=True).dump(author)


# ADMIN ROUTES ----------------------------------------------------------------------

# Route for adding a book to database
@books_bp.route('/add_book/', methods=['POST'])
@jwt_required()
def add_book():
    authorize()
    # Load book schema
    data = BookSchema().load(request.json)
    # Add a new Book model instance
    book = Book(
        # Assign book fields to those in json request
        title = data['title'],
        author_id = data['author_id'],
        description = data['description'],
        price = data['price'],
        date_published = data['date_published'],
        in_stock = data['in_stock'],
        category = data['category']
    )

    # Add and commit book to DB
    db.session.add(book)
    db.session.commit()
    # Respond to client
    return BookSchema(exclude=['author_id']).dump(book), 201


# Route for updating a book in the database
@books_bp.route('/update_book/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_book(id):
    authorize()
    # Select book with id in url
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        # Load BookSchema data in order to access validation rules
        data = BookSchema().load(request.json)
        # Assign book fields to those in json request or leave as is
        book.title = request.json.get('title') or book.title
        book.author_id = request.json.get('author_id') or book.author_id
        book.description = request.json.get('description') or book.description
        book.price = request.json.get('price') or book.price
        book.category = request.json.get('category') or book.category
        book.date_published = request.json.get('date_published') or book.date_published
        book.in_stock = request.json.get('in_stock') or book.in_stock
         # Solves issue with updating boolean values to False
        if request.json.get('in_stock') is not None:
            book.in_stock = request.json.get('in_stock')
        else:
            book.in_stock = book.in_stock
        # Commit changes to the database
        db.session.commit()
        # Respond to client
        return BookSchema(exclude=['author_id']).dump(book)
    else:
        return {'error': f'Book not found with id {id}'}, 404


# Route for deleting a book in the database
@books_bp.route('/delete_book/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_book(id):
    authorize()
    # Select book with id in url
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        # Delete book and commit changes
        db.session.delete(book)
        db.session.commit()
        # Respond to client
        return {'message': f"Book '{book.title}' deleted successfully"}
    else:
        return {'error': f'Book not found with id {id}'}, 404
