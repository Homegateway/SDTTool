# Changelog

## Version 0.9
xx.xx.2023

- Added support for SDT version 4: Conversion from SDT3 to SDT4, markdown, and oneM2M XSD & SVG. 
- Support for namespace prefix in markdown generation.
- Added some short versions for command line arguments.
- Small fixes and improvements. Code restructuring.
- Added support for rich colour output.
- Added new CSV table output of all names, short names, and where they occur in.

## Version 0.8
15.05.2018

- Added *--modelversion** 
- Adopted to new naming scheme for oneM2M XSD and SVG files
- Various fixes for XSD schemas. Support oneM2M Version 2 XSD
- Refactored script directory structure
- Added *--markdownpagebreak* option
- Added first support to generate Swagger files for ModuleClasses and Devices. Not complete yet. 
- Added *-of swagger* option
- Beautified OPML/Mindmanager output
- First work on replacing the hand-crafted output modules by a templating engine (Jinja2, [](http://jinja.pocoo.org/)).
- Profided first templates for markdown and oneM2M XSD.
- Added support for oneM2M release R3
 

## Version 0.7
09.04.2016

- Export to Eclipse Vorto, first version
- First version of export to SVG in oneM2M resource format
- First version of export to oneM2M XSD
- First version of abbreviation support (for oneM2M)
- Fixed errors in Java export
- Fixed errors in OPML export
- Improved markdown export
- Added optional reading of command line arguments from configuration file(s)
- Made SDT3 the default input format
- minor bug fixes


## Version 0.6
04.02.2016

- Improved Java export: output documentation when available, generate static variables for property names, added getter for event payload data points
- Fixed error when exporting SDT2 to markdown
- Added option (``--markdowntables``) to present data points, actions, properties and more in table format

## Version 0.5
13.11.2015

- Added markdown export for SDT3
- Added OPML export for SDT3
- Added support to export SDT3 structure as markdown tables

## Version 0.4
29.10.2015

- Added support for converting SDT2 to SDT3 format
- Added first support for generating Java classes (from SDT3 format only)
- Added --hidedetails option to hide detailed information when generating documentation 

## Version 0.3
03.09.2015

- Fixed duplicate output of DataPoints

## Version 0.2
22.08.2015

- Improved Markdown output for DeviceInfo

## Version 0.1
11.08.2015

- Initial version of SDTTool. 
- Read XML SDT 2.0.1
- Write plain text, markdown and OPML
