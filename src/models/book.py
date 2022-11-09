from init import db, ma
from marshmallow import fields, validate
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError


# VALID_CATEGORIES = ('horror', 'fantasy', 'romance', 'sci-fi', 'crime', 'non-fiction')

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    # category = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='books')

    # orders = db.relationship('Order', back_populates='book', cascade='all, delete')

class BookSchema(ma.Schema):
    
    # category = fields.String(required=True, validate=OneOf(VALID_CATEGORIES))

    class Meta:
        fields = ('id', 'title', 'author', 'series', 'description', 'category_id')

