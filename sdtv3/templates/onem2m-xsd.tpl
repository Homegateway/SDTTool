{% import "onem2m-xsd.macros" as xsd with context -%}
{% if instanceType(object) == 'SDT3ModuleClass' -%}
{{ xsd.renderModuleClass(object) -}}
{% elif instanceType(object) == 'SDT3Device' -%}
{{ xsd.renderDevice(object) -}}
{% if object.subDevices and object.subDevices | length > 0 -%}
{% for subDevice in object.subDevices -%}
{{ renderObject(subDevice) -}}
{% endfor -%}
{% endif -%}
{% elif instanceType(object) == 'SDT3SubDevice' -%}
{{ xsd.renderDevice(object) -}}
{% elif instanceType(object) == 'SDT3Enum' -%}
{{ xsd.renderEnum(object) -}}
{% elif instanceType(object) == 'SDT3Action' -%}
{{ xsd.renderAction(object) -}}
{% endif -%}
