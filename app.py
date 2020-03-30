import quizlet
from flask import Flask

app = Flask(__name__)


knowledge_base = {}

@app.route('/ask', defaults={'question': ''})
@app.route('/ask/<question>')
def root(question):
	if not question:
		return "please ask a question"
	quizlet.ask_question(question, knowledge_base)
	found_answer = [key for key in knowledge_base if quizlet.minify(question) in key]
	if found_answer:
		return knowledge_base[found_answer[0]]
	else:
		return knowledge_base

@app.errorhandler(404)
def not_found(e):
	print(e)
	return "oof"

if __name__ == '__main__':
	app.run(port=8005)
