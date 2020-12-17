#	SDT4oneM2MHelper.py
#
#	Helpers for oneM2M special cases

from .SDT4Classes import *



def prepare4OneM2M(domain):
	_prepareSubDevices(domain.subDevices)
	_prepareDeviceClasses(domain.deviceClasses)
	_prepareModuleClasses(domain.moduleClasses)
	_prepareProductClasses(domain.productClasses)


def _prepareProductClasses(productClasses):
	for pc in productClasses:
		_prepareModuleClasses(pc.moduleClasses)
		_prepareSubDevices(pc.subDevices)


def _prepareDeviceClasses(deviceClasses):
	for dc in deviceClasses:
		_prepareModuleClasses(dc.moduleClasses)
		_prepareSubDevices(dc.subDevices)


def _prepareSubDevices(subDevices):
	for sd in subDevices:
		_prepareModuleClasses(sd.moduleClasses)


def _prepareModuleClasses(moduleClasses):
	for mc in moduleClasses:
		mc.data.insert(0, _createDataPoint('dataGenerationTime', 'datetime', True))
		_prepareActions(mc.actions
		
		)

def _prepareActions(actions):
	for action in actions:	# Add dataGenerationTime to Actions as well
		action.args.insert(0, _createDataPoint('dataGenerationTime', 'datetime', True))
		# Add result if the action has a data type
		if action.type is not None:
			action.args.append(_createDataPoint('result', action.type.type.type, False))


def _createDataPoint(name:str, tpe:str, optional:bool):
	dp 					= SDT4DataPoint(None)
	dp.name 			= name
	dp.optional 		= 'true' if optional else 'false'
	dp.type				= SDT4DataType()
	dp.type.type	 	= SDT4SimpleType()
	dp.type.type.type 	= tpe
	return dp
