#	SDT4Parser.py
#
#	Callback target class for the ElementTree parser to parse a SDT4

from .SDT4Classes import *


class SDT4Parser:

	# Define the element tags of the SDT4

	actionTag 						= 'action'
	actionsTag						= 'actions'
	argTag							= 'arg'
	argsTag							= 'args'
	arrayTypeTag					= 'array'
	constraintTag					= 'constraint'
	constraintsTag					= 'constraints'
	dataPointTag					= 'datapoint'
	dataTag							= 'data'
	dataTypeTag						= 'datatype'
	dataTypesTag					= 'datatypes'
	deviceClassTag					= 'deviceclass'
	deviceClassesTag				= 'deviceclasses'
	domainTag						= 'domain'
	enumTypeTag 					= 'enum'
	enumValueTag 					= 'enumvalue'
	eventTag 						= 'event'
	eventsTag						= 'events'
	excludeTag						= 'exclude'
	extendDeviceTag					= 'extenddevice'
	extendTag						= 'extend'
	importsTag						= 'imports'
	includeTag						= 'include'
	moduleClassTag					= 'moduleclass'
	moduleClassesTag				= 'moduleclasses'
	productClassTag 				= 'productclass'
	productClassesTag				= 'productclasses'
	propertiesTag					= 'properties'
	propertyTag						= 'property'
	simpleTypeTag					= 'simple'
	structTypeTag					= 'struct'
	subDeviceTag 					= 'subdevice'
	subDevicesTag 					= 'subdevices'

	# Document tags
	docTag 							= 'doc'
	ttTag							= 'tt'
	emTag							= 'em'
	bTag							= 'b'
	pTag 							= 'p'
	imgTag							= 'img'
	imgCaptionTag					= 'caption'


	def __init__(self):
		self.elementStack = []
		self.nameSpaces = []
		self.domain = None

	
	def start(self, tag, attrib):

		# First add the name space to the list of used name spaces
		uri, ignore, otag = tag[1:].partition("}")
		if uri not in self.nameSpaces:
			self.nameSpaces.append(uri)
		ntag = otag.lower()

		# Check non-emptyness of attributes
		for at in attrib:
			if len(attrib[at].strip()) == 0:
				raise SyntaxError('empty attribute: ' + at + ' for element ' + tag)


		# Handle all elements 

		# The lastElem always contains the last element on the stack and is
		# used transparently in the code below.
		lastElem = self.elementStack[-1] if len(self.elementStack) > 0 else None

		# Call the handler function for that element tag.
		# First, chech whether this is allowed for the current parent, or raise an exception
		if ntag in handlers:
			(func, instances) = handlers[ntag]
			if instances is None or isinstance(lastElem, instances):
				func(attrib, lastElem, self.elementStack)
			else:
				raise SyntaxError('%s definition is only allowed in %s elements' % (otag, [v._name for v in instances]))

		# Other tags to ignore / just containers
		elif ntag in (SDT4Parser.actionsTag,
					  SDT4Parser.argsTag,
					  SDT4Parser.constraintsTag,
					  SDT4Parser.dataTag,
					  SDT4Parser.dataTypesTag,
					  SDT4Parser.deviceClassesTag,
					  SDT4Parser.eventsTag,
					  SDT4Parser.extendDeviceTag,
					  SDT4Parser.importsTag, 
					  SDT4Parser.moduleClassesTag,
					  SDT4Parser.productClassesTag,
					  SDT4Parser.propertiesTag,
					  SDT4Parser.subDevicesTag):
			pass

		# Encountered an unknwon element
		else:
			raise SyntaxError('Unknown Element: %s %s' % (tag, attrib))


	def end(self, tag):
		uri, ignore, ntag = tag[1:].partition("}")
		ntag = ntag.lower()
		if ntag == SDT4Parser.domainTag:
			self.domain = self.elementStack.pop() # Assign the domain to the parser as result

		elif ntag in (SDT4Parser.actionTag,
					  SDT4Parser.argTag, 
					  SDT4Parser.arrayTypeTag,
					  SDT4Parser.bTag,
					  SDT4Parser.constraintTag,
					  SDT4Parser.eventTag,
					  SDT4Parser.deviceClassTag,
					  SDT4Parser.dataPointTag,
					  SDT4Parser.dataTypeTag,
					  SDT4Parser.docTag,
					  SDT4Parser.emTag,
					  SDT4Parser.enumTypeTag,
					  SDT4Parser.enumValueTag,
					  SDT4Parser.extendTag,
					  SDT4Parser.imgTag,  
					  SDT4Parser.imgCaptionTag,
					  SDT4Parser.moduleClassTag, 
					  SDT4Parser.pTag,
					  SDT4Parser.productClassTag,
					  SDT4Parser.propertyTag,
					  SDT4Parser.simpleTypeTag,
					  SDT4Parser.structTypeTag,
					  SDT4Parser.subDeviceTag,
					  SDT4Parser.ttTag):
			obj = self.elementStack.pop()
			obj.endElement()
		else:
			# ignore others
			pass


	def data(self, data):
		if len(self.elementStack) < 1:
			return




		if isinstance(self.elementStack[-1], SDT4Doc):
			obj = self.elementStack[-1]
			obj.addContent(' ' + ' '.join(data.split()))
		elif isinstance(self.elementStack[-1], (SDT4DocTT, SDT4DocEM, SDT4DocB, SDT4DocP, SDT4DocIMG, SDT4DocCaption)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))


	def close(self): # ignore end of file
		pass


	def comment(self, data): # ignore comments
		pass


