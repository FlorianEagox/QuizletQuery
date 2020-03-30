import quizlet



running = True
while running:
	question = input("Question? ")
	if question in ["exit", "no", "quit"]:
		running = False
	else:
		quizlet.ask_question(question)
		found_answer = [key for key in quizlet.knowledge_base if quizlet.minify(question) in key]
		if found_answer:
			print(quizlet.knowledge_base[found_answer[0]])
		else:
			print(quizlet.knowledge_base)