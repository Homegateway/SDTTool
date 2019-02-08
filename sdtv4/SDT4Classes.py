#	SDT4Classes.py
#
#	SDT4 Base Classes

class SDT4Element:
	pass


#
#	Domain, Includes
#

class SDT4Domain(SDT4Element):
	def __init__(self):
		self._version = '4'
		self.id = None
		self.semanticURI = None
		self.doc = None
		self.includes = []
		self.moduleClasses = []
		self.deviceClasses = []
		self.products = []			# TODO

class SDT4Include(SDT4Element):
	def __init__(self):
		self.parse = None
		self.href = None


#
#	DeviceClass
#

class SDT4DeviceClass(SDT4Element):
	def __init__(self):
		self.id = None
		self.semanticURI = None
		self.doc = None
		self.moduleClasses = []
		self.subDevices = []
		self.properties = []


#
#	SubDevice
#

class SDT4SubDevice(SDT4Element):
	def __init__(self):
		self.id = None
		self.semanticURI = None
		self.doc = None
		self.moduleClasses = []
		self.properties = []

#
#	Properties
#

class SDT4Property(SDT4Element):
	def __init__(self):
		self.name = None
		self.optional = 'false'
		self.semanticURI = None
		self.doc = None
		self.type = None	# This is always a simpleType
		self.value = None

#
#	ModuleClass
#	extends
#

class SDT4ModuleClass(SDT4Element):
	def __init__(self):
		self.name = None
		self.optional = 'false'
		self.semanticURI = None
		self.extends = None
		self.doc = None
		self.actions = []
		self.data = []
		self.events = []
		self.properties = []


class SDT4Extends(SDT4Element):
	def __init__(self):
		self.domain = None
		self.clazz = None
		self.excludes = []
		self.includes = []


class SDT4Exclude(SDT4Element):
	def __init__(self):
		self.name = None
		self.type = 'datapoint'


class SDT4Include(SDT4Element):		# TODO
	def __init__(self):
		self.name = None
		self.type = 'datapoint'

#
#	Action & Arg
#

class SDT4Action(SDT4Element):
	def __init__(self):
		self.name = None
		self.optional = None
		self.semanticURI = None
		self.type = None
		self.doc = None
		self.args = []


class SDT4Arg(SDT4Element):
	def __init__(self):
		self.name = None
		self.type = None
		self.semanticURI = None
		self.doc = None
		# TODO default
		# TODO optional

#
#	Event
#

class SDT4Event(SDT4Element):
	def __init__(self):
		self.name = None
		self.optional = 'false'
		self.semanticURI = None
		self.data = []
		self.doc = None

#
#	DataPoint
#

class SDT4DataPoint(SDT4Element):
	def __init__(self):
		self.name = None
		self.optional = 'false'
		self.type = None
		self.writable = 'true'
		self.readable = 'true'
		self.eventable = 'false'
		self.doc = None
		# TODO default


#
#	DataTypes
#

class SDT4DataType(SDT4Element):
	def __init__(self):
		self.name = None
		self.unitOfMeasure = None
		self.semanticURI = None
		self.constraints = []
		self.type = None
		self.doc = None


class SDT4SimpleType(SDT4DataType):
	def __init__(self):
		self.type = None


class SDT4StructType(SDT4DataType):
	def __init__(self):
		SDT4DataType.__init__(self)
		self.structElements = []


class SDT4ArrayType(SDT4DataType):
	def __init__(self):
		SDT4DataType.__init__(self)
		self.arrayType = None


class SDT4EnumType(SDT4DataType):
	def __init__(self):
		SDT4DataType.__init__(self)
		self.enumValues = []


class SDT4EnumValue(SDT4Element):
	def __init__(self):
		self.name = None
		self.value = None
		self.type = 'integer'
		self.semanticURI = None
		self.doc = None


class SDT4Constraint(SDT4Element):
	def __init__(self):
		SDT3DataType.__init__(self)
		self.name = None
		self.type = None
		self.value = None
		self.semanticURI = None
		self.doc = None

#
#	Doc
#

class SDT4DocBase(SDT4Element):
	def __init__(self):
		self.doc = None
	
	def addContent(self, content):
		pass


class SDT4Doc(SDT4DocBase):
	def __init__(self):
		self.doc = self
		self.content = ''

	def addContent(self, content):
		self.content += content


class SDT4DocTT(SDT4DocBase):
	def __init__(self):
		SDT4DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <tt>' + content + '</tt> ')


class SDT4DocEM(SDT4DocBase):
	def __init__(self):
		SDT4DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <em>' + content + '</em> ')


class SDT4DocB(SDT4DocBase):
	def __init__(self):
		SDT4DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent(' <b>' + content + '</b> ')


class SDT4DocP(SDT4DocBase):
	def __init__(self):
		SDT4DocBase.__init__(self)

	def startParagraph(self):
		self.doc.addContent(' <p>')
	
	def addContent(self, content):
		self.doc.addContent(content)

	def endParagraph(self):
		self.doc.addContent('</p> ')


class SDT4DocIMG(SDT4DocBase):
	def __init__(self):
		SDT4DocBase.__init__(self)

	def startImage(self, src):
		self.addContent(' <img')
		if (src != None):
			self.addContent(' src="' + src + '"')
		self.addContent('>')

	def addContent(self, content):
		self.doc.addContent(content)

	def endImage(self):
		self.doc.addContent('</img> ')


class SDT4DocCaption(SDT4DocBase):
	def __init__(self):
		SDT4DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent('<caption>' + content + '</caption>')

