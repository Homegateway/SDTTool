#	SDT3Parser.py
#
#	Callback target class for the ElementTree parser to parse a SDT3

from SDT3Classes import *

class SDT3Parser:

	# Define the element tags of the SDT3

	includeTag						= 'include'
	domainTag						= 'domain'
	importsTag						= 'imports'
	modulesTag						= 'modules'
	moduleClassTag					= 'moduleclass'
	moduleTag 						= 'module'
	extendsTag						= 'extends'
	devicesTag						= 'devices'
	deviceTag 						= 'device'
	subDevicesTag 					= 'subdevices'
	subDeviceTag 					= 'subdevice'
	deviceInfosTag					= 'deviceinfos'
	deviceInfoTag 					= 'deviceinfo'
	actionsTag						= 'actions'
	actionTag 						= 'action'
	argsTag							= 'args'
	argTag							= 'arg'
	eventsTag						= 'events'
	eventTag 						= 'event'
	dataTag							= 'data'
	dataPointTag					= 'datapoint'
	simpleTypeTag					= 'simpletype'
	structTypeTag					= 'struct'
	arrayTypeTag					= 'array'



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

#		print('-- ' + tag + '\n' + str(self.elementStack))



		# First add the name space to the list of used name spaces

		uri, ignore, ntag = tag[1:].partition("}")
		if (uri not in self.nameSpaces):
			self.nameSpaces.append(uri)
		ntag = ntag.lower()

		# Handle all elements 

		# Domain, includes

		if (ntag == SDT3Parser.domainTag):
			domain = SDT3Domain()
			domain.id = attrib['id'].strip() if 'id' in attrib else None
			self.elementStack.append(domain)

		elif (ntag == SDT3Parser.includeTag):
			if (isinstance(self.elementStack[-1], SDT3Domain)):
				domain = self.elementStack[-1]
				include = SDT3Include()
				include.parse = attrib['parse'].strip() if 'parse' in attrib else None
				include.href = attrib['href'].strip() if 'href' in attrib else None
				domain.includes.append(include)
			else:
				raise SyntaxError('<include> definition is only allowed in <domain> element')


		# ModulClass, Module, Extends

		elif (ntag == SDT3Parser.moduleClassTag):
			if (isinstance(self.elementStack[-1], SDT3Domain)):
				domain = self.elementStack[-1]
				module = SDT3ModuleClass()
				module.name = attrib['name'].strip() if 'name' in attrib else None
				module.optional = attrib['optional'].strip() if 'optional' in attrib else None
				domain.modules.append(module)
				self.elementStack.append(module)
			else:
				raise SyntaxError('<ModuleClass> definition is only allowed in <Domain> element')

		elif (ntag == SDT3Parser.moduleTag):
			if (isinstance(self.elementStack[-1], SDT3Device) or isinstance(self.elementStack[-1], SDT3SubDevice)):
				device = self.elementStack[-1]
				module = SDT3Module()
				module.name = attrib['name'].strip() if 'name' in attrib else None
				module.optional = attrib['optional'].strip() if 'optional' in attrib else None
				device.modules.append(module)
				self.elementStack.append(module)
			else:
				raise SyntaxError('<Module> definition is only allowed in <RootDevice> or <Device> element')

		elif (ntag == SDT3Parser.extendsTag):
			if (isinstance(self.elementStack[-1], SDT3Module) or isinstance(self.elementStack[-1], SDT3ModuleClass)):
				moduleClass = self.elementStack[-1]
				extends = SDT3Extends()
				extends.domain = attrib['domain'].strip() if 'domain' in attrib else None
				extends.clazz = attrib['class'].strip() if 'class' in attrib else None
				moduleClass.extends = extends
			else:
				raise SyntaxError('<extends> definition is only allowed in <Module> or <ModuleClass> element')

		# Action, Arg

		elif (ntag == SDT3Parser.actionTag):
			if (isinstance(self.elementStack[-1], SDT3Module) or isinstance(self.elementStack[-1], SDT3ModuleClass)):
				moduleClass = self.elementStack[-1]
				action = SDT3Action()
				action.name = attrib['name'] if 'name' in attrib else None
				action.optional = attrib['optional'] if 'optional' in attrib else None
				moduleClass.actions.append(action)
				self.elementStack.append(action)
			else:
				raise SyntaxError('<Action> definition is only allowed in <Module> or <ModuleClass> element')

		elif (ntag == SDT3Parser.argTag):
			if (isinstance(self.elementStack[-1], SDT3Action)):
				action = self.elementStack[-1]
				arg = SDT3Arg()
				arg.name = attrib['name'].strip() if 'name' in attrib else None
				action.args.append(arg)
				self.elementStack.append(arg)
			else:
				raise SyntaxError('<Arg> definition is only allowed in <Action> element')

		# Event

		elif (ntag == SDT3Parser.eventTag):
			if (isinstance(self.elementStack[-1], SDT3Module) or isinstance(self.elementStack[-1], SDT3ModuleClass)):
				moduleClass = self.elementStack[-1]
				event = SDT3Event()
				event.name = attrib['name'].strip() if 'name' in attrib else None
				event.optional = attrib['optional'].strip() if 'optional' in attrib else None
				moduleClass.events.append(event)
				self.elementStack.append(event)
			else:
				raise SyntaxError('<Event> definition is only allowed in <Module> or <ModuleClass> element')

		# DataPoint

		elif (ntag == SDT3Parser.dataPointTag):
			if (isinstance(self.elementStack[-1], SDT3Event) or isinstance(self.elementStack[-1], SDT3ModuleClass) or isinstance(self.elementStack[-1], SDT3Module)):
				dataPoint = SDT3DataPoint()
				dataPoint.name = attrib['name'].strip() if 'name' in attrib else None
				dataPoint.optional = attrib['optional'].strip() if 'optional' in attrib else None
				dataPoint.writable = attrib['writable'].strip() if 'writable' in attrib else None
				dataPoint.readable = attrib['readable'].strip() if 'readable' in attrib else None
				dataPoint.eventable = attrib['eventable'].strip() if 'eventable' in attrib else None
				if (isinstance(self.elementStack[-1], SDT3Event)):
					event = self.elementStack[-1]
					event.data.append(dataPoint)
				if (isinstance(self.elementStack[-1], SDT3ModuleClass) or isinstance(self.elementStack[-1], SDT3Module)):
					module = self.elementStack[-1]
					module.data.append(dataPoint)
				self.elementStack.append(dataPoint)

			else:
				raise SyntaxError('<DataPoint> definition is only allowed in <Event>, <Module> or <ModuleClass> element')
	
		# Device, SubDevice

		elif (ntag == SDT3Parser.deviceTag):
			if (isinstance(self.elementStack[-1], SDT3Domain)):
				domain = self.elementStack[-1]
				device = SDT3Device()
				device.id = attrib['id'].strip() if 'id' in attrib else None
				domain.devices.append(device)
				self.elementStack.append(device)
			else:
				raise SyntaxError('<Device> definition is only allowed in <Domain> element')

		elif (ntag == SDT3Parser.subDeviceTag):
			if (isinstance(self.elementStack[-1], SDT3Device)):
				device = self.elementStack[-1]
				subDevice = SDT3SubDevice()
				subDevice.id = attrib['id'].strip() if 'id' in attrib else None
				device.subDevices.append(subDevice)
				self.elementStack.append(subDevice)
			else:
				raise SyntaxError('<SubDevice> definition is only allowed in <Device> element')

		# DeviceInfo & elements

		elif (ntag == SDT3Parser.deviceInfoTag):
			if (isinstance(self.elementStack[-1], SDT3Device) or isinstance(self.elementStack[-1], SDT3SubDevice)):
				deviceInfo = SDT3DeviceInfo()
				deviceInfo.name = attrib['name'].strip() if 'name' in attrib else None
				deviceInfo.optional = attrib['optional'].strip() if 'optional' in attrib else None

				if (isinstance(self.elementStack[-1], SDT3Device)):
					device = self.elementStack[-1]
					device.deviceInfos.append(deviceInfo)
				elif (isinstance(self.elementStack[-1], SDT3SubDevice)):
					subDevice = self.elementStack[-1]
					subDevice.deviceInfos.append(deviceInfo)
				self.elementStack.append(deviceInfo)
			else:
				raise SyntaxError('<DeviceInfo> definition is only allowed in <RootDevice> or <Device> element')


		# Simpletype

		elif (ntag == SDT3Parser.simpleTypeTag or ntag == SDT3Parser.structTypeTag or ntag == SDT3Parser.arrayTypeTag):
			if (isinstance(self.elementStack[-1], SDT3Action) or isinstance(self.elementStack[-1], SDT3DataPoint) or
				isinstance(self.elementStack[-1], SDT3Event) or isinstance(self.elementStack[-1], SDT3Arg) or
				isinstance(self.elementStack[-1], SDT3DeviceInfo) or isinstance(self.elementStack[-1], SDT3StructType) or
				isinstance(self.elementStack[-1], SDT3ArrayType)
			):
				if (ntag == SDT3Parser.simpleTypeTag):
					typeElem = SDT3SimpleType()
					typeElem.type = attrib['type'].strip() if 'type' in attrib else None
				elif (ntag == SDT3Parser.structTypeTag):
					typeElem = SDT3StructType()
				elif (ntag == SDT3Parser.arrayTypeTag):
					typeElem = SDT3ArrayType()
				typeElem.name = attrib['name'].strip() if 'name' in attrib else None
				typeElem.unitOfMeasure = attrib['unitOfMeasure'].strip() if 'unitOfMeasure' in attrib else None
				parentElem = self.elementStack[-1]
				if (isinstance(parentElem, SDT3StructType)):
					parentElem.structElements.append(typeElem)
				elif (isinstance(parentElem, SDT3ArrayType)):
					parentElem.arrayType = typeElem
				else:
					parentElem.type = typeElem
				self.elementStack.append(typeElem)
			else:
				raise SyntaxError('<DataType> definition is only allowed in <Action>, <DataPoint>, <Event>'+
					'<Arg>, <DeviceInfo>, <Struct> or <Array> element')


