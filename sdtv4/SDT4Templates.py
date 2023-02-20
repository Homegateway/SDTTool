#	SDT4Templates.py
#
#	Print SDT4 with templates

from __future__ import annotations
import re
from typing import Any
from .SDT4Classes import *
from common.SDTHelper import *
from common.SDTAbbreviate import *
from rich import print


import jinja2
from jinja2 import contextfunction

class SDT4DataTypes(object):
	def __init__(self, dataTypes):
		self.dataTypes = dataTypes


class SDT4Commons(object):
	def __init__(self, name):
		self.name = name
		self.extendedModuleClasses = dict()
		self.extendedModuleClassesExtend = dict()
		self.extendedSubDevices = dict()
		self.extendedSubDevicesExtend = dict()


templates = {
	'markdown'		: ('markdown.tpl', None, True, None),
	'onem2m-xsd'	: ('onem2m-xsd.tpl', 'enumerationTypes', False, 'xsd'),
	'apjson'		: ('apjson.tpl', None, True, None),
}


# Mapping between domain and namespace prefix
# TODO make this mapping more configurable, maybe on the command line?

namespacePrefixMappings = {
	('agd', 'org.onem2m.agriculture',	'http://www.onem2m.org/xml/protocols/agriculturedomain', 'agriculturedomain'),
	('cid', 'org.onem2m.city',			'http://www.onem2m.org/xml/protocols/citydomain', 'citydomain'),
	('cod', 'org.onem2m.common',		'http://www.onem2m.org/xml/protocols/commondomain', 'commondomain'),
	('hd',  'org.onem2m.horizontal',	'http://www.onem2m.org/xml/protocols/horizontal', 'horizontaldomain'),
	('hed', 'org.onem2m.health',		'http://www.onem2m.org/xml/protocols/healthdomain', 'healthdomain'),
	('hod', 'org.onem2m.home',			'http://www.onem2m.org/xml/protocols/homedomain', 'homedomain'),
	('ind', 'org.onem2m.industry',		'http://www.onem2m.org/xml/protocols/industrydomain', 'industrydomain'),
	('mad', 'org.onem2m.management',	'http://www.onem2m.org/xml/protocols/managementdomain', 'managementdomain'),
	('mdd', 'org.onem2m.metadata',		'http://www.onem2m.org/xml/protocols/metadata', 'metadatadomain'),
	('psd', 'org.onem2m.publicsafety',	'http://www.onem2m.org/xml/protocols/publicsafetydomain', 'publicsafetydomain'),
	('rad', 'org.onem2m.railway',		'http://www.onem2m.org/xml/protocols/railwaydomain', 'railwaydomain'),
	('ved', 'org.onem2m.vehicular',		'http://www.onem2m.org/xml/protocols/vehiculardomain', 'vehiculardomain'),
}


actions:set[SDT4Action] = set()
enumTypes:set = set()
extendedModuleClasses:dict = dict()
extendedModuleClassesExtend:dict = dict()
extendedSubDevices:dict = dict()
extendedSubDevicesExtend:dict = dict()
context = None
optionArgs = None

# constants for abbreviation file
_abbreviationCSVFile = 'Abbreviations.csv'
_undefinedAbbreviationCSVFile = 'UndefinedAbbreviations.csv'
_abbreviationMAPFile = 'Abbreviations.py'

def print4SDT(domain:SDT4Domain, options, directory = None):
	global context
	global optionArgs
	importOccursIn()
	context = getContext(domain, options, directory)
	optionArgs = options
	if context['isSingleFile']:
	# Read abbreviations
		readAbbreviations(context['abbreviationsinfile'])
		result = render(context['templateFile'], context)
		# Export NEW abbreviations
		exportAbbreviations(_abbreviationCSVFile, _abbreviationMAPFile, getAbbreviations())
		exportAbbreviations(_undefinedAbbreviationCSVFile, None, getNewAbbreviations())
		return result
	else:
		renderMultiple(context['templateFile'], context, domain, directory, context['extension'])
	printShortNames(context) # TODO improve printShortnames
	exportOccursIn()



def render(templateFile, context):
	_, filename = os.path.split(templateFile)
	(path, _) = os.path.split(os.path.realpath(__file__))
	#print(context)
	return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path + '/templates'),
        trim_blocks=True,
        lstrip_blocks=True
    ).get_template(filename).render(context)



