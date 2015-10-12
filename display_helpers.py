### Display helpers
from data_helpers import match, by_prefix

try:
	intake = raw_input
except NameError:
	intake = input

def align_order(order):
	return order.rjust(17) + "  "

def instruct(text):
	print(align_order("INSTRUCT ACTION: ") + text)

def ask(question, answers = [], empty_is_allowed = False):
	answer = False
	premsg = "REQUEST ANSWER: "
	while (answer not in answers):
		print(align_order(premsg) + question +((" ["+'/'.join(answers)+"]") if answers else '') + ":")
		answer = intake(align_order(''))
		if not answers or (empty_is_allowed and not answer):
			break
		completions = match(answers, by_prefix(answer))
		if len(completions) == 1 and completions[0] != answer:
			answer = completions[0]
			print(align_order('') + answer)
		premsg = ''
	return answer

def confirm(question):
	return (ask(question, ['y','n']) == 'y')

def tell(text):
	print(align_order("TELL INFO: ") + text)
