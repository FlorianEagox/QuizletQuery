import quizlet

knowledge_base = {}

running = True
while running:
	question = input("Question? ")
	if question in ["exit", "no", "quit"]:
		running = False
	else:
		quizlet.ask_question(question, knowledge_base)
		found_answer = [key for key in knowledge_base if quizlet.minify(question) in key]
		if found_answer:
			print(knowledge_base[found_answer[0]])
		else:
			print(knowledge_base)