def renderMultiple(templateFile:str, context:dict, domain:SDT4Domain, directory:str, extension:str):
	try:
		path = context['path']
		if path:
			path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now
	
	# Prefix for abbreviation files
	prefix = f'{context["namespaceprefix"]}-{"dev-" if domain.id.endswith("device") else "mod-"}'
	


	# Read abbreviations
	readAbbreviations(context['abbreviationsinfile'])
	# Add already existing abbreviations
	readAbbreviations(f'{str(context["path"])}{os.sep}{prefix}{_abbreviationCSVFile}', predefined=False)


	# Export ModuleClasses
	for moduleClass in domain.moduleClasses:
		context['object'] = moduleClass
		# Do an abbreviation first
		abbreviate(moduleClass.name)
		renderComponentToFile(context, outType = OutType.moduleClass)

	# Export Devices
	for subDevice in domain.subDevices:
		context['object'] = subDevice
		abbreviate(subDevice.id)
		renderComponentToFile(context, outType = OutType.subDevice)

	# Export Devices
	for deviceClass in domain.deviceClasses:
		context['object'] = deviceClass
		abbreviate(deviceClass.id)
		renderComponentToFile(context, outType = OutType.device)

	# Export enum types

	context['object'] = SDT4DataTypes(domain.dataTypes)
	renderComponentToFile(context, outType = OutType.enumeration)
	# for dataType in domain.dataTypes:
	# 	if isinstance(dataType.type, SDT4EnumType):
	# 		print(dataType)
	# for enm in enumTypes:
	# 	context['object'] = enm
	# 	renderComponentToFile(context, isEnum=True)

	# Export found Actions
	for action in actions:
		context['object'] = action
		abbreviate(action.name)
		renderComponentToFile(context, outType = OutType.action)

	# Export extras
	commons = SDT4Commons('commonTypes')
	commons.extendedModuleClasses = extendedModuleClasses
	commons.extendedModuleClassesExtend = extendedModuleClassesExtend
	commons.extendedSubDevices = extendedSubDevices
	commons.extendedSubDevicesExtend = extendedSubDevicesExtend
	context['object'] = commons
	renderComponentToFile(context, outType = OutType.unknown)

	# Export abbreviations
	exportAbbreviations(f'{context["path"]}{os.sep}{prefix}{_abbreviationCSVFile}',
						f'{context["path"]}{os.sep}{prefix}{_abbreviationMAPFile}',
						getAbbreviations())
	exportAbbreviations(f'{context["path"]}{os.sep}{prefix}{_undefinedAbbreviationCSVFile}', None, getNewAbbreviations())
	#exportAbbreviations(f'{context["path"]}{os.sep}{domain.id}-{_undefinedAbbreviationCSVFile}', None, getNewAbbreviations())
		


def getContext(domain:SDT4Domain, options:dict, directory:str = None) -> dict[str, Any]:

	path = None
	if directory:
		path = pathlib.Path(directory)

	# read the optional licensefile into the header
	lfile = options['licensefile']
	licenseText = ''
	if lfile != None:
		with open(lfile, 'rt') as f:
			licenseText = f.read()

	templateFile, enumerationsFile, isSingleFile, extension = templates[options['outputFormat']]
	print(options['xsdtargetnamespace'])
	return {
		'domain'						: domain,
	    'hideDetails'					: options['hideDetails'],
    	'markdownPageBreak'				: options['markdownPageBreak'],
    	'licensefile'					: options['licensefile'],
    	'namespaceprefix'				: options['namespaceprefix'],
    	'xsdtargetnamespace' 			: options['xsdtargetnamespace'],
    	'abbreviationsinfile'			: options['abbreviationsinfile'],
    	'modelversion'					: options['modelversion'],
    	'domaindefinition'				: options['domain'],
    	'CDTVersion'					: options['cdtversion'],
    	'license'						: licenseText,
    	'path'							: path,
		'package'						: sanitizePackage(domain.id),
		'templateFile'					: templateFile,
		'extension'						: extension,
		'isSingleFile'					: isSingleFile,
		'enumerationsFile'				: enumerationsFile,
		'extendedModuleClasses'			: extendedModuleClasses,
		'extendedModuleClassesExtend'	: extendedModuleClassesExtend,
		'extendedSubDevices'			: extendedSubDevices,
		'extendedSubDevicesExtend'		: extendedSubDevicesExtend,


    	# pointer to functions
    	'renderComponentToFile'			: renderComponentToFile,
    	'instanceType'					: instanceType,
    	'isString'						: lambda s : isinstance(s, str),
    	'getNSName'						: getNSName,
    	'incLevel'						: incLevel,
    	'decLevel'						: decLevel,
    	'getLevel'						: getLevel,
    	'match'							: match,
    	'addToActions'					: addToActions,
    	'getVersionedFilename'			: getVersionedFilename,
    	'sanitizeName'					: templateSanitizeName,
    	'renderObject'					: renderObject,
    	'debug'							: debug,
    	'countExtend'					: countExtend,
    	'countUnextend'					: countUnextend,
		'getNamespacePrefix'			: getNamespacePrefix,
		'componentName'					: componentName,
		'getNamespaceFromPrefix'		: getNamespaceFromPrefix,
		'getDomainFromPrefix'			: getDomainFromPrefix,
		'getXMLNameSpaces'				: getXMLNameSpaces,

		# Add types
		'OutType'						: OutType,
	}


