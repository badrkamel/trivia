import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
	page = request.args.get('page', 1, type=int)
	start =  (page - 1) * QUESTIONS_PER_PAGE
	end = start + QUESTIONS_PER_PAGE

	questions = [question.format() for question in selection]
	current_questions = questions[start:end]

	return current_questions

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)

	'''
	@Done: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
	'''

	'''
	@Done: Use the after_request decorator to set Access-Control-Allow
	'''

	CORS(app, resources={'/': {'origins': '*'}})

	# CORS Headers 
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
		return response


	'''
	@Done: 
	Create an endpoint to handle GET requests 
	for all available categories.
	'''

	@app.route('/categories', methods=['GET'])
	def categories():
		categories = Category.query.all()
		category_dict = {category.id: category.type for category in categories}

		return jsonify({
				"categories": category_dict
			})


	'''
	@Done: 
	Create an endpoint to handle GET requests for questions, 
	including pagination (every 10 questions). 
	This endpoint should return a list of questions, 
	number of total questions, current category, categories. 

	TEST: At this point, when you start the application
	you should see questions and categories generated,
	ten questions per page and pagination at the bottom of the screen for three pages.
	Clicking on the page numbers should update the questions. 
	'''

	@app.route('/questions', methods=['GET'])	
	def retrieve_questions():

		selection = Question.query.order_by(Question.id).all()
		current_questions = paginate_questions(request, selection)

		categories = Category.query.all()
		category_dict = {category.id: category.type for category in categories}
		
		return jsonify({
				"success":True,
				"questions":current_questions,
				"total_questions":len(selection),
				"categories":category_dict
			})


	'''
	@Done: 
	Create an endpoint to DELETE question using a question ID. 

	TEST: When you click the trash icon next to a question, the question will be removed.
	This removal will persist in the database and when you refresh the page. 
	'''
	@app.route('/questions/<int:question_id>', methods=['DELETE'])
	def delete_question(question_id):
		question = Question.query.get_or_404(question_id)
		question.delete()

		return jsonify({
				"success": True,
				"deleted": question_id,
				"total_questions": len(Question.query.all())
			})

	'''
	@Done: 
	Create an endpoint to POST a new question, 
	which will require the question and answer text, 
	category, and difficulty score.

	TEST: When you submit a question on the "Add" tab, 
	the form will clear and the question will appear at the end of the last page
	of the questions list in the "List" tab.  
	'''

	'''
	@Done: 
	Create a POST endpoint to get questions based on a search term. 
	It should return any questions for whom the search term 
	is a substring of the question. 

	TEST: Search by any phrase. The questions list will update to include 
	only question that include that string within their question. 
	Try using the word "title" to start. 
	'''

	@app.route('/questions', methods=['POST'])
	def new_question():
		try:
			search_term = request.get_json()['searchTerm']
			
			if search_term:
				result = Question.query.order_by(Question.id).filter(
					Question.question.ilike(f'%{search_term}%')
				)

				return jsonify({
					"success": True,
					"questions": [question.format() for question in result],
					"total_questions": len(Question.query.all())
				})

			else:
				question = request.get_json()["question"]
				answer = request.get_json()["answer"]
				category = request.get_json()["category"]
				difficulty = request.get_json()["difficulty"]

				print(question, answer, category, difficulty)
				new_question = Question(
					question=question, 
					answer=answer,
					category=category,
					difficulty=difficulty
				)
				new_question.insert()

				return jsonify({
						"success": True,
						"question": new_question.id,
						"total_questions": len(Question.query.all())
					})
		except Exception as e:
			raise e



	'''
	@Done: 
	Create a GET endpoint to get questions based on category. 

	TEST: In the "List" tab / main screen, clicking on one of the 
	categories in the left column will cause only questions of that 
	category to be shown. 
	'''
	@app.route('/categories/<int:category_id>/questions', methods=['GET'])
	def retrieve_questions_by_category(category_id):
		
		questions = Question.query.order_by(Question.id).filter(Question.category==category_id).all()
		current_questions = paginate_questions(request, selection)

		return jsonify({
			"success": True,
			"questions": current_questions
		})


	'''
	@Done: 
	Create a POST endpoint to get questions to play the quiz. 
	This endpoint should take category and previous question parameters 
	and return a random questions within the given category, 
	if provided, and that is not one of the previous questions. 

	TEST: In the "Play" tab, after a user selects "All" or a category,
	one question at a time is displayed, the user is allowed to answer
	and shown whether they were correct or not. 
	'''
	@app.route('/quizzes', methods=['POST'])
	def play_quiz():
		try:
			prev_questions = request.get_json()["previous_questions"]
			category = request.get_json()["quiz_category"]
			category_id = category['id']

			print(prev_questions, category)

			if prev_questions and category:

				# load questions all questions if "ALL" is selected
				if (category_id == 0):
					selection = Question.query.order_by(func.random())

				# load questions for given category
				else:
					selection = Question.query.filter_by(category=category_id).order_by(func.random())

				if selection:
					# get random question
					# question = questions[random.randrange(0, len(questions))]

					question = selection.filter(Question.id.notin_(prev_questions)).first()

					return jsonify({
						"success": True,
						"question": question.format()
					})

				return jsonify({
					"success": True,
				})
				
			abort(400)

		except:
			abort(400)


	'''
	@Done: 
	Create error handlers for all expected errors 
	including 404 and 422. 
	'''
	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({"success": False,"error": 400,"message": "bad request"}), 400

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({"success": False,"message": "not found","error": 404}), 404

	@app.errorhandler(405)
	def not_allowed(error):
		return jsonify({"success": False,"message": "not allowed","error": 405}), 405

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({"success": False,"message": "unprocessable","error": 422}), 422

	return app