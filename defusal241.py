#!/usr/bin/env python
import cmd

### Helper functions

def align_order(order):
	return order.rjust(20) + "   "

def prefix_match(prefix, matchers):
	result = []
	for matcher in matchers:
		if matcher.startswith(prefix):
			result.append(matcher)
	return result

def instruct(text):
	print align_order("INSTRUCT ACTION: ") + text

def ask(question, answers = []):
	answer = False
	premsg = "REQUEST ANSWER: "
	while (answer not in answers):
		print align_order(premsg) + question + " ["+'/'.join(answers)+"]:"
		answer = raw_input(align_order(''))
		if not answers:
			break
		autocomplete = prefix_match(answer, answers)
		if len(autocomplete) == 1:
			answer = autocomplete[0]
		premsg = ''
	return answer

def confirm(question):
	return (ask(question, ['y','n']) == 'y')

def tell(text):
	print align_order("TELL INFO: ") + text

def number_of_batteries():
	if (number_of_batteries.counter == False):
		try:
			number_of_batteries.counter = int(ask("Number of batteries?"))
		except:
			number_of_batteries.counter = number_of_batteries()
	return number_of_batteries.counter
number_of_batteries.counter = False


##############################
##### MANUAL VERSION 241 #####
##############################
class DefusalShell241(cmd.Cmd):
	intro = "Welcome to the Keep-Talking-and-Nobody-Explodes-DefusalShell"
	prompt = "Manual#241> "
	
	def precmd(self, line):
		print ''
		return line

	def postcmd(self, stop, line):
		print ''
		return stop

	def do_exit(self, arg):
		"Quit defusing bombs."
		return True

	def do_batteries(self, number):
		"Set the number of batteries on the bomb."
		try:
			number_of_batteries.counter = int(number)
		except:
			number_of_batteries.counter = number_of_batteries()
		tell("Okay, bomb has " + str(number_of_batteries()) + " batteries.")

	def do_button(self, arg):
		"Defuse the big button."
		button_colors = ['blue','white','yellow','red','other']
		hold_colors = {'blue': 4, 'white': 1, 'yellow': 5, 'other': 1}
		words = ['abort','detonate','hold','other']

		def timedRelease():
			instruct("Press and hold button...")
			tell("A colored strip lights up on the right.")
			color = ask("Which color?", hold_colors)
			instruct("Release while the countdown timer contains a " + str(hold_colors[color]))
		def immediateRelease():
			instruct("Release immediately after a quick button press.")

		color = ask("Color of button?", button_colors)
		word = ask("Word on button?", words)
		if color == 'blue' and word == 'abort':
			timedRelease()
		elif word == 'detonate' and number_of_batteries() > 1:
			immediateRelease()
		elif color == 'white' and confirm("Lit indicator with label CAR on bomb?"):
			timedRelease()
		elif number_of_batteries() > 2 and confirm("Lit indicator with label FRK on bomb?"):
			immediateRelease()
		elif color == 'yellow':
			timedRelease()
		elif color == 'red' and word == 'hold':
			immediateRelease()
		else:
			timedRelease()


if __name__ == '__main__':
	DefusalShell241().cmdloop()
