#	SDTSVG.py
#
#	SVG Helper for SDTTool


stdHeight      =  30
stdWidth       = 200
sdtBorderSpace =  10
stdGapH        =  50
stdGapV        =  20
stdRound       =  15
stdFontSize    =  12
sdtFontSizeLine=  10
stdFontFamily  = 'sans-serif'
stdFontColor   = 'black'
stdStrokeColor = 'black'
stdStrokeWidth =   1
stdFillColor   = 'white'


class Resource(object):
	"""docstring for Resource"""
	def __init__(self, name, x=sdtBorderSpace, y=sdtBorderSpace, cardinality='1'):
		super(Resource, self).__init__()
		self.x              = x
		self.y              = y
		self.name           = name
		self.cardinality    = cardinality
		self.parent         = None
		self.children  	    = []
		self.specialization = False

	def add(self, obj):
		global stdWidth, stdHeight, stdGapH, stdGapV
		self.children.append(obj)
		obj.x = self.x + stdWidth/2 + stdGapH
		obj.y = self.y + (stdHeight + stdGapV) * len(self.children)
		obj.parent = self
		pass

	def draw(self):
		result = drawResource(self.x, self.y, self.name, self.specialization)
		if self.parent != None:
			result += drawLine(self.parent.x, self.parent.y, self.x, self.y, self.cardinality)
		for o in self.children:
			result += o.draw()
		return result

	def height(self):
		global stdHeight
		max = self.y + stdHeight + sdtBorderSpace
		if len(self.children) == 0:
			return max
		else:
			for c in self.children:
				h = c.height()
				if h > max:
					max = h
			return max

	def width(self):
		global stdWidth
		max = self.x + stdWidth + sdtBorderSpace
		if len(self.children) == 0:
			return max
		else:
			for c in self.children:
				w = c.width()
				if w > max:
					max = w
			return max

		

class Attribute(object):
	"""docstring for Attribute"""
	def __init__(self, name, x=sdtBorderSpace, y=sdtBorderSpace, cardinality='0,1'):
		super(Attribute, self).__init__()
		self.x           = x
		self.y           = y
		self.name        = name
		self.cardinality = cardinality
		self.parent      = None
	
	def draw(self):
		result = drawAttribute(self.x, self.y, self.name)
		if self.parent != None:
			result += drawLine(self.parent.x, self.parent.y, self.x, self.y, self.cardinality)
		return result

	def height(self):
		global stdHeight, sdtBorderSpace
		return self.y + stdHeight + sdtBorderSpace

	def width(self):
		global stdWidth, sdtBorderSpace
		return self.x + stdWidth + sdtBorderSpace

###############################################################################

# SVG Stuff

def svgStart(width=0, height=0, header=None):
	global stdFillColor
	result  = '<?xml version="1.0"?>\n'

	if header != None:
		result += '\n<!--\n'
		result += sanitizeText(header)
		result += '\n-->\n\n'

	if width > 0 and height > 0:
		result += '<svg height="' + str(height) + '" width="' + str(width) + '" xmlns="http://www.w3.org/2000/svg">\n'
	else:
		result += '<svg xmlns="http://www.w3.org/2000/svg">\n'
	result += '<rect width="100%" height="100%" fill="' + stdFillColor + '" />\n'
	return result


def svgFinish():
	return '</svg>\n'


def svgRect(x, y, w, h, rxy=0):
	global stdStrokeColor, stdFillColor, stdStrokeWidth
	result  = '<rect '
	result += 'x="' + str(x) + '" y="' + str(y) + '" '
	result += 'width="' + str(w) + '" height="' + str(h) + '" '
	if rxy != 0:
		result += 'rx="' + str(rxy) + '" ry="' + str(rxy) + '" '
	result += 'stroke="' + stdStrokeColor + '" fill="' + stdFillColor + '" stroke-width="' + str(stdStrokeWidth) +'"'
	result += '/>\n'
	return result


def svgText(x, y, text, anchor=None, fontsize=-1):
	global stdFontColor, stdFontFamily, stdFontSize
	if fontsize == -1:
		fontsize = stdFontSize
	result  = '<text '
	result += 'x="' + str(x) + '" y="' + str(y) + '" '
	result += 'fill="' + stdFontColor + '" '
	result += 'font-family="' + stdFontFamily + '" '
	result += 'font-size="' + str(fontsize) + '" '
	if anchor != None:
		result += 'style="text-anchor: ' + anchor + ';"'
	result += '>' + text + '</text>\n'
	return result


def svgLine(x1, y1, x2, y2, color='black'):
	global stdStrokeWidth
	result  = '<line '
	result += 'x1="' + str(x1) + '" y1="' + str(y1) + '" '
	result += 'x2="' + str(x2) + '" y2="' + str(y2) + '" '
	result += 'stroke="' + color + '" stroke-width="' + str(stdStrokeWidth) + '" '
	result += '/>\n'
	return result


def drawAttribute(x, y, text):
	global stdWidth, stdHeight, stdRound, stdFontSize
	result  = svgRect(x, y, stdWidth, stdHeight, stdRound)
	result += svgText(x+(stdWidth/2), y+((stdHeight+stdFontSize)/2-2), text, 'middle')
	return result


def drawResource(x, y, text, isSpecialization):
	global stdWidth, stdHeight, stdFontSize
	label = '[' + text + ']' if isSpecialization else '&lt;' + text + '&gt;'
	result  = svgRect(x, y, stdWidth, stdHeight)
	result += svgText(x+(stdWidth/2), y+((stdHeight+stdFontSize)/2-2), label, 'middle')
	return result



def drawLine(x1, y1, x2, y2, label):
	global sdtStrokeColor, stdFontSize

	# Draw line to parent
	xs = x1 + stdWidth/2
	ys = y1 + stdHeight
	xm = xs
	ym = y2 + stdHeight/2
	xe = x2
	ye = ym
	result  = svgLine(xs, ys, xm, ym, stdStrokeColor)
	result += svgLine(xm, ym, xe, ye, stdStrokeColor)

	# Draw cardinality
	fs = sdtFontSizeLine
	result += svgText(xe-5, ye-fs/2, label, 'end', fs)
	return result



def sanitizeText(text):
	if (text == None or len(text) == 0):
		return ''
	result = text
	result = result.replace('<', '&lt;')
	result = result.replace('>', '&gt;')
	return result