#	SDT3PrintJava.py
#
#	Generate Java clasess from SDT3 

# TODO export properties

import datetime, os, pathlib, string
from SDT3Classes import *

# Dictionary to temporarly store the found structs.
# TODO: export for each ModuleClass (as done yet) or only once? Check for duplicates?
structs = {}

# Dictionary to temporarly store necessary imports
imports = {}

def print3JavaClasses(domain, directory, options):

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
	fileName = str(path) + os.sep + name + '.java'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getModuleClassHeader(name, module.doc))
		outputFile.write(getModuleClassInterface(module, package, name))
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()
	
	# Export the events in the ModuleClass as classes

	for event in module.events:
		eventName = name + sanitizeName(event.name, True)
		fileName = str(path) + os.sep + eventName + '.java'
		outputFile = None
		try:
			outputFile = open(fileName, 'w')
			outputFile.write(getEventHeader(eventName, event.doc))
			outputFile.write(getJavaEvents(event, package, eventName))
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
	result += newLine() + 'public interface ' + sanitizeName(name, True) + extends + ' {'
	incTab()

	# Properties

	result += getPropertyNames(module.properties)

	# Actions

	hasActions = False
	for action in module.actions:
		if (hasActions == False):
			hasActions = True
			result += newLine() + newLine() + newLine() + '// Actions'

		if action.doc:
			result += newLine() + newLine() + getActionHeader(action.doc)

		returnType = 'void'
		if action.type != None:
			returnType = getType(action.type)
		default = ''
		defaultBody = ''
		if action.optional != None and action.optional:
			default = 'default '
			defaultBody = ' ' + getOptionalActionBody(action.type)
		args = ''
		if action.args != None:
			args = getActionArguments(action.args)
		result += newLine() + default + returnType + ' ' + sanitizeName(action.name, False) + '(' + args + ')' + defaultBody + ';'

	# DataPoints getters/setters
	result += getDataPointSettersGetters(module.data, False)

	decTab()
	result += newLine() + '}'
	return printPackage(package) + printImports() + result


def getMethod(ty, ):
	returnType = 'void'
	if (ty != None):
		returnType = getType(ty)
	default = ''
	defaultBody = ''
	if (action.optional != None and action.optional):
		default = 'default '
		defaultBody = ' ' + getOptionalActionBody(action.type)
	args = ''
	if (action.args != None):
		args = getActionArguments(action.args)
	result += newLine() + default + returnType + ' ' + action.name + '(' + args + ')' + defaultBody + ';'
	return result


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


# Get the Event text

def getJavaEvents(event, package, name):
	result  = newLine() + 'public interface ' + sanitizeName(name, True) + ' {'
	incTab()

	# DataPoints getters/setters
	result += getDataPointSettersGetters(event.data, True)

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


def getJavaMethods(module, package):
	result = ''
	for action in module.actions:
		returnType = 'void'
		if (action.type != None):
			returnType = getType(action.type)
		default = ''
		defaultBody = ''
		if (action.optional != None and action.optional):
			default = 'default '
			defaultBody = ' ' + getOptionalActionBody(action.type)
		args = ''
		if (action.args != None):
			args = getActionArguments(action.args)
		result += newLine() + default + returnType + ' ' + action.name + '(' + args + ')' + defaultBody + ';'
	return result


def getDataPoint(dataPoint):
	return getType(dataPoint.type) + ' ' + dataPoint.name + ';'


def getType(datatype):
	global structs, imports

	# Simple type
	if (isinstance(datatype.type, SDT3SimpleType)):
		ty = datatype.type
		if (ty.type == 'boolean'):
			return 'Boolean'
		elif (ty.type == 'integer'):
			return 'Integer'
		elif (ty.type == 'float'):
			return 'Float'
		elif (ty.type == 'string'):
			return 'String'
		elif (ty.type == 'datetime'):
			imports['Date'] = 'java.util.Date'
			return 'Date'
		elif (ty.type == 'date'):
			imports['Date'] = 'java.util.Date'
			return 'Date'
		elif (ty.type == 'time'):
			imports['Date'] = 'java.util.Date'
			return 'Date'
		elif (ty.type == 'enum'):
			return 'String[]'
		elif (ty.type == 'array'):
			return 'String[]'
		elif (ty.type == 'uri'):
			imports['URI'] = 'java.net.URI'
			return 'URI'
		else:
			return 'xx_' + ty.type

	# Array
	elif (isinstance(datatype.type, SDT3ArrayType)):
		arrayType = datatype.type
		if arrayType.arrayType != None:
			return getType(arrayType.arrayType) + '[]'
		else:
			return sanitizeName(arrayType.name, True) + '[]'

	# Struct
	elif (isinstance(datatype.type, SDT3StructType)):
		name = sanitizeName(datatype.name, True)
		structs[name] = datatype.type
		return name
	return 'Object'


