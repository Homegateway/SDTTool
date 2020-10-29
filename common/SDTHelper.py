#	SDTHelper.py
#
#	Helpers
#
import os, pathlib, time, datetime, argparse, textwrap


# Sanitize a name 
def sanitizeName(name, isClass):
	if (name == None or len(name) == 0):
		return ''
	result = name
	if (isClass):
		result = result[0].upper() + name[1:]
	else:
		result = result[0].lower() + name[1:]
	result =  result.replace(' ', '')\
					.replace('/', '')\
					.replace('.', '')\
					.replace(' ', '')\
					.replace("'", '')\
					.replace('´', '')\
					.replace('`', '')\
					.replace('(', '_')\
					.replace(')', '_')\
					.replace('-', '_')
	return result

# Sanitize the package name
def sanitizePackage(package):
	result = package.replace('/', '.')
	return result

# get a versioned filename
def getVersionedFilename(fileName, extension, name=None, path=None, isModule=False, isAction=False, isSubDevice=False, isEnum=False, isShortName=False, modelVersion=None, namespacePrefix=None):

	prefix  = ''
	postfix = ''
	if name is not None:
		prefix += sanitizeName(name, False) + '_'
	else:
		if namespacePrefix:
			prefix += namespacePrefix.upper() + '-'
			if fileName.startswith(namespacePrefix+':'):
				fileName = fileName[len(namespacePrefix)+1:]
		if isAction:
			prefix += 'act-'
		if isModule:
			prefix += 'mod-'
		# if isEnum:
		# 	prefix += 'enu-'
		if isShortName:
			prefix += 'snm-'

	if modelVersion:
		postfix += '-v' + modelVersion.replace('.', '_')

	fullFilename = ''
	if path:
		fullFilename = path + os.sep
	fullFilename += prefix + sanitizeName(fileName, False) + postfix + '.' + extension

	return fullFilename


def makeDir(directory, parents=True):
	"""	Create a directory including missing parents.
		If the directory exists then this is ignored.
		Return: the path object of the new directory
	"""
	try:
		path = pathlib.Path(directory)
		path.mkdir(parents=parents)
	except FileExistsError:
		# ignore existing directory for now
		pass
	return path


# Create package path and make directories
def getPackage(directory, domain):
	path = makeDir(directory)
	return sanitizePackage(domain.id), path


# Export the content for a ModuleClass or Device
def exportArtifactToFile(name, path, extension, content, isModule=True):
	fileName = getVersionedFilename(name, extension, path=str(path), isModule=isModule)
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(content)		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


# Get a timestamp
def getTimeStamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')


def deleteEmptyFile(filename):
	if os.stat(filename).st_size == 0:
		os.remove(filename)  

#############################################################################
#
#	Tabulator handling
# tabulator level
tab = 0
tabChar = '\t'

def incTab():
	global tab
	tab += 1

def decTab():
	global tab
	if (tab > 0):
		tab -= 1

def setTabChar(val):
	global tabChar
	tabChar = val

def getTabIndent():
	global tabChar
	result = ''
	for _ in range(tab):
		result += tabChar
	return result

def newLine():
	global tab
	result = '\n'
	result += getTabIndent()
	return result


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