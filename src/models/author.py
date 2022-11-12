from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    books = db.relationship('Book', back_populates='author', cascade='all, delete')


class AuthorSchema(ma.Schema):
    books = fields.List(fields.Nested('BookSchema', exclude=['author']))

    name = fields.String(required=True, validate=And(
        Length(min=1, error="Author must be at least 1 character long"),
        Regexp('^[a-zA-Z ]+$')
    ))

    bio = fields.String(validate=Length(min=1, error='Name must be at least 1 character long')
    )

    class Meta:
        ordered = True
        fields = ('id', 'name', 'bio', 'books')