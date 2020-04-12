import quizlet

from flask import Flask, jsonify, request
from flask_cors import CORS
from secrets import token_urlsafe

from datetime import datetime, timedelta
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.url_map.strict_slashes = False
# We need this cause 400/500 errors don't send cors =(
CORS(app, resources={r"/*": {"origins": "*"}})

sched = BackgroundScheduler(daemon=True)
sched.start()

knowledge_bases = dict()


def purge_token(token):
	print('clearing job ' + token)
	knowledge_bases.pop(token)
	if sched.get_job(token):
		sched.remove_job(token)


@app.route('/ask')
@app.route('/ask/')
@app.route('/ask/<question>/')
@app.route('/ask/<question>/<kb_token>/')
def ask(question=None, kb_token=None):
	expiration = 30  # num minutes until this kb expires

	# 400 error handling
	if not question:  # if the user doesn't ask a question
		return "please ask a question", 400

	if not kb_token:  # if the user doesn't provide a knowledge base token, create a new one and give it to them
		kb_token = token_urlsafe(24)
		knowledge_bases[kb_token] = {}
	else:
		# They're asking, so reset the expiration, cause we want to keep their kb
		if sched.get_job(kb_token):
			sched.remove_job(kb_token)
	if not kb_token in knowledge_bases:
		return "Could not find the knowledge base " + str(kb_token), 404

	user_expiration = request.args.get('expiration')
	if user_expiration:
		if user_expiration < 30 and user_expiration > 0:
			expiration = user_expiration
		else:
			return 'invalid expiration. There is a maximum of 30 minutes', 400

	# populate their knowledge base with answers
	found_answer = quizlet.ask_question(question, knowledge_bases[kb_token])

	result = None
	status = 'not_found'
	if found_answer == -1:
		return "There was an error Googling your question, perhaps the maximum daily limit of 100 requests has been reached =(", 400
	if found_answer:
		result = found_answer
		status = 'found'
	else:
		result = knowledge_bases[kb_token]
	# schedule the kb to be deleted
	sched.add_job(lambda: purge_token(kb_token), 'date',
				  run_date=datetime.now() + timedelta(minutes=expiration), id=kb_token)
	return jsonify(kb_token=kb_token, status=status, result=result, expiration=sched.get_job(kb_token).next_run_time)


@app.route('/kb')
@app.route('/kb/')
@app.route('/kb/<token>/')
def full_kb(token=None):
	if token == None:
		return 'You must provide a token', 400
	if token in knowledge_bases:
		return jsonify(knowledge_bases[token])
	else:
		return 'token not found, perhaps it expired', 400


@app.route('/')
def root():
	return 'Welcome to quizlet query API!\n Try the /ask/your+question+here endpoint!'


@app.errorhandler(404)
def not_found(e):
	print(e)
	return "oof"


if __name__ == '__main__':
	app.run(port=8005)
