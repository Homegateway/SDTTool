#	SDT3PrintOneM2MSVG.py
#
#	Generate XSD for oneM2M


import datetime, os, pathlib, string
from SDT3Classes import *
import SDTAbbreviate 



# variable that holds an optional header text
headerText = ''

# variable that holds the domain for the oneM2M XSD definition
domainDefinition = ''

# variable for found enum types
enumTypes = set()

# whether of not create abbreviated XSD
doAbbreviations = False

def print3OneM2MXSD(domain, directory, options):
	global headerText, domainDefinition, enumTypes, doAbbreviations

	# read license text
	lfile = options['licensefile']
	if lfile != None:
		with open(lfile, 'rt') as f:
			headerText = f.read()

	# get the domain
	domainDefinition = options['domain']
	if domainDefinition == None:
		domainDefinition = ''

	# get abbreviation status
	doAbbreviations = options['withabbreviations']
	if doAbbreviations == None:
		doAbbreviations = False


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
		exportModuleClass(module, package, path, abbreviate=False)
		if doAbbreviations:
			exportModuleClass(module, package, path, abbreviate=True)

	# Export enum types
	exportEnumTypes(path, abbreviate=False)
	if doAbbreviations:
		exportEnumTypes(path, abbreviate=True)


	# Export Devices

	# TODO for device in domain.devices:
	# 	exportDevice(device, package, path)


#############################################################################


# Export a ModuleClass definition to a file

def exportModuleClass(module, package, path, name=None, abbreviate=False):

	# export the module class itself
	prefix = ''
	if name != None:
		prefix = sanitizeName(name, True, abbreviate=abbreviate) + '_'
	postfix = ''
	if abbreviate:
		postfix = '.abbr'

	moduleName = sanitizeName(module.name, False, abbreviate=abbreviate)
	fileName = sanitizeName(module.name, False, abbreviate=False)
	fullFilename = str(path) + os.sep + prefix + fileName + postfix + '.xsd'
	outputFile = None
	try:
		outputFile = open(fullFilename, 'w')
		outputFile.write(getModuleClassXSD(module, package, moduleName, path, abbreviate))		
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()


# Get the ModuleClass resource

def getModuleClassXSD(module, package, name, path, abbreviate):

	result  = ''
	result += addModuleClassHeader()
	result += addModuleClass(module, name, abbreviate)
	result += addModuleClassFooter()
	return result


# Add standard header attributes to a module class resource

xsdSchemaTemplate = '''<?xml version="1.0" encoding="UTF-8"?>
<!--
{headerText}
-->

<xs:schema xmlns="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.onem2m.org/xml/protocols/homedomain"
	xmlns:m2m="http://www.onem2m.org/xml/protocols" xmlns:hd="http://www.onem2m.org/xml/protocols/{domain}" elementFormDefault="unqualified" attributeFormDefault="unqualified"
	xmlns:xs="http://www.w3.org/2001/XMLSchema">

	<xs:import namespace="http://www.onem2m.org/xml/protocols" schemaLocation="CDT-commonTypes-v2_5_0.xsd" />
	<xs:import namespace="http://www.onem2m.org/xml/protocols" schemaLocation="CDT-subscription-v2_5_0.xsd" />

'''

def addModuleClassHeader():
	global xsdSchemaTemplate
	global headerText, domainDefinition

	# XML header + license text
	incTab()
	return xsdSchemaTemplate.format(headerText=headerText, domain=domainDefinition)


def addModuleClassFooter():
	decTab()
	return newLine() + '</xs:schema>'


# The main resource definition

flexContainerResourceTemplate = '''
	<xs:element name="{name}">
		<xs:complexType>
			<xs:complexContent>
				<!-- Inherit Common Attributes from data type "flexContainerResource" -->
				<xs:extension base="m2m:flexContainerResource">
					<xs:sequence>
						<!-- Resource Specific Attributes -->
{specificAttributes}

						<!-- Child Resources -->
						<xs:choice minOccurs="0" maxOccurs="1">
							<xs:element name="childResource" type="m2m:childResourceRef" maxOccurs="unbounded" />
							<xs:element ref="m2m:subscription" maxOccurs="unbounded" />
						</xs:choice>
					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
	</xs:element>

	<xs:element name="{name}Annc">
		<xs:complexType>
			<xs:complexContent>
				<!-- Inherit Common Attributes from data type "announcedFlexContainerResource" -->
				<xs:extension base="m2m:announcedFlexContainerResource">
					<xs:sequence>
						<!-- Resource Specific Attributes -->		
{specificAttributesAnnc}

						<!-- Child Resources -->
						<xs:choice minOccurs="0" maxOccurs="1">
							<xs:element name="childResource" type="m2m:childResourceRef" maxOccurs="unbounded" />
							<xs:element ref="m2m:subscription" maxOccurs="unbounded" />
						</xs:choice>
					</xs:sequence>
				</xs:extension>
			</xs:complexContent>
		</xs:complexType>
	</xs:element>
'''

