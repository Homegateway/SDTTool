#	SDT3PrintOPML.py
#
#	Print SDT3 to OPML

import cgi

from .SDT3Classes import *
from common.SDTHelper import *

hideDetails = False


#
#	Print functions
#

def print3DomainOPML(domain, options):
	global hideDetails
	
	# set double white space as an indention for ompl files
	setTabChar('\t')
	
	hideDetails = options['hideDetails']

	result  = '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
	result += '<opml version="1.0">\n'
	result += '<head>\n'
	result += '</head>\n'
	result += '<body>\n'
	result += '<outline text="' + domain.id + '" >'
	incTab()

	if len(domain.includes) > 0:
		result += newLine() + '<outline text="Includes">'
		incTab()
		for include in domain.includes:
			result += newLine() + printInclude(include)
		decTab()
		result += newLine() + '</outline>'

	if domain.doc and hideDetails == False:
		result += newLine() + printDoc(domain.doc)

	if len(domain.modules) > 0:
		result += newLine() + '<outline text="ModuleClasses">'
		incTab()
		for module in domain.modules:
			result += newLine() + printModuleClass(module)
		decTab()
		result += newLine() + '</outline>'

	if len(domain.devices) > 0:
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
	return '<outline text="' + include.href + ' (' + include.parse + ')" />'


#
#	Device, SubDevice
#

def printDevice(device):
	global hideDetails

	result = '<outline text="' + device.id + '">'
	incTab()

	if device.doc and hideDetails == False:
		result += newLine() + printDoc(device.doc)
	if len(device.properties) > 0:
		result += newLine() + '<outline text="Properties">'
		incTab()
		for prop in device.properties:
			result += newLine() + printProperty(prop)
		decTab()
		result += newLine() + '</outline>'
	if len(device.modules) > 0:
		result += newLine() + '<outline text="Modules">'
		incTab()
		for module in device.modules:
			result += newLine() + printModule(module)
		decTab()
		result += newLine() + '</outline>'
	if len(device.subDevices) > 0:
		result += newLine() + '<outline text="SubDevices">'
		incTab()
		for subDevice in device.subDevices:
			result += newLine() + printSubDevice(subDevice)
		decTab()
		result += newLine() + '</outline>'

	decTab()
	result += newLine() + '</outline>'
	return result


def printSubDevice(subDevice):
	global hideDetails

	result = '<outline text="' + subDevice.id + '">'
	incTab()

	if subDevice.doc and hideDetails == False:
		result += newLine() + printDoc(subDevice.doc)
	if len(subDevice.properties) > 0:
		result += newLine() + '<outline text="Properties">'
		incTab()
		for prop in subDevice.properties:
			result += newLine() + printProperty(prop)
		decTab()
		result += newLine() + '</outline>'
	if len(subDevice.modules) > 0:
		result += newLine() + '<outline text="Modules">'
		incTab()
		for module in subDevice.modules:
			result += newLine() + printModule(module)
		decTab()
		result += newLine() + '</outline>'
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	Property
#

def printProperty(prop):
	result = '<outline text="' + prop.name + '" >'
	incTab()
	if prop.doc:
		result += newLine() + printDoc(prop.doc)
	if prop.type:
		result += newLine() + '<outline text="' + printSimpleTypeProperty(prop.type) + '" />'
	opt = []
	if prop.value:
		result += newLine() +  '<outline text="value: ' + prop.value + '" />'
	presult = printOptional(prop.optional)
	if len(presult) > 0:
		opt.append(presult)
	if len(opt) > 0:
		result += '<outline text="' + '&lt;br /&gt;'.join(opt) + '" />'
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	Print Module, ModuleClass
#

def printModule(module):
	global hideDetails

	result =  '<outline text="' + module.name + '">'
	if hideDetails == False:
		result += printModuleDetails(module)
	result += newLine() + '</outline>'
	return result


def printModuleClass(moduleClass):
	global hideDetails

	result =  '<outline text="' + moduleClass.name + '" >'
	if hideDetails == False:
		result += printModuleDetails(moduleClass)
	result += newLine() + '</outline>'
	return result


def printModuleDetails(module):
	incTab()
	result = ''
	if module.doc:
		result += newLine() + printDoc(module.doc)
	if module.extends:
		result += newLine() + printExtends(module.extends)
	if module.optional:
		result += newLine() + '<outline text="optional: ' + module.optional + '" />'
	if len(module.data) > 0:
		result += newLine() + '<outline text="DataPoints">'
		incTab()
		for data in module.data:
			result += newLine() + printDataPoint(data)
		decTab()
		result += newLine() + '</outline>'
	if len(module.actions) > 0:
		result += newLine() + '<outline text="Actions">'
		incTab()
		for action in module.actions:
			result += newLine() + printAction(action)
		decTab()
		result += newLine() + '</outline>'
	if len(module.events) > 0:
		result += newLine() + '<outline text="Events">'
		incTab()
		for event in module.events:
			result += newLine() + printEvent(event)
		decTab()
		result += newLine() + '</outline>'
	if len(module.properties) > 0:
		result += newLine() + '<outline text="Properties">'
		incTab()
		for prop in module.properties:
			result += newLine() + printProperty(prop)
		decTab()
		result += newLine() + '</outline>'

	decTab()
	return result


