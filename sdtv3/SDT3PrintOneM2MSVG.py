#	SDT3PrintOneM2MSVG.py
#
#	Generate SVG in oneM2M's Resource format 


import datetime, os, pathlib, string
from .SDT3Classes import *
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

def print3OneM2MSVG(domain, directory, options):
	global headerText, modelVersion, namespacePrefix

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

	# Create package path and make directories

	#packagePath = directory + os.sep + domain.id.replace('.', os.sep)
	path = pathlib.Path(directory)
	try:
		path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now
	package = sanitizePackage(domain.id)

	# Export ModuleClasses

	for module in domain.modules:
		exportModuleClass(module, package, path)

	# Export Devices

	for device in domain.devices:
		exportDevice(device, package, path)


#############################################################################


# Export a ModuleClass definition to a file

def exportModuleClass(module, package, path, name=None):
	global modelVersion, namespacePrefix

	# export the module class itself

	name = sanitizeName(module.name, False)
	fileName = getVersionedFilename(name, 'svg', path=str(path), isModule=True, modelVersion=modelVersion, namespacePrefix=namespacePrefix)
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getModuleClassSVG(module, package, name, path))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


# Get the ModuleClass resource

def getModuleClassSVG(module, package, name, path):
	res = Resource(sanitizeName(name, False))
	res.specialization = True

	# TODO: Extends?
	# TODO: events?

	addModuleClassHeaderToResource(res)

	# Add properties
	for prop in module.properties:
		pr = Attribute(sanitizeName(prop.name, False))
		pr.cardinality = cardinality01 if prop.optional == "true" else cardinality1
		res.add(pr)


	# DataPoints 
	getDataPoints(res, module.data, name, path)

	# Actions
	getActions(res, module.actions, name, path)

	addModuleClassFooterToResource(res)

	result  = svgStart(res.width(), res.height(), headerText)
	result += res.draw()
	result += svgFinish()
	return result


# Add standard header attributes to a module class resource

def addModuleClassHeaderToResource(resource):

	contDefinition = Attribute('containerDefinition')
	contDefinition.cardinality = cardinality1
	resource.add(contDefinition)

	creator = Attribute('creator')
	creator.cardinality = cardinality01
	resource.add(creator)

	ontologyRef = Attribute('ontologyRef')
	ontologyRef.cardinality = cardinality01
	resource.add(ontologyRef)


# Add standard footer to a module class resource

def addModuleClassFooterToResource(resource):

	subscription = Resource('subscription')
	subscription.cardinality = cardinality0n
	resource.add(subscription)

#############################################################################


# Export a Device definition to a file

def exportDevice(device, package, path):
	global modelVersion, namespacePrefix

	name = sanitizeName(device.id, False)
	packagePath = str(path) + os.sep + name
	path = pathlib.Path(packagePath)

	try:
		path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now

	fileName = getVersionedFilename(name, 'svg', path=str(path), modelVersion=modelVersion, namespacePrefix=namespacePrefix)
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getDeviceSVG(device, package, name))
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()

	# export module classes of the device

	for module in device.modules:
		exportModuleClass(module, package, path, name)


# Get the Device resource

def getDeviceSVG(device, package, name):
	res = Resource(sanitizeName(name, False))
	res.specialization = True

	addDeviceHeaderToResource(res)

	# Add properties
	for prop in device.properties:
		pr = Attribute(sanitizeName(prop.name, False))
		pr.cardinality = cardinality01 if prop.optional == "true" else cardinality1
		res.add(pr)

	# Add modules
	for module in device.modules:
		mod = Resource(sanitizeName(module.name, False))
		mod.cardinality = cardinality01 if module.optional == 'true' else cardinality1
		mod.specialization = True
		res.add(mod)

	addDeviceFooterToResource(res)

	result  = svgStart(res.width(), res.height(), headerText)
	result += res.draw()
	result += svgFinish()
	return result


# Add standard header attributes to a device resource

def addDeviceHeaderToResource(resource):

	contDefinition = Attribute('contDefinition')
	contDefinition.cardinality = cardinality1
	resource.add(contDefinition)

	creator = Attribute('creator')
	creator.cardinality = cardinality01
	resource.add(creator)

	ontologyRef = Attribute('ontologyRef')
	ontologyRef.cardinality = cardinality01
	resource.add(ontologyRef)




