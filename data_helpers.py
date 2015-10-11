### Data helpers

def match(matchers, condition):
	return [match for match in matchers if condition(match)]

def by_prefix(prefix):
	def has_prefix(match):
		return match.startswith(prefix)
	return has_prefix

def by_fuzzy(search):
	def fuzzy_check(match):
		wordmatcher = '.*' + ''.join([singlechar + '.*' for singlechar in search])
		regex = '^' + wordmatcher + '$'
		return re.search(regex, match, re.IGNORECASE) == True
	return fuzzy_check

def odd(number):
	return number % 2 == 1

def even(number):
	return not odd(number)
