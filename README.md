# SDTTool
Version 0.7

*SDTTool* is a tool to read and convert XML files that conform to the *Smart Device Template* schema definition.

## Introduction
The [Smart Device Template](https://github.com/Homegateway/SmartDeviceTemplate) (SDT) schema defined by the Home Gateway Initiative (HGI) is a format to describe concrete and abstract devices as well as capabilities, data models and functions of those devices. See [SDT Introduction](https://github.com/Homegateway/SmartDeviceTemplate/blob/master/SDT/schema3.0/docs/Introduction.md) and [SDT Components](https://github.com/Homegateway/SmartDeviceTemplate/blob/master/SDT3.0/docs/SDT_Components.md) for an introduction to the SDT.

*SDTtool* is a Python 3 script that reads SDT files and generates output in various formats. It can be used to produce documentation for the Devices and ModuleClasses of an SDT as well as to convert between different versions of the SDT.


## Installation
### Prerequisites
An installation of [Python 3](https://www.python.org/downloads/) (version 3.5 or higher) is required. For an earlier version of Python (3.2 or higher) ``pathlib`` must be installed separately (see also [https://pypi.python.org/pypi/pathlib/](https://pypi.python.org/pypi/pathlib/)

### Copying
Download the latest release of *SDTTool* and copy them into a directory of your choice.

## Usage

*SDTTool* is run as follows:

	python3 sdttool.py -i anInputFile.xml 

This will read in the SDT version 2, the default, definitions from the file *anInputFile.xml* and writes the documentation in markdown format to standard out. Writing the output to a new file can be done like this:

	python3 sdttool.py -i anInputFile.xml -o anOutputFile.md

To change the output format the option ``-of`` must be given:

	python3 sdttool.py -i anInputFile.xml -o anOutputFile.opml -of opml

This would write the documentation in the OPML format to the file *anOutputFile.opml*.

The input format can be set by the option ``-if``.  

	python3 sdttool.py -i anInputFile.xml -o anOutputFile.opml -of opml -if sdt2

It is also possible to generate Java interfaces and classes from SDT version 3 with the ``java`` output format. In this case the ``-o`` argument must point to an output directory.

	python3 SDTTool.py -i anInputFile.xml -if sdt3 -o anOutputDirectoy -of java

Running the script without with the ``-h`` option or without any argument will present a an overview about all possible command line parameters.

### Input Formats
- ``-if {sdt2,sdt3,}`` , ``--inputformat {sdt2,sdt3,}``: The input format to read. The default is *sdt3*.

The following input formats are supported for the ``-if`` or ``--inputformat`` command line argument:

- **sdt2**: SDT Version 2.0.1
- **sdt3**: SDT Version 3.0, the default

### Output Formats
- ``-of {plain,opml,markdown,sdt3,java,vorto-dsl,onem2m-svg,onem2m-xsd}``, ``--outputformat {plain,opml,markdown,sdt3,java,vorto-dsl,onem2m-svg,onem2m-xsd}``: The output format for the result. The default is *markdown*.

Output formats for documentation for the ``-of`` or ``--outputformat`` command line argument:

- **plain**: This produces a plain text representation, with indentations, of the components of the input file.
- **markdown**: Markdown is a markup language with plain text formatting syntax designed so that it can be converted to many formats. GitHub natively supports markdown as its documentation format. See also the ``--markdowntables``argument below.
- **opml**: OPML (Outline Processor Markup Language) is a simple XML format for outlines, which can be imported in various mind mapping applications.
- **sdt3**: This output format is only valid when the input format is **sdt2**. It is used to convert SDT definitions from version 2 to version 3.
- **java**: This output format is only valid for the input format **sdt3**. It generates Java interfaces and classes for the input definition. For this output format the argument ``-o`` refers to an output directory, not a single file.
- **vorto-dsl**: This output format generates files that can be used to export Device, ModuleClass and data type definitions to an [Eclipse Vorto repository](http://vorto.eclipse.org). For this output format the argument ``-o`` refers to an output directory, not a single file.
- **onem2m-svg**: This output format generates SVG files that present the structure of Devices and ModuleClass in the graphical representation format used by [oneM2M](http://onem2m.org). For this output format the argument ``-o`` refers to an output directory, not a single file.
- **onem2m-xsd**: This output format generates XSD files according to the type definions of TS-0004 of the oneM2M specifications. For this output format the argument ``-o`` refers to an output directory, not a single file. The oneM2M domain needs to be specified via the ``--domain`` argument.   
In addition to the XSD files the following files are generated as well
	- Skeleton files for enum type definitions are generated in the *hd* sub-directory.
	- Files with newly found abbreviations (``_Abbreviations.*``). One file contains a python map, the other file contains the abbreviations in CSV format. Only new abbreviations, which are not found in the file that was specified with ``--abbreviationsinfile``, are added.

### Basic Arguments
- ``-i <filename>``, ``--infile <filename>``: Required argument. Specify the input file for the conversion.
- ``-o <filename>``, ``--outfile <filename>``: The output file or directory for the result. The default is stdout.

### oneM2M specific arguments
- ``--domain <domain name>``: Specify the domain name for XSD output.
- ``--namespaceprefix <xsd prefix>``: Specify the XSD name space prefix for the model. This argument is mandatory when generating XSD and SVG.
- ``--abbreviationsinfile <filename>``: Specify the file that contains a CSV table of already existing abbreviations.
- ``--abbreviationlength <integer>``: Specify the maximum length for abbreviations. The default is *5*.
- ``--xsdtargetnamespace <URI>`` : Specify the target namespace for the oneM2M XSD.
- ``--modelversion <version number>`` : Specify the version of the model. This is used in the filenames of XSD and SVG files. "." characters are replaced with "_".

### Markdown Specific Arguments
- ``--markdowntables``: Generate tables instead of the usual list output style for markdown.

### Other Arguments
- ``--hidedetails``: Hide the details of module classes and devices when generating the documentation.
- ``--licensefile <filename>``: Add the text of the specified file as a license to the generated files.


### Configuration Files
Sometimes the number of command line arguments can get pretty big. Therefore, it is possible to put some or all arguments into a configuration file. This configuration file can be specified as follows

	python3 SDTTool.py @config

It is also possible to have more than one configuration file:

	python3 SDTTool.py @config1 @config2

or to mix command line arguments and configuration files:

	python3 SDTTool.py @config --markdowntables

## Limitations
- *SDTTool* does not validate the input XML. It is assumed that the input XML conforms to the SDT schema.

## Changelog

### Version 0.7
xx.XX.2016

- Export to Eclipse Vorto, first version
- First version of export to SVG in oneM2M resource format
- First version of export to oneM2M XSD
- Fixed errors in Java export
- Fixed errors in OPML export
- Improved markdown export
- Added optional reading of command line arguments from configuration file(s)
- Made SDT3 the default input format
- minor bug fixes

### Version 0.6
04.02.2016

- Improved Java export: output documentation when available, generate static variables for property names, added getter for event payload data points
- Fixed error when exporting SDT2 to markdown
- Added option (``--markdowntables``) to present data points, actions, properties and more in table format

### Version 0.5
13.11.2015

- Added markdown export for SDT3
- Added OPML export for SDT3
- Added support to export SDT3 structure as markdown tables

See the [Changelog](CHANGELOG.md) for all changes.

## Copyright and License
Copyright (c) 2015 Deutsche Telekom AG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


