#	SDTAbbreviate.py
#
#	Handle abbreviations
# 

import csv
from typing import Dict, List, Tuple
from rich import print, get_console
from enum import IntEnum


# Dictionary for abbreviations (name, abbr)
abbreviations:Dict[str, str] = {}

# Abbreviations that are newly created while processing
newAbbreviation:Dict[str, str] = {}

# Dicionary for existing abbreviations
preDefinedAbbreviations:Dict[str, str] = {}

# Dictionary for mapping of short names to places where used
# shortname -> (longname, [ occursIn ])
abbreviationOccursIn:Dict[str, Tuple[str, List[str]]] = {}

class ElementType(IntEnum):
	moduleClass = 1
	deviceClass = 2
	subDeviceClass = 3
	action = 4
	moduleClassAttribute = 5
	deviceAttribute = 6
	subDeviceAttribute = 7
	actionAttribute = 8



# experimental abreviation function. Move later
def abbreviate(name:str, length:int = 5, elementType:ElementType = None, occursIn:str = None) -> str:
	global abbreviations
	result = ''

	# print(f'{elementType} - {name} - {occursIn}')

	def addOccursIn(sn:str) -> str:
		"""	Add occursIn to the list.
		"""

		if (a := abbreviationOccursIn.get(sn)) is None:
			a = (name, [])
		if occursIn not in a[1]:
			a[1].append(occursIn)
		abbreviationOccursIn[sn] = a
		return sn


	if name in abbreviations:			# return abbreviation if already in dictionary
		return addOccursIn(abbreviations[name])
	if name in preDefinedAbbreviations:	# return abbreviation if it exists in the predefined dictionary
		return addOccursIn(preDefinedAbbreviations[name])

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
		# print(f'clash: {abbr}')
		clashVal += 1
		prf = result[:length]
		pof = str(clashVal)
		abbr = prf[:len(prf)-len(pof)] + pof
		# print(f'resolution: {abbr}')
	#print(f'{name} - {abbr}')

	newAbbreviation[name] = abbr
	return addOccursIn(abbr)


# Add a single abbreviation
def addAbbreviation(name, abbreviation):
	abbreviations[name] = abbreviation


# Return abbreviations
def getAbbreviations():
	return abbreviations.copy()


# Return new abbreviations
def getNewAbbreviations():
	return newAbbreviation.copy()



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
				if not len(row):	# ignore empty rows
					continue
				elif len(row) == 2:
					if predefined:
						preDefinedAbbreviations[row[0]] = row[1]
					else:
						abbreviations[row[0]] = row[1]
				else:
					print('[yellow]Unknown row found (ignored): ' + ', '.join(row))
	except FileNotFoundError as e:
		print(f'[yellow]WARNING: No such file or directory: "{infile}": abbreviation input file ignored')
	except Exception as e:
		raise


def exportAbbreviations(csvFile, mapFile, abbreviations):

	if not abbreviations:
		return
	# Export as python map
	try:
		if mapFile:
			with open(mapFile, 'w') as f:
					f.write(str(abbreviations))
	except IOError as err:
		print(f'[red]{err}')

	# Export as CSV
	try:
		if csvFile:
			with open(csvFile, 'w', newline='') as f:
				writer = csv.writer(f)
				for key in sorted(abbreviations.keys()):
					writer.writerow([key, abbreviations[key]])

	except IOError as err:
		print(f'[red]{err}')
	except Exception as err:
		print(f'[red]{err}')


def importOccursIn(occursInFile:str = 'occursIn.csv'):
	try:
		with open(occursInFile) as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			for row in reader:
				if not len(row):	# ignore empty rows
					continue
				elif len(row) == 3:
					abbreviationOccursIn[row[2]] = (row[0], [ s for s in row[1].split(', ') ]) 
				else:
					print(f'[yellow]Unknown row found (ignored) : {", ".join(row)} ({len(row)})')
	except FileNotFoundError as e:
		print(f'[yellow]WARNING: No such file or directory: "{occursInFile}": occursIn input file ignored')
	except Exception as e:
		print(f'[red]{e}')
		raise


def exportOccursIn(occursInFile:str = 'occursIn.csv'):
	if not abbreviationOccursIn:
		return
	# Export as CSV
	try:
		if occursInFile:
			with open(occursInFile, 'w', newline='') as f:
				writer = csv.writer(f, delimiter=',')
				for key in sorted(abbreviationOccursIn.keys()):
					_n, _l = abbreviationOccursIn[key]
					# clear up the reference list
					_l = [	_t 
							for _t in _l
							if _t is not None and len(_t) and _t != _n
						]
					# if None in _l:
					# 	_l = ['']
					writer.writerow([ _n, ', '.join(_l), key ])
	except IOError as err:
		print(f'[red]{err}')
		get_console().print_exception(show_locals = True)
	except Exception as err:
		print(f'[red]{err}')
		get_console().print_exception(show_locals = True)