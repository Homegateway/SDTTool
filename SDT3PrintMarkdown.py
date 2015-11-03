#	SDT3PrintMarkdown.py
#
#	Print SDT3 to markdown

from SDT3Classes import *

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


# header level
headerLevel = 1

def incHeaderLevel():
	global headerLevel
	headerLevel += 1

def decHeaderLevel():
	global headerLevel
	headerLevel -= 1


def markdownHeader(text):
	global headerLevel
	result = '\n\n'
	for i in range(headerLevel):
		result += '#'
	result += ' ' + text
	return result


#
#	Print functions
#

def print3DomainMarkdown(domain, options):
	global hideDetails
	hideDetails = options['hideDetails']

	result = ''
	result += markdownHeader('Domain "' + domain.id + '"')
	if (domain.doc and hideDetails == False):
		result += '  ' + newLine() + printDoc(domain.doc)
	if (len(domain.includes) > 0):
		result += newLine() + '- **Includes**'
		for include in domain.includes:
			result += printInclude(include)
	if (len(domain.modules) > 0):
		incHeaderLevel()
		result += markdownHeader('ModuleClasses')
		for module in domain.modules:
			result +=  newLine() + printModuleClass(module)
		decHeaderLevel()
	if (len(domain.devices) > 0):
		incHeaderLevel()
		result += markdownHeader('Devices')
		for device in domain.devices:
			result += newLine() + printDevice(device)
		decHeaderLevel()
	return result


def printInclude(include):
	incTab()
	result = newLine() + '- Parse: ' + include.parse 
	result += ', Href: ' + include.href
	decTab()
	return result


#
#	Device, SubDevice
#

def printDevice(device):
	global hideDetails
	incHeaderLevel()
	result = markdownHeader(device.id)
	if (device.doc and hideDetails == False):
		result += '  ' + newLine() + printDoc(device.doc)
	if (device.properties != None and hideDetails == False):
		result += newLine() + printProperties(device.properties)
	if (len(device.modules) > 0):
		incHeaderLevel()
		result += markdownHeader('Modules')
		for module in device.modules:
			result += newLine() + printModule(module)
		decHeaderLevel()
	if (len(device.subDevices) > 0):
		incHeaderLevel()
		result += markdownHeader('SubDevices')
		for subDevice in rootDevice.subDevices:
			result += printSubDevice(subDevice)
		decHeaderLevel()
	decTab()
	decHeaderLevel()
	return result



def printSubDevice(subDevice):
	global hideDetails
	incHeaderLevel()
	result = markdownHeader('SubDevice "' + subDevice.id + '"')
	if (subDevice.doc):
		result += '  ' + newLine() + printDoc(subDevice.doc)
	if (subDevice.properties != None and hideDetails == False):
		result += newLine() + printProperties(subDevice.properties)
	if (len(subDevice.modules) > 0):
		incHeaderLevel()
		result += newLine() + markdownHeader('Modules')
		for module in device.modules:
			result += newLine() + printModule(module)
		decHeaderLevel()
	decHeaderLevel()
	return result


#
#	Properties
#

def printProperties(props):
	result = ''
	if (len(props) > 0):
		result += newLine() + '- Properties'
		for prop in props:
			result += printProperty(prop)
	return result

def printProperty(prop):
	incTab()
	result = newLine() + '- **' + prop.name + '**'
	if (prop.type):
		result += ': ' + printSimpleTypeProperty(prop.type)
	if (prop.doc):
		result += '  ' + newLine() + printDoc(prop.doc)
	incTab()
	if (prop.value != None):
		result += newLine() + '- Value: ' + prop.value
	if (prop.optional != None):
		result += newLine() + '- Optional: ' + prop.optional
	decTab()
	decTab()
	return result


#
#	Print Module, ModuleClass
#

def printModule(module):
	return printModuleDetails(module)

def printModuleClass(moduleClass):
	return printModuleDetails(moduleClass)

