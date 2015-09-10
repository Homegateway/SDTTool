#	SDT2Classes.py
#
#	SDT2 Base Classes

class SDT2Element:
	pass


#
#	Domain, Includes
#

class SDT2Domain(SDT2Element):
	def __init__(self):
		self._version = '2'
		self.id = None
		self.includes = []
		self.modules = []
		self.rootDevices = []

class SDT2Include(SDT2Element):
	def __init__(self):
		self.parse = None
		self.href = None


#
#	RootDevice
#

class SDT2RootDevice(SDT2Element):
	def __init__(self):
		self.id = None
		self.doc = None
		self.modules = []
		self.devices = []
		self.deviceInfo = None


#
#	Device
#

class SDT2Device(SDT2Element):
	def __init__(self):
		self.id = None
		self.doc = None
		self.modules = []
		self.deviceInfo = None


#
#	DeviceInfo & Elements
#

class SDT2DeviceInfo(SDT2Element):
	def __init__(self):
		self.name = None
		self.vendor = None
		self.serialNumber = None
		self.vendorURL = None
		self.firmwareVersion = None
		self.doc = None

class SDT2DeviceInfoName(SDT2Element):
	pass

class SDT2DeviceInfoVendor(SDT2Element):
	pass

class SDT2DeviceInfoFirmwareVersion(SDT2Element):
	pass

class SDT2DeviceInfoVendorURL(SDT2Element):
	pass

class SDT2DeviceInfoSerialNumber(SDT2Element):
	pass


#
#	Module
#	ModuleClass
#	extends
#

class SDT2Module(SDT2Element):
	def __init__(self):
		self.name = None
		self.extends = None
		self.doc = None
		self.actions = []
		self.data = []
		self.events = []


class SDT2ModuleClass(SDT2Module):
	def __init__(self):
		SDT2Module.__init__(self)

class SDT2Extends(SDT2Element):
	def __init__(self):
		self.domain = None
		self.clazz = None


#
#	Action & Arg
#

class SDT2Action(SDT2Element):
	def __init__(self):
		self.name = None
		self.type = None
		self.doc = None
		self.arg = []


class SDT2Arg(SDT2Element):
	def __init__(self):
		self.name = None
		self.type = None


#
#	Event
#

class SDT2Event(SDT2Element):
	def __init__(self):
		self.name = None
		self.data = []
		self.doc = None


#
#	DataPoint
#

class SDT2DataPoint(SDT2Element):
	def __init__(self):
		self.name = None
		self.type = None
		self.writable = None
		self.readable = None
		self.eventable = None
		self.doc = None


#
#	Doc, tt
#

class SDT2DocBase(SDT2Element):

	def __init__(self):
		self.doc = None
	
	def addContent(self, content):
		pass

class SDT2Doc(SDT2DocBase):
	def __init__(self):
		SDT2DocBase.__init__(self)
		self.doc = self
		self.content = ''

	def addContent(self, content):
		self.content += content


class SDT2DocTT(SDT2DocBase):
	def __init__(self):
		SDT2DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <tt>' + content + '</tt> ')


class SDT2DocEM(SDT2DocBase):
	def __init__(self):
		SDT2DocBase.__init__(self)

	def addContent(self, content):
		self.doc.addContent(' <em>' + content + '</em> ')


class SDT2DocB(SDT2DocBase):
	def __init__(self):
		SDT2DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent(' <b>' + content + '</b> ')


class SDT2DocP(SDT2DocBase):
	def __init__(self):
		SDT2DocBase.__init__(self)

	def startParagraph(self):
		self.doc.addContent(' <p>')
	
	def addContent(self, content):
		self.doc.addContent(content)

	def endParagraph(self):
		self.doc.addContent('</p> ')

class SDT2DocIMG(SDT2DocBase):
	def __init__(self):
		SDT2DocBase.__init__(self)

	def startImage(self, src):
		self.addContent(' <img')
		if (src != None):
			self.addContent(' src="' + src + '"')
		self.addContent('>')

	def addContent(self, content):
		self.doc.addContent(content)

	def endImage(self):
		self.doc.addContent('</img> ')

class SDT2DocCaption(SDT2DocBase):
	def __init__(self):
		SDT2DocBase.__init__(self)
	
	def addContent(self, content):
		self.doc.addContent('<caption>' + content + '</caption>')


	