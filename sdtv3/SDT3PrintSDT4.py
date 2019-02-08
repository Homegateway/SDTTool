#	SDT2PrintSDT4.py
#
#	Print SDT4 to SDT4

from .SDT3Classes import *
from common.SDTHelper import decTab, incTab, newLine

# TODO enum
# TODO extends class -> entity
# TODO Product
# TODO DataTypeRef

#
#	Print functions
#

def print2DomainSDT4(domain, options):
	result  = printXMLHeader(domain)
	incTab()
	if len(domain.includes) > 0:
		result += newLine() + printIncludes(domain.includes)
	if len(domain.modules) > 0:
		result += newLine() + printModules(domain.modules)
	if len(domain.devices) > 0:
		result += printDevices(domain.devices)
	decTab()
	result += newLine() + printXMLFooter()
	return result


def printXMLHeader(domain):
	result  = '<?xml version="1.0" encoding="iso-8859-1"?>'
	result += newLine() + '<Domain xmlns="http://homegatewayinitiative.org/xml/dal/4.0"'
	incTab()
	result += newLine() + 'xmlns:xi="http://www.w3.org/2001/XInclude"'
	result += newLine() + 'id="' + domain.id + '">'
	decTab()
	return result


def printXMLFooter():
	result = '</Domain>'
	return result


def printIncludes(includes):
	result  = newLine() + '<Imports>'
	for include in includes:
		incTab()
		result += newLine() + '<xi:include href="' + include.href + '" parse="' + include.parse + '" />'
		decTab()
	result += newLine() + '</Imports>'
	return result


#
#	Devices, SubDevices
#

def printDevices(devices):
	result = newLine() + newLine() + '<DeviceClasses>'
	incTab()
	for device in devices:
		result += printDevice(device)
	decTab()
	result += newLine() + '</DeviceClasses>'
	return result


def printDevice(device):
	result  = newLine() + '<DeviceClass id="' + device.id + '">'
	incTab()
	if device.doc:
		result += newLine() + printDoc(device.doc)
	if device.properties != None:
		result += newLine() + printProperties(device.properties)
	if len(device.modules) > 0:
		result += printModules(device.modules)
	if len(device.subDevices) > 0:
		result += newLine() + '<SubDevices>'
		incTab()
		for subDevice in device.subDevices:
			result += printSubDevice(subDevice)
		decTab()
		result += newLine() + '</SubDevices>'
	decTab()
	result += newLine() + '</DeviceClass>'
	return result


def printSubDevice(subDevice):
	result  = newLine() + '<SubDevice id="' + subDevice.id + '">'
	incTab()
	if subDevice.doc:
		result += newLine() + printDoc(subDevice.doc)
	if subDevice.properties != None:
		result += newLine() + printProperties(subDevice.properties)
	if len(subDevice.modules) > 0:
		result += printModules(subDevice.modules)
	decTab()
	result += newLine() + '</SubDevice>'
	return result


#
#	DeviceInfo
#

def printProperties(properties):
	result  = '<Properties>'
	incTab()
	for property in properties:
		result += newLine() + '<Property name="' + property.name + '"'
		if property.optional and property.optional == 'true':
			result += ' optional="true"'
		if property.value:
			result += ' value="'+ property.value + '"'
		result += '>'
		incTab()
		if property.doc:
			result += newLine() + printDoc(property.doc)
		result += newLine() + printSimpleType(property.type)
		decTab()
		result += newLine() + '</Property>'
	decTab()
	result += newLine() + '</Properties>'
	return result


#
#	ModuleClass
#

def printModules(modules):
	result  = newLine() + '<ModuleClasses>'
	incTab()
	for module in modules:
		result += printModule(module)
	decTab()
	result += newLine() + '</ModuleClasses>'
	return result


def printModule(module):
	result  = newLine() + '<ModuleClass name="' + module.name + '"'
	if module.optional and module.optional == 'true':
		result += ' optional="true"'
	result += '>'
	incTab()
	if module.extends != None:
		result += newLine() + '<extends domain="' + module.extends.domain + '" class="' + module.extends.clazz + '"/>'
	if module.doc != None:
		result += '  ' + newLine() + printDoc(module.doc)
	if len(module.actions) > 0:
		result += newLine() + '<Actions>'
		incTab()
		for action in module.actions:
			result += printAction(action)
		decTab()
		result += newLine() + '</Actions>'
	if len(module.data) > 0:
		result += newLine() + '<Data>'
		incTab()
		for data in module.data:
			result += printDataPoint(data)
		decTab()
		result += newLine() + '</Data>'
	if len(module.events) > 0:
		result += newLine() + '<Events>'
		incTab()
		for event in module.events:
			result += printEvent(event)
		decTab()
		result += newLine() + '</Events>'
	decTab()
	result += newLine() + '</ModuleClass>'
	return result


