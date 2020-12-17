#	SDT4Parser.py
#
#	Callback target class for the ElementTree parser to parse a SDT4

from typing import List
from enum import Enum
from .SDT4Classes import *

class SDT4Tag(Enum):
	actionTag 			= 'action'
	actionsTag			= 'actions'
	argTag				= 'arg'
	argsTag				= 'args'
	arrayTypeTag		= 'array'
	constraintTag		= 'constraint'
	constraintsTag		= 'constraints'
	dataPointTag		= 'datapoint'
	dataTag				= 'data'
	dataTypeTag			= 'datatype'
	dataTypesTag		= 'datatypes'
	deviceClassTag		= 'deviceclass'
	deviceClassesTag	= 'deviceclasses'
	domainTag			= 'domain'
	enumTypeTag 		= 'enum'
	enumValueTag 		= 'enumvalue'
	eventTag 			= 'event'
	eventsTag			= 'events'
	excludeTag			= 'exclude'
	extendDeviceTag		= 'extenddevice'
	extendTag			= 'extend'
	importsTag			= 'imports'
	includeTag			= 'include'
	moduleClassTag		= 'moduleclass'
	moduleClassesTag	= 'moduleclasses'
	productClassTag 	= 'productclass'
	productClassesTag	= 'productclasses'
	propertiesTag		= 'properties'
	propertyTag			= 'property'
	simpleTypeTag		= 'simple'
	structTypeTag		= 'struct'
	subDeviceTag 		= 'subdevice'
	subDevicesTag 		= 'subdevices'

	# Document tags
	docTag 				= 'doc'
	ttTag				= 'tt'
	emTag				= 'em'
	bTag				= 'b'
	pTag 				= 'p'
	imgTag				= 'img'
	imgCaptionTag		= 'caption'


	def isIgnored(self):
		return self in self._ignoredTags

	def isProcessable(self):
		return self in self._handlers
	
	def handler(self):
		return self._handlers[self]
	


# Static list of ignored tags
SDT4Tag._ignoredTags = ( 	#  type: ignore
	SDT4Tag.actionsTag,
	SDT4Tag.argsTag,
	SDT4Tag.constraintsTag,
	SDT4Tag.dataTag,
	SDT4Tag.dataTypesTag,
	SDT4Tag.deviceClassesTag,
	SDT4Tag.eventsTag,
	SDT4Tag.extendDeviceTag,
	SDT4Tag.importsTag, 
	SDT4Tag.moduleClassesTag,
	SDT4Tag.productClassesTag,
	SDT4Tag.propertiesTag,
	SDT4Tag.subDevicesTag
)


class SDT4Parser:
	def __init__(self):
		self.elementStack = []
		self.nameSpaces = []
		self.domain = None

	def start(self, tag, attrib):

		# First add the name space to the list of used name spaces
		uri, _, otag = tag[1:].partition("}")
		if uri not in self.nameSpaces:
			self.nameSpaces.append(uri)
		
		try:
			ntag = SDT4Tag(otag.lower())
		except Exception:
			raise SyntaxError(self._unknownTag(otag))

		# Check non-emptyness of attributes
		for at in attrib:
			if len(attrib[at].strip()) == 0:
				raise SyntaxError(f'empty attribute: {at} for element: {tag}')

		# Handle all elements 

		# The lastElem always contains the last element on the stack and is
		# used transparently in the code below.
		lastElem = self.elementStack[-1] if len(self.elementStack) > 0 else None

		# Call the handler function for that element tag.
		# First, chech whether this is allowed for the current parent, or raise an exception

		if ntag.isProcessable():
			(func, instances) = ntag.handler()
			if instances is None or isinstance(lastElem, instances):
				func(attrib, lastElem, self.elementStack)
			else:
				raise SyntaxError(f'{otag} definition is only allowed in {[v._name for v in instances]} elements')

		# Other tags to ignore / just containers
		elif ntag.isIgnored():
			pass

		# Encountered an unknown element
		else:
			raise SyntaxError(f'Unknown Element: {tag} {attrib}')


	def end(self, tag):
		_, _, otag = tag[1:].partition("}")
		try:
			ntag = SDT4Tag(otag.lower())
		except Exception:
			raise SyntaxError(self._unknownTag(otag))
		if ntag == SDT4Tag.domainTag:
			self.domain = self.elementStack.pop() # Assign the domain to the parser as result
		elif ntag.isProcessable():
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

	
	def _unknownTag(self, tag):
		help = ''
		if tag.lower() == 'simpletype':	help = 'Do you mean "Simple"?'
		return f'unknown tag: {tag}. {help}'



def getAttribute(attrib, attribName):
	return attrib[attribName].strip() if attribName in attrib else None


#
#	Handler for each of the element types
#

