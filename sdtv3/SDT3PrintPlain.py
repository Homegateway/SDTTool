#	SDT3PrintPlain.py
#
#	Print SDT3 to Plain text

from .SDT3Classes import *

hideDetails = False

# tabulator level
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


#
#	Print functions
#

def print3DomainPlain(domain, options):
	global hideDetails
	hideDetails = options['hideDetails']
	
	result = 'Domain [id="' + domain.id + '"]'
	incTab()
	if (domain.doc != None):
		result += newLine() + printDoc(domain.doc)
	for include in domain.includes:
		result += newLine() + printInclude(include)
	for module in domain.modules:
		result += newLine() + printModuleClass(module)
	for device in domain.devices:
		result += newLine() + printDevice(device)
	decTab()
	return result

def printInclude(include):
	return 'Include [parse="' + include.parse + '" href="' + include.href + '"]'


#
#	Device, SubDevice
#

def printDevice(device):
	global hideDetails

	result = 'Device [id="' + device.id + '"]'
	incTab()
	if (device.doc != None and hideDetails == False):
		result += newLine() + printDoc(device.doc)
	if (hideDetails == False):
		for prop in device.properties:
			result += newLine() + printProperty(prop)
	for module in device.modules:
		result += newLine() + printModule(module)
	for subDevice in device.subDevices:
		result += newLine() + printSubDevice(subDevice)
	decTab()
	return result


def printSubDevice(subDevice):
	global hideDetails

	result = 'SubDevice [id="' + subDevice.id + '"]'
	incTab()
	if (subDevice.doc != None and hideDetails == False):
		result += newLine() + printDoc(subDevice.doc)
	if (hideDetails == False):
		for prop in subDevice.properties:
			result += newLine() + printProperty(prop)
	for module in subDevice.modules:
		result += newLine() + printModule(module)
	decTab()
	return result


#
#	Property
#

def printProperty(prop):
	result = 'Property ['
	incTab()
	if (prop.name != None):
		result += 'name="' + prop.name + '"'
	if (prop.value != None):
		result += ' value="' + prop.value + '"'
	if (prop.optional != None):
		result += ' optional="' + prop.optional + '"'
	result += ']'
	if (prop.doc):
		result += newLine() + printDoc(prop.doc)
	if (prop.type):
		result += newLine() + printSimpleTypeProperty(prop.type)
	decTab()
	return result


#
#	Print Module, ModuleClass
#

def printModule(module):
	result =  'Module [name="' + module.name
	if (module.optional != None):
		result += ' optional="' + module.optional + '"'
	result += ']'
	if (hideDetails == False):
		result += printModuleDetails(module)
	return result

def printModuleClass(moduleClass):
	result =  'ModuleClass [name="' + moduleClass.name
	if (moduleClass.optional != None):
		result += ' optional="' + moduleClass.optional + '"'
	result += ']'
	if (hideDetails == False):
		result += printModuleDetails(moduleClass)
	return result

def printModuleDetails(module):
	incTab()
	result = ''
	if (module.doc != None):
		result += newLine() + printDoc(module.doc)
	if (module.extends != None):
		result += newLine() + printExtends(module.extends)
	if (hideDetails == False):
		for prop in module.properties:
			result += newLine() + printProperty(prop)
	for action in module.actions:
		result += newLine() + printAction(action)
	for data in module.data:
		result += newLine() + printDataPoint(data)
	for event in module.events:
		result += newLine() + printEvent(event)
	decTab()
	return result

def printExtends(extends):
	return 'Extends [domain="' + extends.domain + '" class="' + extends.clazz + '"]'


#
#	Action, Argument
#

def printAction(action):
	result = 'Action [name="' + action.name + '"'
	if (action.optional != None):
		result += ' optional="' + action.optional + '"'
	result += ']'
	incTab()
	if (action.doc != None): 
		result += newLine() + printDoc(action.doc)
	for argument in action.args:
		result += newLine() + printArgument(argument)
	if (action.type != None):
		result += newLine() + printDataType(action.type)
	decTab()
	return result


