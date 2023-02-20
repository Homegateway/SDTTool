#	SDT4Classes.py
#
#	SDT4 Base Classes

class SDT4Element:

	# May be overwritten by a child class
	def endElement(self):
		pass

	def getAttribute(self, attrib, attribName:str, default=None):
		if attrib is None:
			return default
		return attrib[attribName].strip() if attribName in attrib else default


#
#	Domain, Includes
#
class SDT4Domain(SDT4Element):
	_name = 'Domain'

	def __init__(self, attrib=None):
		self._version 								= '4'
		self.id 									= self.getAttribute(attrib, 'id')
		self.semanticURI 							= self.getAttribute(attrib, 'semanticURI')
		self.doc 									= None
		self.includes 								= []			# imports
		self.dataTypes:list[SDT4DataType] 			= []
		self.moduleClasses:list[SDT4ModuleClass] 	= []
		self.subDevices:list[SDT4SubDevice] 		= []
		self.deviceClasses:list[SDT4DeviceClass]	= []
		self.productClasses:list[SDT4ProductClass]	= []


class SDT4Include(SDT4Element):
	_name = 'Include'

	def __init__(self, attrib=None):
		self.parse 		= self.getAttribute(attrib, 'parse')
		self.href 		= self.getAttribute(attrib, 'href')


#	Product
class SDT4ProductClass(SDT4Element):
	_name = 'ProductClass'

	def __init__(self, attrib=None):
		self.id 			= self.getAttribute(attrib, 'name')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.doc 			= None
		self.extend 		= None
		self.properties:list[SDT4Property]		 	= []
		self.moduleClasses:list[SDT4ModuleClass] 	= []
		self.subDevices:list[SDT4SubDevice] 		= []
		self.extendDevice:list[SDT4DeviceClass] 	= None # actually an extend


#	DeviceClass
class SDT4DeviceClass(SDT4Element):
	_name = 'DeviceClass'

	def __init__(self, attrib):
		self.id 			= self.getAttribute(attrib, 'id')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.doc 			= None
		self.properties:list[SDT4Property] 			= []
		self.moduleClasses:list[SDT4ModuleClass] 	= []
		self.subDevices:list[SDT4SubDevice]			= []


#	SubDevice
class SDT4SubDevice(SDT4Element):
	_name = 'SubDevice'

	def __init__(self, attrib=None):
		self.id 			= self.getAttribute(attrib, 'id')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.minOccurs 		= self.getAttribute(attrib, 'minOccurs')
		self.maxOccurs 		= self.getAttribute(attrib, 'maxOccurs')
		self.doc 			= None
		self.extend 		= None
		self.properties:list[SDT4Property] 			= []
		self.moduleClasses:list[SDT4ModuleClass] 	= []


#	Properties
class SDT4Property(SDT4Element):
	_name = 'Property'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.optional 		= self.getAttribute(attrib, 'optional', 'false')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.doc 			= None
		self.type 			= self.getAttribute(attrib, 'type')	
		self.value 			= self.getAttribute(attrib, 'value')


#	ModuleClass
class SDT4ModuleClass(SDT4Element):
	_name = 'ModuleClass'

	def __init__(self, attrib=None):
		self.name = self.getAttribute(attrib, 'name')
		self.semanticURI = self.getAttribute(attrib, 'semanticURI')
		self.minOccurs = self.getAttribute(attrib, 'minOccurs')
		self.maxOccurs = self.getAttribute(attrib, 'maxOccurs')
		self.extend = None
		self.doc = None
		self.actions:list[SDT4Action]		= []
		self.data:list[SDT4DataPoint]		= []
		self.events:list[SDT4Event] 		= []
		self.properties:list[SDT4Property]	= []


#	Extend
class SDT4Extend(SDT4Element):
	_name = 'Extend'

	def __init__(self, attrib=None):
		self.domain 	= self.getAttribute(attrib, 'domain')
		self.entity 	= self.getAttribute(attrib, 'entity')
		self.excludes 	= []
		self.includes 	= []
		if self.domain is None or len(self.domain) == 0:
			raise SyntaxError('Extend: "domain" attribute is missing')
		if self.entity is None or len(self.entity) == 0:
			raise SyntaxError('Extend: "entity" attribute is missing')


class SDT4ExtendExclude(SDT4Element):
	_name = 'Exclude'

	def __init__(self, attrib=None):
		self.name = self.getAttribute(attrib, 'name')
		self.type = self.getAttribute(attrib, 'type', 'datapoint')


class SDT4ExtendInclude(SDT4Element):
	_name = 'Include'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.type 			= self.getAttribute(attrib, 'type', 'datapoint')


