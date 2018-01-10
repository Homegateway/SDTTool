#	SDTTool.py
#
#	Main module for the SDTTool

from xml.etree.ElementTree import XMLParser, ParseError
from sdtv2 import *
from sdtv3 import *
from SDTPrinter import *


import io, sys, traceback, argparse, textwrap

version = '0.8'
description = 'SDTTool ' + version + ' - A tool to read and convert Smart Device Templates.'
epilog = 'Read arguments from one or more configuration files: @file1 @file2 ...|n |n See https://github.com/Homegateway for further information.'

#
#	Helper method for loading arguments from file
#

def convertArgLineToArgs(arg_line):
	for arg in arg_line.split():
		if not arg.strip():
			continue
		yield arg

class MultilineFormatter(argparse.HelpFormatter):
	def _fill_text(self, text, width, indent):
		text = self._whitespace_matcher.sub(' ', text).strip()
		paragraphs = text.split('|n ')
		multiline_text = ''
		for paragraph in paragraphs:
			formatted_paragraph = textwrap.fill(paragraph, width, initial_indent=indent, subsequent_indent=indent) + '\n'
			multiline_text = multiline_text + formatted_paragraph
		return multiline_text


#
# Read data from the input file
#

def readDataFromFile(inFile):
	# Read the input file
	with open(inFile, 'r') as inputFile:
		data = inputFile.read()
	return data

#
# Parse the data with the given parser and handle errors
#
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


#
# Read and parse an SDT2 XML
#
def readSDT2XML(inFile):
	# open the file
	data = readDataFromFile(inFile)
	# Parse the data
	return parseData(SDT2Parser(), data)


#
# Read and parse an SDT3 XML
#
def readSDT3XML(inFile):
	# open the file
	data = readDataFromFile(inFile)
	# Parse the data
	return parseData(SDT3Parser(), data)


#
#	Print the output to stdout or to a file
#
def outputResult(outFile, result):
	if result == None:
		return
	if outFile == None:
		print(result)
	else:
		try:
			with open(outFile, 'w') as outputFile:
				outputFile.write(result)
		except IOError as err:
			print(err)


#
#	Check the available name spaces
#
def checkForNamespace(nameSpaces, checkNameSpace):
	for ns in nameSpaces:
		if (ns.find(checkNameSpace) > -1):
			return True
	return False


def main(argv):
	outFile = None

	# Read command line arguments
	
	parser = argparse.ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars='@', formatter_class=MultilineFormatter)
	parser.convert_arg_line_to_args = convertArgLineToArgs

	parser.add_argument('-o', '--outfile', action='store', dest='outFile', help='The output file or directory for the result. The default is stdout')
	parser.add_argument('-if', '--inputformat', choices=('sdt2', 'sdt3'), action='store', dest='inputFormat', default='sdt3', help='The input format to read. The default is sdt3')
	parser.add_argument('-of', '--outputformat', choices=('plain', 'opml', 'markdown', 'sdt3', 'java', 'vorto-dsl', 'onem2m-svg', 'onem2m-xsd', 'swagger'), action='store', dest='outputFormat', default='markdown', help='The output format for the result. The default is markdown')
	parser.add_argument('--hidedetails',  action='store_true', help='Hide the details of module classes and devices when printing documentation')
	parser.add_argument('--markdowntables',  action='store_true', help='Format markdown output as tables for markdown')
	parser.add_argument('--markdownpagebreak',  action='store_true', help='Insert page breaks before ModuleClasse and Device definitions.')
	parser.add_argument('--licensefile',  action='store', dest='licensefile', help='Add the text of license file to output files')

	oneM2MArgs = parser.add_argument_group('oneM2M sepcific')
	oneM2MArgs.add_argument('--domain',  action='store', dest='domain', help='Set the domain for the model')
	oneM2MArgs.add_argument('--namespaceprefix',  action='store', dest='namespaceprefix', help='Specify the name space prefix for the model')
	oneM2MArgs.add_argument('--abbreviationsinfile',  action='store', dest='abbreviationsinfile', help='Specify the file that contains a CSV table of alreadys existing abbreviations.')
	oneM2MArgs.add_argument('--abbreviationlength',  action='store', dest='abbreviationlength', default='5', help='Specify the maximum length for abbreviations. The default is 5.')
	oneM2MArgs.add_argument('--xsdtargetnamespace',  action='store', dest='xsdtargetnamespace', help='Specify the target namespace for the oneM2M XSD (a URI).')
	oneM2MArgs.add_argument('--modelversion',  action='store', dest='modelversion', help='Specify the version of the model.')

	requiredNamed = parser.add_argument_group('required arguments')
	requiredNamed.add_argument('-i', '--infile', action='store', dest='inFile', required=True, help='The SDT input file to parse')
	
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()
	inFile = args.inFile
	outFile = args.outFile
	inputFormat = args.inputFormat
	
	moreOptions = {}
	moreOptions['hideDetails'] 					= args.hidedetails
	moreOptions['markdowntables'] 				= args.markdowntables
	moreOptions['pageBreakBeforeMCandDevices'] 	= args.markdownpagebreak
	moreOptions['licensefile'] 					= args.licensefile
	moreOptions['domain'] 						= args.domain
	moreOptions['namespaceprefix'] 				= args.namespaceprefix
	moreOptions['abbreviationsinfile'] 			= args.abbreviationsinfile
	moreOptions['abbreviationlength'] 			= args.abbreviationlength
	moreOptions['xsdtargetnamespace'] 			= args.xsdtargetnamespace
	moreOptions['modelversion'] 				= args.modelversion
	moreOptions['outputFormat']					= args.outputFormat


	# Read input file. Check for correct format

	if inputFormat == 'sdt2':
		domain, nameSpaces = readSDT2XML(inFile)
		if not checkForNamespace(nameSpaces, 'http://homegatewayinitiative.org/xml/dal/2.0'):
			print('ERROR: Namespace "http://homegatewayinitiative.org/xml/dal/2.0" not found in input file.')
			return

	elif inputFormat == 'sdt3':
		domain, nameSpaces = readSDT3XML(inFile)
		if not checkForNamespace(nameSpaces, 'http://homegatewayinitiative.org/xml/dal/3.0'):
			print('ERROR: Namespace "http://homegatewayinitiative.org/xml/dal/3.0" not found in input file.')
			return

	# Output to destination format
	if args.outputFormat == 'plain':
		outputResult(outFile, printPlain(domain, moreOptions))
	elif args.outputFormat == 'opml':
		outputResult(outFile, printOPML(domain, moreOptions))
	elif args.outputFormat == 'markdown':
		outputResult(outFile, printMarkdown(domain, moreOptions))
	elif args.outputFormat == 'sdt3':
		outputResult(outFile, printSDT3(domain, inputFormat, moreOptions))
	elif args.outputFormat == 'java':
		printJava(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'vorto-dsl':
		printVortoDSL(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'onem2m-svg':
		printOneM2MSVG(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'onem2m-xsd':
		printOneM2MXSD(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'swagger':
		printSwagger(domain, inputFormat, outFile, moreOptions)



if __name__ == "__main__":
	main(sys.argv[1:])
