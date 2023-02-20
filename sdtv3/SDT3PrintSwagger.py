#	SDT3PrintSwagger.py
#
#	Generate Swagger definitions

# TODO: get/update/post/delete as stubs in paths:
# for all datapoints as pathes
# TODO: read/write attributes?
# TODO: struct types

import re
from sdtv3.SDT3Classes import *
from common.SDTHelper import *

# variable that hold an optional header text
headerText = ''

# variable that holds the version of the data model
modelVersion = ''

# variable that holds the status whether the "paths:" label has been printed
didPaths = False

# constant for file extension
fileExtension = 'yaml'

def print3Swagger(domain, directory, options):
	global headerText, modelVersion, fileExtension, didPaths

	lfile = options['licensefile']
	if lfile != None:
		with open(lfile, 'rt') as f:
			headerText = f.read()

	# set double white space as an indention for yaml files
	setTabChar('  ')

	# get the version of the data model
	modelVersion = options['modelversion']

	# Create package path and make directories
	package, path = getPackage(directory, domain)

	# Export ModuleClasses

	for module in domain.modules:
		didPaths = False
		exportArtifactToFile(module.name, path, fileExtension, getModuleClassSwagger(module))

	# Export Devices

	# TODO DEVICES. 
	for device in domain.devices:
		exportArtifactToFile(device.id, path, fileExtension, getDeviceSwagger(device), outType = OutType.device)

#############################################################################

# Get the ModuleClass resource

def getModuleClassSwagger(module):
	doesExtend = ''

	result = 'definitions:'
	result += newLine() + '# Copy the following object definition to a swagger file'
	result += newLine()
	incTab()
	result += newLine() + module.name + ':'
	incTab()

	if module.doc != None:
		result += newLine() + 'description: ' + printDoc(module.doc)

	# Handle inherited ModuleClasses
	if module.extends != None:
		result += newLine() + "allOf:"
		result += newLine() + '- $ref: \'#/definitions/' + module.extends.clazz + '\''
		doesExtend = '- '

	result += newLine() + doesExtend + 'type: object'
	if doesExtend != '':
		incTab()


	# print data points
	if len(module.data) > 0 or len(module.properties) > 0:
		# First, all the properties
		dpResult = ''
		incTab()
		for prop in module.properties:	# Handle properties like data points
			dpResult += printProperty(prop)
		for data in module.data:
			dpResult += printDataPoint(data)
		decTab()
		if len(dpResult):
			result += newLine() + 'properties: ' + dpResult


		# Then list all the required ones
		reqResult = ''
		incTab()
		for prop in module.properties:
			if prop.optional == 'false':
				reqResult += newLine() + '- ' + prop.name
		for data in module.data:
			if data.optional == 'false':
				reqResult += newLine() + '- ' + data.name
		decTab()
		if len(reqResult) > 0:
			result += newLine() + 'required: ' + reqResult

	if doesExtend != '':
		decTab()
	decTab()
	decTab()

	# print access api for data points
	if len(module.data) > 0:
		result += _printPaths()
		incTab()
		for dataPoint in module.data:
			result += newLine()
			result += newLine() + printDataPointPath(dataPoint, module.name)
		decTab()	

	# print actions
	if len(module.actions) > 0:
		result += _printPaths()
		incTab()

		for action in module.actions:
			result += newLine()
			result += newLine() + printAction(action, module.name)
		decTab()

	return result


def getDeviceSwagger(device):
	doesExtend = '- '
	result = 'definitions:'
	result += newLine() + '# Copy the following object definition to a swagger file'
	result += newLine()
	incTab()
	result += newLine() + device.id + ':'
	incTab()
	if device.doc != None:
		result += newLine() + 'description: ' + printDoc(device.doc)

	# Inherited 
	if device.modules != None:
		result += newLine() + "allOf:"
		for module in device.modules:
			result += newLine() + '- $ref: \'#/definitions/' + module.extends.clazz + '\''
		doesExtend = '- '

	result += newLine() + doesExtend + 'type: object'
	if doesExtend != '':
		incTab()

	# print properties
	if len(device.properties) > 0:
		# First, all the properties
		dpResult = ''
		incTab()
		for prop in device.properties:	# Handle properties like data points
			dpResult += printProperty(prop)
		decTab()
		if len(dpResult):
			result += newLine() + 'properties: ' + dpResult

		# Then list all the required properties
		reqResult = ''
		incTab()
		for prop in device.properties:
			if prop.optional == 'false':
				reqResult += newLine() + '- ' + prop.name
		decTab()
		if len(reqResult) > 0:
			result += newLine() + 'required: ' + reqResult

	if doesExtend != '':
		decTab()
	decTab()
	decTab()
	return result


def printDataPoint(dataPoint):
	result  = newLine() + dataPoint.name + ':'
	incTab()
	result += newLine() + printDataType(dataPoint.type)
	if dataPoint.writable == 'false':
		result += newLine() + 'readOnly: true'
	if dataPoint.doc != None:
		result += newLine() + 'description: ' + printDoc(dataPoint.doc)
	decTab()
	return result


def printProperty(prop):
	result = newLine() + prop.name + ':'
	incTab()
	result += newLine() + printDataType(prop.type)
	result += newLine() + 'readOnly: true'
	if prop.doc != None:
		result += newLine() + 'description: ' + printDoc(prop.doc)
	decTab()
	return result