def printExtends(extends):
	return '<outline text="Extends&lt;br /&gt;&lt;br /&gt;domain: ' + extends.domain + '&lt;br /&gt;class: ' + extends.clazz + '" />'


#
#	Action, Argument
#

def printAction(action):
	result = '<outline text="' + action.name + '">'
	incTab()
	if action.doc: 
		result += newLine() + printDoc(action.doc)
	if action.optional:
		result += newLine() + '<outline text="optional: ' + action.optional + '" />'
	if action.type:
		result += newLine() + printDataType(action.type, "Returns&lt;br /&gt;&lt;br /&gt;")
	if len(action.args) > 0:
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
	result = '<outline text="' + action.name + '">'
	incTab()
	if action.type:
		result += newLine() + printDataType(action.type)
	decTab()
	result += newLine() + '</outline>'
	return result


#
#   Event
#

def printEvent(event):
	result = '<outline text="' + event.name + '" >'
	incTab()
	if event.doc:
		result += newLine() + printDoc(event.doc)
	if event.optional:
		result += '<outline text="optional: ' + event.optional + '" />'
	if len(event.data) > 0:
		result += newLine() + '<outline text="DataPoints">'
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
	result = '<outline text="' + datapoint.name + '">'
	incTab()
	if datapoint.doc:
		result += newLine() + printDoc(datapoint.doc)
	if datapoint.type:
		result += newLine() + printDataType(datapoint.type)

	# Handle some optional attributes
	opt = []
	presult = printOptional(datapoint.optional)
	if len(presult) > 0:
		opt.append(presult)
	presult = printReadable(datapoint.readable)
	if len(presult) > 0:
		opt.append(presult)
	presult = printWritable(datapoint.writable)
	if len(presult) > 0:
		opt.append(presult)
	presult = printEventable(datapoint.eventable)
	if len(presult) > 0:
		opt.append(presult)
	if len(opt) > 0:
		result += '<outline text="' + '&lt;br /&gt;'.join(opt) + '" />'
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	DataTypes
#

def printDataType(dataType, prefixtext=""):
	if isinstance(dataType.type, SDT3SimpleType):
		result = printSimpleType(dataType, prefixtext)
	elif isinstance(dataType.type, SDT3StructType):
		result = printStructType(dataType, prefixtext)
	elif isinstance(dataType.type, SDT3ArrayType):
		result = printArrayType(dataType, prefixtext)
	return result


def printSimpleType(dataType, prefixtext=''):
	simpleType = dataType.type
	result  = '<outline text="' + prefixtext + simpleType.type + '">'
	incTab()
	if dataType.doc:
		result += newLine() + printDoc(dataType.doc)
	result += printDataTypeAttributes(dataType)
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	result += newLine() + '</outline>'
	return result


def printSimpleTypeProperty(simpleType):
	result = ''
	if len(result) > 0:
		result += ' '
	result += simpleType.type
	return result


def printStructType(dataType, prefixtext=""):
	result = '<outline text="' + prefixtext
	if dataType.name:
		result += dataType.name + ': '
	result += 'Struct">'
	incTab()
	if dataType.doc:
		result += newLine() + printDoc(dataType.doc)
	result += printDataTypeAttributes(dataType)
	for element in dataType.type.structElements:
		result += newLine() + printDataType(element)
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	result += newLine() + '</outline>'
	return result


def printArrayType(dataType, prefixtext):
	result = '<outline text="' + prefixtext
	if dataType.name:
		result += dataType.name + ': '
	result += 'Array">'
	incTab()
	if dataType.doc:
		result += newLine() + printDoc(dataType.doc)
	result += printDataTypeAttributes(dataType)
	if dataType.type.arrayType:
		result += newLine() + printDataType(dataType.type.arrayType)
	for constraint in dataType.constraints:
		result += newLine() + printConstraint(constraint)
	decTab()
	result += newLine() + '</outline>'
	return result

def printDataTypeAttributes(dataType):
	result = ''
#	if dataType.name:
#		result += newLine() + '<outline text="name: ' + dataType.name + '" />'
	if dataType.unitOfMeasure:
		result += newLine() + '<outline text="unitOfMeasure: ' + dataType.unitOfMeasure + '" />'
	return result


def printConstraint(constraint):
	attr   = []
	result = ''
	if constraint.name:
		attr.append('name: ' + constraint.name)
	if constraint.type:
		attr.append('type: ' + constraint.type)
	if constraint.value:
		attr.append('value: ' + constraint.value)
	if len(attr) > 0:
		result += '<outline text="Constraint&lt;br /&gt;&lt;br /&gt;' + '&lt;br /&gt;'.join(attr) + '">'
	incTab()
	if constraint.doc:
		attr += newLine() + printDoc(constraint.doc)
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	Doc
#
def printDoc(doc):
	result = ''
	incTab()
	s = cgi.escape(doc.content.strip())
	s = s.replace('"', '&quot;')
	result += newLine() + '<outline text="' + s + '" />'
	decTab()
	return result

#
#	various attribute
#
def printOptional(optional):
	result = ''
	if optional:
		result += 'optional: ' + optional
	return result

def printWritable(writable):
	result = ''
	if writable:
		result += 'writable: ' + writable
	return result

def printReadable(readable):
	result = ''
	if readable:
		result += 'readable: ' + readable
	return result

def printEventable(eventable):
	result = ''
	if eventable:
		result += 'eventable: ' + eventable
	return result