# Add standard footer to a device resource

def addDeviceFooterToResource(resource):

	subscription = Resource('subscription')
	subscription.cardinality = cardinality0n
	subscription.specialization = False
	resource.add(subscription)


#############################################################################

# Export a DataPoint definiton to a file

def exportDataPoint(dataPoint, moduleName, path):
	global modelVersion, namespacePrefix

	name = sanitizeName(dataPoint.name, False)
	mName = sanitizeName(moduleName, False)
	fileName = getVersionedFilename(mName + '_' + name, 'svg', path=str(path), modelVersion=modelVersion, namespacePrefix=namespacePrefix)
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getDataPointSVG(dataPoint))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


# Get the DataPoint resource

def getDataPointSVG(dataPoint):
	res = Resource(sanitizeName(dataPoint.name, False))
	res.specialization = True

	addDataPointHeaderToResource(res)
	# Nothing in between
	addDataPointFooterToResource(res)

	result  = svgStart(res.width(), res.height(), headerText)
	result += res.draw()
	result += svgFinish()
	return result


# Construct data points export
def getDataPoints(resource, dataPoints, moduleName, path):
	if (dataPoints == None or len(dataPoints) == 0):
		return
	for dataPoint in dataPoints:

		# First add it to the resource

		dp = Attribute(sanitizeName(dataPoint.name, False))

		if (dataPoint.optional == 'true'):
			dp.cardinality = cardinality01
		else:
			dp.cardinality = cardinality1
		resource.add(dp)

		# write out to a file
		exportDataPoint(dataPoint, moduleName, path)



# Add standard header attributes to a data point resource

def addDataPointHeaderToResource(resource):

	contDefinition = Attribute('contDefinition')
	contDefinition.cardinality = cardinality1
	resource.add(contDefinition)

	creator = Attribute('creator')
	creator.cardinality = cardinality01
	resource.add(creator)

	ontologyRef = Attribute('ontologyRef')
	ontologyRef.cardinality = cardinality01
	resource.add(ontologyRef)


# Add standard footer to a data point resource

def addDataPointFooterToResource(resource):

	subscription = Resource('subscription')
	subscription.cardinality    = cardinality0n
	subscription.specialization = False
	resource.add(subscription)


########################################################################

# Export an action definiton to a file

def exportAction(action, moduleName, path):
	global modelVersion, namespacePrefix

	name = sanitizeName(action.name, False)
	mName = sanitizeName(moduleName, False)
	fileName = getVersionedFilename(name, 'svg', path=str(path), isAction=True, modelVersion=modelVersion, namespacePrefix=namespacePrefix)
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getActionSVG(action))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


# Get the Action resource

def getActionSVG(action):
	res = Resource(sanitizeName(action.name, False))
	res.specialization = True

	addActionHeaderToResource(res)
	# Nothing in between
	addActionFooterToResource(res)

	result  = svgStart(res.width(), res.height(), headerText)
	result += res.draw()
	result += svgFinish()
	return result


# Construct actions export
def getActions(resource, actions, moduleName, path):
	if (actions == None or len(actions) == 0):
		return
	for action in actions:

		# First add it to the resource

		dp = Attribute(sanitizeName(action.name, False))

		if (action.optional == 'true'):
			dp.cardinality = cardinality01
		else:
			dp.cardinality = cardinality1
		resource.add(dp)

		# write out to a file
		exportAction(action, moduleName, path)


# Add standard header attributes to a device resource

def addActionHeaderToResource(resource):

	contDefinition = Attribute('contDefinition')
	contDefinition.cardinality = cardinality1
	resource.add(contDefinition)

	creator = Attribute('creator')
	creator.cardinality = cardinality01
	resource.add(creator)

	ontologyRef = Attribute('ontologyRef')
	ontologyRef.cardinality = cardinality01
	resource.add(ontologyRef)


# Add standard footer to an  resource

def addActionFooterToResource(resource):

	subscription = Resource('subscription')
	subscription.cardinality    = cardinality0n
	subscription.specialization = False
	resource.add(subscription)

