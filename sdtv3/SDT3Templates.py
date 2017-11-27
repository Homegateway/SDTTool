#	SDT3Templates.py
#
#	Print SDT3 with templates

import re
from .SDT3Classes import *
from common.SDTHelper import *
from common.SDTAbbreviate import *

import jinja2
from jinja2 import contextfunction

class SDT3Enum():
	def __init__(self, name):
		self.name = name


templates = {
	'markdown'		: ('markdown.tpl', True, None),
	'onem2m-xsd'	: ('onem2m-xsd.tpl', False, 'xsd')
}
actions = set()
enumTypes = set()

# constants for abbreviation file
constAbbreviationCSVFile = '_Abbreviations.csv'
constAbbreviationMAPFile = '_Abbreviations.py'

def print3SDT(domain, options, directory=None):
	context = getContext(domain, options, directory)
	if context['isSingleFile']:
		result = render(context['templateFile'], context)
		return result
	else:
		renderMultiple(context['templateFile'], context, domain, directory, context['extension'])



def render(templateFile, context):
	_, filename = os.path.split(templateFile)
	(path, _) = os.path.split(os.path.realpath(__file__))
	return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path + '/templates'),
        trim_blocks=True,
        lstrip_blocks=True
    ).get_template(filename).render(context)



def renderMultiple(templateFile, context, domain, directory, extension):
	try:
		path = context['path']
		if path:
			path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now
	

	# Read abbreviations
	readAbbreviations(context['abbreviationsinfile'])
	# Add already existing abbreviations
	localAbbreviationsfile = str(context['path']) + os.sep + constAbbreviationCSVFile
	readAbbreviations(localAbbreviationsfile, predefined=False)


	# Export ModuleClasses
	for module in domain.modules:
		context['object'] = module
		renderComponentToFile(context, isModule=True)

	# Export Devices
	for device in domain.devices:
		context['object'] = device
		renderComponentToFile(context)

	# Export enum types
	for enm in enumTypes:
		context['object'] = enm
		renderComponentToFile(context, isEnum=True)

	# Export found Actions
	for action in actions:
		context['object'] = action
		renderComponentToFile(context, isAction=True)

	# Export abbreviations
	exportAbbreviations(str(context['path']) + os.sep + constAbbreviationCSVFile, \
		str(context['path']) + os.sep + constAbbreviationMAPFile,\
		getAbbreviations())



def getContext(domain, options, directory=None):

	path = None
	if directory:
		path = pathlib.Path(directory)	

	# read the optional licensefile into the header
	lfile = options['licensefile']
	licenseText = ''
	if lfile != None:
		with open(lfile, 'rt') as f:
			licenseText = f.read()

	templateFile, isSingleFile, extension = templates[options['outputFormat']]

	return {
		'domain'						: domain,
	    'hideDetails'					: options['hideDetails'],
    	'pageBreakBeforeMCandDevices'	: options['pageBreakBeforeMCandDevices'],
    	'licensefile'					: options['licensefile'],
    	'namespaceprefix'				: options['namespaceprefix'],
    	'xsdtargetnamespace' 			: options['xsdtargetnamespace'],
    	'abbreviationsinfile'			: options['abbreviationsinfile'],
    	'modelversion'					: options['modelversion'],
    	'domaindefinition'				: options['domain'],
    	'license'						: licenseText,
    	'path'							: path,
		'package'						: sanitizePackage(domain.id),
		'templateFile'					: templateFile,
		'extension'						: extension,
		'isSingleFile'					: isSingleFile,

    	# pointer to functions
    	'renderComponentToFile'			: renderComponentToFile,
    	'instanceType'					: instanceType,
    	'incLevel'						: incLevel,
    	'decLevel'						: decLevel,
    	'getLevel'						: getLevel,
    	'match'							: match,
    	'addToActions'					: addToActions,
    	'addToEnums'					: addToEnums,
    	'getVersionedFilename'			: getVersionedFilename,
    	'sanitizeName'					: sanitizeName,
    	'renderObject'					: renderObject
	}



#############################################################################
#
#	Helpers for template processing
#


def renderComponentToFile(context, name=None, isModule=False, isEnum=False, isAction=False, namespaceprefix=None):
	""" Render a component. """
	namespaceprefix = context['namespaceprefix'] if 'namespaceprefix' in context else None
	fileName     	= sanitizeName(context['object'].name if isModule or isEnum or isAction else context['object'].id, False)
	#print('---' + fileName)
	fullFilename 	= getVersionedFilename(fileName, context['extension'], name=name, path=str(context['path']), isModule=isModule, isEnum=isEnum, isAction=isAction, modelVersion=context['modelversion'], namespacePrefix=namespaceprefix)
	outputFile   	= None
	try:
		outputFile = open(fullFilename, 'w')
		outputFile.write(render(context['templateFile'], context))
	except IOError as err:
		print('File not found: ' + str(err))
	finally:
		if outputFile != None:
			outputFile.close()


def sanitizeName(name, isClass, annc=False):
	""" Sanitize a (file)name. Also add it to the list of abbreviations. """
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
	# If this name is an announced resource, add "Annc" Postfix to both the
	# name as well as the abbreviation.
	if ':' not in name:	# ignore, for example, type/enum definitions
		if annc:
			abbr = abbreviate(result)
			addAbbreviation(result + 'Annc', abbr + 'Annc')
		else:
			abbr = abbreviate(result)
			addAbbreviation(result, abbr)
	return result


def instanceType(ty):
	""" Return the type of an object as a string. """
	#print(type(ty).__name__)
	return type(ty).__name__

level = 1


def incLevel(name=None):
	""" Decrement the current indention level. """
	global level
	level = level + 1
	if name:
		return ''.rjust(level, '#') + ' ' + name
	return ''


def decLevel():
	""" Increment the current indention level. """
	global level
	level = level - 1
	if level == 0:
		level = 1
	return ''


def getLevel():
	""" Return the current indention level. """
	return level


def match(expr, val):
	""" Support method: provide matching to templates. """
	return re.match(expr, val)


def addToActions(action):
	""" Add an action to the list of action found during rendering. """
	actions.add(action)
	return ''


def addToEnums(enum):
	""" Add an enum to th elist of enums found during rendering. """
	enumTypes.add(SDT3Enum(enum))
	return ''

@contextfunction
def renderObject(context, object):
	""" Recursively render another (sub)object while the other is till rendering. """
	newContext = {key: value for key, value in context.items()}
	if isinstance(object, SDT3SubDevice):
		newContext['object'] = object
		renderComponentToFile(newContext)
	return ''

