#!/usr/bin/env python
from __future__ import print_function

import cmd, re

try:
	intake = raw_input
except NameError:
	intake = input

### Helper functions

def align_order(order):
	return order.rjust(20) + "   "

def prefix_match(prefix, matchers):
	return [match for match in matchers if match.startswith(prefix)]

def fuzzy_match(answer, matchers):
	wordmatcher = '.*' + ''.join([singlechar + '.*' for singlechar in answer])
	regex = '^' + wordmatcher + '$'
	return [match for match in matchers if re.search(regex, match, re.IGNORECASE)]

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
		completions = prefix_match(answer, answers)
		if len(completions) == 1 and completions[0] != answer:
			answer = completions[0]
			print(align_order('') + answer)
		premsg = ''
	return answer

def confirm(question):
	return (ask(question, ['y','n']) == 'y')

def tell(text):
	print(align_order("TELL INFO: ") + text)

def number_of_batteries():
	if (number_of_batteries.counter == False):
		try:
			number_of_batteries.counter = int(ask("Number of batteries?"))
		except ValueError:
			number_of_batteries.counter = number_of_batteries()
	return number_of_batteries.counter
number_of_batteries.counter = False

def get_serial():
	if not get_serial.number:
		get_serial.number = ask("What is the serial number?")
	return get_serial.number
get_serial.number = ''

def serial(fn):
	return fn(get_serial())

def is_last_digit(fn):
	def executor(serialnumber):
		digits = re.findall('\d', serialnumber)
		return fn(int(digits[-1])) if digits else False
	return executor

def odd(number):
	return number % 2 == 1
def even(number):
	return not odd(number)


##############################
##### MANUAL VERSION 241 #####
##############################
class DefusalShell241(cmd.Cmd):
	intro = "Welcome to the Keep-Talking-and-Nobody-Explodes-DefusalShell!\nRemember to restart for each game.\n"
	prompt = "Manual#241> "
	
	def precmd(self, line):
		print('')
		return line

	def postcmd(self, stop, line):
		print('')
		return stop

	def emptyline(self):
		pass

	def do_exit(self, arg):
		"Quit defusing bombs."
		return True

	def do_serial(self, serial):
		"Enter complete serial."
		serial()

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

	def do_password(self, arg):
		"Guess the 5-letter password."
		words = "about after again below could every first found great house large learn never other place plant point right small sound spell still study their there these thing think three water where which world would write".split(' ')

		def regex_match(chargroups, words):
			wordmatcher = ''.join(['['+chargroup+']' for chargroup in chargroups])
			regex = '^' + wordmatcher + '$'
			return [word for word in words if re.search(regex, word, re.IGNORECASE)]

		mystery = ['a-z'] * 5
		chars = ''
		matches = words
		charpos = 1
		while len(matches) > 1 and charpos <= 5:
			chars = ask("Which letters for position " + str(charpos) + "?")
			mystery[charpos-1] = chars
			matches = regex_match(mystery, words)
			charpos += 1

		if len(matches) == 1:
			tell("Password is " + matches[0].upper())
		else:
			tell("Mistyped something, try again.")

	def do_complicated_wires(self, arg):
		"Defuse complicated wires... what else."

		while True:
			led = confirm("LED on?")
			colors = []
			while '' not in colors:
				color = ask("Color of wire? (enter seperately or nothing)", ['red', 'blue', 'white'], True)
				colors.append(color)
			colors = set(colors[:-1])
			tell("Okay, wire is " + '-'.join(colors) + '.')
			star = confirm("Star present?")

			red = 'red' in colors
			blue = 'blue' in colors

			lookup = { #Red, Blue, Star, LED
				(0,0,0,0): 'C',
				(0,0,0,1): 'D',
				(0,0,1,0): 'C',
				(0,0,1,1): 'B',
				(0,1,0,0): 'S',
				(0,1,0,1): 'P',
				(0,1,1,0): 'D',
				(0,1,1,1): 'P',
				(1,0,0,0): 'S',
				(1,0,0,1): 'B',
				(1,0,1,0): 'C',
				(1,0,1,1): 'B',
				(1,1,0,0): 'S',
				(1,1,0,1): 'S',
				(1,1,1,0): 'P',
				(1,1,1,1): 'D'
			}

			instruction = lookup[(int(red), int(blue), int(star), int(led))]

			def cut():
				instruct("Cut the wire!")
			def nocut():
				instruct("Do nothing! (do NOT cut the wire)")

			if instruction == 'C':
				cut()
			elif instruction == 'D':
				nocut()
			elif instruction == 'S':
				cut() if serial(is_last_digit(even)) else nocut()
			elif instruction == 'P':
				cut() if confirm("Has parallel port?") else nocut() #TODO save parallel port answer
			elif instruction == 'B':
				cut() if number_of_batteries() >= 2 else nocut()

			if not confirm("\nOne more wire?"):
				break
			print('')


if __name__ == '__main__':
	try:
		DefusalShell241().cmdloop()
	except KeyboardInterrupt:
		pass
