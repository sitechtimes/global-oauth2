# Global OAuth2

Single sign-on authentication system built for in-house Staten Island Tech web apps.

## Installation and Registration

Clone the repository and install poetry.

```linux
pip install poetry
```

Install dependencies and set up server.

```linux
poetry install
```

```linux
python manage.py makemigrations
```

```linux
python manage.py migrate
```

Create a superuser.

```linux
python manage.py createsuperuser
```

Launch the server.

```linux
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/o/applications` to register your application.

![application registration form](./register-application.png)

> **Remember to save the client id and client secret.**

Your application is now registered.

## Implementation

### Flow

```mermaid

```