#############################################################################
#
#	Shortname output
#

def printShortNames(context):
	domain = context['domain']
	namespaceprefix = context['namespaceprefix'] if 'namespaceprefix' in context else None

	# TODO
	#
	#	Sort
	#	Uniqe
	#	combined files?

	# devices
	fileName = sanitizeName(f'devices-{getTimeStamp()}', False)
	fullFilename = getVersionedFilename(fileName, 'csv', path = str(context['path']), outType = OutType.shortName, modelVersion=context['modelversion'], namespacePrefix=namespaceprefix)
	with open(fullFilename, 'w') as outputFile:
		for deviceClass in domain.deviceClasses:
			outputFile.write(f'{deviceClass.id},{getAbbreviation(deviceClass.id)}\n')
	deleteEmptyFile(fullFilename)

	# sub.devices - Instances
	fileName = sanitizeName(f'subDevicesInstances-{getTimeStamp()}', False)
	fullFilename = getVersionedFilename(fileName, 'csv', path=str(context['path']), outType = OutType.shortName, modelVersion=context['modelversion'], namespacePrefix=namespaceprefix)
	with open(fullFilename, 'w') as outputFile:
		for deviceClass in domain.deviceClasses:
			for subDevice in deviceClass.subDevices:
				outputFile.write(f'{subDevice.id},{getAbbreviation(subDevice.id)}\n')
	deleteEmptyFile(fullFilename)

	# sub.devices
	fileName = sanitizeName(f'subDevice-{getTimeStamp()}', False)
	fullFilename = getVersionedFilename(fileName, 'csv', path=str(context['path']), outType = OutType.shortName, modelVersion=context['modelversion'], namespacePrefix=namespaceprefix)
	with open(fullFilename, 'w') as outputFile:
		for name in extendedSubDevicesExtend:
			if (abbr := getAbbreviation(name)) is None:
				continue
			outputFile.write(f'{name},{abbr}\n')
	deleteEmptyFile(fullFilename)


	# ModuleClasses
	fileName = sanitizeName(f'moduleClasses-{getTimeStamp()}', False)
	fullFilename = getVersionedFilename(fileName, 'csv', path=str(context['path']), outType = OutType.shortName, modelVersion=context['modelversion'], namespacePrefix=namespaceprefix)
	with open(fullFilename, 'w') as outputFile:
		for moduleClass in domain.moduleClasses:
			outputFile.write(f'{moduleClass.name}{getAbbreviation(moduleClass.name)}\n')
		for deviceClass in domain.deviceClasses:
			for moduleClass in deviceClass.moduleClasses:
				outputFile.write(f'{moduleClass.name},{getAbbreviation(moduleClass.name)}\n')
			for subDevice in deviceClass.subDevices:
				for moduleClass in subDevice.moduleClasses:
					outputFile.write(f'{moduleClass.name},{getAbbreviation(moduleClass.name)}\n')
	deleteEmptyFile(fullFilename)


	# DataPoints
	fileName = sanitizeName(f'dataPoints-{getTimeStamp()}', False)
	fullFilename = getVersionedFilename(fileName, 'csv', path=str(context['path']), outType = OutType.shortName, modelVersion=context['modelversion'], namespacePrefix=namespaceprefix)
	with open(fullFilename, 'w') as outputFile:
		for moduleClass in domain.moduleClasses:
			for dp in moduleClass.data:
				outputFile.write(f'{dp.name},{moduleClass.name},{getAbbreviation(dp.name)}\n')
		for deviceClass in domain.deviceClasses:
			for moduleClass in deviceClass.moduleClasses:
				for dp in moduleClass.data:
					outputFile.write(f'{dp.name},{moduleClass.name},{getAbbreviation(dp.name)}\n')
			for subDevice in deviceClass.subDevices:
				for moduleClass in deviceClass.moduleClasses:
					for dp in moduleClass.data:
						outputFile.write(f'{dp.name},{moduleClass.name},{getAbbreviation(dp.name)}\n')
	deleteEmptyFile(fullFilename)


	# Actions
	fileName = sanitizeName(f'actions-{getTimeStamp()}', False)
	fullFilename = getVersionedFilename(fileName, 'csv', path=str(context['path']), outType = OutType.shortName, modelVersion=context['modelversion'], namespacePrefix=namespaceprefix)
	with open(fullFilename, 'w') as outputFile:
		for moduleClass in domain.moduleClasses:
			for ac in moduleClass.actions:
				outputFile.write(f'{ac.name},{getAbbreviation(ac.name)}\n')
		for deviceClass in domain.deviceClasses:
			for moduleClass in deviceClass.moduleClasses:
				for ac in moduleClass.actions:
					outputFile.write(f'{ac.name},{getAbbreviation(ac.name)}\n')
			for subDevice in deviceClass.subDevices:
				for moduleClass in deviceClass.moduleClasses:
					for ac in moduleClass.actions:
						outputFile.write(f'{ac.name},{getAbbreviation(ac.name)}\n')
	deleteEmptyFile(fullFilename)



