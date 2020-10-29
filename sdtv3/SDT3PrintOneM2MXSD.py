#	SDT3PrintOneM2MXSD.py
#
#	Generate XSD for oneM2M

import csv, datetime, os, pathlib, re, string
from .SDT3Classes import *
from common.SDTAbbreviate import *


# variable that holds an optional header text
headerText = ''

# variable that holds the domain for the oneM2M XSD definition
domainDefinition = ''

# variable that holds the domain prefix for the oneM2M XSD
namespacePrefix = ''

# variable that holds the file name for predefined abbreviations
abbreviationsInFile = ''

# the target name space for the XSD
targetNamespace = ''

# variable that holds the version of the data model
modelVersion = ''

# variable for found enum types
enumTypes = set()

# variable for found actions
actions = {}

# constants for abbreviation file
constAbbreviationCSVFile = '_Abbreviations.csv'
constAbbreviationMAPFile = '_Abbreviations.py'

def print3OneM2MXSD(domain, directory, options):
	global headerText, domainDefinition, namespacePrefix, enumTypes, doAbbreviations, targetNamespace
	global abbreviationsInFile, modelVersion, constAbbreviationCSVFile

	#
	#	Get various parameters
	#

	# read license text
	lfile = options['licensefile']
	if lfile != None:
		with open(lfile, 'rt') as f:
			headerText = f.read()

	# get the domain and domain prefix
	domainDefinition = options['domain']
	if domainDefinition == None:
		domainDefinition = ''

	namespacePrefix = options['namespaceprefix']
	if namespacePrefix == None:			# ERROR
		print('Error: name space prefix not set')
		return

	# get target name space 
	targetNamespace = options['xsdtargetnamespace']
	if targetNamespace == None:
		targetNamespace = 'undefined'

	# get in and out file names for abbreviations
	abbreviationsInFile = options['abbreviationsinfile']

	# get the version of the data model
	modelVersion = options['modelversion']


	# Create package path and make directories
	path = pathlib.Path(directory)
	try:
		path.mkdir(parents=True)
	except FileExistsError as e:
		pass # on purpose. We override files for now
	package = sanitizePackage(domain.id)


	# Read abbreviations
	SDTAbbreviate.readAbbreviations(abbreviationsInFile)
	# Add already existing abbreviations
	localAbbreviationsfile = str(path) + os.sep + constAbbreviationCSVFile
	SDTAbbreviate.readAbbreviations(localAbbreviationsfile, predefined=False)


	# Export ModuleClasses
	for module in domain.modules:
		exportModuleClass(module, package, path)

	# Export Devices
	for device in domain.devices:
		exportDevice(device, package, path)

	# Export enum types
	exportEnumTypes(path)	

	# Export found Actions
	exportActions(path)


	# Export abbreviations
	exportAbbreviations(str(context['path']) + os.sep + constAbbreviationCSVFile, 
	 					str(context['path']) + os.sep + constAbbreviationMAPFile,
						getAbbreviations())

#############################################################################


# Export a ModuleClass definition to a file

def exportModuleClass(module, package, path, name=None):
	global namespacePrefix, modelVersion

	# export the module class itself

	moduleName   = sanitizeName(module.name, False)
	fileName     = sanitizeName(module.name, False)
	fullFilename = getVersionedFilename(fileName, name=name, path=str(path), isModule=True)
	outputFile   = None
	try:
		outputFile = open(fullFilename, 'w')
		outputFile.write(getModuleClassXSD(module, package, moduleName, path))		
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()


# Get the ModuleClass resource

def getModuleClassXSD(module, package, name, path):

	result  = ''
	result += addModuleClassHeader(module)
	result += addModuleClass(module, name)
	result += addModuleClassFooter(module)
	return result


# Add standard header attributes to a module class resource

xsdSchemaTemplateHeader = '''<?xml version="1.0" encoding="UTF-8"?>
<!--
{headerText}
-->

<xs:schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="{targetnamespace}"
	xmlns:m2m="http://www.onem2m.org/xml/protocols" xmlns:{namespace}="http://www.onem2m.org/xml/protocols/{domain}" elementFormDefault="unqualified" attributeFormDefault="unqualified"
	xmlns:xs="http://www.w3.org/2001/XMLSchema">

	<xs:import namespace="http://www.onem2m.org/xml/protocols" schemaLocation="CDT-subscription-v2_7_0.xsd" />
	<xs:import namespace="http://www.onem2m.org/xml/protocols" schemaLocation="CDT-commonTypes-v2_7_0.xsd" />

	<xs:include schemaLocation="HD-enumerationTypes-v1_0_0.xsd" />{schemas}
'''

