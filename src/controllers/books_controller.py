from flask import Blueprint, request
from init import db
# from models.user import User, UserSchema
from models.book import Book, BookSchema
from models.author import Author, AuthorSchema
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize
from datetime import date, datetime
from marshmallow.exceptions import ValidationError



books_bp = Blueprint('books', __name__, url_prefix='/books')

# Route for displaying all books in database
@books_bp.route('/')
def get_all_books():
    stmt = db.select(Book)
    books = db.session.scalars(stmt)
    return BookSchema(many=True, exclude=['author_id']).dump(books)

# Route for displaying a signle book based on its id
@books_bp.route('/<int:book_id>/')
def get_one_book(book_id):
    # Select books in database filtered by the id in the url
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        return BookSchema(exclude=['author_id']).dump(book)
    else:
        return {'error': f'Book not found with id {book_id}'}, 404


# Route for searching for books based on their title or author
@books_bp.route("/search/")
def search_books():
    # If the request field is called 'title'
    if request.json.get('title'):
        # Select books filtered by title match
        stmt = db.select(Book).filter_by(title=request.json['title'].title()) # title() ensures upper/lower cases match that in databse)
        # Assign selection to a variable
        books = db.session.scalars(stmt)
        # Return database fields specified in BookSchema, based on the selection in the 'books' variable
        return BookSchema(many=True, exclude=['author_id']).dump(books)
    # If the request field is called 'author'
    elif request.json.get('author'):
        # Select books filtered by author match
        stmt = db.select(Author).filter_by(name=request.json['author'].title()) # title() ensures upper/lower cases match that in databse)
        # Assign selection to a variable
        author = db.session.scalars(stmt)
    return AuthorSchema(many=True).dump(author)


# ADMIN ROUTES ----------------------------------------------------------------------

# Route for adding a book to database
@books_bp.route('/add_book/', methods=['POST'])
@jwt_required()
def add_book():
    authorize()
    # Add a new Book model instance
    data = BookSchema().load(request.json)
    book = Book(
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
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        # Load BookSchema data in order to access validation rules
        data = BookSchema().load(request.json)
        book.title = request.json.get('title') or book.title
        book.author_id = request.json.get('author_id') or book.author_id
        book.description = request.json.get('description') or book.description
        book.price = request.json.get('price') or book.price
        book.category = request.json.get('category') or book.category
        book.date_published = request.json.get('date_published') or book.date_published
         # Solves issue with updating boolean values to False
        if request.json.get('in_stock') is not None:
            book.in_stock = request.json.get('in_stock')
        else:
            book.in_stock = book.in_stock

        # Solves issue with @validates('date_published') in models.book not applying to updates
        if request.json.get('date_published'):
            book_date_string = book.date_published
            date_object = datetime.strptime(book_date_string, '%Y-%m-%d').date()
            if date_object >  date.today():
                raise ValidationError("Publication date occurs after today's date")

        db.session.commit()
        return BookSchema(exclude=['author_id']).dump(book)
    else:
        return {'error': f'Book not found with id {id}'}, 404


# Route for deleting a book in the database
@books_bp.route('/delete_book/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_book(id):
    authorize()
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {'message': f"Book '{book.title}' deleted successfully"}
    else:
        return {'error': f'Book not found with id {id}'}, 404
