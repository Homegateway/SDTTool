#	SDT3Classes.py
#
#	SDT3 Base Classes

class SDT3Element:
	pass


#
#	Domain, Includes
#

class SDT3Domain(SDT3Element):
	def __init__(self):
		self._version = '3'
		self.id = None
		self.doc = None
		self.includes = []
		self.modules = []
		self.devices = []

class SDT3Include(SDT3Element):
	def __init__(self):
		self.parse = None
		self.href = None


#
#	Device
#

class SDT3Device(SDT3Element):
	def __init__(self):
		self.id = None
		self.doc = None
		self.modules = []
		self.subDevices = []
		self.properties = []


#
#	SubDevice
#

class SDT3SubDevice(SDT3Element):
	def __init__(self):
		self.id = None
		self.doc = None
		self.modules = []
		self.properties = []

#
#	Properties
#

class SDT3Properties(SDT3Element):
	def __init__(self):
		self.name = None
		self.optional = None
		self.doc = None
		self.type = None
		self.value = None

#
#	Module
#	ModuleClass
#	extends
#

class SDT3Module(SDT3Element):
	def __init__(self):
		self.name = None
		self.optional = None
		self.extends = None
		self.doc = None
		self.actions = []
		self.data = []
		self.events = []
		self.properties = []



class SDT3ModuleClass(SDT3Module):
	def __init__(self):
		SDT3Module.__init__(self)

class SDT3Extends(SDT3Element):
	def __init__(self):
		self.domain = None
		self.clazz = None


#
#	Action & Arg
#

class SDT3Action(SDT3Element):
	def __init__(self):
		self.name = None
		self.optional = None
		self.type = None
		self.doc = None
		self.args = []


class SDT3Arg(SDT3Element):
	def __init__(self):
		self.name = None
		self.type = None
		self.doc = None

#
#	Event
#

class SDT3Event(SDT3Element):
	def __init__(self):
		self.name = None
		self.optional = None
		self.data = []
		self.doc = None

#
#	DataPoint
#

class SDT3DataPoint(SDT3Element):
	def __init__(self):
		self.name = None
		self.optional = None
		self.type = None
		self.writable = 'true'
		self.readable = 'true'
		self.eventable = 'false'
		self.doc = None


#
#	DataTypes
#

class SDT3DataType(SDT3Element):
	def __init__(self):
		self.name = None
		self.unitOfMeasure = None
		self.constraints = []
		self.type = None
		self.doc = None

class SDT3SimpleType(SDT3Element):
	def __init__(self):
		self.type = None

class SDT3StructType(SDT3Element):
	def __init__(self):
		self.structElements = []

class SDT3ArrayType(SDT3Element):
	def __init__(self):
		self.arrayType = None


class SDT3Constraint(SDT3Element):
	def __init__(self):
		self.name = None
		self.type = None
		self.value = None
		self.doc = None

#
#	Doc
#

class SDT3DocBase(SDT3Element):
	def __init__(self):
		self.doc = None
	
	def addContent(self, content):
		pass

class SDT3Doc(SDT3DocBase):
	def __init__(self):
		SDT3DocBase.__init__(self)
		self.doc = self
		self.content = ''

	def addContent(self, content):
		self.content += content

class SDT3DocTT(SDT3DocBase):
	def __init__(self):
		SDT3DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <tt>' + content + '</tt> ')

class SDT3DocEM(SDT3DocBase):
	def __init__(self):
		SDT3DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <em>' + content + '</em> ')

class SDT3DocB(SDT3DocBase):
	def __init__(self):
		SDT3DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent(' <b>' + content + '</b> ')

class SDT3DocP(SDT3DocBase):
	def __init__(self):
		SDT3DocBase.__init__(self)

	def startParagraph(self):
		self.doc.addContent(' <p>')
	
	def addContent(self, content):
		self.doc.addContent(content)

	def endParagraph(self):
		self.doc.addContent('</p> ')

class SDT3DocIMG(SDT3DocBase):
	def __init__(self):
		SDT3DocBase.__init__(self)

	def startImage(self, src):
		self.addContent(' <img')
		if (src != None):
			self.addContent(' src="' + src + '"')
		self.addContent('>')

	def addContent(self, content):
		self.doc.addContent(content)

	def endImage(self):
		self.doc.addContent('</img> ')

class SDT3DocCaption(SDT3DocBase):
	def __init__(self):
		SDT3DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent('<caption>' + content + '</caption>')

