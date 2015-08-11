#	SDT2PrintMarkdown.py
#
#	Print SDT2 to markdown



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

def print2DomainMarkdown(domain):
	result = ''
	result += markdownHeader('Domain "' + domain.id + '"')
	
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

	if (len(domain.rootDevices) > 0):
		incHeaderLevel()
		result += markdownHeader('RootDevices')
		for rootDevice in domain.rootDevices:
			result += newLine() + printRootDevice(rootDevice)
		decHeaderLevel()

	return result

def printInclude(include):
	incTab()
	result = newLine() + '- Parse: ' + include.parse 
	result += ', Href: ' + include.href
	decTab()
	return result



#
#	RootDevice, Device
#

def printRootDevice(rootDevice):
	incHeaderLevel()
	result = markdownHeader('RootDevice "' + rootDevice.id + '"')
	if (rootDevice.doc):
		result += newLine() + printDoc(rootDevice.doc)
	if (rootDevice.deviceInfo != None):
		result += newLine() + printDeviceInfo(rootDevice.deviceInfo)

	if (len(rootDevice.modules) > 0):
		incHeaderLevel()
		result += markdownHeader('Modules')
		for module in rootDevice.modules:
			result += newLine() + printModule(module)
		decHeaderLevel()

	if (len(rootDevice.devices) > 0):
		incHeaderLevel()
		result += markdownHeader('Devices')
		for device in rootDevice.devices:
			result += printDevice(device)
		decHeaderLevel()

	decTab()
	decHeaderLevel()
	return result



def printDevice(device):
	incHeaderLevel()
	result = markdownHeader('Device "' + device.id + '"')

	if (device.doc):
		result += newLine() + printDoc(device.doc)
	if (device.deviceInfo != None):
		result += newLine() + printDeviceInfo(device.deviceInfo)

	if (len(device.modules) > 0):
		incHeaderLevel()
		result += newLine() + markdownHeader('Modules')
		for module in device.modules:
			result += newLine() + printModule(module)
		decHeaderLevel()

	decHeaderLevel()
	return result



#
#	DeviceInfo
#

def printDeviceInfo(deviceInfo):
	result = '- DeviceInfo'
	incTab()
	if (deviceInfo.name != None):
		result += newLine() + '- Name: ' + deviceInfo.name
	if (deviceInfo.vendor != None):
		result += newLine() + '- Vendor: ' + deviceInfo.vendor
	if (deviceInfo.serialNumber != None):
		result += newLine() + '- SerialNumber: ' + deviceInfo.serialNumber
	if (deviceInfo.vendorURL != None):
		result += newLine() + '- VendorURL: ' + deviceInfo.vendorURL
	if (deviceInfo.firmwareVersion != None):
		result += newLine() + '- FirmwareVersion: ' + deviceInfo.firmwareVersion

	decTab()
	return result


#
#	Print Module, ModuleClass
#

def printModule(module):
	result = '- **' + module.name + '**'
	result += printModuleDetails(module)
	return result

def printModuleClass(moduleClass):
	result = '- **' + moduleClass.name + '**'
	result += printModuleDetails(moduleClass)
	return result

def printModuleDetails(module):
	incTab()
	result = ''
	if (module.doc != None):
		result += '  ' + newLine() + printDoc(module.doc)
	if (module.extends != None):
		result += printExtends(module.extends)
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
		result += newLine() + '- Return Type: ' + action.type
	if (len(action.arg) > 0):
		result += newLine() + '- Arguments'
		for argument in action.arg:
			result += printArgument(argument)
	decTab()
	decTab()
	return result

def printArgument(action):
	incTab()
	result = newLine() + '- '
	if (action.name != None):
		result +=  '**' + action.name + '**'
	if (action.type != None):
		result += ' (' + action.type + ')'
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
	if (len(event.data) > 0):
		result += newLine() + '- **Data**'
		for dataPoint in event.data:
			result += printDataPoint(dataPoint)
	decTab()
	decTab()
	return result


#
#	DataPoint
#

def printDataPoint(datapoint):
	incTab()
	result = newLine() + '- **' + datapoint.name + '**'
	if (datapoint.type != None):
		result += ' (' + datapoint.type + ')'
	incTab()
	if (datapoint.doc != None):
		result +=  '  ' + newLine() + printDoc(datapoint.doc)
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
#	Doc
#

def printDoc(doc):
	result = doc.content.strip()
	return result

