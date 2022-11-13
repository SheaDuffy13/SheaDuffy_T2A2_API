# T2A2 - API Webserver

## R1 - Identification of the problem you are trying to solve by building this particular app

------------------------------------------------------------------------------------------------
I need to build a webserver API to store and retrieve items from a database and handle HTTP requests.
The database will need to contain tables for the different entities related to stock and users. Admin users will need to have special privileges and be able to modify stock. The tables will have relationships so a relational database would be best. 

## R2 - Why is it a problem that needs solving?

------------------------------------------------------------------------------------------------

A small bookstore is in need of a website to list its stock online. As the frontend of the website is already covered, the store only needs a database and server to fulfill HTTP requests. At this early stage, all the website would need to do is allow users create an account, log in, view the stock and be able to add items to a wish list. Admins of the store will need to be able to update the stock online.

## R3 - Why have you chosen this database system. What are the drawbacks compared to others?

------------------------------------------------------------------------------------------------

For this task I'll be using the relational database, Postgresql. This system is well optimized for general use cases, extremely programmable and easy to set up. It requires low maintenance and administration services as well as being compatible with various platforms. Postgres also comes with inbuilt security features and extensions.
It is accessible to work with as there is boundless free resources, documentation and community support to refer to. It also facilitates relational mapping between database objects.

Compared to other database systems, Postgres has no warranty, liability or indemnity protection as it is open source. The NoSQL database is another option, being a newer technology, some may find that more appealing.

## R4 - Identify and discuss the key functionalities and benefits of an ORM
------------------------------------------------------------------------------------------------

An ORM (Object Relational Mapper) facilitate the communication between programming languages and databases. It acts as the middleman between systems, creating smoother implementation and better query performance.
In the case of Python and SQLAlchemy, SQLAlchemy will translate Python classes to tables on a relational database. It automatically converts function calls to SQL statements to query the database. A benefit of SQLAlchemy is that it allows developers to create database-agnostic code, meaning communicate between a wide variety of database engines is possible.


## R5 - Endpoints Documentation
------------------------------------------------------------------------------------------------

## AUTHORIZATION:

### **auth/register/** 

- Methods: POST
- Arguments: None
- Authorization: None
- Description: Register user and assign them a wishlist
- Form Data: email, password, name, is_admin
- Response: UserSchema, exclude=password

### **auth/login/**

- Methods: POST
- Arguments: None
- Authorization: Must have registered account
- Description: Log user into site
- Form Data: email, password
- Response: email, token, is_admin

## USERS:

### **/users/**

- Methods: GET
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Return all users
- Form Data: None
- Response: UserSchema, exclude=password


### **/users/admins/**

- Methods: GET
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Return all admin users
- Form Data: None
- Response: UserSchema, exclude=password

### **/users/<int:id>/**

- Methods: GET
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Return user with id
- Form Data: None
- Response: UserSchema, exclude=password

### **/users/update_user/<int:id>/**

- Methods: PUT, PATCH
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Update any user account
- Form Data: name, email, is_admin
- Response: UserSchema, exclude=password

### **/users/delete_user/<int:id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Delete any user
- Form Data: None
- Response: "{user.email} deleted successfully"

### **/users/update_account/**

- Methods: PUT, PATCH
- Arguments: None
- Authorization: Bearer token
- Description: Update current user's account
- Form Data: name, email, password
- Response: UserSchema, exclude=password

### **/users/delete_account/**

- Methods: DELETE
- Arguments: None
- Authorization: Bearer token
- Description: Delete current user's account
- Form Data: None
- Response: "User {user.email} deleted successfully"

## BOOKS:

### **/books/**

- Methods: GET
- Arguments: None
- Description: Return all books
- Form Data: None
- Response: BookSchema

### **/books//<int:book_id>/**

- Methods: GET
- Arguments: id
- Description: Return book with id
- Form Data: None
- Response: BookSchema

### **/books/search/**

- Methods: GET
- Arguments: None
- Description: Return books by title or author name
- Form Data: "title" or "author"
- Response: BookSchema or AuthorSchema(with books)

### **/books/add_book/**

- Methods: POST
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Add book to database
- Form Data: title, author_id, description, price, date_published, in_stock, category
- Response: BookSchema, 201

### **/books/update_book/<int:id>/**

- Methods: PUT, PATCH
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Update book
- Form Data: title, author_id, description, price, date_published, in_stock, category
- Response: BookSchema

### **/books/delete_book/<int:id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Delete book
- Form Data: None
- Response: return {'message': f"Book '{book.title}' deleted successfully"}

## AUTHORS

### /**authors**/

- Methods: GET
- Arguments: None
- Description: Return all authors
- Form Data: None
- Response: AuthorSchema excluding books

### **/authors/<int:id>/**

- Methods: GET
- Arguments: id
- Description: Returns AuthorSchema and all books associated
- Form Data: None
- Response: AuthorSchema with nested books

### **/authors/add_author/**

- Methods: POST
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Add author to database
- Form Data: name, bio
- Response: AuthorSchema

### **/authors/update_author/<int:id>/**

