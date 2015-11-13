#	SDT3PrintMarkdown.py
#
#	Print SDT3 to markdown

from SDT3Classes import *

hideDetails = False
tables = False

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
	global hideDetails, tables
	hideDetails = options['hideDetails']
	tables = options['markdowntables']

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
	global tables

	result = ''
	if (len(props) > 0):
		if tables:
			incHeaderLevel()
			result += markdownHeader('Properties')
			result += newLine() + '|Name |Type |Value |Optional |Documentation |'
			result += newLine() + '|:----|:----|:-----|:--------|:-------------|'
		else:
			result += newLine() + '- Properties'
		for prop in props:
			result += printProperty(prop)
		if tables:
			decHeaderLevel()
	return result


def printProperty(prop):
	global tables
	if tables:
		result  = newLine()
		result += '|' + prop.name
		result += '|' + (printSimpleTypeProperty(prop.type) if prop.type else ' ')
		result += '|' + (prop.value if prop.value else ' ')
		result += '|' + (printBoolean(prop.optional) if prop.optional else 'No')
		result += '|' + (printDoc(prop.doc) if prop.doc else ' ')
		result += '|'
	else:
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
			result += newLine() + '- Optional: ' + printBoolean(prop.optional)
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
	global hideDetails, tables
	if tables:
		incHeaderLevel()
		result = markdownHeader(module.name)
		if (hideDetails):
			return result;
		if (module.doc != None):
			result += '  ' + newLine() + printDoc(module.doc) + newLine()
		if (module.optional != None):
			result += newLine() + '- **Optional**: ' + printBoolean(module.optional)
		if (module.extends != None):
			result += printExtends(module.extends)
		if (module.properties != None and hideDetails == False):
			result += printProperties(module.properties)
		if (len(module.actions) > 0):
			incHeaderLevel()
			result += markdownHeader('Actions')
			result += newLine() + '|Return Type |Name |Arguments |Optional |Documentation |'
			result += newLine() + '|:-----------|:----|:---------|:--------|:-------------|'
			for action in module.actions:
				result += printAction(action)
			decHeaderLevel()
		if (len(module.data) > 0):
			incHeaderLevel()
			result += markdownHeader('Data')
			result += newLine() + '|Name |Type |Optional |Writable |Readable |Eventable |Documentation |'
			result += newLine() + '|:----|:----|:--------|:--------|:--------|:---------|:-------------|'
			for data in module.data:
				result += printDataPoint(data)
			decHeaderLevel()
		if (len(module.events) > 0):
			incHeaderLevel()
			result += markdownHeader('Events')
			result += newLine() + '|Name |Data |Optional |Documentation |'
			result += newLine() + '|:----|:----|:--------|:-------------|'
			for event in module.events:
				result += printEvent(event)
			decHeaderLevel()
		decHeaderLevel()

	else:
		result = '- **' + module.name + '**'
		if (hideDetails):
			return result;
		incTab()
		if (module.doc != None):
			result += '  ' + newLine() + printDoc(module.doc)
		if (module.extends != None):
			result += printExtends(module.extends)
		if (module.optional != None):
			result += newLine() + '- Optional: ' + printBoolean(module.optional)
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
	global tables
	if tables:
		incHeaderLevel()
		result  = markdownHeader('Extends')
		result += newLine() + '|Domain |Class |'
		result += newLine() + '|:------|:-----|'
		result += newLine() + '|' + extends.domain + '|' + extends.clazz + '|'
		#result += newLine() + '[**Extends**][extends]' + newLine()
		decHeaderLevel()
	else:
		result = newLine() + '- Extends'
		incTab()
		result += newLine() + '- Domain: **' + extends.domain + '**, Class: **' + extends.clazz + '**'
		decTab()
	return result


#
#	Action, Argument
#

def printAction(action):
	global tables

	if tables:
		result  = newLine()
		result += '|' + (printDataType(action.type) if action.type else 'None')
		result += '|' + action.name

		result += '|'
		if (len(action.args) > 0):
			for argument in action.args:
				result += printArgument(argument) + '<br />'
		else:
			result += 'None'
		result += ' '

		result += '|' + (printBoolean(action.optional) if action.optional else 'No')
		result += '|' + (printDoc(action.doc) if action.doc else ' ')
		result += '|'

	else:
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
			result += newLine() + '- Optional: ' + printBoolean(action.optional)

		decTab()
		decTab()
	return result

def printArgument(action):
	global tables

	if tables:
		result  =  (action.name if action.name != None else 'None') + ':'
		result += '&nbsp;' + (printDataType(action.type) if action.type != None else 'void')
	else:
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
	global tables

	if tables:
		result  = newLine()
		result += '|' + event.name
		result += '| '
		if (len(event.data) > 0):
			for dataPoint in event.data:
				result += dataPoint.name + ': '
				result += printDataType(dataPoint.type) + '<br />'
		result += '|' + (printBoolean(event.optional) if event.optional else 'No')
		result += '|' + (printDoc(event.doc) if event.doc else ' ')
		result += '|'

	else:
		incTab()
		result = newLine() + '- **' + event.name + '**'
		incTab()
		if (event.doc != None):
			result += '  ' + newLine() + printDoc(event.doc)
		if (event.optional != None):
			result += newLine() + '- Optional: ' + printBoolean(event.optional)

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
	global tables

	if tables:
		result  = newLine()
		result += '|' + datapoint.name
		result += '|' + printDataType(datapoint.type)
		result += '|' + (printBoolean(datapoint.optional) if datapoint.optional else 'No')
		result += '|' + (printBoolean(datapoint.writable) if datapoint.writable else 'Yes')
		result += '|' + (printBoolean(datapoint.readable) if datapoint.readable else 'Yes')
		result += '|' + (printBoolean(datapoint.eventable) if datapoint.eventable else 'No')
		result += '|' + (printDoc(datapoint.doc) if datapoint.doc else ' ')
		result += '|'
	else:
		incTab()
		result = newLine() + '- **' + datapoint.name + '**'
		if (datapoint.type != None):
			result += ': ' + printDataType(datapoint.type)
		incTab()
		if (datapoint.doc != None):
			result +=  '  ' + newLine() + printDoc(datapoint.doc)
		if (datapoint.optional != None):
			result += newLine() + '- Optional: ' + printBoolean(datapoint.optional)
		if (datapoint.writable != None):
			result += newLine() + '- Writable: ' + printBoolean(datapoint.writable)
		if (datapoint.readable != None):
			result += newLine() + '- Readable: ' + printBoolean(datapoint.readable)
		if (datapoint.eventable != None):
			result += newLine() + '- Eventable: ' + printBoolean(datapoint.eventable)
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
	global tables

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
		if tables:
			result += '; ' + printConstraint(constraint)
		else:
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

def printBoolean(value):
	return 'Yes' if value else 'No'

#
#	Doc
#

def printDoc(doc):
	result = doc.content.strip()
	return result

