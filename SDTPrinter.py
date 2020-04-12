#	SDTPrinter.py
#
#	Print an SDT in various formats

import os, pathlib

from sdtv2.SDT2PrintMarkdown import print2DomainMarkdown
from sdtv2.SDT2PrintOPML import print2DomainOPML
from sdtv2.SDT2PrintPlain import print2DomainPlain
from sdtv2.SDT2PrintSDT3 import print2DomainSDT3
from sdtv3.SDT3PrintMarkdown import print3DomainMarkdown
from sdtv3.SDT3PrintOPML import print3DomainOPML
from sdtv3.SDT3PrintPlain import print3DomainPlain
from sdtv3.SDT3PrintJava import print3JavaClasses
from sdtv3.SDT3PrintVortoDSL import print3VortoDSL
from sdtv3.SDT3PrintOneM2MSVG import print3OneM2MSVG
from sdtv3.SDT3PrintOneM2MXSD import print3OneM2MXSD
from sdtv3.SDT3PrintSwagger import print3Swagger
from sdtv3.SDT3Templates import print3SDT
from sdtv3.SDT3PrintSDT4 import print2DomainSDT4
from sdtv4.SDT4PrintOneM2MSVG import print4OneM2MSVG
from sdtv4.SDT4Templates import print4SDT



def printPlain(domain, options):
	printers = {
		'2' : print2DomainPlain,
		'3' : print3DomainPlain
	}
	if domain == None:
		return
	return printers[domain._version](domain, options)
	# if domain._version == '2':
	# 	return print2DomainPlain(domain, options)
	# elif domain._version == '3':
	# 	return print3DomainPlain(domain, options)

def printOPML(domain, options):
	if domain == None:
		return
	if domain._version == '2':
		return print2DomainOPML(domain, options)
	elif domain._version == '3':
		return print3DomainOPML(domain, options)
	else:
		print('Output format is not supported')
		return ''

def printMarkdown(domain, options):
	if domain == None:
		return
	if domain._version == '2':
		return print2DomainMarkdown(domain, options)
	elif domain._version == '3':
		return print3SDT(domain, options)
	elif domain._version == '4':
		return print4SDT(domain, options)

def printSDT3(domain, inputFormat, options):
	if domain == None:
		return
	if domain._version == '2' and inputFormat == 'sdt2':
		return print2DomainSDT3(domain, options)
	else:
		print('Conversion is not supported')
		return ''

def printSDT4(domain, inputFormat, options):
	if domain == None:
		return
	if domain._version == '3' and inputFormat == 'sdt3':
		return print2DomainSDT4(domain, options)
	else:
		print('Conversion is not supported')
		return ''


def printJava(domain, inputFormat, directory, options):
	if inputFormat != 'sdt3':
		print('Only the input format "sdt3" is supported')
		return
	if directory == None:
		print('-o <directory> must be specified')
		return

	_makeDir(directory)
	print3JavaClasses(domain, directory, options)


def printVortoDSL(domain, inputFormat, directory, options):
	if inputFormat != 'sdt3':
		print('Only the input format "sdt3" is supported')
		return
	if directory == None:
		print('-o <directory> must be specified')
		return

	_makeDir(directory)
	print3VortoDSL(domain, directory, options)


def printOneM2MSVG(domain, inputFormat, directory, options):
	if inputFormat not in ['sdt3', 'sdt4' ]:
		print('Only the input formats "sdt3" or "sdt4" are supported')
		return
	if directory == None:
		print('-o <directory> must be specified')
		return

	_makeDir(directory)
	if inputFormat == 'sdt3':
		print3OneM2MSVG(domain, options, directory)
	elif inputFormat == 'sdt4':
		print4OneM2MSVG(domain, options, directory)



def printOneM2MXSD(domain, inputFormat, directory, options):
	if domain == None:
		return
	if inputFormat not in ['sdt3', 'sdt4']:
		print('Only the input formats "sdt3" and "sdt4" are supported')
		return
	if directory == None:
		print('-o <directory> must be specified')
		return
	modelVersion = options['modelversion']
	if modelVersion is None:
		print('--modelVersion <version> must be specified')
		return

	_makeDir(directory)
	if domain._version == '3':
		return print3SDT(domain, options, directory)
	elif domain._version == '4':
		return print4SDT(domain, options, directory)
	return ''


def printSwagger(domain, inputFormat, directory, options):
	if inputFormat != 'sdt3':
		print('Only the input format "sdt3" is supported')
		return
	if directory == None:
		print('-o <directory> must be specified')
		return

	_makeDir(directory)
	print3Swagger(domain, directory, options)



##############################################################################

def _makeDir(directory):
	try:
		path = pathlib.Path(directory)
		path.mkdir(parents=True)
	except FileExistsError as e:
		# ignore existing directory for now
		pass