def printArgument(argument):
	result = 'Arg ['
	if (argument.name != None):
		result += 'name="' + argument.name + '"'
	result += ']'
	incTab()
	if (argument.doc != None): 
		result += newLine() + printDoc(argument.doc)
	if (argument.type):
		result += newLine() + printDataType(argument.type)
	decTab()
	return result

#
#	Event
#

def printEvent(event):
	result = 'Event [name="' + event.name 
	if (event.optional != None):
		result += ' optional="' + event.optional + '"'
	result += ']'
	incTab()
	if (event.doc != None):
		result += newLine() + printDoc(event.doc)	
	for dataPoint in event.data:
		result += newLine() + printDataPoint(dataPoint)
	decTab()
	return result


#
#	DataPoint
#

def printDataPoint(datapoint):
	result = 'DataPoint [name="' + datapoint.name + '"'
	if (datapoint.optional != None):
		result += ' optional="' + datapoint.optional + '"'
	if (datapoint.writable != None):
		result += ' writable="' + datapoint.writable + '"'
	if (datapoint.readable != None):
		result += ' readable="' + datapoint.readable + '"'
	if (datapoint.eventable != None):
		result += ' eventable="' + datapoint.eventable + '"'
	result += ']'
	incTab()
	if (datapoint.doc != None):
		result += newLine() + printDoc(datapoint.doc)
	if (datapoint.type != None):
		result += newLine() + printDataType(datapoint.type)
	decTab()
	return result


#
#	DataTypes
#


def printDataType(dataType):
	if (isinstance(dataType.type, SDT3SimpleType)):
		result = printSimpleType(dataType)
	elif (isinstance(dataType.type, SDT3StructType)):
		result = printStructType(dataType)
	elif (isinstance(dataType.type, SDT3ArrayType)):
		result = printArrayType(dataType)
	return result


def printSimpleType(dataType):
	simpleType = dataType.type
	result = 'SimpleType'
	result += printDataTypeAttributes(dataType)
	if (len(result) > 0):
		result += ' '
	result += '[type="' + simpleType.type + '"]'
	if (dataType.doc != None):
		incTab()
		result += newLine() + printDoc(dataType.doc)
		decTab()
	incTab()
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	return result


def printSimpleTypeProperty(simpleType):
	result = 'SimpleType'
	if (len(result) > 0):
		result += ' '
	result += '[type="' + simpleType.type + '"]'
	return result


def printStructType(dataType):
	result = 'Struct'
	result += printDataTypeAttributes(dataType)
	incTab()
	for element in dataType.type.structElements:
		result += newLine() + printDataType(element)
	decTab()
	if (dataType.doc != None):
		incTab()
		result += newLine() + printDoc(dataType.doc)
		decTab()
		incTab()
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	return result

def printArrayType(dataType):
	arrayType = dataType.type
	result = 'Array'
	result += printDataTypeAttributes(dataType)
	if (arrayType.arrayType != None):
		incTab()
		result += newLine() + printDataType(arrayType.arrayType)
		decTab()
	if (dataType.doc != None):
		incTab()
		result += newLine() + printDoc(dataType.doc)
		decTab()
	incTab()
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	return result


def printDataTypeAttributes(dataType):
	result = ''
	if (dataType.name != None):
		result += 'name="' + dataType.name + '"'
	if (dataType.unitOfMeasure != None):
		if (len(result) > 0):
			result += ' '
		result += 'unitOfMeasure="' + dataType.unitOfMeasure + '"'
	if (len(result) > 0):
		result = ' [' + result + ']'
	return result


def printConstraint(constraint):
	result = 'Constraint'
	attr   = ''
	if (constraint.name != None):
		attr += 'name="' + constraint.name + '"'
	if (constraint.type != None):
		if (len(attr) > 0):
			attr += ' '
		attr += 'type="' + constraint.type + '"'
	if (constraint.value != None):
		if (len(attr) > 0):
			attr += ' '
		attr += 'value="' + constraint.value + '"'
	if (len(attr) > 0):
		result += ' [' + attr + ']'
	if (constraint.doc != None):
		incTab()
		result += newLine() + printDoc(constraint.doc)
		decTab()
	return result


#
#	Doc
#

def printDoc(doc):
	incTab()
	result = 'Doc: ' +	 doc.content.strip()
	decTab()
	return result
