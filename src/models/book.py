from marshmallow import fields, validate, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from init import db, ma
from marshmallow.exceptions import ValidationError
from datetime import date


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
    
    category = fields.String(validate=OneOf(VALID_CATEGORIES))
    author = fields.Nested('AuthorSchema', exclude=['books'])
    author = fields.Nested('AuthorSchema', only=['id', 'name'])
    title = fields.String(required=True, validate=
        Length(min=1, error="Title must be at least 1 character long"))

    description = fields.String(validate=
        Length(min=1, error='Description must be at least 1 character long')
    )
    # in_stock = fields.Boolean(default=False)
    date_published = fields.Date()

    @validates('date_published')
    def validate_date_published(self, date_published):
        if date_published >  date.today():
            raise ValidationError("Publication date occurs after today's date")

    # price = fields.Float(validate=And(
    #     Length(min=1, error='Price must be at least 1 character long'),
    #     Regexp('^[0-9]+$', error='Only numbers and decimals are accepted') # <---------- TODO: MAKE DECIMALS AN OPTION????? ??? ??
    # ))

    # author_id = fields.String(required=True, validate=And(
    #     Length(min=1, error='Author_id must be at least 1 character long'),
    #     Regexp('^[0-9]+$', error='Only numbers and decimals are accepted') # <---------- TODO: MAKE DECIMALS AN OPTION????? ??? ??
    # ))

    class Meta:
        ordered = True
        fields = ('id', 'title', 'category', 'description', 'date_published', 'price', 'in_stock', 'author_id', 'author')

