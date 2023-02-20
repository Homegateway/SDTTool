#	SDTTool.py
#
#	Main module for the SDTTool

from xml.etree.ElementTree import XMLParser, ParseError
from sdtv2 import SDT2Parser
from sdtv3 import SDT3Parser
from sdtv4 import SDT4Parser
import common.SDTHelper as SDTHelper, SDTPrinter


import io, sys, traceback, argparse, os
from rich import print

version = '0.9'
description = 'SDTTool ' + version + ' - A tool to read and convert Smart Device Templates.'
epilog = 'Read arguments from one or more configuration files: @file1 @file2 ...|n |n See https://github.com/Homegateway for further information.'


# class LineNumberingParser(XMLParser):
#     def _start_list(self, *args, **kwargs):
#         # Here we assume the default XML parser which is expat
#         # and copy its element position attributes into output Elements
#         element = super(self.__class__, self)._start_list(*args, **kwargs)
#         element._start_line_number = self.parser.CurrentLineNumber
#         element._start_column_number = self.parser.CurrentColumnNumber
#         element._start_byte_index = self.parser.CurrentByteIndex
#         return element

#     def _end(self, *args, **kwargs):
#         element = super(self.__class__, self)._end(*args, **kwargs)
#         element._end_line_number = self.parser.CurrentLineNumber
#         element._end_column_number = self.parser.CurrentColumnNumber
#         element._end_byte_index = self.parser.CurrentByteIndex
#         return element


#
# Parse the data
#
def parseData(target, data):
	"""	Parse the data with the given parser and handle errors.
	"""
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
		print(f'{split_str[line - 1]}\n{len(split_str[line - 1][0:column])*"-"}')

	return target.domain, target.nameSpaces


#
#	XML Reader
#
def readSDTXML(inFile, sdtVersion=2):
	""" Read and parse an SDT version 2, 3 or 4 XML.
	"""
	# read the data from the input file
	with open(inFile, 'r') as inputFile:
		data = inputFile.read()

	# select parser
	parser = [ None, None, SDT2Parser, SDT3Parser, SDT4Parser ][sdtVersion]()	# no parsers for v 0 and 1

	# Parse the data
	return parseData(parser, data)


#
#	Output
#
def outputResult(outFile, result):
	"""	Print the output to stdout or to a file.
	"""
	if result == None:
		return
	if outFile == None:
		print(result)
	else:
		path = os.path.dirname(outFile)
		if len(path) > 0:
			os.makedirs(path, exist_ok=True)
		try:
			with open(outFile, 'w') as outputFile:
				outputFile.write(result)
		except IOError as err:
			print(err)


def checkForNamespace(nameSpaces, checkNameSpace):
	"""	Check whether a name space can be found in a list of nameSpaces.
	"""
	for ns in nameSpaces:
		if (ns.find(checkNameSpace) > -1):
			return True
	return False