# TODO constraint




		# Doc & elements

		elif (ntag == SDT3Parser.docTag):
			if (isinstance(self.elementStack[-1], SDT3Device) or isinstance(self.elementStack[-1], SDT3SubDevice) or
				isinstance(self.elementStack[-1], SDT3Module) or isinstance(self.elementStack[-1], SDT3ModuleClass) or
				isinstance(self.elementStack[-1], SDT3Action) or isinstance(self.elementStack[-1], SDT3DataPoint) or
				isinstance(self.elementStack[-1], SDT3Event)  or isinstance(self.elementStack[-1], SDT3Arg) or
				isinstance(self.elementStack[-1], SDT3Constraint) or isinstance(self.elementStack[-1], SDT3DeviceInfo)
			):

# TODO Domain
				doc = SDT3Doc()
				elem = self.elementStack[-1]
				elem.doc = doc
				self.elementStack.append(doc)
			else:
				raise SyntaxError('<Doc> definition is only allowed in <RootDevice>, <Device>, <DeviceInfo>, <Module>' +
					'<ModuleClass>, <Action>, <DataPoint>, <Arg>, <Constraint> or <Event> element')

		elif (ntag == SDT3Parser.ttTag):
			if (isinstance(self.elementStack[-1], SDT3Doc) or isinstance(self.elementStack[-1], SDT3DocP)):
				obj = self.elementStack[-1]
				tt = SDT3DocTT()
				tt.doc = obj.doc
				self.elementStack.append(tt)
			else:
				raise SyntaxError('<tt> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.emTag):
			if (isinstance(self.elementStack[-1], SDT3Doc) or isinstance(self.elementStack[-1], SDT3DocP)):
				obj = self.elementStack[-1]
				em = SDT3DocEM()
				em.doc = obj.doc
				self.elementStack.append(em)
			else:
				raise SyntaxError('<em> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.bTag):
			if (isinstance(self.elementStack[-1], SDT3Doc) or isinstance(self.elementStack[-1], SDT3DocP)):
				obj = self.elementStack[-1]
				b = SDT3DocB()
				b.doc = obj.doc
				self.elementStack.append(b)
			else:
				raise SyntaxError('<b> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.pTag):
			if (isinstance(self.elementStack[-1], SDT3Doc) or isinstance(self.elementStack[-1], SDT3DocP)):
				obj = self.elementStack[-1]
				p = SDT3DocP()
				p.doc = obj.doc
				p.startParagraph()
				self.elementStack.append(p)
			else:
				raise SyntaxError('<p> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.imgTag):
			if (isinstance(self.elementStack[-1], SDT3Doc) or isinstance(self.elementStack[-1], SDT3DocP)):
				obj = self.elementStack[-1]
				img = SDT3DocIMG()
				img.doc = obj.doc
				img.startImage(attrib['src'].strip() if 'src' in attrib else None)
				self.elementStack.append(img)
			else:
				raise SyntaxError('<img> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.imgCaptionTag):
			if (isinstance(self.elementStack[-1], SDT3DocIMG)):
				obj = self.elementStack[-1]
				caption = SDT3DocCaption()
				caption.doc = obj.doc
				self.elementStack.append(caption)
			else:
				raise SyntaxError('<caption> definition is only allowed in <img> element')


		# Other tags to ignore / just containers

		elif (ntag == SDT3Parser.devicesTag or
			  ntag == SDT3Parser.subDevicesTag or
			  ntag == SDT3Parser.deviceInfosTag or
			  ntag == SDT3Parser.modulesTag or
			  ntag == SDT3Parser.actionsTag or
			  ntag == SDT3Parser.eventsTag or
			  ntag == SDT3Parser.dataTag or
			  ntag == SDT3Parser.importsTag or
			  ntag == SDT3Parser.argsTag):
			pass

		else:
			print(tag, attrib)


	def end(self, tag):
		uri, ignore, ntag = tag[1:].partition("}")
		ntag = ntag.lower()

		if (ntag == SDT3Parser.domainTag):
			self.domain = self.elementStack.pop()

		elif (ntag == SDT3Parser.moduleClassTag or
			  ntag == SDT3Parser.moduleTag or
  			  ntag == SDT3Parser.deviceTag or
			  ntag == SDT3Parser.subDeviceTag or
			  ntag == SDT3Parser.deviceInfoTag or
			  ntag == SDT3Parser.actionTag or
			  ntag == SDT3Parser.argTag or
			  ntag == SDT3Parser.eventTag or
			  ntag == SDT3Parser.dataPointTag or
			  ntag == SDT3Parser.docTag or
			  ntag == SDT3Parser.ttTag or
			  ntag == SDT3Parser.emTag or 
			  ntag == SDT3Parser.bTag or 
			  ntag == SDT3Parser.imgCaptionTag or
			  ntag == SDT3Parser.simpleTypeTag or 
			  ntag == SDT3Parser.structTypeTag or
			  ntag == SDT3Parser.arrayTypeTag
			  ):
			self.elementStack.pop()



		elif (ntag == SDT3Parser.pTag):
			obj = self.elementStack.pop()
			obj.endParagraph()
		elif (ntag == SDT3Parser.imgTag):
			obj = self.elementStack.pop()
			obj.endImage()


	def data(self, data):
		if (isinstance(self.elementStack[-1], SDT3Doc)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT3DocTT)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT3DocEM)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT3DocB)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT3DocP)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT3DocIMG)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))
		elif (isinstance(self.elementStack[-1], SDT3DocCaption)):
			obj = self.elementStack[-1]
			obj.addContent(' '.join(data.split()))


	def close(self):
		pass


	def comment(self, data):
		pass

