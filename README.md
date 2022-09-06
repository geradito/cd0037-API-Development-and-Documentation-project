# API Development and Documentation Final Project

## Trivia App

Udacity is requiring an application that can increase the bonding experiences for its employees and students. This proejct is a completed web based trivia app that enables users to manage and play the game.

The application supports the following functionalities:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Setting up the Backend

### Install Dependencies

1. **PostgreSQL** - also known as Postgres, is a free and open-source relational database management system

2. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

3. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

4. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: The backend app is hosted at the default, `http://127.0.0.1:5000/`. 
- Authentication: This application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: success True and An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`
-response:
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "sports"
  }, 
  "success": true
}
```
