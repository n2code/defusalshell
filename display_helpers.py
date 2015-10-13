### Display helpers
from data_helpers import match, by_prefix

try:
	intake = raw_input
except NameError:
	intake = input

def align_order(order):
	return order.rjust(17) + "  "

def output(text):
	print(align_order('') + text)

def instruct(text):
	print(align_order("INSTRUCT ACTION: ") + text)

def ask(question, answers = [], empty_is_allowed = False):
	answer = False
	premsg = "REQUEST ANSWER: "
	while (answer not in answers):
		prompt = align_order(premsg) + question
		if answers:
			allowed = "["+'/'.join(answers)+"]"
			prompt += '\n' + align_order('') + allowed
		answer = intake(prompt + ": ")
		if not answers or (empty_is_allowed and not answer):
			break
		completions = match(answers, by_prefix(answer))
		if len(completions) == 1 and completions[0] != answer:
			answer = completions[0]
			output("~~> ".rjust(len(allowed) + len(": ")) + answer)
		premsg = ''
	return answer

def confirm(question):
	return (ask(question, ['y','n']) == 'y')

def tell(text):
	print(align_order("TELL INFO: ") + text)