xsdSchemaTemplateFooter = '''
</xs:schema>
'''

def addModuleClassHeader(module=None):
	global xsdSchemaTemplateHeader, namespacePrefix
	global headerText, domainDefinition, targetNamespace

	# XML header + license text
	incTab()
	return xsdSchemaTemplateHeader.format(headerText=headerText,
										  namespace=namespacePrefix,
										  domain=domainDefinition,
										  targetnamespace=targetNamespace,
										  schemas=getModuleClassSchemas(module))


def addModuleClassFooter(module=None):
	global xsdSchemaTemplateFooter
	decTab()
	return xsdSchemaTemplateFooter.format()


# The main resource definition

flexContainerResourceTemplate = '''
	<xs:element name="{name}" type="{namespacePrefix}:{name}" substitutionGroup="m2m:sg_flexContainerResource"/>
	<xs:complexType name="{name}">
		<xs:complexContent>
			<!-- Inherit Common Attributes from data type "flexContainerResource" -->
			<xs:extension base="m2m:flexContainerResource">
				<xs:sequence>
				
					<!-- Resource Specific Attributes -->
{specificAttributes}

					<!-- Child Resources -->

					<xs:choice minOccurs="0" maxOccurs="1">
						<xs:element name="childResource" type="m2m:childResourceRef" minOccurs="1" maxOccurs="unbounded" />
						<xs:choice minOccurs="1" maxOccurs="unbounded">
{actionElements}

							<xs:element ref="m2m:subscription"  />
						</xs:choice>
					</xs:choice>

				</xs:sequence>
			</xs:extension>
		</xs:complexContent>
	</xs:complexType>

	<xs:element name="{name}Annc" type="{namespacePrefix}:{name}Annc" substitutionGroup="m2m:sg_announcedFlexContainerResource"/>
	<xs:complexType name="{name}Annc">
		<xs:complexContent>
			<!-- Inherit Common Attributes from data type "announcedFlexContainerResource" -->
			<xs:extension base="m2m:announcedFlexContainerResource">
				<xs:sequence>

					<!-- Resource Specific Attributes -->		
{specificAttributesAnnc}

					<!-- Child Resources -->

					<xs:choice minOccurs="0" maxOccurs="1">
						<xs:element name="childResource" type="m2m:childResourceRef" minOccurs="1" maxOccurs="unbounded" />
						<xs:choice minOccurs="1" maxOccurs="unbounded">
{actionElements}

							<xs:element ref="m2m:subscription"  />
						</xs:choice>
					</xs:choice>

				</xs:sequence>
			</xs:extension>
		</xs:complexContent>
	</xs:complexType>
'''

def addModuleClass(module, name):
	global flexContainerResourceTemplate, namespacePrefix
	name = sanitizeName(name, False)
	result = flexContainerResourceTemplate.format(name=name,
												  namespacePrefix=namespacePrefix,
												  specificAttributes=getSpecificAttributes(module, annc=False),
						 						  specificAttributesAnnc=getSpecificAttributes(module, annc=True),
												  actionElements=getSpecificActions(module))

	# small hack: add the announced device name to the abbreviated list
	sanitizeName(name, False, annc=True)

	return result



def getSpecificAttributes(module, annc=False):
	result = ''
	incTab(5)

	# Properties
	if len(module.properties) > 0:
		for prop in module.properties:
			result += getSpecificPropertyXSD(prop, annc)
		result += newLine()

	# DataPoints
	for data in module.data:
		result += getDataPointXSD(data, annc)

	decTab(5)
	return result


def getSpecificActions(module):
	global namespacePrefix, actions
	if len(module.actions) == 0:
		return ''
	result = ''
	incTab(7)
	for action in module.actions:
		result += newLine() + '<xs:element ref="' + namespacePrefix + ':' + action.name + '" />'
		actions[action.name] = action
	decTab(7)
	return result


def getDataPointXSD(data, annc):
	result = ''
	result += newLine() + '<xs:element name="' + sanitizeName(data.name, False) + '"'
	if annc:
		result += ' minOccurs="0"'
	else:
		if data.optional == 'true':	# indicate an optional data point
			result += ' minOccurs="0"'
	result += getDataPointType(data)
	return result;



