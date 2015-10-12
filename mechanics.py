### Game related
import re
from display_helpers import *

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

def has_parallel_port():
	if has_parallel_port.value == None:
		has_parallel_port.value = confirm("Bomb has parallel port?")
	return has_parallel_port.value
has_parallel_port.value = None
