from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
# from models.user import User, UserSchema
# from models.book import Book, BookSchema
from models.author import Author, AuthorSchema
from controllers.auth_controller import authorize


authors_bp = Blueprint('authors', __name__, url_prefix='/authors')

@authors_bp.route('/')
def get_all_authors():
    stmt = db.select(Author)
    authors = db.session.scalars(stmt)
    return AuthorSchema(many=True, exclude=['books']).dump(authors)

@authors_bp.route('/<int:id>/')
def get_author(id):
    book_stmt = db.select(Author).filter_by(id=id)
    books = db.session.scalars(book_stmt)
    if books:
        return AuthorSchema(many=True).dump(books)
    else:
        return {'error': f'category not found with id {id}'}, 404


@authors_bp.route('/add_author/', methods=['POST'])
@jwt_required()
def add_author():
    authorize()
    # Add a new Book model instance
    data = AuthorSchema().load(request.json)
    author = Author(
        name = data['name'],
        bio = data['bio'],
    )
    # Add and commit book to DB
    db.session.add(author)
    db.session.commit()
    # Respond to client
    return AuthorSchema().dump(author), 201

@authors_bp.route('/update_author/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_author(id):
    authorize()
    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)
    if author:
        # Load AuthorSchema data in order to access validation rules
        data = AuthorSchema().load(request.json)
        author.name = request.json.get('title') or author.name
        author.bio = request.json.get('bio') or author.bio

        db.session.commit()
        return AuthorSchema(exclude=['books']).dump(author)
    else:
        return {'error': f'Author not found with id {id}'}, 404


@authors_bp.route('/delete_author/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_book(id):
    authorize()
    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)
    if author:
        db.session.delete(author)
        db.session.commit()
        return {'message': f"Author '{author.name}' deleted successfully"}
    else:
        return {'error': f'Author not found with id {id}'}, 404