def printModuleDetails(module):
	global hideDetails
	result = '- **' + module.name + '**'
	if (hideDetails):
		return result;
	incTab()
	if (module.doc != None):
		result += '  ' + newLine() + printDoc(module.doc)
	if (module.extends != None):
		result += printExtends(module.extends)
	if (module.optional != None):
		result += newLine() + '- Optional: ' + module.optional
	if (module.properties != None and hideDetails == False):
		result += printProperties(module.properties)
	if (len(module.actions) > 0):
		result += newLine() + '- Actions'
		for action in module.actions:
			result += printAction(action)
	if (len(module.data) > 0):
		result += newLine() + '- Data'
		for data in module.data:
			result += printDataPoint(data)
	if (len(module.events) > 0):
		result += newLine() + '- Events'
		for event in module.events:
			result += printEvent(event)
	decTab()
	return result

def printExtends(extends):
	result = newLine() + '- Extends'
	incTab()
	result += newLine() + '- Domain: **' + extends.domain + '**, Class: **' + extends.clazz + '**'
	decTab()
	return result


#
#	Action, Argument
#

def printAction(action):
	incTab()
	result = newLine() + '- **' + action.name + '**'
	incTab()
	if (action.doc != None): 
		result += '  ' + newLine() + printDoc(action.doc)
	if (action.type != None):
		result += newLine() + '- Return Type: ' + printDataType(action.type)
	if (len(action.args) > 0):
		result += newLine() + '- Arguments'
		for argument in action.args:
			result += printArgument(argument)
	if (action.optional != None):
		result += newLine() + '- Optional: ' + action.optional

	decTab()
	decTab()
	return result

def printArgument(action):
	incTab()
	result = newLine() + '- '
	if (action.name != None):
		result +=  '**' + action.name + '**'
	if (action.type != None):
		result += ': ' + printDataType(action.type)
	decTab()
	return result


#
#	Event
#

def printEvent(event):
	incTab()
	result = newLine() + '- **' + event.name + '**'
	incTab()
	if (event.doc != None):
		result += '  ' + newLine() + printDoc(event.doc)
	if (event.optional != None):
		result += newLine() + '- Optional: ' + event.optional

	if (len(event.data) > 0):
		result += newLine() + '- Data'
		for dataPoint in event.data:
			result += printDataPoint(dataPoint)
	decTab()
	decTab()
	return result


#
#	dataPoint
#

def printDataPoint(datapoint):
	incTab()
	result = newLine() + '- **' + datapoint.name + '**'
	if (datapoint.type != None):
		result += ': ' + printDataType(datapoint.type)
	incTab()
	if (datapoint.doc != None):
		result +=  '  ' + newLine() + printDoc(datapoint.doc)
	if (datapoint.optional != None):
		result += newLine() + '- Optional: ' + datapoint.optional
	if (datapoint.writable != None):
		result += newLine() + '- Writable: ' + datapoint.writable
	if (datapoint.readable != None):
		result += newLine() + '- Readable: ' + datapoint.readable
	if (datapoint.eventable != None):
		result += newLine() + '- Eventable: ' + datapoint.eventable
	decTab()
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
	result = ''
	result += printDataTypeAttributes(dataType)
	if (len(result) > 0):
		result += ' '
	result += simpleType.type
	if (dataType.doc != None):
		result += '  ' + newLine() + printDoc(dataType.doc)
	incTab()
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	return result


def printSimpleTypeProperty(simpleType):
	result = ''
	if (len(result) > 0):
		result += ' '
	result += simpleType.type
	return result


def printStructType(dataType):
	result = 'Struct'
	result += printDataTypeAttributes(dataType)
	incTab()
	for element in dataType.type.structElements:
		result += newLine() + printDataType(element)
	decTab()
	if (dataType.doc != None):
		result += '  ' + newLine() + printDoc(dataType.doc)
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
		result += '[' + printDataType(arrayType.arrayType) + ']'
		decTab()
	if (dataType.doc != None):
		result += '  ' + newLine() + printDoc(dataType.doc)
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
	result = ' [Constraint: '
	attr   = ''
	if (constraint.name != None):
		attr += 'name="' + constraint.name + '"'
	if (constraint.type != None):
		if (len(attr) > 0):
			attr += ', '
		attr += 'type="' + constraint.type + '"'
	if (constraint.value != None):
		if (len(attr) > 0):
			attr += ', '
		attr += 'value="' + constraint.value + '"'
	if (constraint.doc != None):
		if (len(attr) > 0):
			attr += ', '
		attr += printDoc(constraint.doc)
	if (len(attr) > 0):
		result += attr
	result += ']'
	return result



#
#	Doc
#

def printDoc(doc):
	result = doc.content.strip()
	return result

