#	SDT2PrintSDT4.py
#
#	Print SDT4 to SDT4

from .SDT3Classes import *
from common.SDTHelper import decTab, incTab, newLine

#
#	Print functions
#

def print2DomainSDT4(domain, options):
	result  = printXMLHeader(domain)
	incTab()
	result += r(printIncludes(domain.includes)) if len(domain.includes) > 0 else ''
	result += r(printModuleClasses(domain.modules)) if len(domain.modules) > 0 else ''
	result += r(printDevices(domain.devices)) if len(domain.devices) > 0 else ''
	decTab()
	result += r(printXMLFooter())
	return result


def printXMLHeader(domain):
	result  = '<?xml version="1.0" encoding="iso-8859-1"?>'
	result += r('<Domain xmlns="http://www.onem2m.org/xml/sdt/4.0"')
	incTab()
	result += r('xmlns:xi="http://www.w3.org/2001/XInclude"')
	result += r('id="' + domain.id + '">')
	decTab()
	return result


def printXMLFooter():
	return '</Domain>'


def printIncludes(includes):
	return _printList(includes, 'Imports', lambda x: r('<xi:include href="' + x.href + '" parse="' + x.parse + '" />'))


#
#	Devices, SubDevices
#

def printDevices(devices):
	return _printList(devices, 'DeviceClasses', printDevice)


def printDevice(device):
	result  = r('<DeviceClass id="' + device.id + '">')
	incTab()
	result += r(printDoc(device.doc)) if device.doc else ''
	result += printProperties(device.properties) if len(device.properties) > 0 else ''
	result += printModuleClasses(device.modules) if len(device.modules) > 0 else ''
	result += _printList(device.subDevices, 'SubDevices', printSubDevice)
	decTab()
	result += r('</DeviceClass>')
	return result


def printSubDevice(subDevice):
	result  = r('<SubDevice id="' + subDevice.id + '">')
	incTab()
	result += r(printDoc(subDevice.doc)) if subDevice.doc else ''
	result += printProperties(subDevice.properties) if len(subDevice.properties) > 0 else ''
	result += printModuleClasses(subDevice.modules) if len(subDevice.modules) > 0 else ''
	decTab()
	result += r('</SubDevice>')
	return result


#
#	DeviceInfo
#

def printProperties(properties):
	return _printList(properties, 'Properties', printProperty)


def printProperty(property):
	result += r('<Property name="' + property.name + '"')
	result += ' optional="true"' if property.optional is not None and property.optional == 'true' else ''
	result += ' value="'+ property.value + '"' if property.value else ''
	result += '>'
	incTab()
	result += r(printDoc(property.doc)) if property.doc else ''
	result += r(printSimpleType(property.type))
	decTab()
	result += newLine() + '</Property>'



#
#	ModuleClass
#

def printModuleClasses(moduleClasses):
	return _printList(moduleClasses, 'ModuleClasses', printModuleClass)



def printModuleClass(moduleClass):
	result  = r('<ModuleClass name="' + moduleClass.name + '"')
	result += ' optional="true"' if moduleClass.optional is not None and moduleClass.optional == 'true' else ''
	result += '>'
	incTab()
	result += r(printDoc(moduleClass.doc)) if moduleClass.doc != None else ''
	result += r('<Extend domain="' + moduleClass.extends.domain + '" entity="' + moduleClass.extends.clazz + '"/>') if moduleClass.extends != None else ''
	result += _printList(moduleClass.actions, 'Actions', printAction)
	result += _printList(moduleClass.data, 'Data', printDataPoint)
	result += _printList(moduleClass.events, 'Events', printEvent)
	decTab()
	result += r('</ModuleClass>')
	return result


#
#	Action, Argument
#

def printAction(action):
	result = r('<Action name="' + action.name + '"')
	result += ' optional="true"' if action.optional is not None and action.optional == 'true' else ''
	result += '>'
	incTab()
	result += r(printDoc(action.doc)) if action.doc != None else ''
	result += r(printDataType(action.type)) if action.type != None else ''
	result += _printList(action.args, 'Args', printArgument)
	decTab()
	result += r('</Action>')
	return result