#############################################################################
#
#	Helpers for template processing
#


def renderComponentToFile(context, name:str = None, outType:OutType = OutType.unknown, namespaceprefix:str = None):
	""" Render a component. """
	namespaceprefix = context['namespaceprefix'] if 'namespaceprefix' in context else None

	if outType == OutType.subDevice and context['object'].extend:
		fileName = sanitizeName(context['object'].extend.entity, False)
	elif outType == OutType.enumeration:
		fileName = sanitizeName(context['enumerationsFile'], False)
	else:
		fileName = sanitizeName(context['object'].name if outType in [ OutType.moduleClass, OutType.enumeration, OutType.action, OutType.unknown ] else context['object'].id, False)
	fullFilename = getVersionedFilename(fileName, context['extension'], name = name, path = str(context['path']), outType = outType, namespacePrefix = namespaceprefix)
	#print('---' + fullFilename)
	outputFile   = None
	try:
		with open(fullFilename, 'w') as outputFile:
			# print(fullFilename)
			outputFile.write(render(context['templateFile'], context))
	except IOError as err:
		print(f'[red]File not found: {str(err)}')



def templateSanitizeName(name, isClass, annc = False, elementType:ElementType = None, occursIn:str = None):
	""" Sanitize a (file)name. Also add it to the list of abbreviations. """

	result = sanitizeName(name, isClass)
	# If this name is an announced resource, add "Annc" Postfix to both the
	# name as well as the abbreviation.
	if ':' not in name:	# ignore, for example, type/enum definitions
		abbr = abbreviate(result, optionArgs['abbreviationlength'], elementType, occursIn)
		addAbbreviation(f'{result}{"Annc" if annc else ""}', f'{abbr}{"Annc" if annc else ""}')
		# if annc:
		# 	addAbbreviation(f'{result}Annc', f'{abbr}')
		# else:
		# 	addAbbreviation(result, abbr)
		# if annc:
		# 	abbr = abbreviate(result)
		# 	addAbbreviation(result + 'Annc', abbr + 'Annc')
		# else:
		# 	abbr = abbreviate(result)
		# 	addAbbreviation(result, abbr)
	return result


