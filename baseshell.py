import cmd

class DefusalShell(cmd.Cmd):
	intro = "Welcome to the Keep-Talking-and-Nobody-Explodes-DefusalShell!\nRemember to restart for each game.\n"

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
