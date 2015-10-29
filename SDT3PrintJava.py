#	SDT3PrintJava.py
#
#	Generate Java clasess from SDT3 

# TODO Add header to the java file. at least describe SDT equivalent (device, moduleclass, type, event, ...)
# TODO export properties

import os, pathlib, string
from SDT3Classes import *

# Dictionary to temporarly store the found structs.
# TODO: export for each ModuleClass (as done yet) or only once. Check for duplicates?
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
			outputFile.write(getJavaEvents(event, package, eventName))
		except IOError as err:
			print(err)
		finally:
			if (outputFile != None):
				outputFile.close()

	# Export struct definitions found in the ModuleClass as classes

	for name,ty in structs.items():
		structName = sanitizeName(name, True)
		fileName = str(path) + os.sep + structName + '.java'
		outputFile = None
		try:
			outputFile = open(fileName, 'w')
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

	# TODO deviceinfo


# Get the ModuleClass text

def getModuleClassInterface(module, package, name):
	result = ''
	extends = ''
	if (module.extends != None):
		extendsID = module.extends.domain + '.' + sanitizeName(module.extends.clazz, True)
		extends = ' extends ' + extendsID
	result += newLine() + 'public interface ' + sanitizeName(name, True) + extends + ' {'
	incTab()

	# Actions

	hasActions = False
	for action in module.actions:
		if (hasActions == False):
			hasActions = True
			result += newLine() + newLine() + '// Actions' + newLine()

		returnType = 'void'
		if (action.type != None):
			returnType = getType(action.type)
		default = ''
		defaultBody = ''
		if (action.optional != None and action.optional):
			default = 'default '
			defaultBody = ' ' + getOptionalActionBody(action.type.type)
		args = ''
		if (action.args != None):
			args = getActionArguments(action.args)
		result += newLine() + default + returnType + ' ' + sanitizeName(action.name, False) + '(' + args + ')' + defaultBody + ';'

	# DataPoints getters/setters
	result += getDatePointSettersGetters(module.data)

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

	# TODO DeviceInfo. Map? Hash
	decTab()
	result += newLine() + '}'
	return printPackage(package) + printImports() + result


# Get the Event text

def getJavaEvents(event, package, name):
	result  = newLine() + 'public interface ' + sanitizeName(name, True) + ' {'
	incTab()

	# DataPoints getters/setters
	result += getDatePointSettersGetters(event.data)

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


def getType(ty):
	global structs, imports

	# Simple type
	if (isinstance(ty, SDT3SimpleType)):
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
		else:
			return 'xx_' + ty.type

	# Array
	elif (isinstance(ty, SDT3ArrayType)):
		if (isinstance(ty.arrayType, SDT3SimpleType)):
			return getType(ty.arrayType) + '[]'
		else:
			return sanitizeName(ty.name) + '[]'

	# Struct
	elif (isinstance(ty, SDT3StructType)):
		name = sanitizeName(ty.name, True)
		structs[name] = ty
		return name
	return 'Object'


def getOptionalActionBody(ty):
	if (ty == 'void'):
		return '{ }'
	elif (ty.lower() == 'boolean'):
		return '{ return false; }'
	elif (ty.lower() == 'integer'):
		return '{ return 0; }'
	elif (ty.lower() == 'float'):
		return '{ return 0.0; }'
	elif (ty.lower() == 'string'):
		return '{ return null; }'
	else:
		return '/* TODO ' + ty + ' */'

def getActionArguments(args):
	result = ''
	for arg in args:
		if (len(result) > 0):
			result += ', '
		result += getType(arg.type) + ' ' + sanitizeName(arg.name, False)
	return result


def getDatePointSettersGetters(dataPoints):
	result = ''
	hasDataPoints = False
	for dataPoint in dataPoints:
		if (hasDataPoints == False):
			hasDataPoints = True
			result += newLine() + newLine() + '// DataPoint getters/setters' + newLine() 

		args = ''
		defaultBody = ''
		if (dataPoint.writable == 'true'):
			args = getType(dataPoint.type) + ' ' + sanitizeName(dataPoint.name, False)
			if (dataPoint.optional == 'true'):
				defaultBody = '{}'
			result += newLine() + 'void _set' + sanitizeName(dataPoint.name, True) + '(' + args + ')' + defaultBody + ';'
		if (dataPoint.readable == 'true'):
			default = ''
			if (dataPoint.optional == 'true'):
				default = 'default '
				defaultBody = ' ' + getOptionalActionBody(dataPoint.type.type)
			result += newLine() + default + getType(dataPoint.type) + ' _get' + sanitizeName(dataPoint.name, True) + '()' + defaultBody + ';'
	return result

#
#	Helpers
#

# Sanitize the name for Java

def sanitizeName(name, isEntity):
	result = name
	if (isEntity):
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
