#	SDT3PrintOneM2MSVG.py
#
#	Generate XSD for oneM2M


import datetime, os, pathlib, string
from SDT3Classes import *


# variable that holds an optional header text
headerText = ''

# variable that holds the domain for the oneM2M XSD definition
domainDefinition = ''

# variable for found enum types
enumTypes = set()

def print3OneM2MXSD(domain, directory, options):
	global headerText, domainDefinition, enumTypes

	# read license text
	lfile = options['licensefile']
	if lfile != None:
		with open(lfile, 'rt') as f:
			headerText = f.read()

	# get the domain
	domainDefinition = options['domain']
	if domainDefinition == None:
		domainDefinition = ''


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

	# Export enum types
	exportEnumTypes(path)


	# Export Devices

	# TODO for device in domain.devices:
	# 	exportDevice(device, package, path)


#############################################################################


# Export a ModuleClass definition to a file

def exportModuleClass(module, package, path, name=None):

	# export the module class itself
	prefix = ''
	if name != None:
		prefix = sanitizeName(name, True) + '_'

	name = sanitizeName(module.name, False)
	fileName = str(path) + os.sep + prefix + name + '.xsd'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getModuleClassXSD(module, package, name, path))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
			outputFile.close()


# Get the ModuleClass resource

def getModuleClassXSD(module, package, name, path):

	result  = ''
	result += addModuleClassHeader()
	result += addModuleClass(module, name)
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

def addModuleClass(module, name):
	global flexContainerResourceTemplate
	return flexContainerResourceTemplate.format(name=sanitizeName(name, False), 
												specificAttributes=getSpecificAttributes(module),
												specificAttributesAnnc=getSpecificAttributes(module, annc=True));


def getSpecificAttributes(module, annc=False):
	result = ''
	incTab(5)
	for data in module.data:
		result += getDataPointXSD(data, annc)
	decTab(5)
	return result


def getDataPointXSD(data, annc):
	result = ''
	result += newLine() + '<xs:element name="' + sanitizeName(data.name, False) + '"'
	if annc:
		result += ' minOccurs="0"'
	result += getDataPointType(data)
	return result;



def getDataPointType(dataPoint):
	global enumTypes
	result = ''
	name = sanitizeName(dataPoint.name, False)

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
			enumTypes.add(name)
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

def exportEnumTypes(path):
	global enumTypes

	if len(enumTypes) > 0:
		# Create package path and make directories
		hdDirectory = str(path) + os.sep + 'hd'
		hdPath = pathlib.Path(hdDirectory)
		try:
			hdPath.mkdir(parents=True)
		except FileExistsError as e:
			pass # on purpose. We override files for now

	for en in enumTypes:
		exportEnumType(hdPath, en)


def exportEnumType(path, en):

	fileName = str(path) + os.sep + en + '.xsd'
	outputFile = None
	try:
		outputFile = open(fileName, 'w')
		outputFile.write(getEnumType(en))		
	except IOError as err:
		print(err)
	finally:
		if (outputFile != None):
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


def getEnumType(en):
	global xsdSchemaTemplate, xsdSchemaTemplateHeader, xsdSchemaTemplateFooter
	global domainDefinition, headerText

	result  = xsdSchemaTemplate.format(headerText=headerText, domain=domainDefinition)
	result += xsdSchemaTemplateHeader.format(name=en)
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

# Sanitize the package name for SVG

def sanitizePackage(package):
	result = package.replace('/', '.')
	return result



# experimental abreviation function. Move later

def abbreviate(name, length=5):
	l = len(name)
	if l <= length:
		result = name
		while l < length:
			for i in range(length - l):
				result += result[i]
			l = len(result)
		return result.upper()
	
	# First char
	result  = name[0]
	
	# Last char
	result += name[-1]

	if len(result) < length:
		mask = name[1:l-1]
		# Camel cases chars
		camels = ''
		for i in range(1,l-1):
			c = name[i]
			if c.isupper():
				camels += c
				mask = mask[:i-1] + mask[i:]
		result = result[:1] + camels + result[1:]

		# Fill with remaining chars of the mask, starting from the back
		lm = len(mask)
		for i in range(0, length - len(result)):
			pos = i + 1
			result = result[:pos] + mask[i] + result[pos:] 

	return result[:length].upper()



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