def getDataPointType(dataPoint):
	name = sanitizeName(dataPoint.name, False)
	return getDataType(name, dataPoint.type)


def getDataType(name, typ):
	global enumTypes, namespacePrefix
	result = ''

	# Array
	if (isinstance(typ.type, SDT3ArrayType)):
		result += '>'
		incTab()
		result += newLine() + '<xs:simpleType>'
		incTab()
		result += newLine() + '<xs:list itemType="' + getSimpleDataType(typ.type.arrayType.type.type) + '" />'
		decTab()
		result += newLine() + '</xs:simpleType>'
		decTab()
		result += newLine() + '</xs:element>'


	# Simple type
	if isinstance(typ.type, SDT3SimpleType) or isinstance(typ, SDT3SimpleType):
		ty = typ.type if isinstance(typ.type, SDT3SimpleType) else typ
		if ty.type == 'enum':
			result += ' >'
			incTab()
			result += newLine() + '<xs:simpleType>'
			incTab()
			result += newLine() + '<xs:list itemType="' + namespacePrefix + ':enum" />'
			decTab()
			result += newLine() + '</xs:simpleType>'
			decTab()
			result += newLine() + '</xs:element>'
			enumTypes.add(name)
		else:
			result += ' type="'
			result += getSimpleDataType(ty.type)
			result += '" />'

	# Struct
	elif (isinstance(typ.type, SDT3StructType)):
		print('structType not supported yet')
		result += 'XXX'
	
	return result


def getSimpleDataType(type):
	result = ''
	if type == 'boolean':
		result += 'xs:boolean'
	elif type == 'integer':
		result += 'xs:integer'
	elif type == 'float':
		result += 'xs:float'
	elif type == 'string':
		result += 'xs:string'
	elif type == 'datetime':
		result += 'm2m:timestamp'	# CHECK
	elif type == 'date':
		result += 'm2m:timestamp'	# CHECK
	elif type == 'time':
		result += 'm2m:timestamp'	# CHECK
	elif type =='uri':
		result += 'xs:anyURI'
	elif type == 'blob':
		result += 'xs:base64Binary'	# CHECK 
	elif re.match('.+:.+', type):	# CHECK enum
		result += type
	return result
	

#############################################################################

# Enum Types

def exportEnumTypes(path):
	global enumTypes, namespacePrefix

	if len(enumTypes) > 0:
		# Create pakage path and make directories
		hdDirectory = str(path) + os.sep + namespacePrefix
		hdPath = pathlib.Path(hdDirectory)
		try:
			hdPath.mkdir(parents=True)
		except FileExistsError as e:
			pass # on purpose. We override files for now

	for enumName in enumTypes:
		exportEnumType(hdPath, enumName)


def exportEnumType(path, enumName):

	fileName = sanitizeName(enumName, False)
	fullFileName = str(path) + os.sep + fileName + '.xsd'
	outputFile = None
	try:
		outputFile = open(fullFileName, 'w')
		outputFile.write(getEnumType(enumName))		
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()


xsdSchemaTemplateEnumHeader = '''
	<xs:simpleType name="{name}">
		<xs:annotation>
			<xs:documentation>TODO</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:integer">'''

xsdSchemaTemplateEnumFooter = '''
		</xs:restriction>
	</xs:simpleType>
</xs:schema>'''


def getEnumType(enumName):
	global xsdSchemaTemplateHeader, xsdSchemaTemplateEnumHeader, xsdSchemaTemplateEnumFooter
	global domainDefinition, headerText, targetNamespace, namespacePrefix

	result  = xsdSchemaTemplateHeader.format(headerText=headerText, namespace=namespacePrefix, domain=domainDefinition, targetnamespace=targetNamespace)
	result += xsdSchemaTemplateEnumHeader.format(name=sanitizeName(enumName, False))
	incTab(3)
	#result += newLine() + '<!-- TODO comment -->'
	result += newLine() + '<xs:enumeration value="1" />'
	decTab(3)
	result += xsdSchemaTemplateEnumFooter.format()
	return result


#############################################################################

# Actions

