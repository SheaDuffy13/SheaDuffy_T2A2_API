from marshmallow import fields
from marshmallow.validate import Regexp
from init import db, ma

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    books = db.relationship('Book', back_populates='author', cascade='all, delete')


class AuthorSchema(ma.Schema):
    books = fields.List(fields.Nested('BookSchema', exclude=['author']))

    name = fields.String(validate=Regexp('[A-Za-z\.]{2,25}( [A-Za-z\.]{2,25})?',
    error='Name must be more than 2 characters and not contain numbers'))

    class Meta:
        ordered = True
        fields = ('id', 'name', 'bio', 'books')