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
 

API Reference

Geting started

Base URL: At present this app can only be run locally and is not hosted as a base URL. 
The backend app is hosted at the default, http://127.0.0.1:5000/
which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require Authentication or API keys.

Error Handling

Errors are returned as JSON objects in the following format:
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return three errors types when requests fail:
    404 : Resource Not found.
    422 : Not processable.

Endpoints    

GET /categories
General:
      This endpoint is resposable for handling GET requests for categories path.
      return  : all available categories and a success message.
Sample: curl http://127.0.0.1:5000/categories
{
    "categories": {
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "success":true
}

GET /questions
General:
        This endpoint is responsable for handling GET requests for questions, 
        including pagination (every 10 questions). 
        return : This endpoint should return a list of paginated questions (page 1 as default), 
        number of total questions, current category, categories.
Sample : curl http://127.0.0.1:5000/questions?page=7
{
    "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "current_category":"sport",
    "questions":[{
        "answer":"Agra",
        "category":"3",
        "difficulty":2,
        "id":15,
        "question":"The Taj Mahal is located in which Indian city?"
    },{
        "answer":"Escher",
        "category":"2",
        "difficulty":1,
        "id":16,
        "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },{
        "answer":"Mona Lisa",
        "category":"2",
        "difficulty":3,
        "id":17,
        "question":"La Giaconda is better known as what?"
    },{
        "answer":"One",
        "category":"2",
        "difficulty":4,
        "id":18,
        "question":"How many paintings did Van Gogh sell in his lifetime?"
    },{
        "answer":"Blood",
        "category":"1",
        "difficulty":4,
        "id":22,
        "question":"Hematology is a branch of medicine involving the study of what?"
    },{
        "answer":"Scarab",
        "category":"4",
        "difficulty":4,
        "id":23,
        "question":"Which dung beetle was worshipped by the ancient Egyptians?"
    }],
    "success":true,
    "total_questions":16
}

GET /categories/<category_id>/questions
General: 
        This endpoint is responsable for getting the questions related to a specific category, 
        return : This endpoint should return a list of questions, 
        number of total questions, current category.
Sample: curl http://127.0.0.1:5000/categories/1/questions
{
    "currentCategory":"Science",
    "questions": [{
        "answer":"Blood",
        "category":"1",
        "difficulty":4,
        "id":22,
        "question":"Hematology is a branch of medicine involving the study of what?"
    }],
    "success":true,
    "total_questions":1
}

DELETE /questions/<question_id>
General: 
    Endpoint to DELETE question using a question ID. 
    return : json object includes the deleted question id 

Sample: curl -X DELETE   http://127.0.0.1:5000//questions/4
{
    "deleted":"4",
    "success":true
}

POST /questions
General: 
      Endpoint to POST a new question OR search for a specific question.
      return : This endpoint should return a list of questions, 
      number of total questions, current category.

Sample for add new question : curl -X POST -H "Content-Type:application/json"  http://127.0.0.1:5000/questions -d "{\"question\":\"who is the best player in the world?\", \"answer\":\"Abo Trika\", \"category\":\"6\",\"difficulty\":\"1\"}"

{
    "success":true
}

Sample for search for questions : curl -X POST -H "Content-Type:application/json"  http://127.0.0.1:5000/questions -d "{\"searchTerm\":\"Tom Hanks\"}"

{
    "questions":[{
        "answer":"Apollo 13",
        "category":"5",
        "difficulty":4,
        "id":2,
        "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }],
    "success":true,
    "total_questions":1
}

POST  /quizzes
General: 
      This endpoint to get questions to play the quiz
      the endpoint should take category and previous question parameters from the request body.
      return : if there is a valid question it will return the formated question with success message
                and if no valid questions it will return just the messege with no questions 
Sample: curl -X POST -H "Content-Type:application/json"  http://127.0.0.1:5000/quizzes -d "{\"previous_questions\":\"[4, 5, 3]\", \"quiz_category\":\"{'5': 'Entertainment'}\"}"

{
    "question":{
        "answer":"Apollo 13",
        "category":"5",
        "difficulty":4,
        "id":2,
        "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    "success":true,
}





## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```