def getAttribute(attrib, attribName):
	return attrib[attribName].strip() if attribName in attrib else None


#
#	Hanlder for each of the element types
#

def handleAction(attrib, lastElem, elementStack):
	action = SDT4Action()
	action.name = getAttribute(attrib, 'name')
	action.optional = getAttribute(attrib, 'optional')
	action.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.actions.append(action)
	elementStack.append(action)


def handleArg(attrib, lastElem, elementStack):
	arg = SDT4Arg()
	arg.name = getAttribute(attrib, 'name')
	arg.optional = getAttribute(attrib, 'optional')
	arg.default = getAttribute(attrib, 'default')
	arg.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.args.append(arg)
	elementStack.append(arg)


def handleArrayType(attrib, lastElem, elementStack):
	arrayType = SDT4ArrayType()
	lastElem.type = arrayType
	elementStack.append(arrayType)


def handleB(attrib, lastElem, elementStack):
	b = SDT4DocB()
	b.doc = lastElem.doc
	elementStack.append(b)


def handleConstraint(attrib, lastElem, elementStack):
	constraint = SDT4Constraint()
	constraint.name = getAttribute(attrib, 'name')
	constraint.type = getAttribute(attrib, 'type')
	constraint.value = getAttribute(attrib, 'value')
	constraint.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.constraints.append(constraint)
	elementStack.append(constraint)


def handleDataPoint(attrib, lastElem, elementStack):
	dataPoint = SDT4DataPoint()
	dataPoint.name = getAttribute(attrib, 'name')
	dataPoint.optional = getAttribute(attrib, 'optional')
	dataPoint.writable = getAttribute(attrib, 'writable')
	dataPoint.readable = getAttribute(attrib, 'readable')
	dataPoint.eventable = getAttribute(attrib, 'eventable')
	dataPoint.default = getAttribute(attrib, 'default')
	dataPoint.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.data.append(dataPoint)
	elementStack.append(dataPoint)


def handleDataType(attrib, lastElem, elementStack):
	dataType = SDT4DataType()
	dataType.name = getAttribute(attrib, 'name')
	dataType.unitOfMeasure = getAttribute(attrib, 'unitOfMeasure')
	dataType.semanticURI = getAttribute(attrib, 'semanticURI')
	if isinstance(lastElem, SDT4ArrayType):
		lastElem.arrayType = dataType
	elif isinstance(lastElem, SDT4StructType):
		lastElem.structElements.append(dataType)
	elif isinstance(lastElem, SDT4Domain):			# DataTypes in Domain
		lastElem.dataTypes.append(dataType)
	else:
		lastElem.type = dataType
	elementStack.append(dataType)


def handleDeviceClass(attrib, lastElem, elementStack):
	device = SDT4DeviceClass()
	device.id = getAttribute(attrib, 'id')
	device.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.deviceClasses.append(device)
	elementStack.append(device)


