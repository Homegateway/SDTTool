#	SDT4Classes.py
#
#	SDT4 Base Classes

class SDT4Element:

	# May be overwritten by a child class
	def endElement(self):
		pass


#
#	Domain, Includes
#
class SDT4Domain(SDT4Element):
	_name = 'Domain'

	def __init__(self):
		self._version = '4'
		self.id = None
		self.semanticURI = None
		self.doc = None
		self.includes = []			# imports
		self.dataTypes = []
		self.moduleClasses = []
		self.subDevices = []
		self.deviceClasses = []
		self.productClasses = []


class SDT4Include(SDT4Element):
	_name = 'Include'

	def __init__(self):
		self.parse = None
		self.href = None


#	Product
class SDT4ProductClass(SDT4Element):
	_name = 'ProductClass'

	def __init__(self):
		self.id = None
		self.semanticURI = None
		self.doc = None
		self.extend = None
		self.properties = []
		self.moduleClasses = []
		self.subDevices = []
		self.extendDevice = None # actually an extend


#	DeviceClass
class SDT4DeviceClass(SDT4Element):
	_name = 'DeviceClass'

	def __init__(self):
		self.id = None
		self.semanticURI = None
		self.doc = None
		self.properties = []
		self.moduleClasses = []
		self.subDevices = []


#	SubDevice
class SDT4SubDevice(SDT4Element):
	_name = 'SubDevice'

	def __init__(self):
		self.id = None
		self.semanticURI = None
		self.minOccurs = None
		self.maxOccurs = None
		self.doc = None
		self.extend = None
		self.properties = []
		self.moduleClasses = []


#	Properties
class SDT4Property(SDT4Element):
	_name = 'Property'

	def __init__(self):
		self.name = None
		self.optional = 'false'
		self.semanticURI = None
		self.doc = None
		self.type = None	# This is always a simpleType
		self.value = None


#	ModuleClass
class SDT4ModuleClass(SDT4Element):
	_name = 'ModuleClass'

	def __init__(self):
		self.name = None
		self.semanticURI = None
		self.minOccurs = None
		self.maxOccurs = None
		self.extend = None
		self.doc = None
		self.actions = []
		self.data = []
		self.events = []
		self.properties = []


#	Extend
class SDT4Extend(SDT4Element):
	_name = 'Extend'

	def __init__(self):
		self.domain = None
		self.entity = None
		self.excludes = []
		self.includes = []


class SDT4ExtendExclude(SDT4Element):
	_name = 'Exclude'

	def __init__(self):
		self.name = None
		self.type = 'datapoint'


class SDT4ExtendInclude(SDT4Element):
	_name = 'Include'

	def __init__(self):
		self.name = None
		self.type = 'datapoint'


#	Action & Arg
class SDT4Action(SDT4Element):
	_name = 'Action'

	def __init__(self):
		self.name = None
		self.optional = None
		self.semanticURI = None
		self.type = None
		self.doc = None
		self.args = []


class SDT4Arg(SDT4Element):
	_name = 'Arg'

	def __init__(self):
		self.name = None
		self.optional = None
		self.default = None
		self.type = None
		self.semanticURI = None
		self.doc = None


#	Event
class SDT4Event(SDT4Element):
	_name = 'Event'

	def __init__(self):
		self.name = None
		self.optional = 'false'
		self.semanticURI = None
		self.data = []
		self.doc = None

#	DataPoint
class SDT4DataPoint(SDT4Element):
	_name = 'DataPoint'

	def __init__(self):
		self.name = None
		self.optional = 'false'
		self.type = None
		self.writable = 'true'
		self.readable = 'true'
		self.eventable = 'false'
		self.default = None
		self.semanticURI = None
		self.doc = None


#	DataTypes
class SDT4DataType(SDT4Element):
	_name = 'DataType'

	def __init__(self):
		self.name = None
		self.unitOfMeasure = None
		self.semanticURI = None
		self.constraints = []
		self.extend = None
		self.type = None
		self.doc = None


class SDT4SimpleType(SDT4DataType):
	_name = 'SimpleType'

	def __init__(self):
		self.type = None


class SDT4StructType(SDT4DataType):
	_name = 'Struct'

	def __init__(self):
		super().__init__()
		self.structElements = []


class SDT4ArrayType(SDT4DataType):
	_name = 'Array'

	def __init__(self):
		super().__init__()
		self.arrayType = None


class SDT4EnumType(SDT4DataType):
	_name = 'Enum'

	def __init__(self):
		super().__init__()
		self.enumValues = []


class SDT4EnumValue(SDT4Element):
	_name = 'EnumValue'

	def __init__(self):
		self.name = None
		self.value = None
		self.type = 'integer'
		self.semanticURI = None
		self.doc = None


class SDT4Constraint(SDT4Element):
	_name = 'Constraint'

	def __init__(self):
		SDT3DataType.__init__(self)
		self.name = None
		self.type = None
		self.value = None
		self.semanticURI = None
		self.doc = None

#
#	Doc & elements
#
class SDT4DocBase(SDT4Element):
	def __init__(self):
		self.doc = None
	
	def addContent(self, content):
		pass


class SDT4Doc(SDT4DocBase):
	_name = 'Doc'

	def __init__(self):
		self.doc = self
		self.content = ''

	def addContent(self, content):
		self.content += content


class SDT4DocTT(SDT4DocBase):
	_name = 'tt'

	def __init__(self):
		SDT4DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <tt>' + content + '</tt> ')


class SDT4DocEM(SDT4DocBase):
	_name = 'em'

	def __init__(self):
		SDT4DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <em>' + content + '</em> ')


class SDT4DocB(SDT4DocBase):
	_name = 'b'

	def __init__(self):
		SDT4DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent(' <b>' + content + '</b> ')


class SDT4DocP(SDT4DocBase):
	_name = 'p'

	def __init__(self):
		SDT4DocBase.__init__(self)

	def startParagraph(self):
		self.doc.addContent(' <p>')
	
	def addContent(self, content):
		self.doc.addContent(content)

	def endElement(self):
		self.doc.addContent('</p> ')


class SDT4DocIMG(SDT4DocBase):
	_name = 'img'

	def __init__(self):
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

	def __init__(self):
		SDT4DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent('<caption>' + content + '</caption>')