def main(argv):
	outFile = None

	# Read command line arguments
	
	parser = argparse.ArgumentParser(description=description, epilog=epilog, fromfile_prefix_chars='@', formatter_class=SDTHelper.MultilineFormatter)
	parser.convert_arg_line_to_args = SDTHelper.convertArgLineToArgs

	parser.add_argument('-o', '--outfile', action='store', dest='outFile', default=None, help='The output file or directory for the result. The default is stdout')
	parser.add_argument('-if', '--inputformat', choices=('sdt2', 'sdt3', 'sdt4'), action='store', dest='inputFormat', default='sdt4', help='The input format to read. The default is sdt4')
	parser.add_argument('-of', '--outputformat', choices=('plain', 'opml', 'markdown', 'sdt3', 'sdt4', 'java', 'vorto-dsl', 'onem2m-svg', 'onem2m-xsd', 'swagger', 'apjson'), action='store', dest='outputFormat', default='markdown', help='The output format for the result. The default is markdown')
	parser.add_argument('--hidedetails',  action='store_true', help='Hide the details of module classes and devices when printing documentation')
	parser.add_argument('--markdowntables',  action='store_true', help='Format markdown output as tables for markdown')
	parser.add_argument('--markdownpagebreak',  action='store_true', help='Insert page breaks before ModuleClasse and Device definitions.')
	parser.add_argument('-lf', '--licensefile',  action='store', dest='licensefile', help='Add the text of license file to output files')

	oneM2MArgs = parser.add_argument_group('oneM2M sepcific')
	oneM2MArgs.add_argument('--domain',  action='store', dest='domain', help='Set the domain for the model')
	oneM2MArgs.add_argument('-ns', '--namespaceprefix',  action='store', dest='namespaceprefix', default='m2m', help='Specify the name space prefix for the model')
	oneM2MArgs.add_argument('--abbreviationsinfile', '-abif',  action='store', dest='abbreviationsinfile', help='Specify the file that contains a CSV table of alreadys existing abbreviations.')
	oneM2MArgs.add_argument('--abbreviationlength',  action='store', dest='abbreviationlength', type=int, default=5, help='Specify the maximum length for abbreviations. The default is 5.')
	oneM2MArgs.add_argument('--xsdtargetnamespace',  action='store', dest='xsdtargetnamespace', help='Specify the target namespace for the oneM2M XSD (a URI).')
	oneM2MArgs.add_argument('--modelversion', '-mv', action='store', dest='modelversion', help='Specify the version of the model.')
	oneM2MArgs.add_argument('--svg-with-attributes',  action='store_true', dest='svgwithattributes', help='Generate SVG for ModuleClass attributes as well.')
	oneM2MArgs.add_argument('--xsdnamespacemapping', '-xsdnsmap',  action='store', dest='xsdnamespacemapping', nargs='*', help='Specify the target namespace for the oneM2M XSD (a URI).')
	oneM2MArgs.add_argument('--cdtversion',  action='store', dest='cdtversion', help='Specify the version number of the oneM2M XSD.')

	requiredNamed = parser.add_argument_group('required arguments')
	requiredNamed.add_argument('-i', '--infile', action='store', dest='inFile', required=True, help='The SDT input file to parse')
	
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	args 		= parser.parse_args()
	inFile 		= args.inFile
	outFile 	= args.outFile
	inputFormat	= args.inputFormat
	
	moreOptions = {}
	moreOptions['hideDetails'] 					= args.hidedetails
	moreOptions['markdowntables'] 				= args.markdowntables
	moreOptions['pageBreakBeforeMCandDevices'] 	= args.markdownpagebreak
	moreOptions['markdownPageBreak']		 	= args.markdownpagebreak # renamed, therefore twice
	moreOptions['licensefile'] 					= args.licensefile
	moreOptions['domain'] 						= args.domain
	moreOptions['namespaceprefix'] 				= args.namespaceprefix
	moreOptions['abbreviationsinfile'] 			= args.abbreviationsinfile
	moreOptions['abbreviationlength'] 			= args.abbreviationlength
	moreOptions['xsdtargetnamespace'] 			= args.xsdtargetnamespace
	moreOptions['xsdnamespacemapping']			= args.xsdnamespacemapping
	moreOptions['modelversion'] 				= args.modelversion
	moreOptions['outputFormat']					= args.outputFormat
	moreOptions['svgwithattributes']			= args.svgwithattributes
	moreOptions['cdtversion']					= args.cdtversion


	# Read input file. Check for correct format

	if inputFormat == 'sdt2':
		domain, nameSpaces = readSDTXML(inFile, 2)
		if not checkForNamespace(nameSpaces, 'http://homegatewayinitiative.org/xml/dal/2.0'):
			print('[red]ERROR: Namespace "http://homegatewayinitiative.org/xml/dal/2.0" not found in input file.')
			return

	elif inputFormat == 'sdt3':
		domain, nameSpaces = readSDTXML(inFile, 3)
		if not checkForNamespace(nameSpaces, 'http://homegatewayinitiative.org/xml/dal/3.0'):
			print('[red]ERROR: Namespace "http://homegatewayinitiative.org/xml/dal/3.0" not found in input file.')
			return

	elif inputFormat == 'sdt4':
		domain, nameSpaces = readSDTXML(inFile, 4)
		if not checkForNamespace(nameSpaces, 'http://www.onem2m.org/xml/sdt/4.0'):
			print('[red]ERROR: Namespace "http://www.onem2m.org/xml/sdt/4.0" not found in input file.')
			return

	# Output to destination format
	if   args.outputFormat == 'plain':		outputResult(outFile, SDTPrinter.printPlain(domain, moreOptions))
	elif args.outputFormat == 'opml':		outputResult(outFile, SDTPrinter.printOPML(domain, moreOptions))
	elif args.outputFormat == 'markdown':	outputResult(outFile, SDTPrinter.printMarkdown(domain, moreOptions))
	elif args.outputFormat == 'sdt3':		outputResult(outFile, SDTPrinter.printSDT3(domain, inputFormat, moreOptions))
	elif args.outputFormat == 'sdt4':		outputResult(outFile, SDTPrinter.printSDT4(domain, inputFormat, moreOptions))
	elif args.outputFormat == 'java':		SDTPrinter.printJava(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'vorto-dsl':	SDTPrinter.printVortoDSL(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'onem2m-svg':	SDTPrinter.printOneM2MSVG(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'onem2m-xsd':	SDTPrinter.printOneM2MXSD(domain, inputFormat, outFile, moreOptions)
	elif args.outputFormat == 'apjson':		outputResult(outFile, SDTPrinter.printApJSON(domain, inputFormat, outFile, moreOptions))
	elif args.outputFormat == 'swagger':	SDTPrinter.printSwagger(domain, inputFormat, outFile, moreOptions)


if __name__ == "__main__":
	main(sys.argv[1:])
