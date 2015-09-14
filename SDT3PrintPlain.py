#	SDT3PrintPlain.py
#
#	Print SDT3 to Plain text

from SDT3Classes import *

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

def print3DomainPlain(domain):
	result = 'Domain [id="' + domain.id + '"]'
	incTab()
	
	for include in domain.includes:
		result += newLine() + printInclude(include)

	# TODO print doc maybe
	
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
	result = 'Device [id="' + device.id + '"]'
	incTab()
	if (device.doc):
		result += newLine() + printDoc(device.doc)
	for deviceInfo in device.deviceInfos:
		result += newLine() + printDeviceInfo(deviceInfo)
	for module in device.modules:
		result += newLine() + printModule(module)
	for subDevice in device.subDevices:
		result += newLine() + printSubDevice(subDevice)
	decTab()
	return result


def printSubDevice(subDevice):
	result = 'SubDevice [id="' + subDevice.id + '"]'
	incTab()
	if (subDevice.doc):
		result += newLine() + printDoc(subDevice.doc)
	for deviceInfo in subDevice.deviceInfos:
		result += newLine() + printDeviceInfo(deviceInfo)
	for module in subDevice.modules:
		result += newLine() + printModule(module)
	decTab()
	return result


#
#	DeviceInfos
#

def printDeviceInfo(deviceInfo):
	result = 'DeviceInfo ['
	incTab()
	if (deviceInfo.name != None):
		result += 'name="' + deviceInfo.name + '"'
	if (deviceInfo.optional != None):
		result += ' optional="' + deviceInfo.optional + '"'
	result += ']'
	if (deviceInfo.doc):
		result += newLine() + printDoc(deviceInfo.doc)
	if (deviceInfo.type):
		result += newLine() + printDataType(deviceInfo.type)
	decTab()
	return result


#
#	Print Module, ModuleClass
#

def printModule(module):
	result =  'Module [name="' + module.name + '"]'
	result += printModuleDetails(module)
	return result

def printModuleClass(moduleClass):
	result =  'ModuleClass [name="' + moduleClass.name + '"]'
	result += printModuleDetails(moduleClass)
	return result

def printModuleDetails(module):
	incTab()
	result = ''
	if (module.extends != None):
		result += newLine() + printExtends(module.extends)
	if (module.doc != None):
		result += newLine() + printDoc(module.doc)
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

# TODO Doc

def printDataType(dataType):
	if (isinstance(dataType, SDT3SimpleType)):
		result = printSimpleType(dataType)
	elif (isinstance(dataType, SDT3StructType)):
		result = printStructType(dataType)
	elif (isinstance(dataType, SDT3ArrayType)):
		result = printArrayType(dataType)
	return result


def printSimpleType(dataType):
	result = 'SimpleType'
	result += printTypeAttributes(dataType)
	return result

def printStructType(dataType):
	result = 'Struct'
	result += printTypeAttributes(dataType)
	incTab()
	for element in dataType.structElements:
		result += newLine() + printDataType(element)
	decTab()
	return result

def printArrayType(dataType):
	result = 'Array'
	if (dataType.arrayType != None):
		incTab()
		result += newLine() + printDataType(dataType.arrayType)
		decTab()
	return result


def printTypeAttributes(dataType):
	result = ''
	if (dataType.name != None):
		result += 'name="' + dataType.name + '"'
	if (dataType.unitOfMeasure != None):
		if (len(result) > 0):
			result += ' '
		result += 'unitOfMeasure="' + dataType.unitOfMeasure + '"'
	if (hasattr(dataType, "type") and dataType.type != None):
		if (len(result) > 0):
			result += ' '
		result += 'type="' + dataType.type + '"'

# TODO Constraints


	if (len(result) > 0):
		result = ' [' + result + ']'
	return result


#
#	Doc
#

def printDoc(doc):
	incTab()
	result = 'Doc' + newLine() + doc.content.strip()
	decTab()
	return result
