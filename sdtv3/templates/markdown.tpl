{%import "markdown.macros" as md with context -%}
# Domain "{{ domain.id }}"
{% if not hideDetails %}
{{ md.doc(domain.doc) }}
{% endif %}
{{ md.printIncludes(domain.includes) }}
{{ md.printModules(domain.modules, True) }}
{{ md.printDevices(domain.devices) }}
{{ md.printLicense(license)}}

