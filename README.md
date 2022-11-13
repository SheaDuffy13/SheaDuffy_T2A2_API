# T2A2 - API Webserver

## R1 - Identification of the problem you are trying to solve by building this particular app
(what the app is)
I need to build a webserver API to store and retrieve items from a databse and handle HTTP requests.
The databse will need to contain tables for the different entities related to stock and users. Admin users will need to have special privileges and modify stock.

## R2 - Why is it a problem that needs solving?

A small bookstore is in need of a website to list its stock online. As the frontend of the website is already covered, the store only needs a database and server to fulfill HTTP requests. At this early stage, all the website would need to do is allow users to view the stock and be able to add them to a wishlist. Admins of the store will need to be able to update the stock online.

## R3 - Why have you chosen this database system. What are the drawbacks compared to others?
(explanation of database system incl comparison to others, why you chose)
Postgres/relational
compare to document based database nor nosql?

For this task I'll be using the relational database, Postgresql. This system is well optimized for general use cases, extremely programmable and easy to set up. It requires low maintenance and administration services aswell as being compatible with various platforms. Postgres also comes with inbuilt security features and extensions.
It should be accessible to work with as there is boundless free resources, documentation and community support to refer to.

Compared to other database systems, Postgres has no warranty, liability or indemnity protection as it is open source. The NoSQL database is another option, being a newer technology.

## R4 - Identify and discuss the key functionalities and benefits of an ORM
(reword q2 from previous workbook) ORM's like SQLAlchemy

An ORM (Object Relational Mapper) facilitate the communication between programming languages and databases.
In the case of Python and SQLAlchemy, SQLAlchemy will translate Python classes to tables on a relational database. It then automatically converts function calls to SQL statements. The interface of SQLAlchemy allows developers to create database-agnostic code, allowing communicate between a wide variety of database engines.


## R5 - Endpoints Documentation
----------------------------------------------------------------

## AUTHORIZATION:

### **auth/register/** 

- Methods: POST
- Arguments: None
- Authorization: None
- Description: Register user and assign them a wishlist
- Form Data:

```json
{
    "email": "",
    "password": "",
    "name": "",
    "is_admin": 0
}
```

- Response:

```json
{
    "id": 4,
    "name": "Pepe Smith",
    "email": "pep2@mail.com",
    "is_admin": false,
    "wishlist": [
        {
            "id": 4,
            "wishlist_items": []
        }
    ]
}
```

### **auth/login/**

- Methods: POST
- Arguments: None
- Authorization: Must have registered account
- Description: Log user into site
- Form Data:

```json
{
    "email": "",
    "password": "",
}
```

- Response:

```json
{
    "email": "pep2@mail.com",
    "token": "eyJhbGc....",
    "is_admin": false
}
```
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
- Form Data: 

```json
{
    "name": "",
    "email": "",
    "is_admin": 0

}
```

- Response: UserSchema, exclude=password

### **/users/delete_user/<int:id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Delete any user
- Form Data: None
- Response: 
	return {'message': f"User '{user.email}' deleted successfully"}

### **/users/update_account/**

- Methods: PUT, PATCH
- Arguments: None
- Authorization: Bearer token
- Description: Update current user's account
- Form Data:

```json
{
    "name": "",
    "email": "",
    "password": ""

}
```

- Response: UserSchema, exclude=password

### **/users/delete_account/**

- Methods: DELETE
- Arguments: None
- Authorization: Bearer token
- Description: Delete current user's account
- Form Data: None
- Response: 
	return {'message': f"User '{user.email}' deleted successfully"}

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
- Form Data:

```json
{
    "title": "",
    // or
    "author": ""
}
```

- Response: BookSchema or AuthorSchema(with books)

### **/books/add_book/**

- Methods: POST
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Add book to database
- Form Data:

```json
{
    "title": "",
    "author_id": ,
    "description": "",
    "price": "",
    "date_published": "",
    "in_stock": "",
    "category": ""
}
```

- Response: BookSchema, 201

### **/books/update_book/<int:id>/**

- Methods: PUT, PATCH
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Update book
- Form Data:

```json
{
    "title": "",
    "author_id": ,
    "description": "",
    "price": "",
    "date_published": "",
    "in_stock": "",
    "category": ""
}
```

- Response: BookSchema

### **/books/delete_book/<int:id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token, is_admin
- Description: Delete book
- Form Data: None
- Response: return {'message': f"Book '{book.title}' deleted successfully"}

## AUTHORS

### /authors/

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
- Form Data:

```json
{
    "name": "",
    "bio": ""
}
```

- Response: AuthorSchema

### **/authors/update_author/<int:id>/**

- Methods: PUT, PATCH
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Update author
- Form Data:

```json
{
    "name": "",
    "bio": ""
}
```

- Response: AuthorSchema exclude books

### **/authors/delete_author/<int:id>/**

- Methods: DELETE
- Arguments: None
- Authorization: Bearer token, is_admin
- Description: Delete Author
- Form Data: None
- Response: 
```
    return {'message': f"Author '{author.name}' deleted successfully"}
```
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

```
        WishlistSchema
    else:
        return {'error': f'Book with id {id} already in wishlist'}, 412 
```

### **/wishlist/delete/<int:item_id>/**

- Methods: DELETE
- Arguments: id
- Authorization: Bearer token
- Description: Delete book from current user's wishlist
- Form Data: None
- Response: 
```py
        return {'message': f'Wishlist item {item_id} deleted from wishlist'}
    else:
        return {'error': f'Wishlist item {item_id} not found in wishlist'}, 404
```
----------------------------------------------------------------

## R6 - An ERD for your app
(incl an explanation with ref to models + associations)

## R7 - Detail any third party services that your app will use

No third party services were used in this application.

## R8 - Describe your projects models in terms of the relationships they have with each other
(what your app database ended up with in its code, whatever is in the finished app's models & schemas. discuss relationships at sqlalchemy models. "What reference is created between a Card and a User?" How to represent a foreign key contstraint on column in sqlalch model. how their impletemted with SQLAlchecmy. code snippet)



## R9 - Discuss the database relations to be implemented in your application
(what your database is planned to be, based on the ERD. discuss at database level using those terms. refer to erd. primary/foreign key. databse psql snippet)

## R10 - Describe the way tasks are allocated and tracked in your project
(columns in trello, what does the column mean, when does a ticket move from one column to another)