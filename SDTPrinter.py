#	SDTPrinter.py
#
#	Print an SDT in various formats

import os

from SDT2PrintMarkdown import print2DomainMarkdown
from SDT2PrintOPML import print2DomainOPML
from SDT2PrintPlain import print2DomainPlain
from SDT2PrintSDT3 import print2DomainSDT3
from SDT3PrintMarkdown import print3DomainMarkdown
from SDT3PrintOPML import print3DomainOPML
from SDT3PrintPlain import print3DomainPlain
from SDT3PrintJava import print3JavaClasses
from SDT3PrintVortoDSL import print3VortoDSL
from SDT3PrintOneM2MSVG import print3OneM2MSVG


def printPlain(domain, options):
	if (domain == None):
		return
	if (domain._version == '2'):
		return print2DomainPlain(domain, options)
	elif (domain._version == '3'):
		return print3DomainPlain(domain, options)

def printOPML(domain, options):
	if (domain == None):
		return
	if (domain._version == '2'):
		return print2DomainOPML(domain, options)
	elif (domain._version == '3'):
		return print3DomainOPML(domain, options)

def printMarkdown(domain, options):
	if (domain == None):
		return
	if (domain._version == '2'):
		return print2DomainMarkdown(domain, options)
	elif (domain._version == '3'):
		return print3DomainMarkdown(domain, options)


def printSDT3(domain, inputFormat, options):
	if (domain == None):
		return
	if (domain._version == '2' and inputFormat == 'sdt2'):
		return print2DomainSDT3(domain, options)
	else:
		print('Conversion is not supported')
		return ''


def printJava(domain, inputFormat, directory, options):
	if (inputFormat != 'sdt3'):
		print('Only the input format "sdt3" is supported yet')
		return
	if (directory == None):
		print('-o <directory> must be specified')
		return

	try:
		os.mkdir(directory)
	except FileExistsError as e:
		# ignore existing directory for now
		pass

	print3JavaClasses(domain, directory, options)


def printVortoDSL(domain, inputFormat, directory, options):
	if (inputFormat != 'sdt3'):
		print('Only the input format "sdt3" is supported yet')
		return
	if (directory == None):
		print('-o <directory> must be specified')
		return

	try:
		os.mkdir(directory)
	except FileExistsError as e:
		# ignore existing directory for now
		pass

	print3VortoDSL(domain, directory, options)


def printOneM2MSVG(domain, inputFormat, directory, options):
	if (inputFormat != 'sdt3'):
		print('Only the input format "sdt3" is supported yet')
		return
	if (directory == None):
		print('-o <directory> must be specified')
		return

	try:
		os.mkdir(directory)
	except FileExistsError as e:
		# ignore existing directory for now
		pass

	print3OneM2MSVG(domain, directory, options)


