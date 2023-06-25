from datetime import date
from marshmallow.exceptions import ValidationError
from marshmallow import fields, validates
from marshmallow.validate import OneOf, Regexp
from init import db, ma


VALID_CATEGORIES = ('horror', 'fantasy', 'romance', 'sci-fi', 'crime', 'non-fiction')

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    date_published = db.Column(db.Date, nullable=False)
    in_stock = db.Column(db.Boolean)
   
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    author = db.relationship('Author', back_populates='books')
    wishlist_items = db.relationship('Wishlist_Item', back_populates='book')

class BookSchema(ma.Schema):
    author = fields.Nested('AuthorSchema', only=['id', 'name'])

    # Checks supplied category is from a valid category
    category = fields.String(validate=OneOf(VALID_CATEGORIES))

    title = fields.String(validate=Regexp(
        '[^\s-]', error='Tile must be more than 1 character'
        ))
    description = fields.String(validate=Regexp(
        '[^\s-]', error='Description must be more than 1 character'
        ))
    date_published = fields.Date()

    @validates('date_published')
    def validate_date_published(self, date_published):
        if date_published >  date.today():
            raise ValidationError("Publication date occurs after today's date")

    class Meta:
        ordered = True
        fields = ('id', 'title', 'category', 'description', 'date_published', 'price', 'in_stock', 'author_id', 'author')

    # author = fields.Nested('AuthorSchema', exclude=['books'])         removes
