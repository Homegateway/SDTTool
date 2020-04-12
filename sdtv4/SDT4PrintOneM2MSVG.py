#	SDT4PrintOneM2MSVG.py
#
#	Generate SVG in oneM2M's Resource format 

import datetime, os, pathlib, string
from .SDT4Classes import *
from common.SDTSVG import *
from common.SDTHelper import *

# definition of cardinality constants
cardinality1 = '1'
cardinality01 = '0..1'
cardinality0n = '0..n'

# variable that hold an optional header text
headerText = ''

# variable that holds the domain prefix for the oneM2M XSD
namespacePrefix = ''

# variable that holds the version of the data model
modelVersion = ''

# variable that holds whether datapoints should be exported as well
exportDataPoints = False

def print4OneM2MSVG(domain, options, directory):
	global headerText, modelVersion, namespacePrefix, exportDataPoints

	lfile = options['licensefile']
	if lfile != None:
		with open(lfile, 'rt') as f:
			headerText = f.read()

	# get the version of the data model
	modelVersion = options['modelversion']
	namespacePrefix = options['namespaceprefix']
	if namespacePrefix == None:			# ERROR
		print('Error: name space prefix not set')
		return

	# Generate SVG's for ModuleClass attributes as well?
	exportDataPoints = options['svgwithattributes']

	# Create package path and make directories
	path = pathlib.Path(directory)
	try:
		path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now
	package = sanitizePackage(domain.id)

	# Export ModuleClasses
	for moduleClass in domain.moduleClasses:
		exportModuleClass(moduleClass, package, path)

	# Export Devices
	for deviceClass in domain.deviceClasses:
		exportDevice(deviceClass, package, path)
		for subDevice in deviceClass.subDevices:
			exportDevice(subDevice, package, path, parent=deviceClass)

	# Export possible SubDevices
	for subDevice in domain.subDevices:
		exportDevice(subDevice, package, path)

def cardinality(obj):
	if obj.minOccurs == '0' and obj.maxOccurs == '1':
		return cardinality01
	if obj.minOccurs == '0' and obj.maxOccurs == 'n':
		return cardinality0n
	return cardinality1


#############################################################################

# Export a ModuleClass definition to a file
def exportModuleClass(module, package, path, name=None):
	# export the module class itself

	name = sanitizeName(module.name, False)
	fileName = getVersionedFilename(name, 'svg', path=str(path), isModule=True, modelVersion=modelVersion, namespacePrefix=namespacePrefix)
	try:
		with open(fileName, 'w') as outputFile:
			outputFile.write(getModuleClassSVG(module, package, name, path))		
	except IOError as err:
		print(err)


# Get the ModuleClass resource
def getModuleClassSVG(module, package, name, path):
	res = Resource(sanitizeName(name, False), specialization=True)

	# TODO: Extends?
	# TODO: events?
	addModuleClassHeaderToResource(res)

	# Add properties
	for prop in module.properties:
		res.add(Attribute(sanitizeName(prop.name, False), cardinality=cardinality01 if prop.optional == "true" else cardinality1))

	# DataPoints 
	getDataPoints(res, module.data, name, path)
	# Actions
	getActions(res, module.actions, name, path)
	addModuleClassFooterToResource(res)
	return svgStart(res.width(), res.height(), headerText) + res.draw() + svgFinish()


# Add standard header attributes to a module class resource
def addModuleClassHeaderToResource(resource):
	resource.add(Attribute('containerDefinition', cardinality=cardinality1))
	resource.add(Attribute('ontologyRef', cardinality=cardinality01))
	resource.add(Attribute('contentSize', cardinality=cardinality1))


# Add standard footer to a module class resource
def addModuleClassFooterToResource(resource):
	resource.add(Resource('subscription', cardinality=cardinality0n))

#############################################################################

# Export a Device definition to a file
def exportDevice(device, package, path, parent=None):
	name = sanitizeName(device.id, False)
	pth = None
	if isinstance(device, SDT4DeviceClass):
		pth = pathlib.Path(str(path) + os.sep + name)
	elif isinstance(device, SDT4SubDevice) and parent is not None and isinstance(parent, SDT4DeviceClass):
		pth = pathlib.Path(str(path) + os.sep + sanitizeName(parent.id, False) + os.sep + name)
	elif isinstance(device, SDT4SubDevice) and parent is None:
		pth = pathlib.Path(str(path) + os.sep + name)
	else:
		return
	
	try:
		pth.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now

	fileName = getVersionedFilename(name, 'svg', path=str(pth), modelVersion=modelVersion, namespacePrefix=namespacePrefix)
	try:
		with open(fileName, 'w') as outputFile:
			outputFile.write(getDeviceSVG(device, package, name))
	except IOError as err:
		print(err)

	# export module classes of the device
	if exportDataPoints:
		for moduleClass in device.moduleClasses:
			exportModuleClass(moduleClass, package, pth, name)


