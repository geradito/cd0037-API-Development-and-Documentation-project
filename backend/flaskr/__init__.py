import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books

def row2dict(row):
    d = {}
    for column in row:
        d[column.id] = column.type

    return d

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        
        if len(selection) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": row2dict(selection)
            }
        )    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
   
    @app.route("/questions")
    def retrieve_questions():
        """
        The reason for returning current category was not very clear to me,
        so i assumed i have to sort questions by category and current category will be for first question
        """
        
        selection = Question.query.order_by(Question.category).all()
        current_questions = paginate_questions(request, selection)

        query_category = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in query_category]
        
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "categories": row2dict(query_category),
                "current_category": categories[0]['type'],
                "total_questions": len(Question.query.all()),
            }
        )
    
   
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question_or_search_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        search = body.get("searchTerm", None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                    }
                )
            else:
                if new_question is None or new_answer is None or new_difficulty is None or new_category is None:
                    abort(422)
                    

                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                    }
                )

        except:
            abort(422)    
    """
    @TODO: 
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_category(category_id):
        selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        category = Category.query.filter(Category.id == category_id).one_or_none()
        
        if len(current_questions) == 0:
            abort(404) 

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "currentCategory": category.format()['type'],
                "totalQuestions": len(selection),
            }
        )
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def retrieve_next_question_in_quize():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)

        if quiz_category['id'] == 0:
            current_question = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        else:
            current_question = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        
        if current_question is None:
            return jsonify(
                {
                    "success": True,
                    "question": None            
                }
            )

        return jsonify(
            {
                "success": True,
                "question": current_question.format()            
            }
        )

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    return app

