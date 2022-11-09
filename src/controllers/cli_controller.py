from unicodedata import category
from flask import Blueprint
from init import db, bcrypt
from models.book import Book
from models.user import User
from models.category import Category

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name = 'Admin Joe',
            email='admin@example.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            address = '',
            phone = '',
            is_admin=True
        ),
        User(
            name='John Smith',
            email='user@example.com',
            password=bcrypt.generate_password_hash('bacon').decode('utf-8'),
            # password = 'eggs',
            address = '123 road St, Suburb, QLD',
            phone = '100 200 300 1',
        )
    ]

    # Add the object as a new row to the table
    db.session.add_all(users)
    db.session.commit()

    categories = [
        Category(
            name = 'horror'
        ),
        Category(
            name='romance'
        ),
        Category(
            name='fantasy'
        ),
    ]

    # Add the object as a new row to the table
    db.session.add_all(categories)
    db.session.commit()

    books = [
        Book(
            title = 'Nevernight',
            author = 'Jay Kristoff',
            description = 'A booky book',
            # category = 'fantasy'
            category_id = categories[2].id
        ),
        Book(
            title = 'Empire Of The Vampire',
            author = 'Jay Kristoff',
            description = 'A booky book book',
            # category = 'fantasy'
            category_id = categories[2].id
        ),
        Book(
            title = 'Sense And Sensibility',
            author = 'Jane Austin',
            description = 'Ye olde jaunt',
            # category = 'romance'
            category_id = categories[1].id
        ),
        Book(
            title = 'Twilight',
            author = 'Stephenie Meyer',
            description = 'Hold on tight spider monkey',
            # category = 'romance'
            category_id = categories[1].id
        ),
        Book(
            title = 'Misery',
            author = 'Stephen King',
            description = 'crazy lady break ankles',
            # category = 'horror'
            category_id = categories[0].id
        ),
        Book(
            title = 'The Call Of Cthulhu',
            author = 'H. P. Lovecraft',
            description = 'calamari boi',
            # category = 'horror'
            category_id = categories[0].id
        )
    ]
    
    db.session.add_all(books)
    db.session.commit()


    print("Table seeded")