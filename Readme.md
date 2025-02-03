# Django Project

This is a Django project that includes user authentication with JWT tokens, profile management, and API documentation using Swagger.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)

## Setup

1. **Clone the repository**:

```sh
   git clone https://github.com/milkaxq/task
   cd task
```

2. **Create a virtual environment (optional but recommended):**:
```sh
    python -m venv venv
    source venv/bin/activate 
```
3. **Install the dependencies:**
```sh
    pip install -r requirements.txt
```

4. **Apply the migrations:**
``` sh
    python manage.py migrate
```

5. **Create a superuser:**
```sh
    python manage.py createsuperuser
```

6. **Run the development server:**
```sh 
    python manage.py runserver
```

## Running Tests

To run the tests, use the following command:

```sh
    python manage.py test
```

## API Endpoints

### Authentication
```python
Register: POST /api/register/

Request Body: { "email": "user@example.com", "password": "password" }
Response: { "id": 1, "email": "user@example.com", "username": "username" }
Login: POST /api/login/

Request Body: { "email": "user@example.com", "password": "password" }
Response: { "access_token": "jwt_token", "refresh_token": "uuid_token" }
Refresh Token: POST /api/refresh_token/

Request Body: { "refresh_token": "uuid_token" }
Response: { "access_token": "new_jwt_token", "refresh_token": "new_uuid_token" }
Logout: POST /api/logout/

Request Body: { "refresh_token": "uuid_token" }
Response: { "success": "User logged out." }
```
### Profile
```python
Get Profile: GET /api/me/

Headers: Authorization: Bearer <jwt_token>
Response: { "email": "user@example.com", "username": "username" }
Update Profile: PUT /api/me/

Headers: Authorization: Bearer <jwt_token>
Request Body: { "username": "new_username" }
Response: { "id": 1, "email": "user@example.com", "username": "new_username" }
```

### Api Documentation
API Documentation
The API documentation is available at the following endpoints:

Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/