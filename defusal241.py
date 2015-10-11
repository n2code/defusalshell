#!/usr/bin/env python
from __future__ import print_function

import cmd, re

try:
	intake = raw_input
except NameError:
	intake = input

execfile("data_helpers.py")
execfile("display_helpers.py")
execfile("mechanics.py")
execfile("baseshell.py")

##############################
##### MANUAL VERSION 241 #####
##############################
class DefusalShell241(DefusalShell):
	prompt = "Manual#241> "
	
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

			print('')
			if not confirm("One more wire?"):
				break
			print('')

	def do_morse(self, arg):
		"Decode morse code. Beeeep beep."

		morse = {
			'.-': 'a',
			'-...': 'b',
			'-.-.': 'c',
			'-..': 'd',
			'.': 'e',
			'..-.': 'f',
			'--.': 'g',
			'....': 'h',
			'..': 'i',
			'.---': 'j',
			'-.-': 'k',
			'.-..': 'l',
			'--': 'm',
			'-.': 'n',
			'---': 'o',
			'.--.': 'p',
			'--.-': 'q',
			'.-.': 'r',
			'...': 's',
			'-': 't',
			'..-': 'u',
			'...-': 'v',
			'.--': 'w',
			'-..-': 'x',
			'-.--': 'y',
			'--..': 'z'
		}
		words = {
			'shell': '3.505',
			'halls': '3.515',
			'slick': '3.522',
			'trick': '3.532',
			'boxes': '3.535',
			'leaks': '3.542',
			'strobe':'3.545',
			'bistro':'3.552',
			'flick': '3.555',
			'bombs': '3.565',
			'break': '3.572',
			'brick': '3.575',
			'steak': '3.582',
			'sting': '3.592',
			'vector':'3.595',
			'beats': '3.600'
		}

		print("Not yet implemented.") #TODO


if __name__ == '__main__':
	try:
		DefusalShell241().cmdloop()
	except KeyboardInterrupt:
		pass
