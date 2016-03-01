#	SDT3PrintVortoDSL.py
#
#	Generate Vorto Information Model from SDT3 

# TODO export properties

import datetime, os, pathlib, string
from SDT3Classes import *

# Define the version of the Vorto import model
vortoModelVersion = '1.0.0'

# Define the vorto model category
vortoModelCategory = 'SDT3'

# Dictionary to temporarly store the found structs.
structs = {}

# Dictionary to temporarly store necessary imports
imports = {}


def print3VortoDSL(domain, directory, options):

	# Create package path and make directories

	packagePath = directory + os.sep + domain.id.replace('.', os.sep)
	path = pathlib.Path(packagePath)
	try:
		path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now
	package = sanitizePackage(domain.id)

	# Export ModuleClasses

	for module in domain.modules:
		exportModuleClass(module, package, path)

	# Export Devices

	for device in domain.devices:
		exportDevice(device, package, path)


# Export a ModuleClass definition to a file

def exportModuleClass(module, package, path):
	global structs

	# export the module class itself

	name = sanitizeName(module.name, True)
	fileName = str(path) + os.sep + name + '.fbmodel'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getModuleClassHeader(name, package, module.doc))
		outputFile.write(getModuleClassInterface(module, package, name))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


	# Export struct definitions found in the ModuleClass as classes

	while len(structs) > 0:
		name,ty = structs.popitem()
		structName = sanitizeName(name, True)
		fileName = str(path) + os.sep + structName + '.java'
		outputFile = None
		try:
			outputFile = open(fileName, 'w')
			outputFile.write(getStructHeader(structName, ty.doc))
			outputFile.write(getStruct(ty, package, name))
		except IOError as err:
			print(err)
		finally:
			if (outputFile != None):
				outputFile.close()
	structs = {}










# Export each Device definition to a separate sub-package

def exportDevice(device, package, path):
	name = sanitizeName(device.id, True)
	package = package + '.' + name.lower()	# MAYBE perhaps to some fixes to the id here as well
	packagePath = str(path) + os.sep + name.lower()
	path = pathlib.Path(packagePath)

	try:
		path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now

	fileName = str(path) + os.sep + name + '.java'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getDeviceHeader(name, device.doc))
		outputFile.write(getDeviceInterface(device, package, name))
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()

	# export module classes of the device

	for module in device.modules:
		exportModuleClass(module, package, path)

	# export sub devices of the device

	if (isinstance(device, SDT3Device)):
		for subdevice in device.subDevices:
			exportDevice(subdevice, package, path)



# Get the ModuleClass text

def getModuleClassInterface(module, package, name):
	result = ''
	extends = ''
	if (module.extends != None):
		extendsID = module.extends.domain + '.' + sanitizeName(module.extends.clazz, True)
		extends = ' extends ' + extendsID
	result += newLine() + 'functionblock ' + sanitizeName(name, True) + extends + ' {'
	incTab()

	# Properties
	# TODO print properties. Extra file
	# result += getPropertyNames(module.properties)

	# DataPoints 
	result += getDataPoints(module.data)

	# Events
	result += getEvents(module.events)

	# Actions
	result += getActions(module.actions)

	decTab()
	result += newLine() + '}'
	return printImports() + result


# Get the Device text

def getDeviceInterface(device, package, name):
	result  = newLine() + 'public interface ' + sanitizeName(name, True)
	zw = ''
	for module in device.modules:
		if (len(zw) == 0):
			zw += ' extends '
		else:
			zw += ', '
		zw += sanitizeName(module.name, True)
	result += zw + ' {'
	incTab()

	# Properties

	result += getPropertyNames(device.properties)


	decTab()
	result += newLine() + '}'
	return printPackage(package) + printImports() + result


# Get the struct text

def getStruct(struct, package, name):
	result  = newLine() + 'public class ' + name + ' {'
	incTab()
	for element in struct.structElements:
		result += newLine() + getType(element) + ' ' + element.name + ';'
	decTab()
	result += newLine() + '}'
	return printPackage(package) + printImports() + result


########################################################################

# Construct data points export
def getDataPoints(dataPoints):
	if (dataPoints == None or len(dataPoints) == 0):
		return ''
	result = ''
	result += newLine() + newLine() + 'status {'
	result += getDataPointsDetails(dataPoints)
	result += newLine() + '}'
	return result


# Construct events export
def getEvents(events):
	if (events == None or len(events) == 0):
		return ''
	result = ''
	result += newLine() + newLine() + 'events {'
	incTab()
	for event in events:
		result += newLine() + sanitizeName(event.name, True) + ' {'
		result += getDataPointsDetails(event.data)
		result += newLine() + '}'
	decTab()
	result += newLine() + '}'
	# TODO documentation
	return result


# Construct actions export
def getActions(actions):
	if (actions == None or len(actions) == 0):
		return ''
	result = ''
	result += newLine() + newLine() + 'operations {'
	incTab()
	for action in actions:
		result += newLine() + sanitizeName(action.name, True) + ' ('
		argResult = []
		for arg in action.args:
			a = arg.name + ' as '
			if (isinstance(arg.type.type, SDT3ArrayType)):
				a += 'multiple '
			a += getType(arg.type)
			argResult.append(a)
		result += ', '.join(argResult)
		result += ') '
		if (action.type):
			result += 'returns '
			if (isinstance(action.type.type, SDT3ArrayType)):
				result += 'multiple '
			result += getType(action.type)
	decTab()
	result += newLine() + '}'
	# TODO documentation
	return result


