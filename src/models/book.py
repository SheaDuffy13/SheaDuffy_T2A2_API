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
    # author = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String)
    year_published = db.Column(db.Date)
    
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    # category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    author = db.relationship('Author', back_populates='books')
    # category = db.relationship('Category', back_populates='books')

    # orders = db.relationship('Order', back_populates='book', cascade='all, delete')

class BookSchema(ma.Schema):
    
    category = fields.String(validate=OneOf(VALID_CATEGORIES))
    # category = fields.Nested('CategorySchema', exclude=['books'])  #can exlude fields like pw or use only , exlude=['password']
    author = fields.Nested('AuthorSchema', exclude=['books'])
    # author = fields.Nested('AuthorSchema', only=['id', 'name', 'bio'])


    author_id = fields.String(required=True, validate=And(
        Length(min=1, error="Author must be at least 1 character long"),
        Regexp('^[a-zA-Z ]+$')
    ))
    title = fields.String(required=True, validate=
        Length(min=1, error="Title must be at least 1 character long"))

    description = fields.String(validate=
        Length(min=1, error='Description must be at least 1 character long')
    )

    year_published = fields.Date()

    @validates('year_published') 
    def validate_year_published(self, year):
        # if year > datetime.date.today().year:
        if year >  date.today():
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
        fields = ('id', 'title', 'category', 'description', 'price', 'year_published', 'author_id', 'author')