#	Action & Arg
class SDT4Action(SDT4Element):
	_name = 'Action'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.optional 		= self.getAttribute(attrib, 'optional')
		self.semanticURI	= self.getAttribute(attrib, 'semanticURI')
		self.type 			= None
		self.doc 			= None
		self.args 			= []
		self.extend 		= None		# Action does not have 'extend' but it is added here to simplify handling in templates



class SDT4Arg(SDT4Element):
	_name = 'Arg'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.optional 		= self.getAttribute(attrib, 'optional')
		self.default 		= self.getAttribute(attrib, 'default')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.type 			= None
		self.doc 			= None


#	Event
class SDT4Event(SDT4Element):
	_name = 'Event'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.optional 		= self.getAttribute(attrib, 'optional', 'false')
		self.semanticURI	= self.getAttribute(attrib, 'semanticURI')
		self.data 			= []
		self.doc 			= None

#	DataPoint
class SDT4DataPoint(SDT4Element):
	_name = 'DataPoint'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.optional 		= self.getAttribute(attrib, 'optional', 'false')
		self.writable 		= self.getAttribute(attrib, 'writable', 'true')
		self.readable 		= self.getAttribute(attrib, 'readable', 'true')
		self.eventable 		= self.getAttribute(attrib, 'eventable', 'false')
		self.default 		= self.getAttribute(attrib, 'default')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.type 			= None
		self.doc 			= None


#	DataTypes
class SDT4DataType(SDT4Element):
	_name = 'DataType'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.unitOfMeasure 	= self.getAttribute(attrib, 'unitOfMeasure')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.constraints 	= []
		self.extend 		= None
		self.type 			= None
		self.doc 			= None


class SDT4SimpleType(SDT4DataType):
	_name = 'SimpleType'

	def __init__(self, attrib=None):
		self.type = self.getAttribute(attrib, 'type')


class SDT4StructType(SDT4DataType):
	_name = 'Struct'

	def __init__(self, attrib=None):
		super().__init__(attrib)
		self.structElements = []


class SDT4ArrayType(SDT4DataType):
	_name = 'Array'

	def __init__(self, attrib=None):
		super().__init__(attrib)
		self.arrayType = None


class SDT4EnumType(SDT4DataType):
	_name = 'Enum'

	def __init__(self, attrib=None):
		super().__init__(attrib)
		self.enumValues = []


class SDT4EnumValue(SDT4Element):
	_name = 'EnumValue'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.value 			= self.getAttribute(attrib, 'value')
		self.type 			= self.getAttribute(attrib, 'type', 'integer')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.doc 			= None


class SDT4Constraint(SDT4Element):
	_name = 'Constraint'

	def __init__(self, attrib=None):
		self.name 			= self.getAttribute(attrib, 'name')
		self.type 			= self.getAttribute(attrib, 'type')
		self.value 			= self.getAttribute(attrib, 'value')
		self.semanticURI 	= self.getAttribute(attrib, 'semanticURI')
		self.doc 			= None

#
#	Doc & elements
#
class SDT4DocBase(SDT4Element):
	def __init__(self, attrib=None):
		self.doc = None
	
	def addContent(self, content):
		pass


class SDT4Doc(SDT4DocBase):
	_name = 'Doc'

	def __init__(self, attrib=None):
		self.doc = self
		self.content = ''

	def addContent(self, content):
		self.content += content


class SDT4DocTT(SDT4DocBase):
	_name = 'tt'

	def __init__(self, attrib=None):
		SDT4DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <tt>' + content + '</tt> ')


class SDT4DocEM(SDT4DocBase):
	_name = 'em'

	def __init__(self, attrib=None):
		SDT4DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <em>' + content + '</em> ')


class SDT4DocB(SDT4DocBase):
	_name = 'b'

	def __init__(self, attrib=None):
		SDT4DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent(' <b>' + content + '</b> ')


class SDT4DocP(SDT4DocBase):
	_name = 'p'

	def __init__(self, attrib=None):
		SDT4DocBase.__init__(self)

	def startParagraph(self):
		self.doc.addContent(' <p>')
	
	def addContent(self, content):
		self.doc.addContent(content)

	def endElement(self):
		self.doc.addContent('</p> ')


class SDT4DocIMG(SDT4DocBase):
	_name = 'img'

	def __init__(self, attrib=None):
		SDT4DocBase.__init__(self)

	def startImage(self, src):
		self.addContent(' <img')
		if (src != None):
			self.addContent(' src="' + src + '"')
		self.addContent('>')

	def addContent(self, content):
		self.doc.addContent(content)

	def endElement(self):
		self.doc.addContent('</img> ')


class SDT4DocCaption(SDT4DocBase):
	_name = 'caption'

	def __init__(self, attrib=None):
		SDT4DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent('<caption>' + content + '</caption>')
