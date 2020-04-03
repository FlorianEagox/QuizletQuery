import quizlet
from flask import Flask, jsonify
from secrets import token_urlsafe

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['CORS_HEADERS'] = 'Content-Type'

knowledge_bases = dict()


@app.route('/ask')
@app.route('/ask/')
@app.route('/ask/<question>/')
@app.route('/ask/<question>/<kb_token>/')
def ask(question=None, kb_token=None):
    # 400 error handling
    if not question:  # if the user doesn't ask a question
        return "please ask a question", 400
    if not kb_token:  # if the user doesn't provide a knowledge base token, create a new kn and give them a token
        kb_token = token_urlsafe(24)
        knowledge_bases[kb_token] = {}
    if not kb_token in knowledge_bases:
        return "Could not find the knowledge base " + str(kb_token), 404

    # populate their knowledge base with answers
    found_answer = quizlet.ask_question(question, knowledge_bases[kb_token])

    result = None
    status = 'not_found'

    if found_answer:
        result = found_answer
        status = 'found'
    else:
        result = knowledge_bases[kb_token]
    return jsonify(kb_token=kb_token, status=status, result=result)


@app.route('/')
def root():
    return 'Welcome to quizlet query API!\n Try the /ask/your+question+here endpoint!'


@app.errorhandler(404)
def not_found(e):
    print(e)
    return "oof"


if __name__ == '__main__':
    app.run(port=8005)