- Methods: PUT, PATCH
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Update author
- Form Data: name, bio
- Response: AuthorSchema exclude books

### **/authors/delete_author/<int:id>/**

- Methods: DELETE
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Delete Author
- Form Data: None
- Response: "Author {author.name} deleted successfully"

## WISHLIST

### **/wishlist/**

- Methods: GET
- Arguments: None
- Authorization: Bearer token
- Description: Return user's wishlist
- Form Data: None
- Response: WishlistSchema

### **/wishlist/add/<int:id>**

- Methods: PUT, PATCH
- Arguments: id
- Authorization: Bearer token
- Description: Add book to current user's wishlist
- Form Data: None
- Response: 
  - WishlistSchema else: 'error': f'Book with id {id} already in wishlist', 412

### **/wishlist/delete/<int:item_id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token
- Description: Delete book from current user's wishlist
- Form Data: None
- Response: 
  - 'Wishlist item {item_id} deleted from wishlist else: 
  - 'Wishlist item {item_id} not found in wishlist'

## R6 - An ERD for your app
------------------------------------------------------------------------------------------------

Below is the ERD diagram I prepared for the webserver app. The 5 entity models are User, Book, Author, Wishlist, and Wishlist_Item. Users have a one-to-one relationships with their wishlist. That wishlist has a many relationship to wishlist_items (the wishlist can have many items). Wishlist_items then have two foreign keys, to a user's wishlist and to a single book. Finally, a book has a foreign key to author. Associations will be built with primary and foreign keys.

![ERD](./docs/API%20ERD.png)

## R7 - Detail any third party services that your app will use

------------------------------------------------------------------------------------------------

No third party services were used in this application, unless you include SQLAlchemy, Marshmallow and the like.

## R8 - Describe your projects models in terms of the relationships they have with each other

------------------------------------------------------------------------------------------------

The entity models in the final database are: User, Book, Author, Wishlist, Wishlist_Item. 
The server uses SQLAlchemy and Marshmallow to handle database communication and serialization. In SQLAlchemy, table models are set up in a file with rows set to form columns in a postgres database table. These rows assign things like data types, nullable, foreign keys and primary keys.

Relationships are set up with a foreign key and a db.relationship field.
As an example: The books table has a many to one relationship with authors, as an author can have many books but a book generally has one author. The relationship is first set up in the books table using a foreign key for the author id.

```py
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    author = db.relationship('Author', back_populates='books')
```

In the author table, books is assigned to a relationship field.

```py

    books = db.relationship('Book', back_populates='author', cascade='all, delete')
```

Marshmallow is handy for object serialization/deserialization and to validate data. The Meta field establishes what data is sent from the table.
In this example, the author schema has the book field nested in a list. This allows an author to be easily selected with all the books under their name.

```py
    class AuthorSchema(ma.Schema):
        books = fields.List(fields.Nested('BookSchema', exclude=['author']))
```

In the book schema, marshmallow is used to validate the characters of a field and the date in another field.

```py
    class BookSchema(ma.Schema):
        description = fields.String(validate=Regexp(
        '[^\s-]', error='Description must be more than 1 character'
        ))

        @validates('date_published')
        def validate_date_published(self, date_published):
            if date_published >  date.today():
                raise ValidationError("Publication date occurs after today's date")

        # The Meta field establishes what data is sent from the table
        class Meta:
        fields = ('id', 'title', 'category', 'description', 'date_published', 'price', 'in_stock', 'author_id', 'author')
```

Database queries with SQLAlchemy can look something like the example below. Database objects are selected and filtered with db.select. The session is then stored in a variable. Schemas are often used to return table fields in a way that can be read by the client.

```py
    # Route for displaying a signle book based on its id
    @books_bp.route('/<int:book_id>/')
    def get_one_book(book_id):
        # Select books in database filtered by the id in the url
        stmt = db.select(Book).filter_by(id=book_id)
        book = db.session.scalar(stmt)
        if book:
            # Return bookshcema of books selected with stmt
            return BookSchema(exclude=['author_id']).dump(book)
        else:
            return {'error': f'Book not found with id {book_id}'}, 404
```

## R9 - Discuss the database relations to be implemented in your application

------------------------------------------------------------------------------------------------

The entity models planned are **User**, **Book**, **Author**, **Wishlist**, **Wishlist_Item**. 
As shown on the ERD, a user will have one Wishlist containing many instances of books. As A wishlist can have many books and a book can be in many wishlists, the table, Wishlist_Items, will serve as a joining table. Wishlist_Items will have 2 foreign keys, Wishlist_id and book_id.
The columns of the database will be the rows in the ERD. Primary keys set the unique value instances of an entity can be referred to with. Foreign keys link tables together, allowing better queries.

## R10 - Describe the way tasks are allocated and tracked in your project

------------------------------------------------------------------------------------------------
This project was tracked in Trello using a Kanban board. Objectives were created using cards which outlined the steps of each task and a timeline. Cards started in the TO DO column. As I undertook each task, its card was moved to the DOING column. There I worked through each checklist until it could be moved to the DONE column.