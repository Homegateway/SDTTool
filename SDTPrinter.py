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

	_makeDir(directory)
	print3JavaClasses(domain, directory, options)


def printVortoDSL(domain, inputFormat, directory, options):
	if (inputFormat != 'sdt3'):
		print('Only the input format "sdt3" is supported yet')
		return
	if (directory == None):
		print('-o <directory> must be specified')
		return

	_makeDir(directory)
	print3VortoDSL(domain, directory, options)


def printOneM2MSVG(domain, inputFormat, directory, options):
	if (inputFormat != 'sdt3'):
		print('Only the input format "sdt3" is supported yet')
		return
	if (directory == None):
		print('-o <directory> must be specified')
		return

	_makeDir(directory)
	#SDT3PrintOneM2MSVG.print3OneM2MSVG(domain, directory, options)
	print3OneM2MSVG(domain, directory, options)


def printOneM2MXSD(domain, inputFormat, directory, options):
	if (inputFormat != 'sdt3'):
		print('Only the input format "sdt3" is supported yet')
		return
	if (directory == None):
		print('-o <directory> must be specified')
		return

	_makeDir(directory)
	print3OneM2MXSD(domain, directory, options)


##############################################################################

def _makeDir(directory):
	try:
		path = pathlib.Path(directory)
		path.mkdir(parents=True)
	except FileExistsError as e:
		# ignore existing directory for now
		pass
