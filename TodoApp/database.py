from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create database URL
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Create all tables
Base.metadata.create_all(bind=engine)



"""
from sqlalchemy import create_engine, Column, String, Integer, inspect, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create database url
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# create engine connect_args: check same_thread false
engine = create_engine (SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
# Create session (session maker auto commit auto flush false bind engine
SessionLocal = sessionmaker (autocommit=False, 
autoflush=False, bind=engine)
# Create base class for declarative_base model
Base = declarative_base ()

inspector = inspect(engine)

columns = inspector.get_columns('users')
for column in columns:
    print(column['name'])


"""

"""
pip install alembic

# Import necessary libraries
from fastapi import FastAPI  # FastAPI framework for building APIs
from sqlalchemy import create_engine, String, Column, Boolean, Integer  # SQLAlchemy components for database interaction
from sqlalchemy.ext.declarative import declarative_base  # Base class for declarative models
from sqlalchemy.orm import sessionmaker  # Session management for database operations


# Database URL for SQLite (note the correction in the URL)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'  # Connection string for SQLite database

# Create the SQLAlchemy engine with the specified database URL
# 'check_same_thread' is set too False to allow multiple threads to share the same connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Create a new session maker for database interactions
SessionLocal = sessionmaker(autocommit=False, 
autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()  # This will be the base class for our database models

"""


"""
Here's your FastAPI and SQLAlchemy code with added comments to help you understand each part:

```python
# Import necessary libraries
from fastapi import FastAPI  # FastAPI framework for building APIs
from sqlalchemy import create_engine, String, Column, Boolean, Integer  # SQLAlchemy components for database interaction
from sqlalchemy.ext.declarative import declarative_base  # Base class for declarative models
from sqlalchemy.orm import sessionmaker  # Session management for database operations

# Database URL for SQLite (note the correction in the URL)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./zoz.db'  # Connection string for SQLite database

# Create the SQLAlchemy engine with the specified database URL
# 'check_same_thread' is set to False to allow multiple threads to share the same connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Create a new session maker for database interactions
SessionLocal = sessionmaker(autocommit=False, 
autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()  # This will be the base class for our database models
```

### Key Points:
- **Imports**: Each import statement is crucial for the functionality of your application.
- **Database URL**: The connection string is essential for connecting to your SQLite database.
 Ensure it is formatted correctly (`sqlite:///`).
- **Engine**: The engine is responsible for managing the connection to the database.
- **SessionLocal**: This is used to create a new session for each request, allowing for database operations.
- **Base**: This serves as the foundation for your ORM models, which will define the structure of your database tables.

Feel free to ask if you need further clarification on any part!
"""

"""
The error you're encountering indicates that the `users` table in your SQLite database does not have a column named
 `email`. This can occur for several reasons, often related to changes in your model 
 definitions that haven't been reflected in the actual database schema. Here’s how 
 to troubleshoot and resolve this issue:

### Steps to Resolve the Error

1. **Check Your Model Definition**:
   Make sure your model definition includes the `email` column correctly. 
   It looks like your model should resemble something like this:

   ```python
   from sqlalchemy import Column, Integer, String, Boolean
   from database import Base  # Adjust the import based on your structure

   class User(Base):
       __tablename__ = "users"

       id = Column(Integer, primary_key=True, index=True)
       email = Column(String, unique=True)
       username = Column(String, unique=True)
       first_name = Column(String)
       last_name = Column(String)
       hashed_password = Column(String)
       is_active = Column(Boolean, default=True)
       role = Column(String)
   ```

2. **Check Database Schema**:
   If you have made changes to your model (like adding the `email` column) after the initial creation 
   of the database, those changes won't automatically apply to the existing database schema.

   - You can check the current schema of your `users` table in SQLite using a tool like SQLiteBrowser
   or by executing SQL commands in Python:

   ```python
   from sqlalchemy import create_engine, inspect

   engine = create_engine('sqlite:///path_to_your_database.db')  # Adjust the path
   inspector = inspect(engine)

   columns = inspector.get_columns('users')
   for column in columns:
       print(column['name'])
   ```

3. **Migrate the Database**:
   If the `email` column is missing, you need to update your database schema. There are a few ways to do this:

   - **Manual Migration**: If you are okay with losing data, 
   you can delete the existing database 
   file (`todos.db`) and let your application recreate 
   it based on the current model definitions.

   - **Use Alembic for Migrations**: If you want to preserve data and manage schema changes properly,
    consider using Alembic, which is a database migration tool for SQLAlchemy. Here’s a basic setup:

     1. Install Alembic:
        ```bash
        pip install alembic
        ```

     2. Initialize Alembic in your project:
        ```bash
        alembic init alembic
        ```

     3. Configure `alembic.ini` to point to your database.

     4. Create a migration script:
        ```bash
        alembic revision --autogenerate -m "Add email column"
        ```

     5. Apply the migration:
        ```bash
        alembic upgrade head
        ```

4. **Test the Insertion Again**:
   After updating the database schema, try inserting 
   the data again to see if the error persists.

### Conclusion

By following these steps, you should be able to resolve the 
OperationalError` related to the missing `email` column in your SQLite database.
 If you continue to face issues, please provide additional details about your database setup or any
 migration attempts you've made.

"""