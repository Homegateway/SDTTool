#	SDT2PrintSDT3.py
#
#	Print SDT2 to SDT3


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

def print2DomainSDT3(domain):
	result  = printXMLHeader(domain)
	incTab()
	if (len(domain.includes) > 0):
		result += newLine() + printIncludes(domain.includes)
	if (len(domain.modules) > 0):
		result += newLine() + printModules(domain.modules, True)
	if (len(domain.rootDevices) > 0):
		result += printRootDevices(domain.rootDevices)
	decTab()
	result += newLine() + printXMLFooter()
	return result


def printXMLHeader(domain):
	result  = '<?xml version="1.0" encoding="iso-8859-1"?>'
	result += newLine() + '<Domain xmlns="http://homegatewayinitiative.org/xml/dal/3.0"'
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
#	Simple Data Type
#	Others are not needed for the conversion from SDT version 2 to 3
#

def printSimpleType(type):
	return '<SimpleType type="' + type + '" />'


#
#	RootDevice, Device
#

def printRootDevices(rootDevices):
	result = newLine() + newLine() + '<Devices>'
	incTab()
	for rootDevice in rootDevices:
		result += printRootDevice(rootDevice)
	decTab()
	result += newLine() + '</Devices>'
	return result


def printRootDevice(rootDevice):
	result  = newLine() + '<Device id="' + rootDevice.id + '">'
	incTab()
	if (rootDevice.doc):
		result += newLine() + printDoc(rootDevice.doc)
	if (rootDevice.deviceInfo != None):
		result += newLine() + printDeviceInfo(rootDevice.deviceInfo)
	if (len(rootDevice.modules) > 0):
		result += printModules(rootDevice.modules)
	if (len(rootDevice.devices) > 0):
		result += newLine() + '<SubDevices>'
		incTab()
		for device in rootDevice.devices:
			result += printDevice(device)
		decTab()
		result += newLine() + '</SubDevices>'
	decTab()
	result += newLine() + '</Device>'
	return result


def printDevice(device):
	result  = newLine() + '<SubDevice id="' + device.id + '">'
	incTab()
	if (device.doc):
		result += newLine() + printDoc(device.doc)
	if (device.deviceInfo != None):
		result += newLine() + printDeviceInfo(device.deviceInfo)
	if (len(device.modules) > 0):
		result += printModules(device.modules)
	decTab()
	result += newLine() + '</SubDevice>'
	return result


#
#	DeviceInfo
#

def printDeviceInfo(deviceInfo):
	result  = '<DeviceInfos>'
	incTab()
	if (deviceInfo.name != None):
		result += newLine() + '<DeviceInfo name="Name">'
		incTab()
		result += newLine() + '<Doc>Original value: ' + deviceInfo.name + '</Doc>'
		result += newLine() + printSimpleType('string')
		decTab()
		result += newLine() + '</DeviceInfo>'
	if (deviceInfo.vendor != None):
		result += newLine() + '<DeviceInfo name="Vendor">'
		incTab()
		result += newLine() + '<Doc>Original value: ' + deviceInfo.vendor + '</Doc>'
		result += newLine() + printSimpleType('string')
		decTab()
		result += newLine() + '</DeviceInfo>'
	if (deviceInfo.serialNumber != None):
		result += newLine() + '<DeviceInfo name="SerialNumber">'
		incTab()
		result += newLine() + '<Doc>Original value: ' + deviceInfo.serialNumber + '</Doc>'
		result += newLine() + printSimpleType('string')
		decTab()
		result += newLine() + '</DeviceInfo>'
	if (deviceInfo.vendorURL != None):
		result += newLine() + '<DeviceInfo name="VendorURL">'
		incTab()
		result += newLine() + '<Doc>Original value: ' + deviceInfo.vendorURL + '</Doc>'
		result += newLine() + printSimpleType('uri')
		decTab()
		result += newLine() + '</DeviceInfo>'
	if (deviceInfo.firmwareVersion != None):
		result += newLine() + '<DeviceInfo name="FirmwareVersion">'
		incTab()
		result += newLine() + '<Doc>Original value: ' + deviceInfo.firmwareVersion + '</Doc>'
		result += newLine() + printSimpleType('string')
		decTab()
		result += newLine() + '</DeviceInfo>'
	decTab()
	result += newLine() + '</DeviceInfos>'
	return result


#
#	Print Module, ModuleClass
#

def printModules(modules, isModuleClazz=False):
	result  = newLine() + '<Modules>'
	incTab()
	for module in modules:
		result += printModule(module, isModuleClazz)
	decTab()
	result += newLine() + '</Modules>'
	return result

def printModule(module, isModuleClazz=False):
	elem = 'ModuleClass' if isModuleClazz else 'Module'
	result  = newLine() + '<' + elem + ' name="' + module.name + '">'
	incTab()
	if (module.extends != None):
		result += newLine() + '<extends domain="' + module.extends.domain + '" class="' + module.extends.clazz + '"/>'
	if (module.doc != None):
		result += '  ' + newLine() + printDoc(module.doc)
	if (len(module.actions) > 0):
		result += newLine() + '<Actions>'
		incTab()
		for action in module.actions:
			result += printAction(action)
		decTab()
		result += newLine() + '</Actions>'
	if (len(module.data) > 0):
		result += newLine() + '<Data>'
		incTab()
		for data in module.data:
			result += printDataPoint(data)
		decTab()
		result += newLine() + '</Data>'
	if (len(module.events) > 0):
		result += newLine() + '<Events>'
		incTab()
		for event in module.events:
			result += printEvent(event)
		decTab()
		result += newLine() + '</Events>'
	decTab()
	result += newLine() + '</' + elem + '>'
	return result


#
#	Action, Argument
#

def printAction(action):
	result = newLine() + '<Action name="' + action.name + '">'
	incTab()
	if (action.doc != None): 
		result += '  ' + newLine() + printDoc(action.doc)
	if (action.type != None):
		result += newLine() + printSimpleType(action.type)
	if (len(action.arg) > 0):
		result += newLine() + '<Args>'
		incTab()
		for argument in action.arg:
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
		result += newLine() + printSimpleType(action.type)
	decTab()
	result += newLine() + '</Arg>'
	return result


#
#	Event
#

def printEvent(event):
	result = newLine() + '<Event name="' + event.name + '">'
	incTab()
	if (event.doc != None):
		result += newLine() + printDoc(event.doc)
	if (len(event.data) > 0):
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
	if (datapoint.writable != None):
		result += ' writable="' + datapoint.writable + '"'
	if (datapoint.readable != None):
		result += ' readable="' + datapoint.readable + '"'
	if (datapoint.eventable != None):
		result += ' eventable="' + datapoint.eventable + '"'
	result += '>'

	incTab()
	if (datapoint.doc != None):
		result += newLine() + printDoc(datapoint.doc)
	if (datapoint.type != None):
		result += newLine() + printSimpleType(datapoint.type)
	decTab()
	result += newLine() + '</DataPoint>'
	return result


#
#	Doc
#

def printDoc(doc):
	result = '<Doc>' + doc.content.strip() + '</Doc>'
	return result