# Construct data points cores export
def getDataPointsDetails(dataPoints):
	result = ''
	incTab()
	for dataPoint in dataPoints:
		result += newLine()

		if (dataPoint.optional == 'true'):
			result += 'optional '
		else:
			result += 'mandatory '

		if (isinstance(dataPoint.type.type, SDT3ArrayType)):
			result += 'multiple '

		result += sanitizeName(dataPoint.name, False)
		result += ' as ' + getType(dataPoint.type) 
		result += ' with {'
		result += 'readable : ' + dataPoint.readable + ', '
		result += 'writable : ' + dataPoint.writable + ', '
		result += 'eventable : ' + dataPoint.eventable
		result += '} '

		if dataPoint.doc:
			result += ' "' + dataPoint.doc.doc.content.strip() + '"'

	decTab()
	return result


########################################################################


def getType(datatype):
	global structs, imports

	# Simple type
	if (isinstance(datatype.type, SDT3SimpleType)):
		ty = datatype.type
		if (ty.type == 'boolean'):
			return 'boolean'
		elif (ty.type == 'integer'):
			return 'int'
		elif (ty.type == 'float'):
			return 'float'
		elif (ty.type == 'string'):
			return 'string'
		elif (ty.type == 'datetime'):
			return 'datetime'
		elif (ty.type == 'date'):
			return 'datetime'	# TOOD
		elif (ty.type == 'time'):
			return 'datetime'	# TODO
		elif (ty.type == 'enum'):
			return 'string'
		elif (ty.type =='uri'):
			return 'string'	 	# TODO
		elif (ty.type == 'blob'):
			return 'base64Binary'	# TODO 


	# Array
	elif (isinstance(datatype.type, SDT3ArrayType)):
		arrayType = datatype.type
		if arrayType.arrayType != None:
			return getType(arrayType.arrayType)
		else:
			return sanitizeName(arrayType.name, True)

	# Struct
	elif (isinstance(datatype.type, SDT3StructType)):
		name = sanitizeName(datatype.name, True)
		structs[name] = datatype.type
		return name
	return 'XX_'


def getPropertyNames(properties):
	result = ''
	if properties != None and len(properties) > 0:
		result += newLine() + newLine() + newLine() + '// Properties' + newLine()
		for prop in properties:
			# result += newLine() + getPropertyHeader(prop.doc)
			result += newLine() + 'static final String PROP_' + sanitizeName(prop.name, False) + ' = "' + prop.name + '";'
	return result

#
#	Headers
#

commentTemplate = '''namespace {namespace}
version {version}
displayname "{displayname}"
description "{description}"
category {category}
'''

commentTemplateNoDoc = '''namespace {namespace}
version {version}
displayname "{displayname}"
category {category}
'''



def getHeader(aName, package, documentation, ty):
	global commentTemplate, commentTemplateNoDoc
	global vortoModelVersion, vortoModelCategory

	if documentation:
		return commentTemplate.format(namespace=package, 
			version=vortoModelVersion,
			displayname=aName,
			description=documentation.doc.content.strip(),
			category=vortoModelCategory)
	else:
		return commentTemplateNoDoc.format(namespace=package, 
			version=vortoModelVersion,
			displayname=aName,
			category=vortoModelCategory)


def getModuleClassHeader(aName, package, documentation):
	return getHeader(aName, package, documentation, 'Event')



def getStructHeader(aName, documentation):
	return ''#  getHeader(aName, documentation, 'Struct')

def getDeviceHeader(aName, documentation):
	return ''# getHeader(aName, documentation, 'Device')



#
#	Helpers
#

# Sanitize the name for Vorto

def sanitizeName(name, isClass):
	if (name == None or len(name) == 0):
		return ''
	result = name
	if (isClass):
		result = result[0].upper() + name[1:]
	else:
		result = result[0].lower() + name[1:]
	result = result.replace(' ', '')
	result = result.replace('/', '')
	result = result.replace('.', '')
	result = result.replace(' ', '')
	result = result.replace("'", '')
	result = result.replace('´', '')
	result = result.replace('`', '')
	result = result.replace('(', '_')
	result = result.replace(')', '_')
	result = result.replace('-', '_')

	return result

# Sanitize the package name for Java

def sanitizePackage(package):
	result = package.replace('/', '.')
	return result

# Print the package at the beginning of a Java file

def printPackage(package):
	return 'package ' + package + ';' + newLine()

def printImports():
	global imports

	result = ''
	for name, imp in imports.items():
		result += newLine() + 'import ' + imp + ';'
	imports = {}
	return result + newLine()

# Tabulator handling

tab = 0

def incTab():
	global tab
	tab += 1

def decTab():
	global tab
	if (tab > 0):
		tab -= 1

def newLine():
	global tab
	result = '\n'
	for i in range(tab):
		result += '\t'
	return result
