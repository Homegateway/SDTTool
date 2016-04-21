#	SDTAbbreviate.py
#
#	Handle abbreviations
# 

import csv

# Dictionary for abbreviations (name, abbr)
abbreviations = {}

def SDTAbbreviateInit(options):
	pass


# experimental abreviation function. Move later

def abbreviate(name, length=5):
	global abbreviations

	if name in abbreviations:	# return abbreviation if already in dictionary
		return abbreviations[name]

	l = len(name)
	if l <= length:
		result = name
		while l < length:
			for i in range(length - l):
				result += result[i]
			l = len(result)
		return result
	
	# First char
	result  = name[0]
	
	# Last char
	result += name[-1]

	if len(result) < length:
		mask = name[1:l-1]
		# Camel cases chars
		camels = ''
		for i in range(1,l-1):
			c = name[i]
			if c.isupper():
				camels += c
				mask = mask[:i-1] + mask[i:]
		result = result[:1] + camels + result[1:]

		# Fill with remaining chars of the mask, starting from the back
		lm = len(mask)
		for i in range(0, length - len(result)):
			pos = i + 1
			result = result[:pos] + mask[i] + result[pos:] 

	# put the new abbreviation into the global dictionary.
	# resolve clashes
	abbr = result[:length]
	clashVal = -1
	while abbr in list(abbreviations.values()):
		#print('clash: ' + abbr)
		clashVal += 1
		prf = result[:length]
		pof = str(clashVal)
		abbr = prf[:len(prf)-len(pof)] + pof
		#print('resolution: ' + abbr)

	abbreviations[name] = abbr
	return abbreviations[name]

# Return abbreviations

def getAbbreviations():
	global abbreviations
	return abbreviations.copy()





