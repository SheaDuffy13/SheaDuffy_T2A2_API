from flask import Blueprint
from init import db, bcrypt
from models.book import Book
from models.user import User
from models.author import Author
from models.wishlist import Wishlist
from models.wishlist_item import Wishlist_Item

db_commands = Blueprint('db', __name__)

# Assigns terminal command to create all tables in database
@db_commands.cli.command('create')
def create_all():
    # Create all tables in database
    db.create_all()
    print("Tables created")

# Assigns a terminal command to delete all tables in database
@db_commands.cli.command('drop')
def drop_db():
    # Delete all tables in database
    db.drop_all()
    print("Tables dropped")

# Assigns a terminal command to seed all tables in database
@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name = 'Admin Joe',
            email='admin@example.com',
            password=bcrypt.generate_password_hash('Eggs12').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Smith',
            email='user@example.com',
            password=bcrypt.generate_password_hash('Bacon12').decode('utf-8'),
        )
    ]

    # Add the users as new rows to the table
    db.session.add_all(users)
    # Commit the changes
    db.session.commit()

    authors = [
        Author(
            name = 'Jay Kristoff',
            bio = 'A bio on this author'
        ),
        Author(
            name='Jane Austin',
            bio = 'A bio on this author'
        ),
        Author(
            name='Stephenie Meyer',
            bio = 'A bio on this author'
        ),
        Author(
            name='Stephen King',
            bio = 'A bio on this author'
        ),
        Author(
            name='H. P. Lovecraft',
            bio = 'A bio on this author'
        ),
    ]

    # Add the authors as new rows to the table
    db.session.add_all(authors)
    # Commit the changes
    db.session.commit()

    books = [
        Book(
            title = 'Nevernight',
            author = authors[0],
            description = 'A booky book',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'fantasy',
            in_stock = True
        ),
        Book(
            title = 'Empire Of The Vampire',
            author = authors[0],
            description = 'A booky book book',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'fantasy',
            in_stock = True
        ),
        Book(
            title = 'Sense And Sensibility',
            author = authors[1],
            description = 'Ye olde jaunt',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'romance',
            in_stock = True
        ),
        Book(
            title = 'Twilight',
            author = authors[2],
            description = 'Hold on tight spider monkey',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'romance',
            in_stock = True
        ),
        Book(
            title = 'Misery',
            author = authors[3],
            description = 'crazy lady break ankles',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'horror',
            in_stock = True
        ),
        Book(
            title = 'The Call Of Cthulhu',
            author = authors[4],
            description = 'calamari boi',
            price = 10.00,
            date_published = '2005-04-07',
            category = 'horror',
            in_stock = True
        )
    ]
    # # Add the books as new rows to the table
    db.session.add_all(books)
    # Commit the changes
    db.session.commit()

    wishlists = [
        Wishlist(
            user_id = 1,
        ),
        Wishlist(
            user_id = 2,
        ),
    ]
    db.session.add_all(wishlists)
    db.session.commit()


    wishlist_items = [
        Wishlist_Item(
            wishlist_id = 2,
            book_id = 1
        ),
        Wishlist_Item(
            wishlist_id = 2,
            book_id = 2
        ),
        
    ]
    db.session.add_all(wishlist_items)
    db.session.commit()

    print("Table seeded")