def handleDoc(attrib, lastElem, elementStack):
	doc = SDT4Doc()
	lastElem.doc = doc
	elementStack.append(doc)


def handleDomain(attrib, lastElem, elementStack):
	domain = SDT4Domain()
	domain.id = getAttribute(attrib, 'id')
	domain.semanticURI = getAttribute(attrib, 'semanticURI')
	elementStack.append(domain)


def handleEM(attrib, lastElem, elementStack):
	em = SDT4DocEM()
	em.doc = lastElem.doc
	elementStack.append(em)


def handleEnumType(attrib, lastElem, elementStack):
	enumType = SDT4EnumType()
	lastElem.type = enumType
	elementStack.append(enumType)


def handleEnumValue(attrib, lastElem, elementStack):
	value = SDT4EnumValue()
	value.name = getAttribute(attrib, 'name')
	value.value = getAttribute(attrib, 'value')
	value.type = getAttribute(attrib, 'type')
	value.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.enumValues.append(value)
	elementStack.append(value)


def handleEvent(attrib, lastElem, elementStack):
	event = SDT4Event()
	event.name = getAttribute(attrib, 'name')
	event.optional = getAttribute(attrib, 'optional')
	event.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.events.append(event)
	elementStack.append(event)


def handleExtendExclude(attrib, lastElem, elementStack):
	exclude = SDT4ExtendExclude()
	exclude.name = getAttribute(attrib, 'name')
	exclude.type = getAttribute(attrib, 'type')
	lastElem.excludes.append(exclude)


def handleExtend(attrib, lastElem, elementStack):
	extend = SDT4Extend()
	extend.domain = getAttribute(attrib, 'domain')
	extend.entity = getAttribute(attrib, 'entity')
	if isinstance(lastElem, SDT4ProductClass): # for ProductClass
		lastElem.extendDevice = extend
	else: # normal extend
		lastElem.extend = extend
	elementStack.append(extend)


def handleImg(attrib, lastElem, elementStack):
	img = SDT4DocIMG()
	img.doc = lastElem.doc
	img.startImage(getAttribute(attrib, 'src'))
	elementStack.append(img)


def handleImgCaption(attrib, lastElem, elementStack):
	caption = SDT4DocCaption()
	caption.doc = lastElem.doc
	elementStack.append(caption)


def handleInclude(attrib, lastElem, elementStack):
	# Unfortunately, there are two "include" element types to handle
	if isinstance(lastElem, SDT4Extend):
		include = SDT4ExtendInclude()
		include.name = getAttribute(attrib, 'name')
		include.type = getAttribute(attrib, 'type')
		lastElem.excludes.append(include)
	else:
		include = SDT4Include()
		include.parse = getAttribute(attrib, 'parse')
		include.href = getAttribute(attrib, 'href')
		lastElem.includes.append(include)



def handleModuleClass(attrib, lastElem, elementStack):
	mc = SDT4ModuleClass()
	mc.name = getAttribute(attrib, 'name')
	mc.semanticURI = getAttribute(attrib, 'semanticURI')
	mc.minOccurs = getAttribute(attrib, 'minOccurs')
	mc.maxOccurs = getAttribute(attrib, 'maxOccurs')
	lastElem.moduleClasses.append(mc)
	elementStack.append(mc)


def handleP(attrib, lastElem, elementStack):
	p = SDT4DocP()
	p.doc = lastElem.doc
	p.startParagraph()
	elementStack.append(p)


def handleProductClass(attrib, lastElem, elementStack):
	product = SDT4ProductClass()
	product.id = getAttribute(attrib, 'name')
	product.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.productClasses.append(product)
	elementStack.append(product)


def handleProperty(attrib, lastElem, elementStack):
	prop = SDT4Property()
	prop.name = getAttribute(attrib, 'name')
	prop.optional = getAttribute(attrib, 'optional')
	prop.value = getAttribute(attrib, 'value')
	prop.semanticURI = getAttribute(attrib, 'semanticURI')
	lastElem.properties.append(prop)
	elementStack.append(prop)


def handleSimpleType(attrib, lastElem, elementStack):
	simpleType = SDT4SimpleType()
	simpleType.type = getAttribute(attrib, 'type')
	lastElem.type = simpleType
	elementStack.append(simpleType)


