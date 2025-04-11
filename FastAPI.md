Overview : FastAPI - Python Web framework
modern RESTfuls APIS - Data validation, serialization, Exception handling, Status codes, Swagger config, python request objects.

Request:
Http Request Methods -CRUD Operations
POST - Create
GET - Read
PUT - Update
DELETE - delete

New way to run fastapi - fastapi run main.py (can use dev mode and prod mode with this)

Path parameters:
Ex: @app.get("/books/{book_id}")
    async def read_books(book_id: str): #here the type string helps with typesafety
        return xyz
request URL: https://111/books/1

Query parameters: (query comes after a ? which are name value_pairs)
Ex: @app.get("/books/")
    async def read_books(book_id: str): 
        return xyz
request URL: https://111/books/?book_id=1

Post Request: requests have a body
Ex: "app.post("/books/create/book")
    async def create_book(new_book = Body()):
        return xyz

Put has a body similar to post, used for update.

Using pydantic for data validation:
- create a response class from basemodel
class BookRequest(basemodel):
    #validations
Ex: "app.post("/books/create/book")
    async def create_book(new_book : BookRequest()):
        return xyz

in pydantic validation class, we can add individual field validations along with overall strucutre and datatypes. Ex: min, max length, gt, lt, optional etc.
WE can create a model config in the response class, which has desceiptions of field.

We can add extra validation to path parameters too, by importing Path
Ex: @app.get("/books/{book_id}")
    async def read_books(book_id: int = Path(gt=0)): #here the type string helps with typesafety
        return xyz
request URL: https://111/books/1

We can add extra validation to Query parameters too, by importing Query
Ex: @app.get("/books/")
    async def read_books(book_id: int = Query(gt=0, lt= 999)): 
        return xyz
request URL: https://111/books/?book_id=1

Http Status Code: 1xx - Information response
                  2xx - Success
                  3xx - Redirection
                  4xx - client errors
                  5xx - server errors

Example exception: raise HTTPEXception(status_code=404, detial=Item Not Found)

Explicit status code: 
From starlette import status

Working with Database:
1. engine = create_engine(db_url)
2. sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
3. db = sessionlocal()
   try: 
        yield db 
   finally:
        db.close

Dependency Injection:
db_dependency = Annotated[Session, Depends(get_db_session)]
Ex: @app.get("/books/)
    async def read_books(book_id: str,db: db_dependency):
        return xyz

JWT Authorization: header.payload.signature
header: algorithm for signing, type of toke. Then these two parts are encoded using base64
payload : information like subject, name, role, id etc