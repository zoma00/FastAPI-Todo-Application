from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import todos, auth, admin, users

app = FastAPI(app = FastAPI(
    title="Your API Title",
    description="A brief description of your API",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Your Name",
        "url": "http://example.com/contact",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
))

# Create database tables defined in models
models.Base.metadata.create_all(bind=engine)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(admin.router)
app.include_router(users.router)


"""
Here's a comprehensive description for your FastAPI application based on the provided API documentation structure:

---

# FastAPI Todo Application API Documentation

## Overview

This FastAPI application provides a robust API for managing todos and user authentication. 
The application supports CRUD operations (Create, Read, Update, Delete) for todos and user 
management functionalities, including user creation, password reset, and role-based access control. 
The API is designed to be intuitive and easy to use, with automatic documentation generated via FastAPI.

## API Endpoints

### Authentication (`/auth`)

1. **Create User** (`POST /auth/`)
   - **Request Body**: 
     - `username`: Required string (Username)
     - `email`: Required string (Email)
     - `first_name`: Required string (First Name)
     - `last_name`: Required string (Last Name)
     - `password`: Required string (Password)
     - `role`: Required string (Role)
   - **Responses**:
     - `201`: User created successfully.
     - `422`: Validation error.

2. **Reset Password** (`POST /auth/reset-password/`)
   - **Request Body**:
     - `username`: Required string (Username)
     - `new_password`: Required string (New Password)
   - **Responses**:
     - `200`: Password reset successfully.
     - `422`: Validation error.

3. **Login for Access Token** (`POST /auth/token`)
   - **Request Body**:
     - `grant_type`: Optional string (Grant Type)
     - `username`: Required string (Username)
     - `password`: Required string (Password)
     - `scope`: Optional string (Scope)
     - `client_id`: Optional string (Client Id)
     - `client_secret`: Optional string (Client Secret)
   - **Responses**:
     - `200`: Access token returned.
     - `422`: Validation error.

### Todo Management (`/todo`)

1. **Read All Todos** (`GET /todo`)
   - **Authorization**: Requires OAuth2 token.
   - **Responses**:
     - `200`: List of all todos.

2. **Read Todo by ID** (`GET /todo/{todo_id}`)
   - **Path Parameters**:
     - `todo_id`: Required integer (Todo Id)
   - **Authorization**: Requires OAuth2 token.
   - **Responses**:
     - `200`: Todo item details.
     - `422`: Validation error.

3. **Update Todo** (`PUT /todo/{todo_id}`)
   - **Path Parameters**:
     - `todo_id`: Required integer (Todo Id)
   - **Request Body**:
     - `title`: Required string (Title, minimum 3 characters)
     - `description`: Required string (Description, 3 to 100 characters)
     - `priority`: Required integer (Priority, range 0 to 6)
     - `complete`: Required boolean (Complete status)
   - **Authorization**: Requires OAuth2 token.
   - **Responses**:
     - `200`: Updated todo item.
     - `422`: Validation error.

4. **Delete Todo** (`DELETE /todo/{todo_id}`)
   - **Path Parameters**:
     - `todo_id`: Required integer (Todo Id)
   - **Authorization**: Requires OAuth2 token.
   - **Responses**:
     - `204`: Todo deleted successfully.
     - `422`: Validation error.

5. **Create Todo** (`POST /todo`)
   - **Request Body**:
     - `title`: Required string (Title, minimum 3 characters)
     - `description`: Required string (Description, 3 to 100 characters)
     - `priority`: Required integer (Priority, range 0 to 6)
     - `complete`: Required boolean (Complete status)
   - **Authorization**: Requires OAuth2 token.
   - **Responses**:
     - `201`: Todo created successfully.
     - `422`: Validation error.

### Admin Operations (`/admin`)

1. **Read All Todos (Admin)** (`GET /admin/todo`)
   - **Authorization**: Requires OAuth2 token with admin role.
   - **Responses**:
     - `200`: List of all todos.

2. **Delete Todo (Admin)** (`DELETE /admin/todo/{todo_id}`)
   - **Path Parameters**:
     - `todo_id`: Required integer (Todo Id)
   - **Authorization**: Requires OAuth2 token with admin role.
   - **Responses**:
     - `204`: Todo deleted successfully.
     - `422`: Validation error.

### User Management (`/user`)

1. **Get User Details** (`GET /user/`)
   - **Authorization**: Requires OAuth2 token.
   - **Responses**:
     - `200`: User details.

2. **Change Password** (`PUT /user/password`)
   - **Request Body**:
     - `password`: Required string (Current Password)
     - `new_password`: Required string (New Password, minimum 6 characters)
   - **Authorization**: Requires OAuth2 token.
   - **Responses**:
     - `204`: Password changed successfully.
     - `422`: Validation error.

## Download OpenAPI Specification

You can download the OpenAPI specification for this API [here](#).

---

This description provides a clear overview of your API, making it easy for users to understand
its functionality and how to interact with it. You can use this text in your GitHub repository's 
README file or documentation section.
"""