def handleStructType(attrib, lastElem, elementStack):
	structType = SDT4StructType()
	lastElem.type = structType
	self.elementStack.append(structType)


def handleSubDevice(attrib, lastElem, elementStack):
	subDevice = SDT4SubDevice()
	subDevice.id = getAttribute(attrib, 'id')
	subDevice.semanticURI = getAttribute(attrib, 'semanticURI')
	subDevice.minOccurs = getAttribute(attrib, 'minOccurs')
	subDevice.maxOccurs = getAttribute(attrib, 'maxOccurs')
	lastElem.subDevices.append(subDevice)
	elementStack.append(subDevice)


def handleTT(attrib, lastElem, elementStack):
	tt = SDT4DocTT()
	tt.doc = lastElem.doc
	elementStack.append(tt)


#
#	Assignment of element types and (handlerFunction, (tuple of allowed parents))
#


handlers = {
	SDT4Parser.actionTag 		: (handleAction, (SDT4ModuleClass,)),
	SDT4Parser.argTag 			: (handleArg, (SDT4Action,)),
	SDT4Parser.arrayTypeTag 	: (handleArrayType, (SDT4DataType,)),
	SDT4Parser.bTag 			: (handleB, (SDT4Doc, SDT4DocP)),
	SDT4Parser.constraintTag 	: (handleConstraint, (SDT4DataType,)),
	SDT4Parser.dataPointTag		: (handleDataPoint, (SDT4Event, SDT4ModuleClass)),
	SDT4Parser.dataTypeTag 		: (handleDataType, (SDT4Action, SDT4DataPoint, SDT4Event, SDT4Arg, SDT4StructType, SDT4ArrayType, SDT4Domain)),
	SDT4Parser.deviceClassTag 	: (handleDeviceClass, (SDT4Domain,)),
	SDT4Parser.docTag 			: (handleDoc, (SDT4Domain, SDT4ProductClass, SDT4DeviceClass, SDT4SubDevice, SDT4DataType, SDT4ModuleClass, SDT4Action, SDT4DataPoint, SDT4Event, SDT4EnumValue, SDT4Arg, SDT4Constraint, SDT4Property)),
	SDT4Parser.domainTag 		: (handleDomain, None),
	SDT4Parser.emTag 			: (handleEM, (SDT4Doc, SDT4DocP)),
	SDT4Parser.enumTypeTag 		: (handleEnumType, (SDT4DataType,)),
	SDT4Parser.enumValueTag 	: (handleEnumValue, (SDT4EnumType,)),
	SDT4Parser.eventTag 		: (handleEvent, (SDT4ModuleClass,)),
	SDT4Parser.excludeTag 		: (handleExtendExclude, (SDT4Extend,)),
	SDT4Parser.extendTag 		: (handleExtend, (SDT4ModuleClass, SDT4DataType, SDT4ProductClass, SDT4SubDevice)),
	SDT4Parser.imgTag 			: (handleImg, (SDT4Doc, SDT4DocP)),
	SDT4Parser.imgCaptionTag 	: (handleImgCaption, (SDT4DocIMG,)),
	SDT4Parser.includeTag 		: (handleInclude, (SDT4Domain, SDT4Extend)),
	SDT4Parser.moduleClassTag 	: (handleModuleClass, (SDT4Domain, SDT4ProductClass, SDT4DeviceClass, SDT4SubDevice, SDT4ProductClass)),
	SDT4Parser.pTag 			: (handleP, (SDT4Doc, SDT4DocP)),
	SDT4Parser.productClassTag	: (handleProductClass, (SDT4Domain,)),
	SDT4Parser.propertyTag		: (handleProperty, (SDT4ProductClass, SDT4DeviceClass, SDT4SubDevice, SDT4ModuleClass)),
	SDT4Parser.simpleTypeTag 	: (handleSimpleType, (SDT4DataType, SDT4Property)),
	SDT4Parser.structTypeTag	: (handleStructType, (SDT4DataType,)),
	SDT4Parser.subDeviceTag 	: (handleSubDevice, (SDT4DeviceClass, SDT4ProductClass, SDT4Domain)),
	SDT4Parser.ttTag 			: (handleTT, (SDT4Doc, SDT4DocP))
}
