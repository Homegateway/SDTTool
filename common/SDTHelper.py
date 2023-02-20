#	SDTHelper.py
#
#	Helpers
#
from enum import IntEnum, auto
import os, pathlib, time, datetime, argparse, textwrap
from pathlib import Path


class OutType(IntEnum):
	action			= auto()
	device			= auto()
	enumeration 	= auto()
	moduleClass		= auto()
	shortName 		= auto()
	subDevice		= auto()
	unknown			= auto()

	def prefix(self) -> str:
		return {
			self.action: 'act-',
			self.device: 'dev-',
			self.enumeration: '',
			self.moduleClass: 'mod-',
			self.shortName: 'snm',
			self.subDevice: 'sub-',
			self.unknown: '',
		}[self.value]

	
# Sanitize a name 
def sanitizeName(name:str, isClass:bool) -> str:
	if not name:
		return ''
	result = name
	result = f'{result[0].upper() if isClass else result[0].lower()}{name[1:]}'
	# if isClass:
	# 	result = result[0].upper() + name[1:]
	# else:
	# 	result = result[0].lower() + name[1:]
	return result.replace(' ', '')\
				 .replace('/', '')\
				 .replace('.', '')\
				 .replace(' ', '')\
				 .replace("'", '')\
				 .replace('´', '')\
				 .replace('`', '')\
				 .replace('(', '_')\
				 .replace(')', '_')\
				 .replace('-', '_')

# Sanitize the package name
def sanitizePackage(package:str) -> str:
	return  package.replace('/', '.')

# get a versioned filename
def getVersionedFilename(fileName:str, extension:str='', name:str = None, path:str = None, outType:OutType = OutType.device, modelVersion:str = None, namespacePrefix:str = None):

	prefix  = ''
	postfix = ''
	if name is not None:
		prefix += f'{sanitizeName(name, False)}_'
	else:
		if namespacePrefix:
			prefix += namespacePrefix.upper() + '-'
			if fileName.startswith(namespacePrefix+':'):
				fileName = fileName[len(namespacePrefix)+1:]
		prefix += f'{outType.prefix()}'

	if modelVersion:
		postfix += f'-v{modelVersion.replace(".", "_")}'

	fullFilename = ''
	if path:
		fullFilename = path + os.sep
	fullFilename += f'{prefix}{sanitizeName(fileName, False)}{postfix}'
	if extension:
		fullFilename += f'.{extension}'

	return fullFilename


def makeDir(directory:str, parents:bool = True) -> Path:
	"""	Create a directory including missing parents.
		If the directory exists then this is ignored.
		Return: the path object of the new directory
	"""
	try:
		path = pathlib.Path(directory)
		path.mkdir(parents = parents)
	except FileExistsError:
		# ignore existing directory for now
		pass
	return path


# Create package path and make directories
def getPackage(directory, domain):
	path = makeDir(directory)
	return sanitizePackage(domain.id), path


# Export the content for a ModuleClass or Device
def exportArtifactToFile(name:str, path:str, extension:str, content, outType:OutType = OutType.moduleClass) -> None:
	fileName = getVersionedFilename(name, extension, path = str(path), outType = outType)
	outputFile = None
	try:
		with open(fileName, 'w') as outputFile:
			outputFile.write(content)		
	except IOError as err:
		print(err)


# Get a timestamp
def getTimeStamp() -> str:
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')


def deleteEmptyFile(filename:str) -> None:
	if os.stat(filename).st_size == 0:
		os.remove(filename)  

#############################################################################
#
#	Tabulator handling
# tabulator level
tab = 0
tabChar = '\t'

def incTab() -> None:
	global tab
	tab += 1

def decTab() -> None:
	global tab
	if tab > 0:
		tab -= 1

def setTabChar(val:str) -> None:
	global tabChar
	tabChar = val

def getTabIndent() -> str:
	return ''.join(tabChar for _ in range(tab))

def newLine() -> str:
	return f'\n{getTabIndent()}'

	# result = '\n'
	# result += getTabIndent()
	# return result


#
#	Helper methods for argument parsing
#

def convertArgLineToArgs(arg_line):
	"""	Convert single lines to arguments. Deliver one at a time.
		Skip empty lines.
	"""
	for arg in arg_line.split():
		if not arg.strip():
			continue
		yield arg

class MultilineFormatter(argparse.HelpFormatter):
	"""	Formatter for argparse.
	"""
	def _fill_text(self, text, width, indent):
		text = self._whitespace_matcher.sub(' ', text).strip()
		paragraphs = text.split('|n ')
		multiline_text = ''
		for paragraph in paragraphs:
			formatted_paragraph = textwrap.fill(paragraph, width, initial_indent=indent, subsequent_indent=indent) + '\n'
			multiline_text = multiline_text + formatted_paragraph
		return multiline_text