def handleAction(attrib, lastElem, elementStack):
	"""	Create and add an Action.
	"""
	action = SDT4Action(attrib)
	lastElem.actions.append(action)
	elementStack.append(action)


def handleArg(attrib, lastElem, elementStack):
	"""	Create and add an Action argument.
	"""
	arg = SDT4Arg(attrib)
	lastElem.args.append(arg)
	elementStack.append(arg)


def handleArrayType(attrib, lastElem, elementStack):
	"""	Create and add an ArrayType data type.
	"""
	arrayType = SDT4ArrayType(attrib)
	lastElem.type = arrayType
	elementStack.append(arrayType)


def handleB(attrib, lastElem, elementStack):
	"""	Create and add a <b> documentation tag.
	"""
	b = SDT4DocB(attrib)
	b.doc = lastElem.doc
	elementStack.append(b)


def handleConstraint(attrib, lastElem, elementStack):
	"""	Create and add a Constraint element.
	"""
	constraint = SDT4Constraint(attrib)
	lastElem.constraints.append(constraint)
	elementStack.append(constraint)


def handleDataPoint(attrib, lastElem, elementStack):
	"""	Create and add a DataPoint element.
	"""
	dataPoint = SDT4DataPoint(attrib)
	lastElem.data.append(dataPoint)
	elementStack.append(dataPoint)


def handleDataType(attrib, lastElem, elementStack):
	"""	Create and add a DataType. Depending on the DataType the handling is a bit different.
	"""
	dataType = SDT4DataType(attrib)
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
	"""	Create and add a DeviceClass.
	"""
	device = SDT4DeviceClass(attrib)
	lastElem.deviceClasses.append(device)
	elementStack.append(device)


def handleDoc(attrib, lastElem, elementStack):
	"""	Create and add a documentation element.
	"""
	doc = SDT4Doc(attrib)
	lastElem.doc = doc
	elementStack.append(doc)


def handleDomain(attrib, lastElem, elementStack):
	"""	Create and add a Domain.
	"""
	domain = SDT4Domain(attrib)
	elementStack.append(domain)


def handleEM(attrib, lastElem, elementStack):
	"""	Create and add an <em> documentation tag.
	"""
	em = SDT4DocEM(attrib)
	em.doc = lastElem.doc
	elementStack.append(em)


def handleEnumType(attrib, lastElem, elementStack):
	"""	Create and add an Enum data type.
	"""
	enumType = SDT4EnumType(attrib)
	lastElem.type = enumType
	elementStack.append(enumType)


def handleEnumValue(attrib, lastElem, elementStack):
	"""	Create and add a EnumValue element.
	"""
	value = SDT4EnumValue(attrib)
	lastElem.enumValues.append(value)
	elementStack.append(value)


def handleEvent(attrib, lastElem, elementStack):
	"""	Create and add an Event element.
	"""
	event = SDT4Event(attrib)
	lastElem.events.append(event)
	elementStack.append(event)


def handleExtendExclude(attrib, lastElem, elementStack):
	"""	Create and add an Extends->Exclude element.
	"""
	exclude = SDT4ExtendExclude(attrib)
	lastElem.excludes.append(exclude)


def handleExtend(attrib, lastElem, elementStack):
	"""	Create and add an Extend element.
	"""
	extend = SDT4Extend(attrib)
	if isinstance(lastElem, SDT4ProductClass): # for ProductClass
		lastElem.extendDevice = extend
	else: # normal extend
		lastElem.extend = extend
	elementStack.append(extend)


def handleImg(attrib, lastElem, elementStack):
	"""	Create and add a <img> documentation tag.
	"""
	img = SDT4DocIMG(attrib)
	img.doc = lastElem.doc
	img.startImage(getAttribute(attrib, 'src'))
	elementStack.append(img)


def handleImgCaption(attrib, lastElem, elementStack):
	"""	Create and add a <caption> documentation tag.
	"""
	caption = SDT4DocCaption(attrib)
	caption.doc = lastElem.doc
	elementStack.append(caption)


def handleInclude(attrib, lastElem, elementStack):
	"""	Create and add include elements. 
		Unfortunately, there are two "include" element types to handle.
	"""
	if isinstance(lastElem, SDT4Extend):
		include = SDT4ExtendInclude(attrib)
		lastElem.includes.append(include)
		elementStack.append(include)
	else:
		include = SDT4Include(attrib)
		lastElem.includes.append(include)
		elementStack.append(include)


def handleModuleClass(attrib, lastElem, elementStack):
	"""	Create and add a ModuleClass element.
	"""
	mc = SDT4ModuleClass(attrib)
	lastElem.moduleClasses.append(mc)
	elementStack.append(mc)


def handleP(attrib, lastElem, elementStack):
	"""	Create and add a <p> documentation tag.
	"""
	p = SDT4DocP(attrib)
	p.doc = lastElem.doc
	p.startParagraph()
	elementStack.append(p)


