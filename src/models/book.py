from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# VALID_CATEGORIES = ('horror', 'fantasy', 'romance', 'sci-fi', 'crime', 'non-fiction')

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    category = db.Column(db.String, nullable=False)

    # orders = db.relationship('Order', back_populates='book', cascade='all, delete')

class BookSchema(ma.Schema):
    
    # category = fields.String(required=True, validate=OneOf(VALID_CATEGORIES))

    class Meta:
        fields = ('id', 'title', 'author', 'description', 'category')

