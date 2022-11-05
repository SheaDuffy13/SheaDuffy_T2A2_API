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

@categories_bp.route('/<string:category_name>/')
def get_category(category_name):
    stmt = db.select(Category).filter_by(name=category_name)
    cat = db.session.scalar(stmt)
    book_stmt = db.select(Book).filter_by(category=category_name.lower())
    books = db.session.scalars(book_stmt)
    if cat:
        return BookSchema(many=True).dump(books)
    else:
        return {'error': f'category not found with name {category_name}'}, 404

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