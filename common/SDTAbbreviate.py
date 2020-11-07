#	SDTAbbreviate.py
#
#	Handle abbreviations
# 

import csv
from typing import Dict

# Dictionary for abbreviations (name, abbr)
abbreviations:Dict[str, str] = {}

# Dicionary for existing abbreviations
preDefinedAbbreviations:Dict[str, str] = {}


# experimental abreviation function. Move later
def abbreviate(name:str, length:int=5) -> str:
	global abbreviations
	result = ''

	if name in abbreviations:			# return abbreviation if already in dictionary
		return abbreviations[name]
	if name in preDefinedAbbreviations:	# return abbreviation if it exists in the predefined dictionary
		return preDefinedAbbreviations[name]

	l = len(name)

	# name is less of equal the max allowed length
	if l <= length:
		result = name
		#Fill up to the length by repeating
		#while l < length:
		#	for i in range(length - l):
		#		result += result[i]
		#	l = len(result)

	else:	# length of the name is longer than the allowed name. So do some shortening
		# First char
		result  = name[0]
		# Last char
		result += name[-1]

		# Fill up the abbreviation
		if len(result) < length:
			mask = name[1:l-1]
			# Camel case chars
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
	while abbr in list(abbreviations.values()) or abbr in list(preDefinedAbbreviations.values()	):
		#print('clash: ' + abbr)
		clashVal += 1
		prf = result[:length]
		pof = str(clashVal)
		abbr = prf[:len(prf)-len(pof)] + pof
		#print('resolution: ' + abbr)

	return abbr


# Add a single abbreviation
def addAbbreviation(name, abbreviation):
	abbreviations[name] = abbreviation


# Return abbreviations
def getAbbreviations():
	return abbreviations.copy()


# Return an abbreviation for a longName
def getAbbreviation(name):
	if name in abbreviations:
		return abbreviations[name]
	if name in preDefinedAbbreviations:
		return preDefinedAbbreviations[name]
	return None


# Read already existing abbreviations
def readAbbreviations(infile, predefined=True):
	global preDefinedAbbreviations, abbreviations
	if infile == None:
		return
	try:
		with open(infile) as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='\\')
			for row in reader:
				if len(row) == 2:
					if predefined:
						preDefinedAbbreviations[row[0]] = row[1]
					else:
						abbreviations[row[0]] = row[1]
				else:
					print('Unknwon row found (ignored): ' + ', '.join(row))
	except FileNotFoundError as e:
		print(str(e) + ' (abbreviation input file ignored)')
	except Exception as e:
		raise


def exportAbbreviations(csvFile, mapFile, abbreviations):

	# Export as python map
	outputFile = None
	try:
		outputFile = open(mapFile, 'w')
		outputFile.write(str(abbreviations))
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()

	# Export as CSV
	outputFile = None
	try:
		outputFile = open(csvFile, 'w', newline='')
		writer = csv.writer(outputFile)
		for key, value in abbreviations.items():
			writer.writerow([key, value])
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()