def instanceType(ty, withNameSpace=True):
	""" Return the type of an object as a string. Replace domain with namespace, if set.
	"""
	# print(type(ty).__name__)

	# Handle just strings
	if isinstance(ty, str): # ty is just a string and contains the type already
		return str
	# Handle normal classes
	tyn = type(ty).__name__
	if tyn in ['SDT4ModuleClass', 'SDT4ArrayType', 'SDT4SimpleType', 'SDT4EnumType', 'SDT4Action', 'SDT4DeviceClass', 'SDT4SubDevice', 'SDT4Commons', 'SDT4DataTypes', 'NoneType']:
		return tyn

	# Handle data types
	ns = context['namespaceprefix']
	if ty.type is None and ty.extend is not None:
		# print(ty.extend.entity)
		if ty.extend.domain == context['domain'].id and ns is not None:
			return f'{ns}:{ty.extend.entity}' if withNameSpace else ty.extend.entity
		return f'{ty.extend.domain}:{ty.extend.entity}' if withNameSpace else ty.extend.entity
	return type(ty.type).__name__


def getNSName(name) -> str:
	""" Return the correct name, including namespace prefix, if set. """
	return '%s:%s' % (context['namespaceprefix'], name) if context['namespaceprefix'] is not None else name


def countExtend(lst) -> int:
	return sum(map(lambda o : o.extend is not None, lst))
	# cnt = 0
	# for obj in lst:
	# 	if obj.extend is not None:
	# 		cnt += 1
	# return cnt


def countUnextend(lst) -> int:
	return len(lst) - countExtend(lst)


# def shortname(name):
# 	abbr = abbreviate(name, optionArgs['abbreviationlength'])
# 	addAbbreviation(name, abbr)
# 	return abbr


def getNamespacePrefix(obj) -> str:
	"""	Try to map the extended domain to a short name prefix.
		Otherwise return the defined namespace prefix for this object.
	"""
	if obj.extend is not None:
		domain = obj.extend.domain
		for (k,v,d, do) in namespacePrefixMappings:
			if domain.startswith(v):
				return k
		print(f'[yellow]WARNING: No definition found for domain: {domain}')
		return context['namespaceprefix']
	return context['namespaceprefix']


def getNamespaceFromPrefix(prfx:str) -> str:
	"""	Try to find the full prefix from the short prefix.
	"""
	for (k,v,d, do) in namespacePrefixMappings:
		if k == prfx:
			return v
	print(f'[red]Namespace not found for prefix: {prfx}')
	return None


def getDomainFromPrefix(prfx:str) -> str:
	for (k,v,d, do) in namespacePrefixMappings:
		if k == prfx:
			return do
	print(f'[red]Namespace not found for prefix: {prfx}')
	return None


def getXMLNameSpaces():
	result = ''
	for (k,v,d, do) in namespacePrefixMappings:
		result += f'xmlns:{k}="{d}" '
	return result


def componentName(obj):
	"""	Return the name or id of an SDT object as a string.
		If the object extends another object then that name is returned.
	"""
	if obj.extend is not None:
		return obj.extend.entity
	return obj.id if isinstance(obj, (SDT4DeviceClass, SDT4SubDevice)) else obj.name


#
#	Header level
#

level = 1

def incLevel(name=None) -> str:
	""" Increment the current indention level. """
	global level
	level += 1
	return ''.rjust(level, '#') + ' ' + name if name else ''


def decLevel() -> str:
	""" Decrement the current indention level. """
	global level
	level -= 1
	if level == 0:
		level = 1
	return ''


def getLevel() -> str:
	""" Return the current indention level. """
	return level


def debug(txt) -> str:
	""" Print text to console."""
	print(txt)
	return ''


def match(expr, val):
	""" Support method: provide matching to templates. """
	return re.match(expr, val)


def addToActions(action):
	""" Add an action to the list of action found during rendering. """
	actions.add(action)
	return ''


@contextfunction
def renderObject(context, object):
	""" Recursively render another (sub)object while the other is till rendering. """
	newContext = {key: value for key, value in context.items()} # Copy the old context
	if isinstance(object, SDT4SubDevice):
		if object.extend is None:	# Only when not extending
			newContext['object'] = object
			renderComponentToFile(newContext, outType = OutType.subDevice)
	return ''

