import quizlet
from flask import Flask, jsonify
from secrets import token_urlsafe

app = Flask(__name__)


knowledge_bases = dict()


@app.route('/ask', defaults={'question': '', 'kb_token': ''})
@app.route('/ask/<question>/', defaults={'kb_token': ''})
@app.route('/ask/<question>/<kb_token>/')
def root(question, kb_token):
    if not question:  # if the user doesn't ask a question
        return "please ask a question", 400
    if not kb_token:  # if the user doesn't provide a knowledge base token, create a new kn and give them a token
        kb_token = token_urlsafe(24)
        knowledge_bases[kb_token] = {}
    if not kb_token in knowledge_bases:
        return "Could not find the knowledge base " + str(kb_token), 404
    # populate their knowledge base with answers
    quizlet.ask_question(question, knowledge_bases[kb_token])
    found_answer = [key for key in knowledge_bases[kb_token] if quizlet.minify(
        question) in key]  # Get all the questions containing their question

    result = None
    if found_answer:
        result = knowledge_bases[kb_token][found_answer[0]]
    else:
        result = knowledge_bases[kb_token]
    return jsonify(kb_token=kb_token, result=result)


@app.errorhandler(404)
def not_found(e):
    print(e)
    return "oof"


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(port=8005)