xsdActionTemplate = '''
	<xs:element name="{name}" substitutionGroup="m2m:sg_flexContainerResource">
		<xs:complexType>
			<xs:complexContent>
				<!-- Inherit Common Attributes from data type "flexContainerResource" -->
				<xs:extension base="m2m:flexContainerResource">
					<xs:sequence>

						<!-- Resource Specific Attributes -->
					
						<!-- Child Resources -->

						<xs:choice minOccurs="0" maxOccurs="1">
							<xs:element name="childResource" type="m2m:childResourceRef" maxOccurs="unbounded" />
							<xs:choice minOccurs="1" maxOccurs="unbounded">
								<xs:element ref="m2m:subscription" />
							</xs:choice>
						</xs:choice>
					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
	</xs:element>

	<xs:element name="{name}Annc" substitutionGroup="m2m:sg_announcedFlexContainerResource">
		<xs:complexType>
			<xs:complexContent>
				<!-- Inherit Common Attributes from data type "announcedFlexContainerResource" -->
				<xs:extension base="m2m:announcedFlexContainerResource">
					<xs:sequence>

						<!-- Resource Specific Attributes -->
										
						<!-- Child Resources -->

						<xs:choice minOccurs="0" maxOccurs="1">
							<xs:element name="childResource" type="m2m:childResourceRef" maxOccurs="unbounded" />
							<xs:choice minOccurs="1" maxOccurs="unbounded">
								<xs:element ref="m2m:subscription" />
							</xs:choice>
						</xs:choice>	
					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
	</xs:element>
'''

def exportActions(path):
	global actions
	for actionName in actions:
		exportAction(path, actions[actionName])



def exportAction(path, action):
	name = sanitizeName(action.name, False)
	fullFileName = getVersionedFilename(name, path=str(path), isAction=True)
	outputFile = None
	try:
		outputFile = open(fullFileName, 'w')
		outputFile.write(getAction(action))		
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()


def getAction(action):
	global xsdActionTemplate

	result = ''
	result += addModuleClassHeader()
	result += xsdActionTemplate.format(name=sanitizeName(action.name, False))
	result += addModuleClassFooter()

	# small hack: add the announced device name to the abbreviated list
	sanitizeName(action.name, False, annc=True)

	return result


#############################################################################

# Properties

def getSpecificPropertyXSD(prop, annc):
	result = ''
	result += newLine() + '<xs:element name="' + sanitizeName(prop.name, False) + '"'
	if annc:
		result += ' minOccurs="0"'
	else:
		if prop.optional == 'true':	# indicate an optional property
			result += ' minOccurs="0"'
	result += getDataType(prop.name, prop.type)
	return result;


#############################################################################

# Devices

xsdSchemaTemplateDeviceHeader = '''<?xml version="1.0" encoding="UTF-8"?>
<!--
{headerText}
-->

<xs:schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="{targetnamespace}"
	xmlns:m2m="http://www.onem2m.org/xml/protocols" xmlns:{namespace}="http://www.onem2m.org/xml/protocols/{domain}" elementFormDefault="unqualified" attributeFormDefault="unqualified"
	xmlns:xs="http://www.w3.org/2001/XMLSchema">

	<xs:import namespace="http://www.onem2m.org/xml/protocols" schemaLocation="CDT-subscription-v2_7_0.xsd" />
	<xs:import namespace="http://www.onem2m.org/xml/protocols" schemaLocation="CDT-commonTypes-v2_7_0.xsd" />

	<xs:include schemaLocation="HD-enumerationTypes-v1_0_0.xsd" />{schemas}

'''

xsdSchemaTemplateDeviceFooter = '''
</xs:schema>
'''

