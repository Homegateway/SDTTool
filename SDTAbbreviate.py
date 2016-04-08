#	SDTAbbreviate.py
#
#	Handle abbreviations
# 

import csv

def SDTAbbreviateInit(options):
	pass




# experimental abreviation function. Move later

def abbreviate(name, length=5):
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

	return result[:length]








