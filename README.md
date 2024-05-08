# Global OAuth2

Single sign-on authentication system built for in-house Staten Island Tech web apps.

- [Installation and Registration](#installation-and-registration)
- [Implementation](#implementation)
  - [Flow](#flow)
  - [Steps](#steps)
- [Routes](#routes)
  - [/users/signup/](#post-userssignup)
  - [/users/verify](#get-usersverify)
  - [/users/get_user](#get-usersget_user)
- [Models](#models)
  - [User](#user)
  - [Permission Manager](#permission-manager)

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

> **Remember to save the client id in frontend .env and both client id and secret in backend .env. The client secret should NEVER go in the frontend.**

Your application is now registered.

## Implementation

### Flow

```mermaid
flowchart TD
A[Resource Client] -- 1: Auth URL --> B(Auth Server)
B -- 2: Authorization Code --> A
A -- 3: Authorization Code --> C[Resource Backend]
C -- 4: Basic Header, Auth Code --> B
B -- 5: Access, Refresh Tokens --> C
C -- 6: Access, Refresh Tokens --> A
```

### Steps

1. Generate a redirect url using the following format. When the user logs in, they will be redirected to the redirect uri

```linux
http://localhost:8000/o/authorize/?response_type=code&client_id={{ CLIENT_ID }}&redirect_uri={{ REDIRECT_URI }}
```

> **The redirect uri must be the one you defined when you registered the application.**

2. Authorization code will be sent back to the redirect uri with url query key: `code`.

3. Send authorization code to backend for use in token post request.

4. Now you will retrieve the access and refresh tokens. First, generate a Basic header. To do this, base64 encode a string in this format, and attach it as a header and construct the body to the post request as shown.

```js
stringToBeEncoded = `${client_id}:${client_secret}`; // javascript syntax

... headers: {
  "Authorization": `Basic ${base64Encode(stringToBeEncoded)}`
}
... body: {
  "grant_type": "authorization_code",
  "code": {...}, // sent from the frontend
  "redirect_uri": {...} // as defined in your application
}

// POST TO:
'http://127.0.0.1:8000/o/token/'
```

5. Access and refresh tokens returned from the post request to `http://127.0.0.1:8000/o/token/`. Sample response:

![sample api response](./sample-response.png)

6. Tokens sent to frontend.

You are now signed in and can query user data.

## Routes

### [POST] /users/signup/

Generates a user model. Returns a link to verify account. Body format:

```js
... body: {
  "email": {...},
  "password": {...},
  "first_name": {...},
  "last_name": {...},
  "graduating_year": {...}
}

// returns:
{
  "email-code": "http://127.0.0.1:8000/users/verify/?code={example}"
}
```

### [GET] /users/verify

URI query `code` required. Link to GET request generated on signup. Sets `user.verified` to `True`.

### [GET] /users/get_user

Send access token as Bearer authorization header.

```js
// returns:
{
  "email": {...},
  "first_name": {...},
  "last_name": {...},
  "uuid": {...}
}
```

## Models

### User

Extension of Django built-in AbstractUser model. Adds fields:

```python
class User(AbstractUser):
  verified = models.BooleanField(default=False)
  uuid = models.CharField(max_length=50, blank=True)
  graduating_year = models.IntegerField(default=2030)
  pass
```

### Permission Manager

Arbitrary model for creating custom Django permission groups.

```python
class PermManager(models.Model):
  class Meta:
    managed = False

    default_permissions = ()

    permissions = (
      ('club_attendance_admin', 'Club Attendance admin'),
      ('bathroom_pass_admin', 'Bathroom Pass admin')
    )
```
