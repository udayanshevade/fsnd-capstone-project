# FSND Capstone Project - Casting Agency

The capstone project for the Udacity Fullstack NanoDegree:

Covers all the basic ideas from the ND, including:

- RESTful API design
- Using ORM models
- Decorators
- Error handling
- Authorization/Authentication
- Unit Testing
- Deployment

The API can be found live [here](https://fsnd-capstone-project-api.onrender.com/healthcheck).

## Behavior

The API handles the basic functionality for a casting agency.

It works with two main resources at the moment:

1. actors
2. movies

There are three main user roles:

1. Assistant: can only read data
2. Director: has limited update permissions
3. Producer: has full access to create, update or destroy any record in the database

## Instructions

- Set up a virtual environment: `python3 -m venv env && source env/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Create a local database: `createdb castingagency` (with the default user/password)
- Ensure the required env vars are exported or defined in a `.env` file at the root directory of the project
- Run the development server: `flask run`
- Access the local API at: http://127.0.0.1:5000

## Testing

- Create a test database `createdb castingagencytest`
- Ensure test env vars are exported or defined in a `.env.test` file at the root directory of the project
- Run the test suite: `python3 test_app.py`

## Postman collection

Use the included Postman collection to preview API requests on all endpoints.

## Deployment/hosting

The API is hosted using Render. See their full instructions on hosting a Flask app [here](https://render.com/docs/deploy-flask).

Create a PostgreSQL DB instance on Render. Its Internal Database URL will be used by our hosted Flask app for the live version of the API.

The deployment on Render is connected to this GitHub repository. Latest changes pushed to the `main` branch will be picked up automatically and deployed.

## Authentication/Authorization

The project uses Auth0 to handle JWTs for authentication and authorization.

To get API tokens associated with the app:

1. Go to the following URL (replacing the {{variables}} with actual values):
   > https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
2. Login with the credentials for the role you wish to test, e.g. with the email and password for the "assistant" account
3. You will be redirected to a url which contains the JWT for that user. Copy that token for use with the API.

The different permissions for different levels of access to the API are:

- `view:actors`
- `view:movies`
- `delete:actors`
- `post:actors`
- `update:actors`
- `update:movies`
- `post:movies`
- `delete:movies`

## Technologies:

- [Python 3.11.4](https://www.python.org/downloads/release/python-3114/)
- [Flask 2.3.2](https://flask.palletsprojects.com/en/2.3.x/)
- [PostgreSQL 14](https://www.postgresql.org/download/macosx/)
- [SQLAlchemy 3.0.5](https://www.sqlalchemy.org/)
- [Auth0](https://auth0.com/)
- [Render](https://render.com/)
- [Postman](https://www.postman.com/)