#
#	Action, Argument
#

def printAction(action):
	result = newLine() + '<Action name="' + action.name + '"'
	if action.optional and action.optional == 'true':
		result += ' optional="true"'
	result += '>'
	incTab()
	if action.doc != None:
		result += '  ' + newLine() + printDoc(action.doc)
	if action.type != None:
		result += newLine() + printDataType(action.type)
	if len(action.args) > 0:
		result += newLine() + '<Args>'
		incTab()
		for argument in action.args:
			result += printArgument(argument)
		decTab()
		result += newLine() + '</Args>'
	decTab()
	result += newLine() + '</Action>'
	return result


def printArgument(action):
	result  = newLine() + '<Arg name="' + action.name + '">'
	incTab();
	if (action.type):
		result += newLine() + printDataType(action.type)
	decTab()
	result += newLine() + '</Arg>'
	return result


#
#	Event
#

def printEvent(event):
	result = newLine() + '<Event name="' + event.name + '"'
	if module.optional and module.optional == 'true':
		result += ' optional="true"'
	result += '>'
	incTab()
	if event.doc != None:
		result += newLine() + printDoc(event.doc)
	if len(event.data) > 0:
		result += newLine() + '<Data>'
		incTab()
		for dataPoint in event.data:
			result += printDataPoint(dataPoint)
		decTab()
		result += newLine() + '</Data>'
	decTab()
	result += newLine() + '</Event>'
	return result


#
#	DataPoint
#

def printDataPoint(datapoint):
	result = newLine() + '<DataPoint name="' + datapoint.name + '"'
	if datapoint.optional and datapoint.optional == 'true':
		result += ' optional="true"'
	if datapoint.writable and datapoint.writable == 'false':
		result += ' writable="false"'
	if datapoint.readable and datapoint.readable == 'false':
		result += ' readable="false"'
	if datapoint.eventable and datapoint.eventable == 'true':
		result += ' eventable="true"'
	result += '>'

	incTab()
	if datapoint.doc != None:
		result += newLine() + printDoc(datapoint.doc)
	if datapoint.type != None:
		result += newLine() + printDataType(datapoint.type)
	decTab()
	result += newLine() + '</DataPoint>'
	return result


#
#	Print the data types
#
def printDataType(dataType):
	result = '<DataType'
	if dataType.name:
		result += ' name="' + dataType.name + '"'
	if dataType.unitOfMeasure:
		result += ' unitOfMeasure="' + dataType.unitOfMeasure + '"'
	result += '>'
	if dataType.doc != None:
		result += newLine() + printDoc(dataType.doc)
	incTab()
	if isinstance(dataType.type, SDT3SimpleType):
		result += newLine() + printSimpleType(dataType.type)
	elif isinstance(dataType.type, SDT3StructType):
		result += newLine() + printStructType(dataType.type)
	elif isinstance(dataType.type, SDT3ArrayType):
		result += newLine() + printArrayType(dataType.type)
	if dataType.constraints:
		result += newLine() + '<Constraints>'
		incTab()
		for constraint in dataType.constraints:
			result += printConstraint(constraint)
		decTab()
	decTab()
	result += newLine() + '</DataType>'
	return result


def printSimpleType(dataType):
	return '<SimpleType type="' + dataType.type + '" />'


def printStructType(dataType):
	result = '<StructType>'
	incTab()
	for element in dataType.type.structElements:
		result += newLine() + printDataType(element)
	decTab()
	result += '</StructType>'
	return result


def printArrayType(dataType):
	arrayType = dataType.type
	result = '<ArrayType>'
	incTab()
	result += newLine() + printDataType(dataType.arrayType)
	decTab()
	result += newLine() + '</ArrayType>'
	return result


def printConstraint(constraint):
	result = newLine() + '<Constraint name="' + containt.name + '"'
	if constraint.type:
		result += ' type="' + constraint.type + '"'
	if constraint.value:
		result += ' value="' + constraint.value + '"'
	result += '>'
	incTab()
	if constraint.doc != None:
		result += newLine() + printDoc(constraint.doc)
	decTab()
	result += newLine() + '</Constraint>'
	return result



#
#	Doc
#

def printDoc(doc):
	result = '<Doc>' + doc.content.strip() + '</Doc>'
	return result

