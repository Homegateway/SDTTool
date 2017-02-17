#	SDT2PrintOPML.py
#
#	Print SDT2 to OPML


import cgi

from .SDT2Classes import *

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

def print2DomainOPML(domain, options):
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

	if (len(domain.modules) > 0):
		result += newLine() + '<outline text="ModuleClasses">'
		incTab()
		for module in domain.modules:
			result += newLine() + printModuleClass(module)
		decTab()
		result += newLine() + '</outline>'

	if (len(domain.rootDevices) > 0):
		result += newLine() + '<outline text="RootDevices">'
		incTab()
		for rootDevice in domain.rootDevices:
			result += newLine() + printRootDevice(rootDevice)
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
#	RootDevice, Device
#

def printRootDevice(rootDevice):
	global hideDetails

	result = '<outline text="RootDevice [id=&quot;' + rootDevice.id + '&quot;]" >'
	incTab()

	if (rootDevice.deviceInfo != None and hideDetails == False):
		result += newLine() + printDeviceInfo(rootDevice.deviceInfo)
	if (rootDevice.doc and hideDetails == False):
		result += newLine() + printDoc(rootDevice.doc)

	if (len(rootDevice.modules) > 0):
		result += newLine() + '<outline text="Modules">'
		incTab()
		for module in rootDevice.modules:
			result += newLine() + printModule(module)
		decTab()
		result += newLine() + '</outline>'
	
	if (len(rootDevice.devices) > 0):
		result += newLine() + '<outline text="Devices">'
		incTab()
		for device in rootDevice.devices:
			result += newLine() + printDevice(device)
		decTab()
		result += newLine() + '</outline>'
	
	decTab()
	result += newLine() + '</outline>'
	return result


def printDevice(device):
	global hideDetails

	result = '<outline text="Device [id=&quot;' + device.id + '&quot;]">'
	incTab()

	if (device.deviceInfo != None and hideDetails == False):
		result += newLine() + printDeviceInfo(device.deviceInfo)
	if (device.doc and hideDetails == False):
		result += newLine() + printDoc(device.doc)
	if (len(device.modules) > 0):
		result += newLine() + '<outline text="Modules">'
		incTab()
		for module in device.modules:
			result += newLine() + printModule(module)
		decTab()
		result += newLine() + '</outline>'
	decTab()
	result += newLine() + '</outline>'
	return result


#
#	DeviceInfo
#

def printDeviceInfo(deviceInfo):
	result = '<outline text="DeviceInfo">'
	incTab()
	if (deviceInfo.name != None):
		result += newLine() + '<outline text="name=&quot;' + deviceInfo.name + '&quot;"/>'

	if (deviceInfo.vendor != None):
		result += newLine() + '<outline text="vendor=&quot;' + deviceInfo.vendor + '&quot;"/>'
	
	if (deviceInfo.serialNumber != None):
		result += newLine() + '<outline text="serialNumber=&quot;' + deviceInfo.serialNumber + '&quot;"/>'
	
	if (deviceInfo.vendorURL != None):
		result += newLine() + '<outline text="vendorURL=&quot;' + deviceInfo.vendorURL + '&quot;"/>'

	if (deviceInfo.firmwareVersion != None):
		result += newLine() + '<outline text="firmwareVersion=&quot;' + deviceInfo.firmwareVersion + '&quot;"/>'

	decTab()
	result += newLine() + '</outline>'
	return result


#
#	Print Module, ModuleClass
#

def printModule(module):
	global hideDetails

	result =  '<outline text="Module [name=&quot;' + module.name + '&quot;">'
	if (hideDetails == False):
		result += printModuleDetails(module)
	result += newLine() + '</outline>'
	return result


def printModuleClass(moduleClass):
	global hideDetails

	result =  '<outline text="ModuleClass [name=&quot;' + moduleClass.name + '&quot;]">'
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

	decTab()
	return result


def printExtends(extends):
	return '<outline text="Extends [domain=&quot;' + extends.domain + '&quot; class=&quot;' + extends.clazz + '&quot;]" />'


#
#	Action, Argument
#

def printAction(action):
	result = '<outline text="Action [name=&quot;' + action.name + '&quot;'
	if (action.type != None):
		result += ' type=&quot;' + action.type + '&quot;'
	result += ']">'

	incTab()
	if (action.doc != None): 
		result += newLine() + printDoc(action.doc)

	if (len(action.arg) > 0):
		result += newLine() + '<outline text="Arg">'
		incTab()
		for argument in action.arg:
			result += newLine() + printArgument(argument)
		decTab()
		result += newLine() + '</outline>'

	decTab()
	result += newLine() + '</outline>'
	return result


def printArgument(action):
	result = '<outline text="Arg ['
	if (action.type != None):
		result += 'type=&quot;' + action.type + '&quot;'
	if (action.name != None):
		result += ' name=&quot;' + action.name + '&quot;'
	result += ']" />'
	return result


#
#             Event
#

def printEvent(event):
	result = '<outline text="Event [name=&quot;' + event.name + '&quot;]">'
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
	if (datapoint.type != None):
		result += ' type=&quot;' + datapoint.type + '&quot;'
	if (datapoint.writable != None):
		result += ' writable=&quot;' + datapoint.writable + '&quot;'
	if (datapoint.readable != None):
		result += ' readable=&quot;' + datapoint.readable + '&quot;'
	if (datapoint.eventable != None):
		result += ' eventable=&quot;' + datapoint.eventable + '&quot;'
	result += ']" />'

	if (datapoint.doc != None):
		incTab()
		result += newLine() + printDoc(datapoint.doc)
		decTab()

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
