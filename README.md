
# QuizletQuery
A minimal API for searching Quizlet.
## TL;DR
This API searches google and webscrapes Quizlet to sort of answer questions. It works okay but has some limitations. Below you'll learn how to use the API, but just use the demo if you want to use the program.
## Demo
You can try a live, running version of the program at 
> **https://sethpainter.com/quizletquery**
## About
This is a simple python, flask application that attempts to answer questions by using Quizlet flashcards. A wealth of academic content exists as structured data in the form of Quizlet flashcard sets, but they are not searchable or parsable. This tool aims to make this data easily searchable.
## How it works
When the backend receives a request containing a question, it sends the question to a Google Custom Search engine (CSE) and retrieves to top ten relevant links (Anything buried further down likely does not contain your question, but rather irrelevant information). This CSE is configured to return only Quizlet links.

The server then scrapes the returned pages and goes through each question. After scraping a page, if the question is found, the server will stop and return the flashcard containing it (And any additional flashcards containing your question) along with the Quizlet URL from which it came. In addition to searching for your question, the server also stores every other flashcard in the set as it is likely relevant to your initial query and be used to return results much faster for subsequent queries. These results are stored in an object called a knowledge base. If the question is not found in the current page, then it goes through each Quizlet page until it is. If by the end of all ten Google results, your question is not found in any flashcards, it is possible and often likely that the desired information was found, but worded differently, and so, the server will return the knowledge base so that the frontend can offer the user the ability to manually search through it for relevant flashcards.

All successful results will return a token for the knowledge base that the user can use in subsequent queries. If the user does not use the knowledge base within 30 minutes (or a shorter specified expiration) the knowledge base will be deleted from the server.

## API Usage
The server is run like any flask / gunicorn application and currently running at
**Base URL:**
> https://api.sethpainter.com/quizletquery/
### Ask
> `/ask/<your+question+here>/[knowledge_base_token][?expiration=20]`
#### Request
The first parameter is your question to search, you can use standard URL encoding.
The second is an optional knowledge base token which you receive after making your first query.
The optional `expiration` is how many minutes you'd like your knowledge base to persist without being touched, if unspecified, it is set to 30 minutes.
#### Response
For the query of "what is the radius of the earth"
The program should return something like

```
{
  "expiration": "Sun, 12 Apr 2020 08:59:10 GMT",
  "kb_token": "vQpc7l9YqRKliCv3-rOAl-yNwEc1Zk_b",
  "result": [
    {
      "answer": "6,371km or 3,959mi",
      "question": "What is the radius of the earth?",
      "url_id": "155205723"
    }
  ],
  "status": "found"
}
```
* The expiration is obviously when the program will delete the knowledge base if it isn't accessed again.
* The `kb_token` is a URL-safe token that the user should use in the URL with `[knowledge_base_token]` for subsequent relevant queries.
* The `status` indicates whether or not the server found you question in the flashcards it found.
If the question was not found, it will return `not_found`, but it will also return the full knowledge base.
* The `result` object is where all the found content will be returned.
It is an array of flashcards containing the question, answer, and URL from which it came.

The `URL` field can be used in a link like:
> https://Quizlet.com/url

Sometimes the webscraping won't find the answer to some of the questions, so the answer field will be blank.
If during the search, your question isn't found in any flashcards, the status will be changed to `not_found`, and the program will return the full knowledge base.
#### Errors
* If no question is specified, the server returns 400
* If the `expiration` is not between 0 and 30 minutes, the server returns 400
* If the server cannot find the knowledge base found, it will return 404
* If an error occurred in the process of googling the question, (possibly due to the maximum # of requests, 501)

### Knowledgebase
This can be used to get a full knowledge base without asking a question.
> `/kb/<knowledge_base_token>`

#### Request
The only parameter is the token
#### Response
A request like this
>`https://api.sethpainter.com/quizletquery/kb/vQpc7l9YqRKliCv3-rOAl-yNwEc1Zk_b`

Should return something like this
```
{
  "Can you name a mineral that is heavy?": {
    "answer": "Magnetite (Iron).",
    "url_id": "155205723"
  },
  "Do we know what the Earth's interior looks like?": {
    "answer": "No we do not, BUT we do know it is very hot.",
    "url_id": "155205723"
  },
  ...
}
```
#### Errors
* If the user doesn't provide a token, 400
* If the token cannot be found, 404

## Frontend
In the `/frontend/` directory of the project, I've created a static frontend that uses the API. it's live at the demo link above
>**https://sethpainter.com/quizletquery**

I made it so that anyone could extend it in any way they want and the frontend included here serves as an example of how you might use the API in your frontend. It's written mostly with javascript but could be greatly improved as I did not put a ton of time into styling it as this is primarily a backend project.
## Limitations
This program is definitely not perfect and there are a lot of things that could be improved in the future
### Google CSE allows maximum 100 queries per day
Given the small scope of the project, I've just included my CSE API key, but if it gains more users or grows in scale, 
I would either have to require users to provide their own API key or pay $5 per 10,000 queries. I could possibly switch to a search engine that allows more free queries.
### The server uses exact string matching
This is a major limitation. When viewing text, a human can obviously distinguish slightly different, but nearly exact flashcards with their questions, but this program cannot. It uses a very rudimentary algorithm to compare strings that will not account for similar strings with text in different locations. The program removes all none alphanumeric characters and casing from both strings to compare them.
I could fix this by making use of a fuzzy string comparison library like FuzzyWuzzy
### The application is written to work only when served on a single thread
I (so far) did not want to use a database, file, or other form of persistent storage, given that all data has a maximum idle lifetime of 30 minutes. As such, I wrote the server to store all knowledge bases as a dictionary.
When serving the application with multiple workers, each worker will not have access to the same dictionary and there is no way to consistently serve the same user the same dictionary, and the program will not function properly when run with multiple workers.
## Contribution and Usage
Do whatever the frick you please with it. I'd greatly appreciate it, if you like it, to share it with someone else or consider checking out some of my other stuff.
If you have the ability to contribute and can fix some issues or add useful features, gopher it!