flexContainerDeviceResourceTemplate = '''
	<xs:element name="{deviceName}" substitutionGroup="m2m:sg_flexContainerResource">
		<xs:complexType>
			<xs:complexContent>
				<!-- Inherit Common Attributes from data type "flexContainerResource" -->
				<xs:extension base="m2m:flexContainerResource">
					<xs:sequence>
					
						<!-- Resource Specific Attributes -->
{deviceProperties}						

						<!-- Child Resources -->
						
						<xs:choice minOccurs="0" maxOccurs="1">
							<xs:element name="childResource" type="m2m:childResourceRef" minOccurs="1" maxOccurs="unbounded" />
							<xs:choice minOccurs="1" maxOccurs="unbounded">
{moduleClasses}

								<xs:element ref="m2m:subscription"  />
							</xs:choice>
						</xs:choice>

					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
	</xs:element>

	<xs:element name="{deviceName}Annc" substitutionGroup="m2m:sg_announcedFlexContainerResource">
		<xs:complexType>
			<xs:complexContent>
				<!-- Inherit Common Attributes from data type "announcedFlexContainerResource" -->
				<xs:extension base="m2m:announcedFlexContainerResource">
					<xs:sequence>

						<!-- Resource Specific Attributes -->		
{devicePropertiesAnnc}
						<!-- Child Resources -->

						<xs:choice minOccurs="0" maxOccurs="1">
							<xs:element name="childResource" type="m2m:childResourceRef" minOccurs="1" maxOccurs="unbounded" />
							<xs:choice minOccurs="1" maxOccurs="unbounded">
{moduleClassesAnnc}

								<xs:element ref="m2m:subscription"  />
							</xs:choice>
						</xs:choice>

					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
	</xs:element>
'''


def exportDevice(device, package, path):
	global namespacePrefix, modelVersion

	# export the module class itself

	name 	     = sanitizeName(device.id, False)
	fullFilename = getVersionedFilename(name, name=None, path=str(path))
	outputFile   = None

	try:
		outputFile = open(fullFilename, 'w')
		outputFile.write(getDeviceXSD(device, package, name, path))		
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()


def getDeviceXSD(device, package, deviceName, path):
	result  = ''
	incTab()
	result += addDeviceHeader(device)
	result += addDevice(device, deviceName)
	result += addDeviceFooter()
	decTab()
	return result


def addDeviceHeader(device):
	global xsdSchemaTemplateDeviceHeader, namespacePrefix
	global headerText, domainDefinition, targetNamespace

	# XML header + license text
	return xsdSchemaTemplateDeviceHeader.format(headerText=headerText, 
												namespace=namespacePrefix,
												domain=domainDefinition,
												targetnamespace=targetNamespace,
												schemas=getDeviceSchemas(device))


def addDeviceFooter():
	global xsdSchemaTemplateDeviceFooter
	return xsdSchemaTemplateDeviceFooter.format()


def addDevice(device, deviceName):
	global flexContainerDeviceResourceTemplate
	incTab(5)
	result = flexContainerDeviceResourceTemplate.format(deviceName=deviceName, 
														deviceProperties=getDeviceProperties(device),
														devicePropertiesAnnc=getDeviceProperties(device, annc=True),
													    moduleClasses=getDeviceModuleClasses(device),
													    moduleClassesAnnc=getDeviceModuleClasses(device, withAnnc=True))

	# small hack: add the announced device name to the abbreviated list
	sanitizeName(deviceName, False, annc=True)

	decTab(5)
	return result


def getDeviceSchemas(device):
	global namespacePrefix

	result = ''

	# Referenced modules
	parentModuleClasses = {}
	parentModuleClassNames = []
	for module in device.modules:
		parentModuleClassName = module.extends.domain + '.' + module.extends.clazz
		if module.name == module.extends.clazz:
			name = getVersionedFilename(module.name, isModule=True)
			result += newLine() + '<xs:include schemaLocation="' + name + '" />'
		else:
			parentModuleClasses[module.name] = module
			if parentModuleClassName not in parentModuleClassNames:
				name = getVersionedFilename(module.extends.clazz, isModule=True)
				result += newLine() + '<xs:include schemaLocation="' + name + '" />'
				parentModuleClassNames.append(parentModuleClassName)

	# Special handling when the extended class is actually different from the parent class 
	extraElements = ''
	if len(parentModuleClasses) > 0:
		extraElements += newLine()
		for name in parentModuleClasses:
			module = parentModuleClasses[name]
			# For now, we only check for a different name. Here we need to create a new XSD but with the same content as the orignal class.
			if module.name != module.extends.clazz:
				extraElements += newLine() + '<xs:element name="' + module.name + '" type="' + namespacePrefix + ':' + module.extends.clazz + '" />'
				extraElements += newLine() + '<xs:element name="' + module.name + 'Annc" type="' + namespacePrefix + ':' + module.extends.clazz + 'Annc" />'

			#	Future improvement to add more elements when extending the inherited ModuleClass
			#   <xs:element name="freshTemperature">
            #		<xs:complexType>
			#			<xs:complexContent>
			#				<xs:extension base="hd:temperature">
			#
			#				</xs:extension>
			#			</xs:complexContent>
			#		</xs:complexType>
			#	</xs:element>

	result += extraElements
	return result