def printArgument(action):
	result  = r('<Arg name="' + action.name + '">')
	incTab();
	result += r(printDataType(action.type)) if (action.type) else ''
	decTab()
	result += r('</Arg>')
	return result


#
#	Event
#

def printEvent(event):
	result = r('<Event name="' + event.name + '"')
	result += ' optional="true"'  if module.optional is not None and module.optional == 'true' else ''
	result += '>'
	incTab()
	result += r(printDoc(event.doc)) if event.doc != None else ''
	result += _printList(event.data, 'Data', printDataPoint)
	decTab()
	result += r('</Event>')
	return result


#
#	DataPoint
#

def printDataPoint(datapoint):
	result = r('<DataPoint name="' + datapoint.name + '"')
	result += ' optional="true"' if datapoint.optional is not None and datapoint.optional == 'true' else ''
	result += ' writable="false"' if datapoint.writable is not None and datapoint.writable == 'false' else ''
	result += ' readable="false"' if datapoint.readable is not None and datapoint.readable == 'false' else ''
	result += ' eventable="true"' if datapoint.eventable is not None and datapoint.eventable == 'true' else ''
	result += '>'
	incTab()
	result += r(printDoc(datapoint.doc)) if datapoint.doc != None else ''
	result += r(printDataType(datapoint.type)) if datapoint.type != None else ''
	decTab()
	result += r('</DataPoint>')
	return result


#
#	Print the data types
#
def printDataType(dataType):

	# special handling for oneM2M enum definitions up to v3
	name = dataType.type.type if isinstance(dataType.type, SDT3SimpleType) and dataType.type.type.startswith('hd:') else dataType.name

	result = '<DataType'
	result += ' name="' + name + '"' if name is not None else ''
	result += ' unitOfMeasure="' + dataType.unitOfMeasure + '"' if dataType.unitOfMeasure else ''
	result += '>'

	incTab()
	result += r(printDoc(dataType.doc)) if dataType.doc != None else ''
	if isinstance(dataType.type, SDT3SimpleType):
		result += newLine() + printSimpleType(dataType.type)
	elif isinstance(dataType.type, SDT3StructType):
		result += newLine() + printStructType(dataType.type)
	elif isinstance(dataType.type, SDT3ArrayType):
		result += newLine() + printArrayType(dataType.type)
	result += _printList(dataType.constraints, 'Constraints', printConstraint)
	decTab()
	result += r('</DataType>')
	return result


def printSimpleType(dataType):
	result = '<Simple type="' + dataType.type + '" />'
	# hack for oneM2M enums
	if dataType.type.startswith('hd:'):
		result  = '<Enum>'
		incTab()
		result += r('<!-- TODO: Add enum values -->')
		result += r('<EnumValue name="name" value="1" />')
		decTab()
		result += r('</Enum>')
	return result


def printStructType(dataType):
	result = '<Struct>'
	incTab()
	for element in dataType.type.structElements:
		result += newLine() + printDataType(element)
	decTab()
	result += '</Struct>'
	return result


def printArrayType(dataType):
	result = '<Array>'
	incTab()
	result += r(printDataType(dataType.arrayType))
	decTab()
	result += r('</Array>')
	return result


def printConstraint(constraint):
	result = r('<Constraint name="' + containt.name + '"')
	result += ' type="' + constraint.type + '"' if constraint.type else ''
	result += ' value="' + constraint.value + '"' if constraint.value is not None else ''
	result += '>'
	incTab()
	result += r(printDoc(constraint.doc)) if constraint.doc != None else ''
	decTab()
	result += newLine() + '</Constraint>'
	return result


#
#	Doc
#

def printDoc(doc):
	return '<Doc>' + doc.content.strip() + '</Doc>'


#
#	misc functions to help printing results
#

def _printList(lst, element, func):
	result = ''
	if len(lst) > 0:
		result += '%s<%s>' % (newLine(), element)
		incTab()
		for l in lst:
			result += func(l)
		decTab()
		result += '%s</%s>' % (newLine(), element)
	return result


def r(line):
	return '%s%s' % (newLine(), line)