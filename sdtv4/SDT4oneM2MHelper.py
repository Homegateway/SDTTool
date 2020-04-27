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
		mc.data.insert(0, _createDPDataGenerationTime())



def _createDPDataGenerationTime():
	dp = SDT4DataPoint()
	dp.name = 'dataGenerationTime'
	dp.optional = 'true'
	dp.type = SDT4SimpleType()
	dp.type.type = SDT4SimpleType()
	dp.type.type.type = "datetime"
	return dp
