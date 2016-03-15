#	SDT3PrintOneM2MSVG.py
#
#	Generate SVG in oneM2M's Resource format 


import datetime, os, pathlib, string
from SDT3Classes import *
from SDTSVG import *

cardinality1 = '1'
cardinality01 = '0..1'
cardinality0n = '0..n'



def print3OneM2MSVG(domain, directory, options):

	# Create package path and make directories

	packagePath = directory + os.sep + domain.id.replace('.', os.sep)
	path = pathlib.Path(packagePath)
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


# Export a ModuleClass definition to a file

def exportModuleClass(module, package, path):

	# export the module class itself

	name = sanitizeName(module.name, True)
	fileName = str(path) + os.sep + name + '.svg'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getModuleClassSVG(module, package, name, path))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


# Export a DataPoint definiton to a file

def exportDataPoint(dataPoint, moduleName, path):
	name = sanitizeName(dataPoint.name, True)
	mName = sanitizeName(moduleName, True)
	fileName = str(path) + os.sep + mName + '_' + name + '.svg'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getDataPointSVG(dataPoint))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


# Export a Device definition to a file

def exportDevice(device, package, path):
	name = sanitizeName(device.id, True)
	packagePath = str(path) + os.sep + name.lower()
	path = pathlib.Path(packagePath)

	# TODO: SubDevices

	try:
		path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now

	fileName = str(path) + os.sep + name + '.svg'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getDeviceSVG(device, package, name, path))
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()

	# export module classes of the device

	for module in device.modules:
		exportModuleClass(module, package, path)



# Get the ModuleClass resource

def getModuleClassSVG(module, package, name, path):
	res = Resource(sanitizeName(name, True))

	# TODO: Extends?
	# TODO: events?
	# TODO: actions?

	addHeaderToResource(res)

	# DataPoints 
	getDataPoints(res, module.data, name, path)

	addFooterToResource(res)

	result  = svgStart(res.width(), res.height())
	result += res.draw()
	result += svgFinish()
	return result


# Get the Device resource

def getDeviceSVG(device, package, name):
	res = Resource(sanitizeName(name, True))

	# TODO: oneM2M specifics

	for module in device.modules:
		mod = Resource(sanitizeName(module.name, True))
		mod.cardinality = cardinality1
		res.add(mod)

	result  = svgStart(res.width(), res.height())
	result += res.draw()
	result += svgFinish()
	return result


# Get the DataPoint resource

def getDataPointSVG(dataPoint):
	res = Resource(sanitizeName(dataPoint.name, False))

	addHeaderToResource(res)
	# Nothing in between
	addFooterToResource(res)

	result  = svgStart(res.width(), res.height())
	result += res.draw()
	result += svgFinish()
	return result


########################################################################

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


########################################################################


#
#	Helpers
#

# Sanitize the name for Vorto

def sanitizeName(name, isClass):
	if (name == None or len(name) == 0):
		return ''
	result = name
	if (isClass):
		result = result[0].upper() + name[1:]
	else:
		result = result[0].lower() + name[1:]
	result = result.replace(' ', '')
	result = result.replace('/', '')
	result = result.replace('.', '')
	result = result.replace(' ', '')
	result = result.replace("'", '')
	result = result.replace('´', '')
	result = result.replace('`', '')
	result = result.replace('(', '_')
	result = result.replace(')', '_')
	result = result.replace('-', '_')

	return result

# Sanitize the package name for Java

def sanitizePackage(package):
	result = package.replace('/', '.')
	return result



# Add standard header attributes to a resource

def addHeaderToResource(resource):

	contDefinition = Attribute('contDefinition')
	contDefinition.cardinality = cardinality1
	resource.add(contDefinition)

	creator = Attribute('creator')
	creator.cardinality = cardinality01
	resource.add(creator)

	ontologyRef = Attribute('ontologyRef')
	ontologyRef.cardinality = cardinality01
	resource.add(ontologyRef)



# Add standard footer to a resource

def addFooterToResource(resource):

	subscription = Resource('subscription')
	subscription.cardinality = cardinality0n
	resource.add(subscription)
