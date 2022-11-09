from flask import Blueprint, request, jsonify
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


# @books_bp.route("/search/title/")
# def search_title():
#     # create an empty list in case the query string is not valid
#     # if request.json['title']:
#     stmt = db.select(Book).filter_by(title=request.json['title'].title())
#     books = db.session.scalars(stmt)
#     return BookSchema(many=True).dump(books)

# @books_bp.route("/search/author/")
# def search_author():
#     # elif request.json['author']:
#     stmt = db.select(Book).filter_by(author=request.json['author'].title())
#     books = db.session.scalars(stmt)
#     return BookSchema(many=True).dump(books)


@books_bp.route("/search/", methods=["GET"])
def search_books():
    # if request.json['title']: 
    if request.json.get('title'):
        stmt = db.select(Book).filter_by(title=request.json['title'].title())
        books = db.session.scalars(stmt)
    # elif request.json['author']:
    elif request.json.get('author'):
        stmt = db.select(Book).filter_by(author=request.json['author'].title())
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


@books_bp.route('/add_book/', methods=['POST'])
@jwt_required()
def add_book():
    authorize()
    # Add a new Book model instance
    data = BookSchema().load(request.json)
    book = Book(
        title = data['title'],
        author = data['author'],
        description = data['description'],
        category_id = data['category_id']
    )
    # Add and commit book to DB
    db.session.add(book)
    db.session.commit()
    # Respond to client
    return BookSchema().dump(book), 201
    # CONSTRAINTS?????????


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


@books_bp.route('/update/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_book(id):
    authorize()
    stmt = db.select(Book).filter_by(id=id)
    book = db.session.scalar(stmt)
    if book:
        book.title = request.json.get('title') or book.title
        book.author = request.json.get('author') or book.author
        book.description = request.json.get('description') or book.description
        book.category_id = request.json.get('category_id') or book.category_id

        db.session.commit()  
        return BookSchema().dump(book)
    else:
        return {'error': f'Book not found with id {id}'}, 404