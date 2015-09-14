#	SDT2Parser.py
#
#	Callback target class for the ElementTree parser to parse a SDT2

from SDT2Classes import *

class SDT2Parser:

	# Define the element tags of the SDT3

	includeTag						= 'include'
	domainTag						= 'domain'
	importsTag						= 'imports'
	modulesTag						= 'modules'
	moduleClassTag					= 'moduleclass'
	moduleTag 						= 'module'
	extendsTag						= 'extends'
	rootDevicesTag					= 'rootdevices'
	rootDeviceTag 					= 'rootdevice'
	devicesTag 						= 'devices'
	deviceTag 						= 'device'
	deviceInfoTag					= 'deviceinfo'
	deviceInfoNameTag				= 'name'
	deviceInfoVendorTag				= 'vendor'
	deviceInfoFirmwareVersionTag	= 'firmwareversion'
	deviceInfoVendorURLTag			= 'vendorurl'
	deviceInfoSerialNumberTag		= 'serialnumber'
	actionsTag						= 'actions'
	actionTag 						= 'action'
	argTag							= 'arg'
	eventsTag						= 'events'
	eventTag 						= 'event'
	dataTag							= 'data'
	dataPointTag					= 'datapoint'
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

		uri, ignore, ntag = tag[1:].partition("}")
		if (uri not in self.nameSpaces):
			self.nameSpaces.append(uri)
		ntag = ntag.lower()

		# Handle all elements 

		# Domain, includes

		if (ntag == SDT2Parser.domainTag):
			domain = SDT2Domain()
			domain.id = attrib['id'].strip() if 'id' in attrib else None
			self.elementStack.append(domain)

		elif (ntag == SDT2Parser.includeTag):
			if (isinstance(self.elementStack[-1], SDT2Domain)):
				domain = self.elementStack[-1]
				include = SDT2Include()
				include.parse = attrib['parse'].strip() if 'parse' in attrib else None
				include.href = attrib['href'].strip() if 'href' in attrib else None
				domain.includes.append(include)
			else:
				raise SyntaxError('<include> definition is only allowed in <domain> element')

		# ModulClass, Module, Extends

		elif (ntag == SDT2Parser.moduleClassTag):
			if (isinstance(self.elementStack[-1], SDT2Domain)):
				domain = self.elementStack[-1]
				module = SDT2ModuleClass()
				module.name = attrib['name'].strip() if 'name' in attrib else None
				#module.extends = attrib['extends'].strip() if 'extends' in attrib else None
				domain.modules.append(module)
				self.elementStack.append(module)
			else:
				raise SyntaxError('<ModuleClass> definition is only allowed in <Domain> element')

		elif (ntag == SDT2Parser.moduleTag):
			if (isinstance(self.elementStack[-1], SDT2RootDevice) or isinstance(self.elementStack[-1], SDT2Device)):
				device = self.elementStack[-1]
				module = SDT2Module()
				module.name = attrib['name'].strip() if 'name' in attrib else None
				#module.extends = attrib['extends'].strip() if 'extends' in attrib else None
				device.modules.append(module)
				self.elementStack.append(module)
			else:
				raise SyntaxError('<Module> definition is only allowed in <RootDevice> or <Device> element')

		elif (ntag == SDT2Parser.extendsTag):
			if (isinstance(self.elementStack[-1], SDT2Module) or isinstance(self.elementStack[-1], SDT2ModuleClass)):
				moduleClass = self.elementStack[-1]
				extends = SDT2Extends()
				extends.domain = attrib['domain'].strip() if 'domain' in attrib else None
				extends.clazz = attrib['class'].strip() if 'class' in attrib else None
				moduleClass.extends = extends
			else:
				raise SyntaxError('<extends> definition is only allowed in <Module> or <ModuleClass> element')

		# RootDevice, Device

		elif (ntag == SDT2Parser.rootDeviceTag):
			if (isinstance(self.elementStack[-1], SDT2Domain)):
				domain = self.elementStack[-1]
				rootDevice = SDT2RootDevice()
				rootDevice.id = attrib['id'].strip() if 'id' in attrib else None
				domain.rootDevices.append(rootDevice)
				self.elementStack.append(rootDevice)
			else:
				raise SyntaxError('<RootDevice> definition is only allowed in <Domain> element')

		elif (ntag == SDT2Parser.deviceTag):
			if (isinstance(self.elementStack[-1], SDT2RootDevice)):
				rootDevice = self.elementStack[-1]
				device = SDT2Device()
				device.id = attrib['id'].strip() if 'id' in attrib else None
				rootDevice.devices.append(device)
				self.elementStack.append(device)
			else:
				raise SyntaxError('<Device> definition is only allowed in <RootDevice> element')

		# Action, Arg

		elif (ntag == SDT2Parser.actionTag):
			if (isinstance(self.elementStack[-1], SDT2Module) or isinstance(self.elementStack[-1], SDT2ModuleClass)):
				moduleClass = self.elementStack[-1]
				action = SDT2Action()
				action.name = attrib['name'] if 'name' in attrib else None
				action.type = attrib['type'].strip() if 'type' in attrib else None
				moduleClass.actions.append(action)
				self.elementStack.append(action)
			else:
				raise SyntaxError('<Action> definition is only allowed in <Module> or <ModuleClass> element')

		elif (ntag == SDT2Parser.argTag):
			if (isinstance(self.elementStack[-1], SDT2Action)):
				action = self.elementStack[-1]
				arg = SDT2Arg()
				arg.name = attrib['name'].strip() if 'name' in attrib else None
				arg.type = attrib['type'].strip() if 'type' in attrib else None
				action.arg.append(arg)
			else:
				raise SyntaxError('<Arg> definition is only allowed in <Action> element')

		# Event

		elif (ntag == SDT2Parser.eventTag):
			if (isinstance(self.elementStack[-1], SDT2Module) or isinstance(self.elementStack[-1], SDT2ModuleClass)):
				moduleClass = self.elementStack[-1]
				event = SDT2Event()
				event.name = attrib['name'].strip() if 'name' in attrib else None
				moduleClass.events.append(event)
				self.elementStack.append(event)
			else:
				raise SyntaxError('<Event> definition is only allowed in <Module> or <ModuleClass> element')

		# DataPoint

		elif (ntag == SDT2Parser.dataPointTag):
			if (isinstance(self.elementStack[-1], SDT2Event) or isinstance(self.elementStack[-1], SDT2ModuleClass) or isinstance(self.elementStack[-1], SDT2Module)):
				dataPoint = SDT2DataPoint()
				dataPoint.name = attrib['name'].strip() if 'name' in attrib else None
				dataPoint.type = attrib['type'].strip() if 'type' in attrib else None
				dataPoint.writable = attrib['writable'].strip() if 'writable' in attrib else None
				dataPoint.readable = attrib['readable'].strip() if 'readable' in attrib else None
				dataPoint.eventable = attrib['eventable'].strip() if 'eventable' in attrib else None
				if (isinstance(self.elementStack[-1], SDT2Event)):
					event = self.elementStack[-1]
					event.data.append(dataPoint)
				if (isinstance(self.elementStack[-1], SDT2ModuleClass) or isinstance(self.elementStack[-1], SDT2Module)):
					module = self.elementStack[-1]
					module.data.append(dataPoint)
				self.elementStack.append(dataPoint)

			else:
				raise SyntaxError('<DataPoint> definition is only allowed in <Event>, <Module> or <ModuleClass> element')

		# DeviceInfo & elements

		elif (ntag == SDT2Parser.deviceInfoTag):
			if (isinstance(self.elementStack[-1], SDT2RootDevice) or isinstance(self.elementStack[-1], SDT2Device)):
				deviceInfo = SDT2DeviceInfo()
				if (isinstance(self.elementStack[-1], SDT2RootDevice)):
					rootDevice = self.elementStack[-1]
					rootDevice.deviceInfo = deviceInfo
				elif (isinstance(self.elementStack[-1], SDT2Device)):
					device = self.elementStack[-1]
					device.deviceInfo = deviceInfo
				self.elementStack.append(deviceInfo)
			else:
				raise SyntaxError('<DeviceInfo> definition is only allowed in <RootDevice> or <Device> element')

		# Doc & elements

		elif (ntag == SDT2Parser.docTag):
			if (isinstance(self.elementStack[-1], SDT2RootDevice) or isinstance(self.elementStack[-1], SDT2Device) or
				isinstance(self.elementStack[-1], SDT2Module) or isinstance(self.elementStack[-1], SDT2ModuleClass) or
				isinstance(self.elementStack[-1], SDT2Action) or isinstance(self.elementStack[-1], SDT2DataPoint) or
				isinstance(self.elementStack[-1], SDT2Event)
			):
				doc = SDT2Doc()
				elem = self.elementStack[-1]
				elem.doc = doc
				self.elementStack.append(doc)
			else:
				raise SyntaxError('<Doc> definition is only allowed in <RootDevice>, <Device>, <Module>' +
					'<ModuleClass>, <Action>, <DataPoint> or <Event> element')

		elif (ntag == SDT2Parser.ttTag):
			if (isinstance(self.elementStack[-1], SDT2Doc) or isinstance(self.elementStack[-1], SDT2DocP)):
				obj = self.elementStack[-1]
				tt = SDT2DocTT()
				tt.doc = obj.doc
				self.elementStack.append(tt)
			else:
				raise SyntaxError('<tt> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT2Parser.emTag):
			if (isinstance(self.elementStack[-1], SDT2Doc) or isinstance(self.elementStack[-1], SDT2DocP)):
				obj = self.elementStack[-1]
				em = SDT2DocEM()
				em.doc = obj.doc
				self.elementStack.append(em)
			else:
				raise SyntaxError('<em> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT2Parser.bTag):
			if (isinstance(self.elementStack[-1], SDT2Doc) or isinstance(self.elementStack[-1], SDT2DocP)):
				obj = self.elementStack[-1]
				b = SDT2DocB()
				b.doc = obj.doc
				self.elementStack.append(b)
			else:
				raise SyntaxError('<b> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT2Parser.pTag):
			if (isinstance(self.elementStack[-1], SDT2Doc) or isinstance(self.elementStack[-1], SDT2DocP)):
				obj = self.elementStack[-1]
				p = SDT2DocP()
				p.doc = obj.doc
				p.startParagraph()
				self.elementStack.append(p)
			else:
				raise SyntaxError('<p> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT2Parser.imgTag):
			if (isinstance(self.elementStack[-1], SDT2Doc) or isinstance(self.elementStack[-1], SDT2DocP)):
				obj = self.elementStack[-1]
				img = SDT2DocIMG()
				img.doc = obj.doc
				img.startImage(attrib['src'].strip() if 'src' in attrib else None)
				self.elementStack.append(img)
			else:
				raise SyntaxError('<img> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT2Parser.imgCaptionTag):
			if (isinstance(self.elementStack[-1], SDT2DocIMG)):
				obj = self.elementStack[-1]
				caption = SDT2DocCaption()
				caption.doc = obj.doc
				self.elementStack.append(caption)
			else:
				raise SyntaxError('<caption> definition is only allowed in <img> element')


		# Other tags to ignore / just containers

		elif (ntag == SDT2Parser.deviceInfoNameTag and isinstance(self.elementStack[-1], SDT2DeviceInfo)):
			self.elementStack.append(SDT2DeviceInfoName())
		elif (ntag == SDT2Parser.deviceInfoVendorTag and isinstance(self.elementStack[-1], SDT2DeviceInfo)):
			self.elementStack.append(SDT2DeviceInfoVendor())
		elif (ntag == SDT2Parser.deviceInfoFirmwareVersionTag and isinstance(self.elementStack[-1], SDT2DeviceInfo)):
			self.elementStack.append(SDT2DeviceInfoFirmwareVersion())
		elif (ntag == SDT2Parser.deviceInfoVendorURLTag and isinstance(self.elementStack[-1], SDT2DeviceInfo)):
			self.elementStack.append(SDT2DeviceInfoVendorURL())
		elif (ntag == SDT2Parser.deviceInfoSerialNumberTag and isinstance(self.elementStack[-1], SDT2DeviceInfo)):
			self.elementStack.append(SDT2DeviceInfoSerialNumber())

		elif (ntag == SDT2Parser.rootDevicesTag or
			  ntag == SDT2Parser.devicesTag or
			  ntag == SDT2Parser.modulesTag or
			  ntag == SDT2Parser.actionsTag or
			  ntag == SDT2Parser.eventsTag or
			  ntag == SDT2Parser.dataTag or
			  ntag == SDT2Parser.importsTag):
			pass

		else:
			# print(tag, attrib)
			pass
		

	def end(self, tag):
		uri, ignore, ntag = tag[1:].partition("}")
		ntag = ntag.lower()

		if (ntag == SDT2Parser.domainTag):
			self.domain = self.elementStack.pop()

		elif (ntag == SDT2Parser.moduleClassTag or
			  ntag == SDT2Parser.moduleTag or
			  ntag == SDT2Parser.rootDeviceTag or
			  ntag == SDT2Parser.deviceTag or
			  ntag == SDT2Parser.actionTag or
			  ntag == SDT2Parser.deviceInfoTag or
			  ntag == SDT2Parser.deviceInfoNameTag or
			  ntag == SDT2Parser.deviceInfoVendorTag or
			  ntag == SDT2Parser.deviceInfoFirmwareVersionTag or
			  ntag == SDT2Parser.deviceInfoVendorURLTag or
			  ntag == SDT2Parser.deviceInfoSerialNumberTag or
			  ntag == SDT2Parser.eventTag or
			  ntag == SDT2Parser.dataPointTag or
			  ntag == SDT2Parser.docTag or
			  ntag == SDT2Parser.ttTag or
			  ntag == SDT2Parser.emTag or 
			  ntag == SDT2Parser.bTag or 
			  ntag == SDT2Parser.imgCaptionTag):
			self.elementStack.pop()

		elif (ntag == SDT2Parser.pTag):
			obj = self.elementStack.pop()
			obj.endParagraph()
		elif (ntag == SDT2Parser.imgTag):
			obj = self.elementStack.pop()
			obj.endImage()


	def data(self, data):
		if (isinstance(self.elementStack[-1], SDT2DeviceInfoName)):
			deviceInfo = self.elementStack[-2]
			deviceInfo.name = data
		elif (isinstance(self.elementStack[-1], SDT2DeviceInfoVendor)):
			deviceInfo = self.elementStack[-2]
			deviceInfo.vendor = data
		elif (isinstance(self.elementStack[-1], SDT2DeviceInfoFirmwareVersion)):
			deviceInfo = self.elementStack[-2]
			deviceInfo.firmwareVersion = data
		elif (isinstance(self.elementStack[-1], SDT2DeviceInfoVendorURL)):
			deviceInfo = self.elementStack[-2]
			deviceInfo.vendorURL = data
		elif (isinstance(self.elementStack[-1], SDT2DeviceInfoSerialNumber)):
			deviceInfo = self.elementStack[-2]
			deviceInfo.serialNumber = data
		elif (isinstance(self.elementStack[-1], SDT2Doc)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT2DocTT)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT2DocEM)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT2DocB)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT2DocP)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT2DocIMG)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT2DocCaption)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))


	def close(self):
		pass

	def comment(self, data):
		#print('comment' + data)
		pass