def handleProductClass(attrib, lastElem, elementStack):
	"""	Create and add a ProductClass.
	"""
	product = SDT4ProductClass(attrib)
	lastElem.productClasses.append(product)
	elementStack.append(product)


def handleProperty(attrib, lastElem, elementStack):
	"""	Create and add a Property.
	"""
	prop = SDT4Property(attrib)
	lastElem.properties.append(prop)
	elementStack.append(prop)


def handleSimpleType(attrib, lastElem, elementStack):
	"""	Create and add a SimpleType data type element.
	"""
	simpleType = SDT4SimpleType(attrib)
	lastElem.type = simpleType
	elementStack.append(simpleType)


def handleStructType(attrib, lastElem, elementStack):
	"""	Create and add Struct data type.
	"""
	structType = SDT4StructType(attrib)
	lastElem.type = structType
	elementStack.append(structType)


def handleSubDevice(attrib, lastElem, elementStack):
	"""	Create and add a SubDevice.
	"""
	subDevice = SDT4SubDevice(attrib)
	lastElem.subDevices.append(subDevice)
	elementStack.append(subDevice)


def handleTT(attrib, lastElem, elementStack):
	"""	Create and add a <tt> documentation tag.
	"""
	tt = SDT4DocTT(attrib)
	tt.doc = lastElem.doc
	elementStack.append(tt)



# Static assignment of element types and (handlerFunction, (tuple of allowed parents))
# This only happens here bc of the function declarations above
SDT4Tag._handlers = {	#  type: ignore
	SDT4Tag.actionTag 		: (handleAction, (SDT4ModuleClass,)),
	SDT4Tag.argTag 			: (handleArg, (SDT4Action,)),
	SDT4Tag.arrayTypeTag 	: (handleArrayType, (SDT4DataType,)),
	SDT4Tag.bTag 			: (handleB, (SDT4Doc, SDT4DocP)),
	SDT4Tag.constraintTag 	: (handleConstraint, (SDT4DataType,)),
	SDT4Tag.dataPointTag	: (handleDataPoint, (SDT4Event, SDT4ModuleClass)),
	SDT4Tag.dataTypeTag 	: (handleDataType, (SDT4Action, SDT4DataPoint, SDT4Event, SDT4Arg, SDT4StructType, SDT4ArrayType, SDT4Domain)),
	SDT4Tag.deviceClassTag 	: (handleDeviceClass, (SDT4Domain)),
	SDT4Tag.docTag 			: (handleDoc, (SDT4Domain, SDT4ProductClass, SDT4DeviceClass, SDT4SubDevice, SDT4DataType, SDT4ModuleClass, SDT4Action, SDT4DataPoint, SDT4Event, SDT4EnumValue, SDT4Arg, SDT4Constraint, SDT4Property)),
	SDT4Tag.domainTag 		: (handleDomain, None),
	SDT4Tag.emTag 			: (handleEM, (SDT4Doc, SDT4DocP)),
	SDT4Tag.enumTypeTag 	: (handleEnumType, (SDT4DataType,)),
	SDT4Tag.enumValueTag 	: (handleEnumValue, (SDT4EnumType,)),
	SDT4Tag.eventTag 		: (handleEvent, (SDT4ModuleClass,)),
	SDT4Tag.excludeTag 		: (handleExtendExclude, (SDT4Extend,)),
	SDT4Tag.extendTag 		: (handleExtend, (SDT4ModuleClass, SDT4DataType, SDT4ProductClass, SDT4SubDevice)),
	SDT4Tag.imgTag 			: (handleImg, (SDT4Doc, SDT4DocP)),
	SDT4Tag.imgCaptionTag 	: (handleImgCaption, (SDT4DocIMG,)),
	SDT4Tag.includeTag 		: (handleInclude, (SDT4Domain, SDT4Extend)),
	SDT4Tag.moduleClassTag 	: (handleModuleClass, (SDT4Domain, SDT4ProductClass, SDT4DeviceClass, SDT4SubDevice)),
	SDT4Tag.pTag 			: (handleP, (SDT4Doc, SDT4DocP)),
	SDT4Tag.productClassTag	: (handleProductClass, (SDT4Domain,)),
	SDT4Tag.propertyTag		: (handleProperty, (SDT4ProductClass, SDT4DeviceClass, SDT4SubDevice, SDT4ModuleClass)),
	SDT4Tag.simpleTypeTag 	: (handleSimpleType, (SDT4DataType, SDT4Property)),
	SDT4Tag.structTypeTag	: (handleStructType, (SDT4DataType,)),
	SDT4Tag.subDeviceTag 	: (handleSubDevice, (SDT4Domain, SDT4DeviceClass, SDT4ProductClass)),
	SDT4Tag.ttTag 			: (handleTT, (SDT4Doc, SDT4DocP))
}