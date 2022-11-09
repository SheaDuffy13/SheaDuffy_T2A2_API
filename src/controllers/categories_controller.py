from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User, UserSchema
from models.book import Book, BookSchema
from models.category import Category, CategorySchema


categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/')
def get_all_categories():
    stmt = db.select(Category)
    categories = db.session.scalars(stmt)
    return CategorySchema(many=True).dump(categories)

# @categories_bp.route('/<string:category_name>/')
@categories_bp.route('/<int:id>/')
def get_category(id):
    # stmt = db.select(Category).filter_by(name=category_name)
    # stmt = db.select(Category).filter_by(id=id)
    # categ = db.session.scalar(stmt)
    # book_stmt = db.select(Book).filter_by(category=category_name.lower())
    book_stmt = db.select(Book).filter_by(category_id=id)
    books = db.session.scalars(book_stmt)
    if books:
        return BookSchema(many=True).dump(books)
        # return CategorySchema().dump(categ) and BookSchema(many=True).dump(books) 
    else:
        return {'error': f'category not found with id {id}'}, 404

# @categories_bp.route('/<string:category>/')
# def get_category(category):
#     stmt = db.select(Book).filter_by(category=category.lower())
#     books = db.session.scalars(stmt)
#     # solved error catching only returning empty list
#     check_category = db.select(Category).filter_by(name=category.lower())
#     valid_category = db.session.scalars(check_category)
#     if books in valid_category:
#         return BookSchema(many=True).dump(books)
#     else:
#         return {'error': f'category not found with name {category}'}, 404