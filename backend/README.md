# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Error Handling

<p>Errors are returned as JSON objects in the following format:</p>

```json
{
    "success": false,
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail:

 * 400: Bad Request
 * 404: Resource Not Found
 * 405: Method Not Allowed
 * 422: Not Processable
 
### Endpoints

#### GET /categories
- General:
    - Returns a list of category objects, id value, and category type
- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }
  ]
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, and total questions value.
  - Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"test", "answer":"test", "category":2, "difficulty":3}'`
```
{
  "success": true,
  "question": 24,
  "total_value": 50
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/questions/3```
```
{
  "deleted": 3,
  "success": true,
  "total_questions": 49
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```