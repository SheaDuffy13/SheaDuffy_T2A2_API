from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.author import Author, AuthorSchema
from controllers.auth_controller import authorize
from init import db


authors_bp = Blueprint('authors', __name__, url_prefix='/authors')


# Route to view all authors
@authors_bp.route('/')
def get_all_authors():
    # Select all authors in the database
    stmt = db.select(Author)
    # Assign selection to variable
    authors = db.session.scalars(stmt)
    # return author data based on the selection
    return AuthorSchema(many=True, exclude=['books']).dump(authors)


# Route to view all books by one author
@authors_bp.route('/<int:id>/')
def get_author(id):
    # Find author with id from url
    book_stmt = db.select(Author).filter_by(id=id)
    books = db.session.scalars(book_stmt)
    # If found
    if books:
        # Return author info along with all books belonging to them, nested in the author schema
        return AuthorSchema(many=True).dump(books)
    else:
        return {'error': f'category not found with id {id}'}, 404


# Route for admin to add new author to database
@authors_bp.route('/add_author/', methods=['POST'])
@jwt_required()
def add_author():
    authorize()
    # Add a new Book model instance
    data = AuthorSchema().load(request.json)
    # set fields to those in the json request
    author = Author(
        name = data['name'],
        bio = data['bio'],
    )
    # Add and commit book to database
    db.session.add(author)
    db.session.commit()
    # Respond to client
    return AuthorSchema().dump(author), 201


# Route for admin to update author in database
@authors_bp.route('/update_author/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_author(id):
    authorize()
    # Find author with id from url
    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)
    if author:
        # Load AuthorSchema data in order to access validation rules
        data = AuthorSchema().load(request.json)
        # set fields to those in the json request or leave be
        author.name = request.json.get('title') or author.name
        author.bio = request.json.get('bio') or author.bio
        # Commit changes to database
        db.session.commit()
        # Respond to client
        return AuthorSchema(exclude=['books']).dump(author)
    else:
        return {'error': f'Author not found with id {id}'}, 404


# Route for admin to delete author in database
@authors_bp.route('/delete_author/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_book(id):
    authorize()
    # Find author with id from url
    stmt = db.select(Author).filter_by(id=id)
    author = db.session.scalar(stmt)
    if author:
        # Delete author from database
        db.session.delete(author)
        # Commit changes to database
        db.session.commit()
        # Respond to client
        return {'message': f"Author '{author.name}' deleted successfully"}
    else:
        return {'error': f'Author not found with id {id}'}, 404