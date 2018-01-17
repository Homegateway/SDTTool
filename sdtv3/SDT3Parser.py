#	SDT3Parser.py
#
#	Callback target class for the ElementTree parser to parse a SDT3

from .SDT3Classes import *

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
	propertiesTag					= 'properties'
	propertyTag						= 'property'
	actionsTag						= 'actions'
	actionTag 						= 'action'
	argsTag							= 'args'
	argTag							= 'arg'
	eventsTag						= 'events'
	eventTag 						= 'event'
	dataTag							= 'data'
	dataPointTag					= 'datapoint'
	dataTypeTag						= 'datatype'
	simpleTypeTag					= 'simpletype'
	structTypeTag					= 'struct'
	arrayTypeTag					= 'array'
	constraintsTag					= 'constraints'
	constraintTag					= 'constraint'



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

		# Check non-emptyness of attributes
		for at in attrib:
			value = attrib[at].strip()
			if len(value) == 0:
				raise SyntaxError('empty attribute: ' + at + ' for element ' + tag)


		# Handle all elements 

		# The lastElem always contains the last element on the stack and is
		# used transparently in the code below.
		if (len(self.elementStack) > 0):
			lastElem = self.elementStack[-1]
			#print(lastElem)

		# Domain, includes

		if (ntag == SDT3Parser.domainTag):
			self.domain = SDT3Domain()
			self.domain.id = attrib['id'].strip() if 'id' in attrib else None
			self.elementStack.append(self.domain)

		elif (ntag == SDT3Parser.includeTag):
			if (isinstance(lastElem, SDT3Domain)):
				self.domain = self.elementStack[-1]
				include = SDT3Include()
				include.parse = attrib['parse'].strip() if 'parse' in attrib else None
				include.href = attrib['href'].strip() if 'href' in attrib else None
				self.domain.includes.append(include)
			else:
				raise SyntaxError('<include> definition is only allowed in <domain> element')


		# ModulClass, Module, Extends

		elif (ntag == SDT3Parser.moduleClassTag):
			if (isinstance(lastElem, SDT3Domain)):
				module = SDT3ModuleClass()
				module.name = attrib['name'].strip() if 'name' in attrib else None
				module.optional = attrib['optional'].strip() if 'optional' in attrib else None
				lastElem.modules.append(module)
				self.elementStack.append(module)
			else:
				raise SyntaxError('<ModuleClass> definition is only allowed in <Domain> element')

		elif (ntag == SDT3Parser.moduleTag):
			if (isinstance(lastElem, SDT3Device) or isinstance(lastElem, SDT3SubDevice)):
				module = SDT3Module()
				module.name = attrib['name'].strip() if 'name' in attrib else None
				module.optional = attrib['optional'].strip() if 'optional' in attrib else None
				lastElem.modules.append(module)
				self.elementStack.append(module)
			else:
				raise SyntaxError('<Module> definition is only allowed in <RootDevice> or <Device> element')

		elif (ntag == SDT3Parser.extendsTag):
			if (isinstance(lastElem, SDT3Module) or isinstance(lastElem, SDT3ModuleClass) or isinstance(lastElem, SDT3SubDevice)):
				extends = SDT3Extends()
				extends.domain = attrib['domain'].strip() if 'domain' in attrib else None
				extends.clazz = attrib['class'].strip() if 'class' in attrib else None
				lastElem.extends = extends
			else:
				raise SyntaxError('<extends> definition is only allowed in <Module> or <ModuleClass> element')

		# Action, Arg

		elif (ntag == SDT3Parser.actionTag):
			if (isinstance(lastElem, SDT3Module) or isinstance(lastElem, SDT3ModuleClass)):
				action = SDT3Action()
				action.name = attrib['name'] if 'name' in attrib else None
				action.optional = attrib['optional'] if 'optional' in attrib else None
				lastElem.actions.append(action)
				self.elementStack.append(action)
			else:
				print(self.elementStack)

				raise SyntaxError('<Action> definition is only allowed in <Module> or <ModuleClass> element')

		elif (ntag == SDT3Parser.argTag):
			if (isinstance(lastElem, SDT3Action)):
				arg = SDT3Arg()
				arg.name = attrib['name'].strip() if 'name' in attrib else None
				lastElem.args.append(arg)
				self.elementStack.append(arg)
			else:
				raise SyntaxError('<Arg> definition is only allowed in <Action> element')

		# Event

		elif (ntag == SDT3Parser.eventTag):
			if (isinstance(lastElem, SDT3Module) or isinstance(lastElem, SDT3ModuleClass)):
				event = SDT3Event()
				event.name = attrib['name'].strip() if 'name' in attrib else None
				event.optional = attrib['optional'].strip() if 'optional' in attrib else None
				lastElem.events.append(event)
				self.elementStack.append(event)
			else:
				raise SyntaxError('<Event> definition is only allowed in <Module> or <ModuleClass> element')

		# DataPoint

		elif (ntag == SDT3Parser.dataPointTag):
			if (isinstance(lastElem, SDT3Event) or isinstance(lastElem, SDT3ModuleClass) or isinstance(lastElem, SDT3Module)):
				dataPoint = SDT3DataPoint()
				dataPoint.name = attrib['name'].strip() if 'name' in attrib else None
				dataPoint.optional = attrib['optional'].strip() if 'optional' in attrib else dataPoint.optional
				dataPoint.writable = attrib['writable'].strip() if 'writable' in attrib else dataPoint.writable
				dataPoint.readable = attrib['readable'].strip() if 'readable' in attrib else dataPoint.readable
				dataPoint.eventable = attrib['eventable'].strip() if 'eventable' in attrib else dataPoint.eventable
				lastElem.data.append(dataPoint)
				self.elementStack.append(dataPoint)
			else:
				raise SyntaxError('<DataPoint> definition is only allowed in <Event>, <Module> or <ModuleClass> element')
	
		# Device, SubDevice

		elif (ntag == SDT3Parser.deviceTag):
			if (isinstance(lastElem, SDT3Domain)):
				device = SDT3Device()
				device.id = attrib['id'].strip() if 'id' in attrib else None
				lastElem.devices.append(device)
				self.elementStack.append(device)
			else:
				raise SyntaxError('<Device> definition is only allowed in <Domain> element')

		elif (ntag == SDT3Parser.subDeviceTag):
			if (isinstance(lastElem, SDT3Device)):
				subDevice = SDT3SubDevice()
				subDevice.id = attrib['id'].strip() if 'id' in attrib else None
				lastElem.subDevices.append(subDevice)
				self.elementStack.append(subDevice)
			else:
				raise SyntaxError('<SubDevice> definition is only allowed in <Device> element')

		# Property & elements

		elif (ntag == SDT3Parser.propertyTag):
			if (isinstance(lastElem, SDT3Device) or isinstance(lastElem, SDT3SubDevice)
				or isinstance(lastElem, SDT3Module) or isinstance(lastElem, SDT3ModuleClass)):
				prop = SDT3Property()
				prop.name = attrib['name'].strip() if 'name' in attrib else None
				prop.optional = attrib['optional'].strip() if 'optional' in attrib else None
				prop.value = attrib['value'].strip() if 'value' in attrib else None
				lastElem.properties.append(prop)
				self.elementStack.append(prop)
			else:
				raise SyntaxError('<Property> definition is only allowed in <Device>, <SubDevice>, <Module> or <ModuleClass> element')

		# DataType

		elif (ntag == SDT3Parser.dataTypeTag):
			if (isinstance(lastElem, SDT3Action)     or isinstance(lastElem, SDT3DataPoint) or
				isinstance(lastElem, SDT3Event)      or isinstance(lastElem, SDT3Arg) or
				isinstance(lastElem, SDT3StructType) or isinstance(lastElem, SDT3ArrayType)
			):
				dataType = SDT3DataType()
				dataType.name = attrib['name'].strip() if 'name' in attrib else None
				dataType.unitOfMeasure = attrib['unitOfMeasure'].strip() if 'unitOfMeasure' in attrib else None
				if (isinstance(lastElem, SDT3ArrayType)):
					lastElem.arrayType = dataType
				elif (isinstance(lastElem, SDT3StructType)):
					lastElem.structElements.append(dataType)
				else:
					lastElem.type = dataType
				self.elementStack.append(dataType)
			else:
				raise SyntaxError('<DataType> definition is only allowed in <Action>, <DataPoint>, <Event>'+
					'<Arg>, <DeviceInfo>, <Struct> or <Array> element')

		# SimpleType

		elif (ntag == SDT3Parser.simpleTypeTag):
			if (isinstance(lastElem, SDT3DataType) or isinstance(lastElem, SDT3Property)):
				typeElem = SDT3SimpleType()
				typeElem.type = attrib['type'].strip() if 'type' in attrib else None
				lastElem.type = typeElem
				self.elementStack.append(typeElem)
			else:
				raise SyntaxError('<SimpleType> definition is only allowed in <DataType> or <Property> element')

		# Array

		elif (ntag == SDT3Parser.arrayTypeTag):
			if (isinstance(lastElem, SDT3DataType)):
				typeElem = SDT3ArrayType()
				lastElem.type = typeElem
				self.elementStack.append(typeElem)
			else:
				raise SyntaxError('<Array> definition is only allowed in <DataType> element')

		# Struct

		elif (ntag == SDT3Parser.structTypeTag):
			if (isinstance(lastElem, SDT3DataType)):
				typeElem = SDT3StructType()
				lastElem.type = typeElem
				self.elementStack.append(typeElem)
			else:
				raise SyntaxError('<Array> definition is only allowed in <DataType> element')

		# Constraint

		elif (ntag == SDT3Parser.constraintTag):
			if (isinstance(lastElem, SDT3DataType)):
				constraint = SDT3Constraint()
				constraint.name = attrib['name'].strip() if 'name' in attrib else None
				constraint.type = attrib['type'].strip() if 'type' in attrib else None
				constraint.value = attrib['value'].strip() if 'value' in attrib else None
				lastElem.constraints.append(constraint)
				self.elementStack.append(constraint)
			else:
				raise SyntaxError('<Constraint> definition is only allowed in <DataType> element')
	
		# Doc & elements

		elif (ntag == SDT3Parser.docTag):
			if (isinstance(lastElem, SDT3Domain)     or	isinstance(lastElem, SDT3Device) or
				isinstance(lastElem, SDT3SubDevice)  or isinstance(lastElem, SDT3DataType) or
				isinstance(lastElem, SDT3Module)     or isinstance(lastElem, SDT3ModuleClass) or
				isinstance(lastElem, SDT3Action)     or isinstance(lastElem, SDT3DataPoint) or
				isinstance(lastElem, SDT3Event)      or isinstance(lastElem, SDT3Arg) or
				isinstance(lastElem, SDT3Constraint) or isinstance(lastElem, SDT3Property)
			):
				doc = SDT3Doc()
				lastElem.doc = doc
				self.elementStack.append(doc)
			else:
				raise SyntaxError('<Doc> definition is only allowed in <RootDevice>, <Device>, <Property>, <Module>' +
					'<ModuleClass>, <Action>, <DataPoint>, <Arg>, <Constraint>, <DataType> or <Event> element')

		elif (ntag == SDT3Parser.ttTag):
			if (isinstance(lastElem, SDT3Doc) or isinstance(lastElem, SDT3DocP)):
				tt = SDT3DocTT()
				tt.doc = lastElem.doc
				self.elementStack.append(tt)
			else:
				raise SyntaxError('<tt> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.emTag):
			if (isinstance(lastElem, SDT3Doc) or isinstance(lastElem, SDT3DocP)):
				em = SDT3DocEM()
				em.doc = lastElem.doc
				self.elementStack.append(em)
			else:
				raise SyntaxError('<em> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.bTag):
			if (isinstance(lastElem, SDT3Doc) or isinstance(lastElem, SDT3DocP)):
				b = SDT3DocB()
				b.doc = lastElem.doc
				self.elementStack.append(b)
			else:
				raise SyntaxError('<b> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.pTag):
			if (isinstance(lastElem, SDT3Doc) or isinstance(lastElem, SDT3DocP)):
				p = SDT3DocP()
				p.doc = lastElem.doc
				p.startParagraph()
				self.elementStack.append(p)
			else:
				raise SyntaxError('<p> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.imgTag):
			if (isinstance(lastElem, SDT3Doc) or isinstance(lastElem, SDT3DocP)):
				img = SDT3DocIMG()
				img.doc = lastElem.doc
				img.startImage(attrib['src'].strip() if 'src' in attrib else None)
				self.elementStack.append(img)
			else:
				raise SyntaxError('<img> definition is only allowed in <Doc> or <p> element')

		elif (ntag == SDT3Parser.imgCaptionTag):
			if (isinstance(lastElem, SDT3DocIMG)):
				caption = SDT3DocCaption()
				caption.doc = lastElem.doc
				self.elementStack.append(caption)
			else:
				raise SyntaxError('<caption> definition is only allowed in <img> element')


		# Other tags to ignore / just containers

		elif (ntag == SDT3Parser.devicesTag or
			  ntag == SDT3Parser.subDevicesTag or
			  ntag == SDT3Parser.propertiesTag or
			  ntag == SDT3Parser.modulesTag or
			  ntag == SDT3Parser.actionsTag or
			  ntag == SDT3Parser.eventsTag or
			  ntag == SDT3Parser.dataTag or
			  ntag == SDT3Parser.importsTag or
			  ntag == SDT3Parser.argsTag or
			  ntag == SDT3Parser.constraintsTag):
			pass

		else:
			print('*** Unknown Element: ' + tag, attrib)


	def end(self, tag):
		uri, ignore, ntag = tag[1:].partition("}")
		ntag = ntag.lower()

		if (ntag == SDT3Parser.domainTag):
			self.domain = self.elementStack.pop()

		elif (ntag == SDT3Parser.moduleClassTag or
			  ntag == SDT3Parser.moduleTag or
  			  ntag == SDT3Parser.deviceTag or
			  ntag == SDT3Parser.subDeviceTag or
			  ntag == SDT3Parser.propertyTag or
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
			  ntag == SDT3Parser.arrayTypeTag or
			  ntag == SDT3Parser.dataTypeTag or
			  ntag == SDT3Parser.constraintTag
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
			obj.addContent(' ' + ' '.join(data.split()))
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

