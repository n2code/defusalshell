import cmd
from mechanics import *

class DefusalShell(cmd.Cmd):
	print("Welcome to the Keep-Talking-and-Nobody-Explodes-DefusalShell!\nRemember to restart for each game.")

	def precmd(self, line):
		print('')
		return line

	def postcmd(self, stop, line):
		return stop

	def cmdloop(self):
		try:
			cmd.Cmd.cmdloop(self)
		except KeyboardInterrupt as e:
			self.cmdloop()

	def do_exit(self, arg):
		"Quit defusing the current bomb."
		return True

	def do_serial(self, serial):
		"Enter complete serial."
		if serial:
			get_serial.number = serial
		tell("Okay, serial is " + get_serial() + ".")

	def do_batteries(self, number):
		"Set the number of batteries on the bomb."
		try:
			number_of_batteries.counter = int(number)
		except:
			number_of_batteries.counter = number_of_batteries()
		tell("Okay, bomb has " + str(number_of_batteries()) + " batteries.")
