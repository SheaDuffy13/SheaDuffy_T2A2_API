from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from models.book import Book, BookSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize


books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/')
def get_all_books():
    stmt = db.select(Book)
    books = db.session.scalars(stmt)
    return BookSchema(many=True).dump(books)

@books_bp.route('/<int:id>/')
def get_one_book(id):
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        return BookSchema().dump(book)
    else:
        return {'error': f'Book not found with id {id}'}, 404


@books_bp.route('/create_book', methods=['POST'])
@jwt_required()
def create_book():
    authorize()
    # Create a new Book model instance
    data = BookSchema().load(request.json)
    book = Book(
        title = data['title'],
        author = data['author'],
        description = data['description'],
        category = data['category']
    )
    # Add and commit book to DB
    db.session.add(book)
    db.session.commit()
    # Respond to client
    return BookSchema().dump(book), 201


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