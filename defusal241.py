#!/usr/bin/env python
from __future__ import print_function

from baseshell import *
from display_helpers import *
from data_helpers import *
from mechanics import *

import re

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
			instruct("Password is " + matches[0].upper())
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
				cut() if has_parallel_port() else nocut()
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
		alphabet = {letter: code for code, letter in morse.items()}

		def morse_of(word):
			morse_word = [alphabet[char] for char in word]
			return ' '.join(morse_word)

		morse_stream = {(morse_of(word) + ' ') * 3: freq for word, freq in words.items()}

		stream = ''
		matches = morse_stream
		tell("Enter morse code, use the keys . and -")
		while len(matches) > 1:
			stream += ask("Enter next letter") + ' '
			matches = match(morse_stream, by_contains(stream))

		if len(matches) == 1:
			detected = matches[0]
			stream_end = detected.index(stream) + len(stream)
			next_morse_letter = detected[stream_end:stream_end + detected[stream_end:].index(' ')]
			tell("Detected! Next incoming sequence should be: " + next_morse_letter)
			instruct("Respond frequency is " + morse_stream[detected] + " Mhz.")
		else:
			tell("Input error, try again.")

	def do_memory(self, arg):
		config = ''
		while re.match('^\d{4}$', config) is None:
			config = ask("Button labels from left to right? (e.g. 1342)")

		buttons = [(pos + 1, config[pos]) for pos in range(4)] #(position, label)
		stage = 1
		pressed = {} #stage: (position, label)

		def button_in_position((pos, lab)): #returns label
			return [label for (position, label) in buttons if position == pos][0]

		def button_with_label((position, label)): #returns label
			return label

		def as_pressed_in_stage(stage): #returns (position, label)
			return pressed[stage]

		def number(position): #returns (position, dummy)
			return (position, '0')

		def press(label):
			instruct("Press label " + label)
			pressed[stage] = [(pos, lab) for (pos, lab) in buttons if lab == label][0]

		while stage <= 5:
			tell("STAGE " + ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE'][stage - 1])
			display = ask("Display shows...?", ['1', '2', '3', '4', 'x'])
			if display == 'x':
				tell("Cancelling memory.")
				return
			display = int(display)

			if stage == 1:
				if display == 1: press(button_in_position(number(2)))
				if display == 2: press(button_in_position(number(2)))
				if display == 3: press(button_in_position(number(3)))
				if display == 4: press(button_in_position(number(4)))
			if stage == 2:
				if display == 1: press(4)
				if display == 2: press(button_in_position(as_pressed_in_stage(1)))
				if display == 3: press(button_in_position(number(1)))
				if display == 4: press(button_in_position(as_pressed_in_stage(1)))
			if stage == 3:
				if display == 1: press(button_with_label(as_pressed_in_stage(2)))
				if display == 2: press(button_with_label(as_pressed_in_stage(1)))
				if display == 3: press(button_in_position(number(3)))
				if display == 4: press(4)
			if stage == 4:
				if display == 1: press(button_in_position(as_pressed_in_stage(1)))
				if display == 2: press(button_in_position(number(1)))
				if display == 3: press(button_in_position(as_pressed_in_stage(2)))
				if display == 4: press(button_in_position(as_pressed_in_stage(2)))
			if stage == 5:
				if display == 1: press(button_with_label(as_pressed_in_stage(1)))
				if display == 2: press(button_with_label(as_pressed_in_stage(2)))
				if display == 3: press(button_with_label(as_pressed_in_stage(4)))
				if display == 4: press(button_with_label(as_pressed_in_stage(3)))

			stage += 1

		tell("Memory solved!")


if __name__ == '__main__':
	try:
		DefusalShell241().cmdloop()
	except KeyboardInterrupt:
		pass