def addModuleClass(module, name, abbreviate):
	global flexContainerResourceTemplate
	return flexContainerResourceTemplate.format(name=sanitizeName(name, False, abbreviate=abbreviate), 
												specificAttributes=getSpecificAttributes(module, annc=False, abbreviate=abbreviate),
												specificAttributesAnnc=getSpecificAttributes(module, annc=True, abbreviate=abbreviate));


def getSpecificAttributes(module, annc=False, abbreviate=False):
	result = ''
	incTab(5)
	for data in module.data:
		result += getDataPointXSD(data, annc, abbreviate)
	decTab(5)
	return result


def getDataPointXSD(data, annc, abbreviate):
	result = ''
	result += newLine() + '<xs:element name="' + sanitizeName(data.name, False, abbreviate=abbreviate) + '"'
	if annc:
		result += ' minOccurs="0"'
	result += getDataPointType(data, abbreviate)
	return result;



def getDataPointType(dataPoint, abbreviate):
	global enumTypes
	result = ''
	name = sanitizeName(dataPoint.name, False, abbreviate)

	# Simple type
	if (isinstance(dataPoint.type.type, SDT3SimpleType)):
		ty = dataPoint.type.type
		if (ty.type == 'enum'):
			result += ' />'
			incTab()
			result += newLine() + '<xs:simpleType>'
			incTab()
			result += newLine() + '<xs:list itemType="hd:' + name + '" />'
			decTab()
			result += newLine() + '</xs:simpleType>'
			decTab()
			enumTypes.add(dataPoint.name)
		else:
			result += ' type="'
			if (ty.type == 'boolean'):
				result += 'xs:boolean'
			elif (ty.type == 'integer'):
				result += 'xs:integer'
			elif (ty.type == 'float'):
				result += 'xs:float'
			elif (ty.type == 'string'):
				result += 'xs:string'
			elif (ty.type == 'datetime'):
				result += 'm2m:timestamp'	# CHECK
			elif (ty.type == 'date'):
				result += 'm2m:timestamp'	# CHECK
			elif (ty.type == 'time'):
				result += 'm2m:timestamp'	# CHECK
			elif (ty.type =='uri'):
				result += 'm2m:URI'			# CHECK
			elif (ty.type == 'blob'):
				result += 'xs:base64Binary'	# CHECK 
			result += '" />'

	# Array
	elif (isinstance(dataPoint.type.type, SDT3ArrayType)):
		print('arrayType not supported yet')
		result += 'XXX'

	# Struct
	elif (isinstance(dataPoint.type.type, SDT3StructType)):
		print('structType not supported yet')
		result += 'XXX'
	
	return result

# Enum Types

def exportEnumTypes(path, abbreviate=False):
	global enumTypes

	if len(enumTypes) > 0:
		# Create package path and make directories
		hdDirectory = str(path) + os.sep + 'hd'
		hdPath = pathlib.Path(hdDirectory)
		try:
			hdPath.mkdir(parents=True)
		except FileExistsError as e:
			pass # on purpose. We override files for now

	for enumName in enumTypes:
		exportEnumType(hdPath, enumName, abbreviate)


def exportEnumType(path, enumName, abbreviate):

	postfix = ''
	if abbreviate:
		postfix = '.abbr'

	fileName = sanitizeName(enumName, False, abbreviate=False)
	fullFileName = str(path) + os.sep + fileName + postfix + '.xsd'
	outputFile = None
	try:
		outputFile = open(fullFileName, 'w')
		outputFile.write(getEnumType(enumName, abbreviate))		
	except IOError as err:
		print(err)
	finally:
		if outputFile != None:
			outputFile.close()


xsdSchemaTemplateHeader = '''
	<xs:simpleType name="{name}">
		<xs:annotation>
			<xs:documentation>TODO</xs:documentation>
		</xs:annotation>
		<xs:restriction base="xs:integer">'''

xsdSchemaTemplateFooter = '''
		</xs:restriction>
	</xs:simpleType>
</xs:schema>'''


def getEnumType(enumName, abbreviate=False):
	global xsdSchemaTemplate, xsdSchemaTemplateHeader, xsdSchemaTemplateFooter
	global domainDefinition, headerText

	result  = xsdSchemaTemplate.format(headerText=headerText, domain=domainDefinition)
	result += xsdSchemaTemplateHeader.format(name=sanitizeName(enumName, False, abbreviate))
	incTab(3)
	result += newLine() + '<!-- TODO comment -->'
	result += newLine() + '<xs:enumeration value="1" />'
	decTab(3)
	result += xsdSchemaTemplateFooter.format()
	return result

#############################################################################

#
#	Helpers
#

# Sanitize the name for SVG

def sanitizeName(name, isClass, abbreviate=False):
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

	if abbreviate:
		result = SDTAbbreviate.abbreviate(result)
	return result

# Sanitize the package name for SVG

def sanitizePackage(package):
	result = package.replace('/', '.')
	return result



# Tabulator handling

tab = 0

def incTab(count=1):
	global tab
	tab += count

def decTab(count=1):
	global tab
	if (tab > 0):
		tab -= count

def newLine():
	global tab
	result = '\n'
	for i in range(tab):
		result += '\t'
	return result





