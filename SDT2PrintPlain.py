#	SDT2PrintPlain.py
#
#	Print SDT2 to Plain text

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

def print2DomainPlain(domain):
	result = 'Domain [id="' + domain.id + '"]'
	incTab()
	for include in domain.includes:
		result += newLine() + printInclude(include)	
	for module in domain.modules:
		result += newLine() + printModuleClass(module)
	for rootDevice in domain.rootDevices:
		result += newLine() + printRootDevice(rootDevice)
	decTab()
	return result

def printInclude(include):
	return 'Include [parse="' + include.parse + '" href="' + include.href + '"]'


#
#	RootDevice, Device
#

def printRootDevice(rootDevice):
	result = 'RootDevice [id="' + rootDevice.id + '"]'
	incTab()
	if (rootDevice.deviceInfo != None):
		result += newLine() + printDeviceInfo(rootDevice.deviceInfo)
	if (rootDevice.doc):
		result += newLine() + printDoc(rootDevice.doc)
	for module in rootDevice.modules:
		result += newLine() + printModule(module)
	for device in rootDevice.devices:
		result += newLine() + printDevice(device)
	decTab()
	return result

def printDevice(device):
	result = 'Device [id="' + device.id + '"]'
	incTab()
	if (device.deviceInfo != None):
		result += newLine() + printDeviceInfo(device.deviceInfo)
	if (device.doc):
		result += newLine() + printDoc(device.doc)
	for module in device.modules:
		result += newLine() + printModule(module)
	decTab()
	return result


#
#	DeviceInfo
#

def printDeviceInfo(deviceInfo):
	result = 'DeviceInfo'
	incTab()
	if (deviceInfo.name != None):
		result += newLine() + 'name="' + deviceInfo.name + '"'
	if (deviceInfo.vendor != None):
		result += newLine() + 'vendor="' + deviceInfo.vendor + '"'
	if (deviceInfo.serialNumber != None):
		result += newLine() + 'serialNumber="' + deviceInfo.serialNumber + '"'
	if (deviceInfo.vendorURL != None):
		result += newLine() + 'vendorURL="' + deviceInfo.vendorURL + '"'
	if (deviceInfo.firmwareVersion != None):
		result += newLine() + 'firmwareVersion="' + deviceInfo.firmwareVersion + '"'
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
	if (action.type != None):
		result += ' type="' + action.type + '"'
	result += ']'
	incTab()
	if (action.doc != None): 
		result += newLine() + printDoc(action.doc)
	for argument in action.arg:
		result += newLine() + printArgument(argument)
	decTab()
	return result

def printArgument(action):
	result = 'Arg ['
	if (action.type != None):
		result += 'type="' + action.type + '"'
	if (action.name != None):
		result += ' name="' + action.name + '"'
	result += ']'
	return result


#
#	Event
#

def printEvent(event):
	result = 'Event [name="' + event.name + '"]'
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
	result = ''
	result = 'DataPoint [name="' + datapoint.name + '"'
	if (datapoint.type != None):
		result += ' type="' + datapoint.type + '"'
	if (datapoint.writable != None):
		result += ' writable="' + datapoint.writable + '"'
	if (datapoint.readable != None):
		result += ' readable="' + datapoint.readable + '"'
	if (datapoint.eventable != None):
		result += ' eventable="' + datapoint.eventable + '"'
	result += ']'
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
	result = 'Doc' + newLine() + doc.content.strip()
	decTab()
	return result
