#	SDT3PrintOPML.py
#
#	Print SDT3 to OPML

import cgi

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


#
#	Print functions
#

def print3DomainOPML(domain, options):
	global hideDetails
	hideDetails = options['hideDetails']

	result  = '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
	result += '<opml version="1.0">\n'
	result += '<head>\n'
	result += '</head>\n'
	result += '<body>\n'
	result += '<outline text="Domain [id=&quot;' + domain.id + '&quot;]" >'
	incTab()

	if (len(domain.includes) > 0):
		result += newLine() + '<outline text="Includes">'
		incTab()
		for include in domain.includes:
			result += newLine() + printInclude(include)
		decTab()
		result += newLine() + '</outline>'

	if (domain.doc and hideDetails == False):
		result += newLine() + printDoc(domain.doc)

	if (len(domain.modules) > 0):
		result += newLine() + '<outline text="ModuleClasses">'
		incTab()
		for module in domain.modules:
			result += newLine() + printModuleClass(module)
		decTab()
		result += newLine() + '</outline>'

	if (len(domain.devices) > 0):
		result += newLine() + '<outline text="Devices">'
		incTab()
		for device in domain.devices:
			result += newLine() + printDevice(device)
		decTab()
		result += newLine() + '</outline>'

	decTab()
	result += newLine() + '</outline>\n'
	result += '</body>\n'
	result += '</opml>\n'
	return result

def printInclude(include):
	return '<outline text="Include [parse=&quot;' + include.parse + '&quot; href=&quot;' + include.href + '&quot;]" />'


#
#	Device, SubDevice
#

def printDevice(device):
	global hideDetails

	result = '<outline text="Device [id=&quot;' + device.id + '&quot;]" >'
	incTab()

	if (device.doc and hideDetails == False):
		result += newLine() + printDoc(device.doc)

	if (len(device.modules) > 0):
		result += newLine() + '<outline text="Modules">'
		incTab()
		for module in device.modules:
			result += newLine() + printModule(module)
		decTab()
		result += newLine() + '</outline>'
	
	if (len(device.subDevices) > 0):
		result += newLine() + '<outline text="SubDevices">'
		incTab()
		for subDevice in device.subDevices:
			result += newLine() + printSubDevice(subDevice)
		decTab()
		result += newLine() + '</outline>'

	if (len(device.properties) > 0):
		result += newLine() + '<outline text="Properties">'
		incTab()
		for prop in device.properties:
			result += newLine() + printProperty(prop)
		decTab()
		result += newLine() + '</outline>'

	decTab()
	result += newLine() + '</outline>'
	return result


def printSubDevice(subDevice):
	global hideDetails

	result = '<outline text="SubDevice [id=&quot;' + subDevice.id + '&quot;]">'
	incTab()

	if (subDevice.doc and hideDetails == False):
		result += newLine() + printDoc(subDevice.doc)
	if (len(subDevice.modules) > 0):
		result += newLine() + '<outline text="Modules">'
		incTab()
		for module in subDevice.modules:
			result += newLine() + printModule(module)
		decTab()
		result += newLine() + '</outline>'
	if (len(subDevice.properties) > 0):
		result += newLine() + '<outline text="Properties">'
		incTab()
		for prop in subDevice.properties:
			result += newLine() + printProperty(prop)
		decTab()
		result += newLine() + '</outline>'
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	Property
#

def printProperty(prop):
	result = '<outline text="Property ['
	attr =''
	if prop.name != None:
		if len(attr) > 0:
			attr += ' '
		result += 'name=&quot;' + prop.name + '&quot;'
	if prop.type != None:
		if len(attr) > 0:
			attr += ' '
		result += 'type=&quot;' + printSimpleTypeProperty(prop.type) + '&quot;'
	if prop.value != None:
		if len(attr) > 0:
			attr += ' '
		result += 'value=&quot;' + prop.value + '&quot;'
	if prop.optional != None:
		if len(attr) > 0:
			attr += ' '
		result += 'optional=&quot;' + prop.optional + '&quot;'
	result += attr + ']">'
	incTab()
	if (prop.doc):
		result += newLine() + printDoc(prop.doc)
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	Print Module, ModuleClass
#

def printModule(module):
	global hideDetails

	result =  '<outline text="Module [name=&quot;' + module.name + '&quot;'
	if (module.optional != None):
		result += ' optional=&quot;' + module.optional + '&quot;'
	result += ']">'
	if (hideDetails == False):
		result += printModuleDetails(module)
	result += newLine() + '</outline>'
	return result


def printModuleClass(moduleClass):
	global hideDetails

	result =  '<outline text="ModuleClass [name=&quot;' + moduleClass.name + '&quot;'
	if (moduleClass.optional != None):
		result += ' optional=&quot;' + module.optional + '&quot;'
	result += ']">'
	if (hideDetails == False):
		result += printModuleDetails(moduleClass)
	result += newLine() + '</outline>'
	return result


def printModuleDetails(module):
	incTab()
	result = ''
	if (module.extends != None):
		result += newLine() + printExtends(module.extends)
	
	if (module.doc != None):
		result += newLine() + printDoc(module.doc)

	if (len(module.actions) > 0):
		result += newLine() + '<outline text="Actions">'
		incTab()
		for action in module.actions:
			result += newLine() + printAction(action)
		decTab()
		result += newLine() + '</outline>'

	if (len(module.data) > 0):
		result += newLine() + '<outline text="Data">'
		incTab()
		for data in module.data:
			result += newLine() + printDataPoint(data)
		decTab()
		result += newLine() + '</outline>'

	if (len(module.events) > 0):
		result += newLine() + '<outline text="Events">'
		incTab()
		for event in module.events:
			result += newLine() + printEvent(event)
		decTab()
		result += newLine() + '</outline>'

	if (len(module.properties) > 0):
		result += newLine() + '<outline text="Properties">'
		incTab()
		for prop in module.properties:
			result += newLine() + printProperty(prop)
		decTab()
		result += newLine() + '</outline>'

	decTab()
	return result


