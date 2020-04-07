import requests
from bs4 import BeautifulSoup
import json


cse_request_url = 'https://www.googleapis.com/customsearch/v1/'
cse_cx = '009651248597238434110:rv56718xitr'
cse_key = 'AIzaSyDO22ReOgKlXN-1xQ3Mg78fiKTi-AB7NEg'
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def minify(string): return ''.join(e for e in string if e.isalnum()).lower()


def find_answer_from_quizlet(url, knowledge_base):
	page = BeautifulSoup(requests.get(
		url, headers=headers).content, 'html.parser')
	for el in [el.select('*') for el in page.select('.SetPageTerm-content')]:
		knowledge_base[el[0].get_text()] = el[-1].get_text()


def get_search_results(question):
	querystring = {'cx': cse_cx, 'key': cse_key, 'q': question}
	results = json.loads(requests.request(
		'GET', cse_request_url, params=querystring).text)
	return [item['link'] for item in results['items']]


def ask_question(question, knowledge_base={}):
	found_answers = []
	for url in get_search_results(question):
		found_answers = [key for key in knowledge_base if minify(
			question) in minify(key)]
		if not found_answers:
			find_answer_from_quizlet(url, knowledge_base)
	if found_answers:
		return [{'question': found_question, 'answer': knowledge_base[found_question]} for found_question in found_answers]
	return found_answers
