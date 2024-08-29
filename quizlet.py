import requests
from bs4 import BeautifulSoup
import json
import cloudscraper
import re
from thefuzz import fuzz

cse_request_url = 'https://www.googleapis.com/customsearch/v1'
cse_cx = '009651248597238434110:rv56718xitr'
cse_key = 'AIzaSyDO22ReOgKlXN-1xQ3Mg78fiKTi-AB7NEg'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def minify(string): return ''.join(e for e in string if e.isalnum()).lower()


def find_answer_from_quizlet(url, knowledge_base):
    with open("output.txt", "a") as myfile:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, headers=headers)
        myfile.write(str(response.content))
        myfile.write("\n\n\n")
        
        if response.status_code == 200:
            page = BeautifulSoup(response.content, 'html.parser')
            terms = []
            for e in page.select('.SetPageTerms-term'):
                term_pair = e.select('.TermText')
                left = re.sub('<[^>]*>', '', str(term_pair[0].decode_contents())) if len(term_pair) > 0 else "error"
                right = re.sub('<[^>]*>', '', str(term_pair[1].decode_contents())) if len(term_pair) > 1 else "error"
                terms.append((left, right))
        
            return terms

def get_search_results(question):
    querystring = {'cx': cse_cx, 'key': cse_key, 'q': question}
    results = json.loads(requests.request(
        'GET', cse_request_url, params=querystring).text)
    return [item['link'] for item in results['items']]


def ask_question(question, knowledge_base={}):
    found_answers = []
    urls = []
    try:
        urls = get_search_results(question)
    except:
        return -1
    
    terms = []
    for url in urls:
        found_answers = [key for key in knowledge_base if minify(
            question) in minify(key)]
        if not found_answers:
            print("FINDING ANSWERS FROM " + url)
            if term:= find_answer_from_quizlet(url, knowledge_base):
                terms += term

    choices = []
    for (left, right) in terms:
        left_ratio  = fuzz.ratio(question, left)
        right_ratio = fuzz.ratio(question, right)
        if (left_ratio > right_ratio):
            ratio = left_ratio
            opposite_term = right
        else:
            ratio = right_ratio
            opposite_term = left

        choices.append((ratio, opposite_term))

    ranked_choices = sorted(choices, key=lambda x: x[0], reverse=True)
    print(question)
    print("----------------------\nbest choices:")
    for (ratio, term) in ranked_choices[:6]:
        print(f"- {ratio:>4} | {term}")

question = "michaelangelos laurentian library is part of the complex that includes"
ask_question(question)
       