def getModuleClassSchemas(module):
	if module == None:
		return ''
	result = ''

	# Referenced Actions
	for action in module.actions:
		name = getVersionedFilename(action.name, isAction=True)
		result += newLine() + '<xs:include schemaLocation="' + name + '" />'
	return result


def getDeviceModuleClasses(device, withAnnc=False):
	global namespacePrefix
	result = ''
	incTab(2)
	for module in device.modules:
		name = sanitizeName(module.name, False, annc=withAnnc) # Side effect: add abbreviated annc resource
		result += newLine() + '<xs:element ref="' + namespacePrefix + ':' + name + '" />'
		# if this is an announced ressource, then add an extra line for it
		if withAnnc:
			result += newLine() + '<xs:element ref="' + namespacePrefix + ':' + name + 'Annc" />'
	decTab(2)
	return result;


def getDeviceProperties(device, annc=False):
	result = ''
	# Properties
	for prop in device.properties:
		result += getSpecificPropertyXSD(prop, annc)
	return result



#############################################################################

# Export abbreviations

# def exportAbbreviations(path, abbreviations):
# 	global constAbbreviationCSVFile, constAbbreviationMAPFile

# 	# Export as python map
# 	fullFilename = str(path) + os.sep + constAbbreviationMAPFile
# 	outputFile = None
# 	try:
# 		outputFile = open(fullFilename, 'w')
# 		outputFile.write(abbreviations)
# 	except IOError as err:
# 		print(err)
# 	finally:
# 		if outputFile != None:
# 			outputFile.close()

# 	# Export as CSV
# 	fullFilename = str(path) + os.sep + constAbbreviationCSVFile
# 	outputFile = None
# 	try:
# 		outputFile = open(fullFilename, 'w', newline='')
# 		writer = csv.writer(outputFile)
# 		for key, value in abbreviations.items():
# 			writer.writerow([key, value])
# 	except IOError as err:
# 		print(err)
# 	finally:
# 		if outputFile != None:
# 			outputFile.close()


# create a python map
# def getAbbreviations(abbreviations):
# 	result  = '#!/usr/bin/python'
# 	result += newLine(2)
# 	result += newLine() + 'map = {'
# 	incTab()
# 	vals = ''
# 	for key in abbreviations:
# 		if len(vals) > 0:
# 			vals += ','
# 		vals += newLine() + '\'' + key + '\':\'' + abbreviations[key] + '\''
# 	result += vals
# 	decTab()
# 	result += newLine() + '}'
# 	return result


#############################################################################


#
#	Helpers
#

# Sanitize the name for SVG

def sanitizeName(name, isClass, annc=False):
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

	# If this name is an announced resource, add "Annc" Postfix to both the
	# name as well as the abbreviation.
	if annc:
		abbr = SDTAbbreviate.abbreviate(result)
		SDTAbbreviate.addAbbreviation(result + 'Annc', abbr + 'Annc')
	else:
		abbr = SDTAbbreviate.abbreviate(result)
		SDTAbbreviate.addAbbreviation(result, abbr)

	return result

# Sanitize the package name for XSD

def sanitizePackage(package):
	result = package.replace('/', '.')
	return result

# get a versioned filename

def getVersionedFilename(fileName, name=None, path=None, isModule=False, isAction=False):
	global modelVersion, namespacePrefix

	prefix  = ''
	postfix = ''
	if name != None:
		prefix += sanitizeName(name, False) + '_'
	else:
		if namespacePrefix != None:
			prefix += namespacePrefix.upper() + '-'
		if isAction:
			prefix += 'act-'
		if isModule:
			prefix += 'mod-'

	if modelVersion != None:
		postfix += '-v' + modelVersion.replace('.', '_')

	fullFilename = ''
	if path != None:
		fullFilename = path + os.sep
	fullFilename += prefix + sanitizeName(fileName, False) + postfix + '.xsd'

	return fullFilename


# Tabulator handling

tab = 0

def incTab(count=1):
	global tab
	tab += count

def decTab(count=1):
	global tab
	if (tab > 0):
		tab -= count

def newLine(count=1):
	global tab
	result = ''
	for j in range(count):
		result += '\n'
		for i in range(tab):
			result += '\t'
	return result





