#	SDTTool.py
#
#	Main module for the SDTTool

from xml.etree.ElementTree import XMLParser, ParseError
from SDT2Parser import SDT2Parser
from SDT2Printer import *

import io, sys, traceback, argparse

version = '0.4'
description = 'SDTTool ' + version + ' - A tool to read and convert Smart Device Templates.'
epilog = 'See https://github.com/Homegateway for further information.'


def readSDT2XML(inFile):

	# Read the input file
	inputFile = open(inFile, 'r')
	data = inputFile.read()
	inputFile.close()

	# Parse the file
	target = SDT2Parser()
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

def outputResult(outFile, result):
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


def main(argv):

	# Read command line arguments
	parser = argparse.ArgumentParser(description=description, epilog=epilog)
	parser.add_argument('-o', '--outfile', action='store', dest='outFile', help='The output file for the result. The default is stdout')
	parser.add_argument('-if', '--inputformat', choices=('sdt2', ''), action='store', dest='inputFormat', default='sdt2', help='The input format to read. The default is sdt2')
	parser.add_argument('-of', '--outputformat', choices=('plain', 'opml', 'markdown', 'sdt3'), action='store', dest='outputFormat', default='markdown', help='The output format for the result. The default is markdown')
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

	if (inputFormat == 'sdt2'):
		domain, nameSpaces = readSDT2XML(inFile)

	if (outputFormat == 'plain'):
		outputResult(outFile, printPlain(domain))
	elif (outputFormat == 'opml'):
		outputResult(outFile, printOPML(domain))
	elif (outputFormat == 'markdown'):
		outputResult(outFile, printMarkdown(domain))
	elif (outputFormat == 'sdt3'):
		outputResult(outFile, printSDT3(domain))



if __name__ == "__main__":
	main(sys.argv[1:])
