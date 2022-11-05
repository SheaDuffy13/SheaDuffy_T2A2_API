from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from models.book import Book, BookSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


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

