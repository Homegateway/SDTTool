# SDTTool
Version 0.5

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

*SDTTool* is called as follows:

	python3 sdttool.py -i anInputFile.xml 

This will read in the SDT version 2 definitions from the file *anInputFile.xml* and writes the documentation in markdown format to standard out. Writing the output to a new file can be done like this:

	python3 sdttool.py -i anInputFile.xml -o anOutputFile.md

To change the output format the option ``-of`` must be given:

	python3 sdttool.py -i anInputFile.xml -o anOutputFile.opml -of opml

This would write the documentation in the OPML format to the file *anOutputFile.opml*.

The input format can be set by the option ``-if``.  
Please note that only ``sdt2`` is supported at the moment.


	python3 sdttool.py -i anInputFile.xml -o anOutputFile.opml -of opml -if sdt2

Running the script without with the ``-h`` option or without any will present a an overview about all possible command line parameters.

### Input Formats
The following input formats are supported for the ``-if`` or ``--inputformat`` command line argument:

- **sdt2**: SDT Version 2.0.1, the default
- **sdt3**: SDT Version 3.0

### Output Formats
Output formats for documentation for the ``-of`` or ``--outputformat`` command line argument:

- **plain**: This produces a plain text representation, with indentations, of the components of the input file.
- **markdown**: Markdown is a markup language with plain text formatting syntax designed so that it can be converted to many formats. GitHub natively supports markdown as its documentation format.
- **opml**: OPML (Outline Processor Markup Language) is a simple XML format for outlines, which can be imported in various mind mapping applications.
- **sdt3**: This output format is only valid when the input format is **sdt2**. It is used to convert SDT definitions from version 2 to version 3.
- **java**: This output format is only valid for the input format **sdt3**. It generates Java interfaces and classes for the input definition. For this output format the argument ``-o`` refers to an output directory, not a single file.

### Other Arguments
- ``-i INFILE``, ``--infile INFILE``: Required argument. Specify the input file for the conversion.
- ``-o OUTFILE``, ``--outfile OUTFILE``: The output file or directory for the result. The default is stdout.
- ``--hidedetails``: Hide the details of module classes and devices when generating the documentation.
- ``--markdowntables``: Generate tables instead of the usual list output style for markdown.


## Limitations
- *SDTTool* does not validate the input XML. It is assumed that the input XML conforms to the SDT schema.

## Changelog

### Version 0.5
13.11.2015
- Added markdown export for SDT3
- Added OPML export for SDT3
- Added support to export SDT3 structure as markdown tables

### Version 0.4
29.10.2015
- Added support for converting SDT2 to SDT3 format
- Added first support for generating Java classes (from SDT3 format only)
- Added --hidedetails option to hide detailed information when generating documentation 

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