def printAction(action, moduleName):
	result  = '/pathTo' + moduleName[0].upper() + moduleName[1:] + 'Object/' + action.name + ':'
	incTab()
	result += newLine() + 'post:'
	incTab()
	if action.doc != None:
		result += newLine() + 'description: ' + printDoc(action.doc)
	result += newLine() + 'operationId: ' + moduleName + action.name[0].upper() + action.name[1:]
	result += _printProducesConsumes()

	#TODO parameters 

	result += _printResponse('200')
	decTab()
	decTab()
	result += newLine() + 'jj'


	return result



  # /pathToNumberValueObject/previousNumberValue:
  #   post:
  #     description: Decrement the "numberValue" by the value of "stepValue", down to the value of "minValue".
  #     operationId: numberValuePreviousNumberValue
  #     responses:
  #       default:
  #         description: Bad request
  #       200:
  #         description: Successful response



def printDataPointPath(dataPoint, moduleName):
	result  = '/pathTo' + moduleName[0].upper() + moduleName[1:] + 'Object/datapoint/' + dataPoint.name + ':'


	incTab()
	if dataPoint.readable == 'true':
		result += newLine() + 'get:'
		incTab()
		result += newLine() + 'operationId: ' + moduleName + dataPoint.name[0].upper() + dataPoint.name[1:] + 'Read'
		result += _printProducesConsumes()
		result += _printResponse('200', dataPoint.type)
		decTab()

	if dataPoint.writable == 'true':
		result += newLine() + 'put:'
		incTab()
		result += newLine() + 'operationId: ' + moduleName + dataPoint.name[0].upper() + dataPoint.name[1:] + 'Write'
		result += _printProducesConsumes()

		result += newLine() + 'parameters:'
		incTab()
		result += newLine() + '- in: body'
		incTab()
		result += newLine() + 'name: ' + dataPoint.name
		result += newLine() + 'required: true'
		result += newLine() + 'schema:'
		incTab()
		result += newLine() + printDataType(dataPoint.type)
		decTab()
		decTab()
		decTab()
		result += _printResponse('201')
		decTab()

	decTab()
	return result



# print a data type
def printDataType(dataType):
	result = ''
	if isinstance(dataType.type, SDT3SimpleType):
		result = printSimpleType(dataType.type)
	elif isinstance(dataType.type, SDT3ArrayType):
		result = printArrayType(dataType.type)
	elif isinstance(dataType, SDT3SimpleType):
		result = printSimpleType(dataType)
	# struct not supported yet
	return result


# print a simple data type
def printSimpleType(dataType):
	type = dataType.type
	result = ''
	if type == 'boolean':
		result += 'type: boolean'
	elif type == 'integer':
		result += 'type: number'
		result += newLine() + 'format: int64'
	elif type == 'float':
		result += 'type: number'
		result += newLine() + 'format: float'
	elif type == 'string':
		result += 'type: string'
	elif type == 'datetime':
		result += 'type: string'
		result += newLine() + 'format: date-time'
	elif type == 'date':
		result += 'type: string'
		result += newLine() + 'format: date'
	elif type == 'time':
		result += 'type: string'
		result += newLine() + 'format: date-time'
	elif type =='uri':
		result += 'type: string'
	elif type == 'blob':
		result += 'type: string'
		result += newLine() + 'format: binary'
	elif type == 'enum':
		result += 'type: string'
		result += newLine() + 'enum: [ "TODO value1", "TODO value2" ]'
	elif re.match('.+:.+', type):	# CHECK enum
		result += 'type: string'
		result += newLine() + '# Add values of ' + type
		result += newLine() + 'enum: [ "TODO value1", "TODO value2" ]'
	return result


# print an array and its data type
def printArrayType(dataType):
	result = 'type: array'
	result += newLine() + 'items:'
	incTab()
	result += newLine() + printSimpleType(dataType.arrayType.type)
	decTab()
	return result


# print the documentation. convert at least some of the attributes.
def printDoc(doc):
	incTab()
	result = doc.content.strip()
	result = result.replace('<em>', '*')
	result = result.replace('</em>', '*')
	result = result.replace('<b>', '**')
	result = result.replace('</b>', '**')
	result = result.replace('<p>', '\n' + getTabIndent())
	result = result.replace('</p>', '')
	result = result.replace('<tt>', '')
	result = result.replace('</tt>', '')
	result = result.replace('<img>', '')
	result = result.replace('</img>', '')
	result = '|' + newLine() + result
	decTab()
	return result


# helper: print "paths:" label
def _printPaths():
	global didPaths

	result = ''
	if not didPaths:
		result += newLine() + newLine() + 'paths:'
		result += newLine() + '# Copy and adapt the following path definition(s) to a swagger file'
		didPaths = True
	return result

# helper: print "produces...consumes" for actions
def _printProducesConsumes():
	result = ''
	result += newLine() + 'consumes:'
	incTab()
	result += newLine() + '- text/plain'
	decTab()
	result += newLine() + 'produces:'
	incTab()
	result += newLine() + '- text/plain'
	decTab()
	return result

# helper: print the response part part
def _printResponse(positiveResponeNumber, returnSchemaType = None):
	result = ''
	result += newLine() + 'responses:'
	incTab()
	result += newLine() + 'default:'
	incTab()
	result += newLine() + 'description: Bad request'
	decTab()
	result += newLine() + positiveResponeNumber + ':'
	incTab()
	result += newLine() + 'description: Successful response'
	if returnSchemaType != None:
		result += newLine() + 'schema:'
		incTab()
		result += newLine() + printDataType(returnSchemaType)
		decTab()
	decTab()
	decTab()
	return result
