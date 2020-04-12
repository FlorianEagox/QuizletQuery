let kb_token;
const base_url = 'https://api.sethpainter.com/quizletquery';
const txtQuery = document.querySelector('#txtQuery');
const elResults = document.querySelector('#results');
const questions = elResults.querySelector('#kb-display #found-questions');
document.querySelector('#frmQuery').addEventListener('submit', e => {
	e.preventDefault();
	document.querySelectorAll('.clearable').forEach(el => el.innerHTML = '');
	document.querySelectorAll('.result').forEach(result => result.classList.add('inactive'));
	query(txtQuery.value);
})
async function query(text) {
	const animLoader = document.querySelector('#loader');
	animLoader.classList.remove('inactive')
	let url = `${base_url}/ask/${text}/${kb_token}`;

	let res = await (fetch(url).catch(err => {
		elResults.innerHTML = 'Oopsie! An error occoured<br/>' + err;
		animLoader.classList.add('inactive');
		return;
	}));
	if (res.ok) {
		const results = await res.json();
		kb_token = results.kb_token;
		display(results)
	} else {
		if (res.status == 404) {
			// if we get a 404, then our token has expired, so lets reset it and try again
			kb_token = '';
			query(txtQuery.value);
		} else {
			elResults.innerHTML = 'Oopsie! An error occoured<br/>' + await res.text();
		}
	}
	// txtQuery.value = '';
	animLoader.classList.add('inactive')
}
function display(results) {
	const answerInfo = results.result;
	if (results.status == 'found') {
		const first = document.querySelector('#first');
		first.classList.remove('inactive');
		answerInfo.forEach((question, index) => {
			const elQuestionContainer = document.createElement('div');
			if (index == 1) {
				const elMultiple = document.createElement('div');
				elMultiple.classList.add('multiple-answers');
				elMultiple.textContent = 'Other Possible Answers:';
				elQuestionContainer.appendChild(elMultiple);
			}
			elQuestionContainer.classList.add('question-container');
			const elQuestion = document.createElement('p');
			elQuestion.classList.add('found-question');
			const elQuestionLink = document.createElement('a');
			elQuestionLink.textContent = question.question;
			elQuestionLink.href = 'https://quizlet.com/' + question.answer.url;
			elQuestionLink.target = 'blank'
			elQuestion.appendChild(elQuestionLink);
			elQuestionContainer.appendChild(elQuestion);
			const elAnswer = document.createElement('p');
			elAnswer.classList.add('found-answer');
			elAnswer.textContent = question.answer.answer;
			elQuestionContainer.appendChild(elQuestion);
			elQuestionContainer.appendChild(elAnswer);
			first.appendChild(elQuestionContainer);
		});
	} else {
		const elKbDisplay = document.querySelector('#kb-display');
		elKbDisplay.classList.remove('inactive');
		console.log(answerInfo)
		Object.keys(answerInfo).forEach(question => {
			const foundQuestion = document.createElement('div');
			foundQuestion.classList.add('found-question');
			const elQuestion = document.createElement('p');
			elQuestion.classList.add('question');
			const elQuestionLink = document.createElement('a');
			elQuestionLink.href = 'https://quizlet.com/' + answerInfo[question].url;
			elQuestionLink.target = 'blank';
			elQuestionLink.textContent = question;
			elQuestion.appendChild(elQuestionLink);
			foundQuestion.appendChild(elQuestion);
			const elAnswer = document.createElement('p');
			elAnswer.classList.add('answer');
			elAnswer.innerHTML = answerInfo[question].answer;
			foundQuestion.appendChild(elAnswer);
			questions.appendChild(foundQuestion);
		});
		elKbDisplay.appendChild(questions)
	}
}
const filter = document.querySelector('#filter');
filter.addEventListener('input', e => {
	Array.from(questions.children).forEach(question => {
		question.style.display = (question.querySelector('.question').textContent.toUpperCase().includes(filter.value.toUpperCase()) || question.querySelector('.answer').textContent.toUpperCase().includes(filter.value.toUpperCase())) ? 'flex' : 'none';
	})
});