def printExtends(extends):
	return '<outline text="Extends [domain=&quot;' + extends.domain + '&quot; class=&quot;' + extends.clazz + '&quot;]" />'


#
#	Action, Argument
#

def printAction(action):
	result = '<outline text="Action [name=&quot;' + action.name + '&quot;'
	if (action.optional != None):
		result += ' optional=&quot;' + action.optional + '&quot;'
	result += ']">'

	incTab()
	if (action.doc != None): 
		result += newLine() + printDoc(action.doc)

	if (action.type != None):
		result += newLine() + printDataType(action.type)

	if (len(action.args) > 0):
		result += newLine() + '<outline text="Args">'
		incTab()
		for argument in action.args:
			result += newLine() + printArgument(argument)
		decTab()
		result += newLine() + '</outline>'

	decTab()
	result += newLine() + '</outline>'
	return result


def printArgument(action):
	result = '<outline text="Arg ['
	if (action.name != None):
		result += 'name=&quot;' + action.name + '&quot;'
	result += ']">'
	incTab()
	if (action.type != None):
		result += newLine() + printDataType(action.type)
	decTab()
	result += newLine() + '</outline>'
	return result


#
#             Event
#

def printEvent(event):
	result = '<outline text="Event [name=&quot;' + event.name + '&quot;'
	if (event.optional != None):
		result += ' optional=&quot;' + event.optional + '&quot;'
	result += ']">'
	incTab()
	if (event.doc != None):
		result += newLine() + printDoc(event.doc)
	if (len(event.data) > 0):
		result += newLine() + '<outline text="Data">'
		incTab()
		for dataPoint in event.data:
			result += newLine() + printDataPoint(dataPoint)
		decTab()
		result += newLine() + '</outline>'
	decTab()
	result += newLine() + '</outline>'
	return result

 

#
#	DataPoint
#

def printDataPoint(datapoint):
	result = '<outline text="DataPoint [name=&quot;' + datapoint.name + '&quot;'
	if (datapoint.optional != None):
		result += ' optional=&quot;' + datapoint.optional + '&quot;'
	if (datapoint.writable != None):
		result += ' writable=&quot;' + datapoint.writable + '&quot;'
	if (datapoint.readable != None):
		result += ' readable=&quot;' + datapoint.readable + '&quot;'
	if (datapoint.eventable != None):
		result += ' eventable=&quot;' + datapoint.eventable + '&quot;'
	result += ']">'
	incTab()
	if (datapoint.doc != None):
		result += newLine() + printDoc(datapoint.doc)
	if (datapoint.type != None):
		result += newLine() + printDataType(datapoint.type)
	decTab()
	result += newLine() + '</outline>'
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
	result  = '<outline text="SimpleType [type=&quot;' + simpleType.type + '&quot;'
	result += printDataTypeAttributes(dataType)
	result += ']">'
	incTab()
	if (dataType.doc != None):
		result += newLine() + printDoc(dataType.doc)
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	result += newLine() + '</outline>'
	return result


def printSimpleTypeProperty(simpleType):
	result = ''
	if (len(result) > 0):
		result += ' '
	result += simpleType.type
	return result


def printStructType(dataType):
	result = '<ouline text="Struct'
	attr = printDataTypeAttributes(dataType)
	if (len(attr) > 0):
		result += ' [' + attr + ']'
	result += '">'

	incTab()
	for element in dataType.type.structElements:
		result += newLine() + printDataType(element)
	decTab()
	if (dataType.doc != None):
		result += newLine() + printDoc(dataType.doc)
	incTab()
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	result += '</outline>'
	return result

def printArrayType(dataType):
	arrayType = dataType.type
	result = '<outline text="Array'
	attr = printDataTypeAttributes(dataType)
	if (len(attr) > 0):
		result += ' [' + attr + ']'
	result += '">'
	incTab()
	if (arrayType.arrayType != None):
		result += newLine() + printDataType(arrayType.arrayType)
	if (dataType.doc != None):
		result += newLine() + printDoc(dataType.doc)
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	result += newLine() + '</outline>'
	return result

def printDataTypeAttributes(dataType):
	result = ''
	if (dataType.name != None):
		result += 'name=&quot;' + dataType.name + '&quot;'
	if (dataType.unitOfMeasure != None):
		if (len(result) > 0):
			result += ' '
		result += 'unitOfMeasure=&quot;' + dataType.unitOfMeasure + '&quot;'
	return result


def printConstraint(constraint):
	result = '<outline text="Constraint ['
	attr   = ''
	if (constraint.name != None):
		attr += 'name=&quot;' + constraint.name + '&quot;'
	if (constraint.type != None):
		if (len(attr) > 0):
			attr += ' '
		attr += 'type=&quot;' + constraint.type + '&quot;'
	if (constraint.value != None):
		if (len(attr) > 0):
			attr += ' '
		attr += 'value=&quot;' + constraint.value + '&quot;'
	if (len(attr) > 0):
		result += attr
	result += ']">'
	incTab()
	if (constraint.doc != None):
		attr += newLine() + printDoc(constraint.doc)
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	Doc
#

def printDoc(doc):
	incTab()
	result = '<outline text="Doc">'
	s = cgi.escape(doc.content.strip())
	s = s.replace('"', '&quot;')
	result += newLine() + '<outline text="' + s + '" />'
	decTab()
	result += newLine() + '</outline>'
	return result
