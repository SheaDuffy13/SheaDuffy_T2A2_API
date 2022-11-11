from flask import Blueprint, request, jsonify
from init import db
from models.user import User, UserSchema
from models.book import Book, BookSchema
from models.author import Author, AuthorSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize
from datetime import date, datetime
from marshmallow.exceptions import ValidationError



books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/')
def get_all_books():
    stmt = db.select(Book)
    books = db.session.scalars(stmt)
    return BookSchema(many=True, exclude=['author_id']).dump(books)


@books_bp.route('/<int:id>/')
def get_one_book(id):
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        return BookSchema(exclude=['author_id']).dump(book)
    else:
        return {'error': f'Book not found with id {id}'}, 404


@books_bp.route("/search/")
def search_books():
    # if request.json['title']: 
    if request.json.get('title'):
        stmt = db.select(Book).filter_by(title=request.json['title'].title())
        books = db.session.scalars(stmt)
        return BookSchema(many=True, exclude=['author_id']).dump(books)
    # elif request.json['author']:
    elif request.json.get('author'):
        stmt = db.select(Author).filter_by(name=request.json['author'].title())
        author = db.session.scalars(stmt)
    return AuthorSchema(many=True).dump(author)


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
    )

    # Add and commit book to DB
    db.session.add(book)
    db.session.commit()
    # Respond to client
    return BookSchema(exclude=['author_id']).dump(book), 201


@books_bp.route('/update_book/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_book(id):
    authorize()
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        book.title = request.json.get('title') or book.title
        # book.author = request.json.get('author') or book.author
        book.author_id = request.json.get('author_id') or book.author_id
        book.description = request.json.get('description') or book.description
        book.price = request.json.get('price') or book.price
        book.date_published = request.json.get('date_published') or book.date_published
        # book.category_id = request.json.get('category_id') or book.category_id
        book.author_id = request.json.get('author_id') or book.author_id

        # Solves issue of @validates('date_published') in models.book not applying to post-creation updates
        if request.json.get('date_published'):
            book_date_string = book.date_published 
            date_object = datetime.strptime(book_date_string, '%Y-%m-%d').date()
            if date_object >  date.today():
                raise ValidationError("Publication date occurs after today's date")

        db.session.commit()
        return BookSchema(exclude=['author_id']).dump(book)
    else:
        return {'error': f'Book not found with id {id}'}, 404


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
