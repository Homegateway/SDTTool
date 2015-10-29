#	SDTTool.py
#
#	Main module for the SDTTool

from xml.etree.ElementTree import XMLParser, ParseError
from SDT2Parser import SDT2Parser
from SDT3Parser import SDT3Parser
from SDTPrinter import *


import io, sys, traceback, argparse

version = '0.4'
description = 'SDTTool ' + version + ' - A tool to read and convert Smart Device Templates.'
epilog = 'See https://github.com/Homegateway for further information.'

# Read data from the input file
def readDataFromFile(inFile):
	# Read the input file
	inputFile = open(inFile, 'r')
	data = inputFile.read()
	inputFile.close()
	return data

# Parse the data with the given parser and handle errors
def parseData(target, data):
	parser = XMLParser(target=target)
	errormsg = ''
	try:
		try:
			parser.feed(data)
		except SyntaxError as err:
			errormsg = str(err)
			print(err)
		except:
			traceback.print_exc()
		finally:
			parser.close()
	except ParseError as err:
		formatted_e = errormsg
		line = int(formatted_e[formatted_e.find("line ") + 5: formatted_e.find(",")])
		column = int(formatted_e[formatted_e.find("column ") + 7:])
		split_str = data.split("\n")
		print("{}\n{}^".format(split_str[line - 1], len(split_str[line - 1][0:column])*"-"))

	return target.domain, target.nameSpaces


# Read and parse an SDT2 XML
def readSDT2XML(inFile):
	# open the file
	data = readDataFromFile(inFile)
	# Parse the data
	return parseData(SDT2Parser(), data)


# Read and parse an SDT3 XML
def readSDT3XML(inFile):
	# open the file
	data = readDataFromFile(inFile)
	# Parse the data
	return parseData(SDT3Parser(), data)



def outputResult(outFile, result):
	if (result == None):
		return
	if (outFile == None):
		print(result)
	else:
		outputFile = None
		try:
			outputFile = open(outFile, 'w')
			outputFile.write(result)
		except IOError as err:
			print(err)
		finally:
			if (outputFile != None):
				outputFile.close()


def checkForNamespace(nameSpaces, checkNameSpace):
	for ns in nameSpaces:
		if (ns.find(checkNameSpace) > -1):
			return True
	return False


def main(argv):
	outFile = None

	# Read command line arguments
	parser = argparse.ArgumentParser(description=description, epilog=epilog)
	parser.add_argument('-o', '--outfile', action='store', dest='outFile', help='The output file or directory for the result. The default is stdout')
	parser.add_argument('-if', '--inputformat', choices=('sdt2', 'sdt3', ''), action='store', dest='inputFormat', default='sdt2', help='The input format to read. The default is sdt2')
	parser.add_argument('-of', '--outputformat', choices=('plain', 'opml', 'markdown', 'sdt3', 'java'), action='store', dest='outputFormat', default='markdown', help='The output format for the result. The default is markdown')
	parser.add_argument('--hidedetails',  action='store_true', help='Hide the details of module classes and devices when printing documentation')
	requiredNamed = parser.add_argument_group('required arguments')
	requiredNamed.add_argument('-i', '--infile', action='store', dest='inFile', required=True, help='The SDT input file to parse')
	
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	results = parser.parse_args()
	inFile = results.inFile
	outFile = results.outFile
	inputFormat = results.inputFormat
	outputFormat = results.outputFormat
	
	moreOptions = {}
	moreOptions['hideDetails'] = results.hidedetails


	# Read input file. Check for correct format

	if (inputFormat == 'sdt2'):
		domain, nameSpaces = readSDT2XML(inFile)
		if (checkForNamespace(nameSpaces, 'http://homegatewayinitiative.org/xml/dal/2.0') == False):
			print('ERROR: Namespace "http://homegatewayinitiative.org/xml/dal/2.0" not found in input file.')
			return

	elif (inputFormat == 'sdt3'):
		domain, nameSpaces = readSDT3XML(inFile)
		if (checkForNamespace(nameSpaces, 'http://homegatewayinitiative.org/xml/dal/3.0') == False):
			print('ERROR: Namespace "http://homegatewayinitiative.org/xml/dal/3.0" not found in input file.')
			return

	# Output to destination format

	if (outputFormat == 'plain'):
		outputResult(outFile, printPlain(domain, moreOptions))
	elif (outputFormat == 'opml'):
		outputResult(outFile, printOPML(domain, moreOptions))
	elif (outputFormat == 'markdown'):
		outputResult(outFile, printMarkdown(domain, moreOptions))
	elif (outputFormat == 'sdt3'):
		outputResult(outFile, printSDT3(domain, inputFormat, moreOptions))
	elif (outputFormat == 'java'):
		printJava(domain, inputFormat, outFile, moreOptions)



if __name__ == "__main__":
	main(sys.argv[1:])
