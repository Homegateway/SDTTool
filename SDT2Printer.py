#	SDT2Printer.py
#
#	Print a SDT2 in various formats


from SDT2PrintMarkdown import print2DomainMarkdown
from SDT2PrintOPML import print2DomainOPML
from SDT2PrintPlain import print2DomainPlain


def printPlain(domain):
	return print2DomainPlain(domain)

def printOPML(domain):
	return print2DomainOPML(domain)

def printMarkdown(domain):
	return print2DomainMarkdown(domain)

