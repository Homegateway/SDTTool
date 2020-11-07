{%import "acme-ap.macros" as ac with context -%}
# resourceType, shortName, dataType, cardinality, optionalCreate, optionalUpdate, optionalDiscovery, announced
{{ ac.printModuleClasses(domain.moduleClasses) -}}
{{ ac.printSubDevices(domain.subDevices) -}}
{{ ac.printDeviceClasses(domain.deviceClasses) -}}