# Get the Device resource

def getDeviceSVG(device, package, name):
	res = Resource(sanitizeName(name, False), specialization=True)
	addDeviceHeaderToResource(res)

	# Add properties
	for prop in device.properties:
		res.add( Attribute(sanitizeName(prop.name, False), cardinality=cardinality01 if prop.optional == "true" else cardinality1))

	# Add modules
	for module in device.moduleClasses:
		res.add(Resource(sanitizeName(module.name, False), cardinality=cardinality(module), specialization=True))

	# Add sub-devices
	if isinstance(device, SDT4DeviceClass):
		for subDevice in device.subDevices:
			res.add(Resource(sanitizeName(subDevice.id, False), cardinality=cardinality(subDevice), specialization=True))

	addDeviceFooterToResource(res)
	return svgStart(res.width(), res.height(), headerText) + res.draw() + svgFinish()



# Add standard header attributes to a device resource
def addDeviceHeaderToResource(resource):
	resource.add(Attribute('containerDefinition', cardinality=cardinality1))
	resource.add(Attribute('ontologyRef', cardinality=cardinality01))
	resource.add(Attribute('contentSize', cardinality=cardinality1))
	resource.add(Attribute('nodeLink', cardinality=cardinality01))


# Add standard footer to a device resource
def addDeviceFooterToResource(resource):
	resource.add(Resource('subscription', cardinality=cardinality0n))


#############################################################################

# Export a DataPoint definiton to a file
def exportDataPoint(dataPoint, moduleName, path):
	name = sanitizeName(dataPoint.name, False)
	mName = sanitizeName(moduleName, False)
	fileName = getVersionedFilename(mName + '_' + name, 'svg', path=str(path), modelVersion=modelVersion, namespacePrefix=namespacePrefix)
	try:
		with open(fileName, 'w') as outputFile:
			outputFile.write(getDataPointSVG(dataPoint))		
	except IOError as err:
		print(err)


# Get the DataPoint resource
def getDataPointSVG(dataPoint):
	res = Resource(sanitizeName(dataPoint.name, False), specialization=True)
	addDataPointHeaderToResource(res)
	# Nothing in between
	addDataPointFooterToResource(res)
	return svgStart(res.width(), res.height(), headerText) + res.draw() + svgFinish()


# Construct data points export
def getDataPoints(resource, dataPoints, moduleName, path):
	if dataPoints == None or len(dataPoints) == 0:
		return
	for dataPoint in dataPoints:
		# First add it to the resource
		resource.add(Attribute(sanitizeName(dataPoint.name, False), \
			cardinality=cardinality01 if dataPoint.optional == 'true' else cardinality1))
		# write out to a file
		if exportDataPoints:
			exportDataPoint(dataPoint, moduleName, path)


# Add standard header attributes to a data point resource
def addDataPointHeaderToResource(resource):
	resource.add(Attribute('containerDefinition', cardinality=cardinality1))
	resource.add(Attribute('ontologyRef', cardinality=cardinality01))
	resource.add(Attribute('contentSize', cardinality=cardinality1))


# Add standard footer to a data point resource
def addDataPointFooterToResource(resource):
	resource.add(Resource('subscription', cardinality=cardinality0n, specialization=False))


########################################################################

# Export an action definiton to a file
def exportAction(action, moduleName, path):
	fileName = getVersionedFilename(sanitizeName(action.name, False), \
		'svg', path=str(path), isAction=True, modelVersion=modelVersion, \
		namespacePrefix=namespacePrefix)
	try:
		with open(fileName, 'w') as outputFile:
			outputFile.write(getActionSVG(action))
	except IOError as err:
	 	print(err)


# Get the Action resource
def getActionSVG(action):
	res = Resource(sanitizeName(action.name, False), specialization=True)
	addActionHeaderToResource(res)
	# Nothing in between
	addActionFooterToResource(res)
	return svgStart(res.width(), res.height(), headerText) + res.draw() + svgFinish()


# Construct actions export
def getActions(resource, actions, moduleName, path):
	if actions == None or len(actions) == 0:
		return
	for action in actions:
		# First add it to the resource
		resource.add(Attribute(sanitizeName(action.name, False), \
				cardinality=cardinality01 if action.optional == 'true' else cardinality1))
		# write out to a file
		exportAction(action, moduleName, path)


# Add standard header attributes to a device resource
def addActionHeaderToResource(resource):
	resource.add(Attribute('containerDefinition', cardinality=cardinality1))
	resource.add(Attribute('ontologyRef', cardinality=cardinality01))
	resource.add(Attribute('contentSize', cardinality=cardinality1))


# Add standard footer to an  resource
def addActionFooterToResource(resource):
	resource.add(Resource('subscription', cardinality=cardinality0n))

