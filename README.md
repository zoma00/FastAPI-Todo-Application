# FastAPI-Todo-Application
A modern and robust API for managing todos, built with FastAPI. This application features user authentication, role-based access control, and comprehensive CRUD operations for todos. It leverages automatic documentation generation for seamless integration and testing. 



# FastAPI Todo Application API Documentation

## Overview

This FastAPI application provides a robust API for managing todos and user authentication. The application supports CRUD operations (Create, Read, Update, Delete) for todos and user management functionalities, including user creation, password reset, and role-based access control. The API is designed to be intuitive and easy to use, with automatic documentation generated via FastAPI.

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

