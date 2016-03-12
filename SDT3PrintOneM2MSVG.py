#	SDT3PrintOneM2MSVG.py
#
#	Generate SVG in oneM2M's Resource format 


import datetime, os, pathlib, string
from SDT3Classes import *
from SDTSVG import *


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
	global structs

	# export the module class itself

	name = sanitizeName(module.name, True)
	fileName = str(path) + os.sep + name + '.svg'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getModuleClassInterface(module, package, name))		
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
		outputFile.write(getDeviceInterface(device, package, name))
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()

	# export module classes of the device

	for module in device.modules:
		exportModuleClass(module, package, path)



# Get the ModuleClass text

def getModuleClassInterface(module, package, name):
	res = Resource(sanitizeName(name, True))

	# TODO: Extends
	# TODO: oneM2M specifics
	# TODO: events?
	# TODO: actions?

	if (module.extends != None):
		pass
		#extendsID = module.extends.domain + '.' + sanitizeName(module.extends.clazz, True)
		#extends = ' extends ' + extendsID

	# DataPoints 
	getDataPoints(res, module.data)


	result  = svgStart(res.width(), res.height())
	result += res.draw()
	result += svgFinish()
	return result


# Get the Device text

def getDeviceInterface(device, package, name):
	res = Resource(sanitizeName(name, True))

	# TODO: oneM2M specifics

	for module in device.modules:
		mod = Resource(sanitizeName(module.name, True))
		mod.cardinality = '1'
		res.add(mod)

	result  = svgStart(res.width(), res.height())
	result += res.draw()
	result += svgFinish()
	return result


########################################################################

# Construct data points export
def getDataPoints(resource, dataPoints):
	if (dataPoints == None or len(dataPoints) == 0):
		return
	getDataPointsDetails(resource, dataPoints)



# Construct data points cores export
def getDataPointsDetails(resource, dataPoints):
	for dataPoint in dataPoints:
		dp = Resource(sanitizeName(dataPoint.name, False))

		if (dataPoint.optional == 'true'):
			dp.cardinality = '0,1'
		else:
			dp.cardinality = '1'
		resource.add(dp)


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

