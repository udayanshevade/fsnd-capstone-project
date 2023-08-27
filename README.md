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

### Endpoints

#### GET '/actors'

Returns a list of all actors in the database.
Sample curl:
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/actors
Sample response output:

```
{
   "actors": [
      {
         "id": 1,
         "name": "Morgan Freeman",
         "birthdate": "Tue, 01 Jun 1937 00:00:00 GMT"
      },
      {
         "id": 2,
         "name": "Nicolas Cage",
         "birthdate": "Tue, 07 Jan 1964 00:00:00 GMT"
      }
   ],
   "success": true
}
```

#### GET '/actors/<actor_id>'

Returns a single actor by the specified id.
Sample curl:
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/actors/1
Sample response output:

```
{
   "actor": {
      "id": 1,
      "name": "Morgan Freeman",
      "birthdate": "Tue, 01 Jun 1937 00:00:00 GMT"
   },
   "success": true
}
```

#### PATCH '/actors/<actor_id>'

Updates the data for a single actor by the specified id.
Sample curl:
curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Nicolas Cage", "birthdate": "Sat, 01 Jan 2000 00:00:00 GMT"}'

```
{
   "actor": {
      "id": 1,
      "name": "Updated Actor",
      "birthdate": "01-01-2000"
   },
   "success": true
}
```

#### POST '/actors'

Creates a new entry for an actor.
Sample curl:
curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Created Actor", "birthdate": "01-01-2000"}'

```
{
   "actor": {
      "id": 3,
      "name": "Created Actor",
      "birthdate": "Tue, 01 Jan 2000 00:00:00 GMT"
   },
   "success": true
}
```

#### DELETE '/actors/<actor_id>'

Creates a new entry for an actor.
Sample curl:
curl http://127.0.0.1:5000/actors/3 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```
{
   "removed": 3,
   "success": true
}
```

#### GET '/movies'

Returns a list of all movies in the database.
Sample curl:
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/movies
Sample response output:

```
{
   "movies": [
      {
         "id": 1,
         "title": "Driving Miss Daisy",
         "description": "An old Jewish woman and her African-American chauffeur in the American South have a relationship that grows and improves over the years."
      },
      {
         "id": 2,
         "title": "Con Air",
         "description": "Newly-paroled ex-con and former U.S. Ranger Cameron Poe finds himself trapped in a prisoner-transport plane when the passengers seize control."
      },
      {
         "id": 3,
         "title": "Dawn of the Dead",
         "description": "During an escalating zombie epidemic, two Philadelphia SWAT team members, a traffic reporter and his TV executive girlfriend seek refuge in a secluded shopping mall."
      }
   ],
   "success": true
}
```

#### GET '/movies/<movie_id>'

Returns a single movie by the specified id.
Sample curl:
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://127.0.0.1:5000/movies/1
Sample response output:

```
{
   "movie": {
      "id": 1,
      "title": "Driving Miss Daisy",
      "description": "An old Jewish woman and her African-American chauffeur in the American South have a relationship that grows and improves over the years."
   },
   "success": true
}
```

#### PATCH '/movies/<movie_id>'

Updates the data for a single movie by the specified id.
Sample curl:
curl http://127.0.0.1:5000/movies/3 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"Dawn of the Dead", "description": "A nurse, a policeman, a young married couple, a salesman and other survivors of a worldwide plague that is producing aggressive, flesh-eating zombies, take refuge in a mega Midwestern shopping mall."}'

```
{
   "movie": {
      "id": 3,
      "title": "Dawn of the Dead",
      "description": "A nurse, a policeman, a young married couple, a salesman and other survivors of a worldwide plague that is producing aggressive, flesh-eating zombies, take refuge in a mega Midwestern shopping mall."
   },
   "success": true
}
```

#### POST '/movies'

Creates a new entry for an movie.
Sample curl:
curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"The Room", "description": "In San Francisco, an amiable banker\'s seemingly perfect life is turned upside down when his deceitful fiancée embarks on an affair with his best friend."}'

```
{
   "movie": {
      "id": 4,
      "title": "The Room",
      "description": "In San Francisco, an amiable banker\'s seemingly perfect life is turned upside down when his deceitful fiancée embarks on an affair with his best friend."
   },
   "success": true
}
```

#### DELETE '/movies/<movie_id>'

Creates a new entry for an movies.
Sample curl:
curl http://127.0.0.ovies1:5000/movies/4 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"

```
{
   "removed": 4,
   "success": true
}
```

---

There are three main user roles:

1. Assistant: can only read data
2. Director: has limited update permissions
3. Producer: has full access to create, update or destroy any record in the database

## Local Setup Instructions

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

## Deployment and hosting instructions

The API is hosted with Render. See their full instructions on deploying a Flask app [here](https://render.com/docs/deploy-flask).

- Create a Web Service application on Render.
- Specify the `build` and `start` commands, and [include all necessary environment variables](https://render.com/docs/configure-environment-variables).
- Connect the app to a GitHub repository so latest changes can be picked up and automatically deployed.
- [Create a separate PostgreSQL DB instance](https://render.com/docs/databases#creating-a-database) on Render as well.
- Reference its Internal Database Url in the Web Service app via environment variables, so the server can connect to the production database instance.

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