def getOptionalActionBody(datatype):
	if (datatype == None or datatype.type == None):
		return '{ }'
	if (isinstance(datatype, SDT3ArrayType)):
		return '{ return null; }'
	elif (datatype.type == 'void'):
		return '{ }'
	elif (datatype.type.lower() == 'boolean'):
		return '{ return false; }'
	elif (datatype.type.lower() == 'integer'):
		return '{ return 0; }'
	elif (datatype.type.lower() == 'float'):
		return '{ return 0.0f; }'
	elif (datatype.type.lower() == 'string'):
		return '{ return null; }'
	elif (datatype.type.lower() == 'datetime'):
		return '{ return null; }'
	elif (datatype.type.lower() == 'date'):
		return '{ return null; }'
	elif (datatype.type.lower() == 'time'):
		return '{ return null; }'
	elif (datatype.type.lower() == 'enum'):
		return '{ return null; }'
	elif (datatype.type.lower() == 'array'):
		return '{ return null; }'
	else:
		return '/* TODO ' + datatype.type + ' */ ;'

def getActionArguments(args):
	result = ''
	for arg in args:
		if (len(result) > 0):
			result += ', '
		result += getType(arg.type) + ' ' + sanitizeName(arg.name, False)
	return result


def getDataPointSettersGetters(dataPoints, isEvent):
	result = ''
	hasDataPoints = False
	for dataPoint in dataPoints:
		if (hasDataPoints == False):
			hasDataPoints = True
			result += newLine() + newLine() + newLine() +  '// DataPoints - getters/setters'

		if dataPoint.doc:
			result += newLine() + newLine() + getDataPointHeader(dataPoint.doc)

		args = ''
		defaultBody = ''
		if (dataPoint.writable == 'true' and isEvent == False):
			args = getType(dataPoint.type) + ' ' + sanitizeName(dataPoint.name, False)
			default = ''
			if (dataPoint.optional == 'true'):
				default = 'default '
				defaultBody = ' {}'
			result += newLine() + default + 'void _set' + sanitizeName(dataPoint.name, True) + '(' + args + ')' + defaultBody + ';'
		if (dataPoint.readable == 'true'):
			default = ''
			if (dataPoint.optional == 'true'):
				default = 'default '
				defaultBody = ' ' + getOptionalActionBody(dataPoint.type.type)
			result += newLine() + default + getType(dataPoint.type) + ' _get' + sanitizeName(dataPoint.name, True) + '()' + defaultBody + ';'
	return result


def getPropertyNames(properties):
	result = ''
	if properties != None and len(properties) > 0:
		result += newLine() + newLine() + newLine() + '// Properties' + newLine()
		for prop in properties:
			result += newLine() + getPropertyHeader(prop.doc)
			result += newLine() + 'static final String PROP_' + sanitizeName(prop.name, False) + ' = "' + prop.name + '";'
	return result

#
#	Headers
#

commentTemplate = '''/*
{type} : {name}

{doc}

Created: {date}
*/

'''

commentTemplateNoDoc = '''/*
{type} : {name}

Created: {date}
*/

'''

commentTemplateAction = '/* {doc} */'

commentTemplateDataPoint = '/* {doc} */'

commentTemplateProperty = '/* {doc} */'


def getHeader(aName, documentation, ty):
	global commentTemplate, commentTemplateNoDoc
	if documentation:
		return commentTemplate.format(name=aName, 
			type=ty,
			doc=documentation.doc.content.strip(),
			date=str(datetime.datetime.now())[:19])
	else:
		return commentTemplateNoDoc.format(name=aName, 
			type=ty,
			date=str(datetime.datetime.now())[:19])


def getModuleClassHeader(aName, documentation):
	return getHeader(aName, documentation, 'ModuleClass')

def getEventHeader(aName, documentation):
	return getHeader(aName, documentation, 'Event')

def getStructHeader(aName, documentation):
	return getHeader(aName, documentation, 'Struct')

def getDeviceHeader(aName, documentation):
	return getHeader(aName, documentation, 'Device')

def getActionHeader(documentation):
	global commentTemplateAction
	if documentation:
		return commentTemplateAction.format(doc=documentation.doc.content.strip())
	return ''

def getDataPointHeader(documentation):
	global commentTemplateDataPoint
	if documentation:
		return commentTemplateDataPoint.format(doc=documentation.doc.content.strip())
	return ''

def getPropertyHeader(documentation):
	global commentTemplateProperty
	if documentation:
		return commentTemplateProperty.format(doc=documentation.doc.content.strip())
	return ''


#
#	Helpers
#

# Sanitize the name for Java

def sanitizeName(name, isClass):
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
