"""

PIDDLE (Plug-In Drawing, Does Little Else)
2D Plug-In Drawing System

Magnus Lie Hetland
Andy Robinson
Joseph J. Strout
and others

February-March 1999

On coordinates: units are Big Points, approximately 1/72 inch.
The origin is at the top-left, and coordinates increase down (y)
and to the right (x).

"""
from __future__ import annotations
import rdkix.sping.colors
from rdkix.sping.colors import Color
from rdkix.sping.colors import HexColor
__all__ = ['AffineMatrix', 'Canvas', 'Color', 'Font', 'HexColor', 'StateSaver', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'cm', 'coral', 'cornflower', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'figureArc', 'figureCurve', 'figureLine', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'getFileObject', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'inch', 'indianred', 'indigo', 'ivory', 'keyBksp', 'keyClear', 'keyDel', 'keyDown', 'keyEnd', 'keyHome', 'keyLeft', 'keyPgDn', 'keyPgUp', 'keyRight', 'keyTab', 'keyUp', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'modControl', 'modShift', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'transparent', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
class AffineMatrix:
    def __init__(self, init = None):
        ...
    def rotate(self, theta):
        """
        counter clockwise rotation in standard SVG/libart coordinate system
        """
    def scale(self, sx, sy):
        ...
    def translate(self, tx, ty):
        ...
class Canvas:
    """
    This is the base class for a drawing canvas.  The 'plug-in renderers'
              we speak of are really just classes derived from this one, which implement
              the various drawing methods.
    """
    def __init__(self, size = (300, 300), name = 'PIDDLE'):
        """
        Initialize the canvas, and set default drawing parameters.
                            Derived classes should be sure to call this method.
        """
    def arcPoints(self, x1, y1, x2, y2, startAng = 0, extent = 360):
        """
        Return a list of points approximating the given arc.
        """
    def canUpdate(self):
        """
        Returns 1 if the drawing can be meaningfully updated over time                     (e.g., screen graphics), 0 otherwise (e.g., drawing to a file).
        """
    def clear(self):
        """
        Call this to clear and reset the graphics context.
        """
    def curvePoints(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        Return a list of points approximating the given Bezier curve.
        """
    def drawArc(self, x1, y1, x2, y2, startAng = 0, extent = 360, edgeColor = None, edgeWidth = None, fillColor = None, dash = None, **kwargs):
        """
        Draw a partial ellipse inscribed within the rectangle x1,y1,x2,y2,                     starting at startAng degrees and covering extent degrees.   Angles                     start with 0 to the right (+x) and increase counter-clockwise.                     These should have x1<x2 and y1<y2.
        """
    def drawCurve(self, x1, y1, x2, y2, x3, y3, x4, y4, edgeColor = None, edgeWidth = None, fillColor = None, closed = 0, dash = None, **kwargs):
        """
        Draw a Bezier curve with control points x1,y1 to x4,y4.
        """
    def drawEllipse(self, x1, y1, x2, y2, edgeColor = None, edgeWidth = None, fillColor = None, dash = None, **kwargs):
        """
        Draw an orthogonal ellipse inscribed within the rectangle x1,y1,x2,y2.                     These should have x1<x2 and y1<y2.
        """
    def drawFigure(self, partList, edgeColor = None, edgeWidth = None, fillColor = None, closed = 0, dash = None, **kwargs):
        """
        drawFigure(partList) -- draws a complex figure
                            partlist: a set of lines, curves, and arcs defined by a tuple whose
                                              first element is one of figureLine, figureArc, figureCurve
                                              and whose remaining 4, 6, or 8 elements are parameters.
        """
    def drawImage(self, image, x1, y1, x2 = None, y2 = None, **kwargs):
        """
        Draw a PIL Image into the specified rectangle.  If x2 and y2 are
                            omitted, they are calculated from the image size.
        """
    def drawLine(self, x1, y1, x2, y2, color = None, width = None, dash = None, **kwargs):
        """
        Draw a straight line between x1,y1 and x2,y2.
        """
    def drawLines(self, lineList, color = None, width = None, dash = None, **kwargs):
        """
        Draw a set of lines of uniform color and width.                      lineList: a list of (x1,y1,x2,y2) line coordinates.
        """
    def drawMultiLineString(self, s, x, y, font = None, color = None, angle = 0, **kwargs):
        """
        Breaks string into lines (on 
        , 
        , 
        
        , or 
        ), and calls drawString on each.
        """
    def drawPolygon(self, pointlist, edgeColor = None, edgeWidth = None, fillColor = None, closed = 0, dash = None, **kwargs):
        """
        drawPolygon(pointlist) -- draws a polygon
                            pointlist: a list of (x,y) tuples defining vertices
                            closed: if 1, adds an extra segment connecting the last point to the first
                            
        """
    def drawRect(self, x1, y1, x2, y2, edgeColor = None, edgeWidth = None, fillColor = None, dash = None, **kwargs):
        """
        Draw the rectangle between x1,y1, and x2,y2.                     These should have x1<x2 and y1<y2.
        """
    def drawRoundRect(self, x1, y1, x2, y2, rx = 8, ry = 8, edgeColor = None, edgeWidth = None, fillColor = None, dash = None, **kwargs):
        """
        Draw a rounded rectangle between x1,y1, and x2,y2,                     with corners inset as ellipses with x radius rx and y radius ry.                     These should have x1<x2, y1<y2, rx>0, and ry>0.
        """
    def drawString(self, s, x, y, font = None, color = None, angle = 0, **kwargs):
        """
        Draw a string starting at location x,y.
        """
    def flush(self):
        """
        Call this to indicate that any comamnds that have been issued                     but which might be buffered should be flushed to the screen
        """
    def fontAscent(self, font = None):
        """
        Find the ascent (height above base) of the given font.
        """
    def fontDescent(self, font = None):
        """
        Find the descent (extent below base) of the given font.
        """
    def fontHeight(self, font = None):
        """
        Find the height of one line of text (baseline to baseline) of the given font.
        """
    def getSize(self):
        ...
    def isInteractive(self):
        """
        Returns 1 if onClick, onOver, and onKey events are possible, 0 otherwise.
        """
    def save(self, file = None, format = None):
        """
        For backends that can be save to a file or sent to a
                            stream, create a valid file out of what's currently been
                            drawn on the canvas.  Trigger any finalization here.
                            Though some backends may allow further drawing after this call,
                            presume that this is not possible for maximum portability
        
                            file may be either a string or a file object with a write method
                                 if left as the default, the canvas's current name will be used
        
                            format may be used to specify the type of file format to use as
                                 well as any corresponding extension to use for the filename
                                 This is an optional argument and backends may ignore it if
                                 they only produce one file format.
        """
    def setInfoLine(self, s):
        """
        For interactive Canvases, displays the given string in the                     'info line' somewhere where the user can probably see it.
        """
    def stringBox(self, s, font = None):
        ...
    def stringWidth(self, s, font = None):
        """
        Return the logical width of the string if it were drawn                     in the current font (defaults to self.font).
        """
class Font:
    """
    This class represents font typeface, size, and style.
    """
    def __cmp__(self, other):
        """
        Compare two fonts to see if they're the same.
        """
    def __init__(self, size = 12, bold = 0, italic = 0, underline = 0, face = None):
        ...
    def __repr__(self):
        ...
    def __setattr__(self, name, value):
        ...
class StateSaver:
    """
    This is a little utility class for saving and restoring the
              default drawing parameters of a canvas.  To use it, add a line
              like this before changing any of the parameters:
    
                      saver = StateSaver(myCanvas)
    
              then, when "saver" goes out of scope, it will automagically
              restore the drawing parameters of myCanvas.
    """
    def __del__(self):
        ...
    def __init__(self, canvas):
        ...
def getFileObject(file, openFlags = 'wb'):
    """
    Common code for every Canvas.save() operation takes a string
              or a potential file object and assures that a valid fileobj is returned
    """
__version__: str = '1.0.0'
__version_maj_number__: str = '1.0'
__version_min_number__: str = '0'
aliceblue: rdkix.sping.colors.Color  # value = Color(0.94,0.97,1.00)
antiquewhite: rdkix.sping.colors.Color  # value = Color(0.98,0.92,0.84)
aqua: rdkix.sping.colors.Color  # value = Color(0.00,1.00,1.00)
aquamarine: rdkix.sping.colors.Color  # value = Color(0.50,1.00,0.83)
azure: rdkix.sping.colors.Color  # value = Color(0.94,1.00,1.00)
beige: rdkix.sping.colors.Color  # value = Color(0.96,0.96,0.86)
bisque: rdkix.sping.colors.Color  # value = Color(1.00,0.89,0.77)
black: rdkix.sping.colors.Color  # value = Color(0.00,0.00,0.00)
blanchedalmond: rdkix.sping.colors.Color  # value = Color(1.00,0.92,0.80)
blue: rdkix.sping.colors.Color  # value = Color(0.00,0.00,1.00)
blueviolet: rdkix.sping.colors.Color  # value = Color(0.54,0.17,0.89)
brown: rdkix.sping.colors.Color  # value = Color(0.65,0.16,0.16)
burlywood: rdkix.sping.colors.Color  # value = Color(0.87,0.72,0.53)
cadetblue: rdkix.sping.colors.Color  # value = Color(0.37,0.62,0.63)
chartreuse: rdkix.sping.colors.Color  # value = Color(0.50,1.00,0.00)
chocolate: rdkix.sping.colors.Color  # value = Color(0.82,0.41,0.12)
cm: float = 28.346456692913385
coral: rdkix.sping.colors.Color  # value = Color(1.00,0.50,0.31)
cornflower: rdkix.sping.colors.Color  # value = Color(0.39,0.58,0.93)
cornsilk: rdkix.sping.colors.Color  # value = Color(1.00,0.97,0.86)
crimson: rdkix.sping.colors.Color  # value = Color(0.86,0.08,0.24)
cyan: rdkix.sping.colors.Color  # value = Color(0.00,1.00,1.00)
darkblue: rdkix.sping.colors.Color  # value = Color(0.00,0.00,0.55)
darkcyan: rdkix.sping.colors.Color  # value = Color(0.00,0.55,0.55)
darkgoldenrod: rdkix.sping.colors.Color  # value = Color(0.72,0.53,0.04)
darkgray: rdkix.sping.colors.Color  # value = Color(0.66,0.66,0.66)
darkgreen: rdkix.sping.colors.Color  # value = Color(0.00,0.39,0.00)
darkkhaki: rdkix.sping.colors.Color  # value = Color(0.74,0.72,0.42)
darkmagenta: rdkix.sping.colors.Color  # value = Color(0.55,0.00,0.55)
darkolivegreen: rdkix.sping.colors.Color  # value = Color(0.33,0.42,0.18)
darkorange: rdkix.sping.colors.Color  # value = Color(1.00,0.55,0.00)
darkorchid: rdkix.sping.colors.Color  # value = Color(0.60,0.20,0.80)
darkred: rdkix.sping.colors.Color  # value = Color(0.55,0.00,0.00)
darksalmon: rdkix.sping.colors.Color  # value = Color(0.91,0.59,0.48)
darkseagreen: rdkix.sping.colors.Color  # value = Color(0.56,0.74,0.55)
darkslateblue: rdkix.sping.colors.Color  # value = Color(0.28,0.24,0.55)
darkslategray: rdkix.sping.colors.Color  # value = Color(0.18,0.31,0.31)
darkturquoise: rdkix.sping.colors.Color  # value = Color(0.00,0.81,0.82)
darkviolet: rdkix.sping.colors.Color  # value = Color(0.58,0.00,0.83)
deeppink: rdkix.sping.colors.Color  # value = Color(1.00,0.08,0.58)
deepskyblue: rdkix.sping.colors.Color  # value = Color(0.00,0.75,1.00)
dimgray: rdkix.sping.colors.Color  # value = Color(0.41,0.41,0.41)
dodgerblue: rdkix.sping.colors.Color  # value = Color(0.12,0.56,1.00)
figureArc: int = 2
figureCurve: int = 3
figureLine: int = 1
firebrick: rdkix.sping.colors.Color  # value = Color(0.70,0.13,0.13)
floralwhite: rdkix.sping.colors.Color  # value = Color(1.00,0.98,0.94)
forestgreen: rdkix.sping.colors.Color  # value = Color(0.13,0.55,0.13)
fuchsia: rdkix.sping.colors.Color  # value = Color(1.00,0.00,1.00)
gainsboro: rdkix.sping.colors.Color  # value = Color(0.86,0.86,0.86)
ghostwhite: rdkix.sping.colors.Color  # value = Color(0.97,0.97,1.00)
gold: rdkix.sping.colors.Color  # value = Color(1.00,0.84,0.00)
goldenrod: rdkix.sping.colors.Color  # value = Color(0.85,0.65,0.13)
gray: rdkix.sping.colors.Color  # value = Color(0.50,0.50,0.50)
green: rdkix.sping.colors.Color  # value = Color(0.00,0.50,0.00)
greenyellow: rdkix.sping.colors.Color  # value = Color(0.68,1.00,0.18)
grey: rdkix.sping.colors.Color  # value = Color(0.50,0.50,0.50)
honeydew: rdkix.sping.colors.Color  # value = Color(0.94,1.00,0.94)
hotpink: rdkix.sping.colors.Color  # value = Color(1.00,0.41,0.71)
inch: int = 72
indianred: rdkix.sping.colors.Color  # value = Color(0.80,0.36,0.36)
indigo: rdkix.sping.colors.Color  # value = Color(0.29,0.00,0.51)
ivory: rdkix.sping.colors.Color  # value = Color(1.00,1.00,0.94)
keyBksp: str = '\x08'
keyClear: str = '\x1b'
keyDel: str = '\x7f'
keyDown: str = '\x1f'
keyEnd: str = '\x04'
keyHome: str = '\x01'
keyLeft: str = '\x1c'
keyPgDn: str = '\x0c'
keyPgUp: str = '\x0b'
keyRight: str = '\x1d'
keyTab: str = '\t'
keyUp: str = '\x1e'
khaki: rdkix.sping.colors.Color  # value = Color(0.94,0.90,0.55)
lavender: rdkix.sping.colors.Color  # value = Color(0.90,0.90,0.98)
lavenderblush: rdkix.sping.colors.Color  # value = Color(1.00,0.94,0.96)
lawngreen: rdkix.sping.colors.Color  # value = Color(0.49,0.99,0.00)
lemonchiffon: rdkix.sping.colors.Color  # value = Color(1.00,0.98,0.80)
lightblue: rdkix.sping.colors.Color  # value = Color(0.68,0.85,0.90)
lightcoral: rdkix.sping.colors.Color  # value = Color(0.94,0.50,0.50)
lightcyan: rdkix.sping.colors.Color  # value = Color(0.88,1.00,1.00)
lightgoldenrodyellow: rdkix.sping.colors.Color  # value = Color(0.98,0.98,0.82)
lightgreen: rdkix.sping.colors.Color  # value = Color(0.56,0.93,0.56)
lightgrey: rdkix.sping.colors.Color  # value = Color(0.83,0.83,0.83)
lightpink: rdkix.sping.colors.Color  # value = Color(1.00,0.71,0.76)
lightsalmon: rdkix.sping.colors.Color  # value = Color(1.00,0.63,0.48)
lightseagreen: rdkix.sping.colors.Color  # value = Color(0.13,0.70,0.67)
lightskyblue: rdkix.sping.colors.Color  # value = Color(0.53,0.81,0.98)
lightslategray: rdkix.sping.colors.Color  # value = Color(0.47,0.53,0.60)
lightsteelblue: rdkix.sping.colors.Color  # value = Color(0.69,0.77,0.87)
lightyellow: rdkix.sping.colors.Color  # value = Color(1.00,1.00,0.88)
lime: rdkix.sping.colors.Color  # value = Color(0.00,1.00,0.00)
limegreen: rdkix.sping.colors.Color  # value = Color(0.20,0.80,0.20)
linen: rdkix.sping.colors.Color  # value = Color(0.98,0.94,0.90)
magenta: rdkix.sping.colors.Color  # value = Color(1.00,0.00,1.00)
maroon: rdkix.sping.colors.Color  # value = Color(0.50,0.00,0.00)
mediumaquamarine: rdkix.sping.colors.Color  # value = Color(0.40,0.80,0.67)
mediumblue: rdkix.sping.colors.Color  # value = Color(0.00,0.00,0.80)
mediumorchid: rdkix.sping.colors.Color  # value = Color(0.73,0.33,0.83)
mediumpurple: rdkix.sping.colors.Color  # value = Color(0.58,0.44,0.86)
mediumseagreen: rdkix.sping.colors.Color  # value = Color(0.24,0.70,0.44)
mediumslateblue: rdkix.sping.colors.Color  # value = Color(0.48,0.41,0.93)
mediumspringgreen: rdkix.sping.colors.Color  # value = Color(0.00,0.98,0.60)
mediumturquoise: rdkix.sping.colors.Color  # value = Color(0.28,0.82,0.80)
mediumvioletred: rdkix.sping.colors.Color  # value = Color(0.78,0.08,0.52)
midnightblue: rdkix.sping.colors.Color  # value = Color(0.10,0.10,0.44)
mintcream: rdkix.sping.colors.Color  # value = Color(0.96,1.00,0.98)
mistyrose: rdkix.sping.colors.Color  # value = Color(1.00,0.89,0.88)
moccasin: rdkix.sping.colors.Color  # value = Color(1.00,0.89,0.71)
modControl: int = 2
modShift: int = 1
navajowhite: rdkix.sping.colors.Color  # value = Color(1.00,0.87,0.68)
navy: rdkix.sping.colors.Color  # value = Color(0.00,0.00,0.50)
oldlace: rdkix.sping.colors.Color  # value = Color(0.99,0.96,0.90)
olive: rdkix.sping.colors.Color  # value = Color(0.50,0.50,0.00)
olivedrab: rdkix.sping.colors.Color  # value = Color(0.42,0.56,0.14)
orange: rdkix.sping.colors.Color  # value = Color(1.00,0.65,0.00)
orangered: rdkix.sping.colors.Color  # value = Color(1.00,0.27,0.00)
orchid: rdkix.sping.colors.Color  # value = Color(0.85,0.44,0.84)
palegoldenrod: rdkix.sping.colors.Color  # value = Color(0.93,0.91,0.67)
palegreen: rdkix.sping.colors.Color  # value = Color(0.60,0.98,0.60)
paleturquoise: rdkix.sping.colors.Color  # value = Color(0.69,0.93,0.93)
palevioletred: rdkix.sping.colors.Color  # value = Color(0.86,0.44,0.58)
papayawhip: rdkix.sping.colors.Color  # value = Color(1.00,0.94,0.84)
peachpuff: rdkix.sping.colors.Color  # value = Color(1.00,0.85,0.73)
peru: rdkix.sping.colors.Color  # value = Color(0.80,0.52,0.25)
pink: rdkix.sping.colors.Color  # value = Color(1.00,0.75,0.80)
plum: rdkix.sping.colors.Color  # value = Color(0.87,0.63,0.87)
powderblue: rdkix.sping.colors.Color  # value = Color(0.69,0.88,0.90)
purple: rdkix.sping.colors.Color  # value = Color(0.50,0.00,0.50)
red: rdkix.sping.colors.Color  # value = Color(1.00,0.00,0.00)
rosybrown: rdkix.sping.colors.Color  # value = Color(0.74,0.56,0.56)
royalblue: rdkix.sping.colors.Color  # value = Color(0.25,0.41,0.88)
saddlebrown: rdkix.sping.colors.Color  # value = Color(0.55,0.27,0.07)
salmon: rdkix.sping.colors.Color  # value = Color(0.98,0.50,0.45)
sandybrown: rdkix.sping.colors.Color  # value = Color(0.96,0.64,0.38)
seagreen: rdkix.sping.colors.Color  # value = Color(0.18,0.55,0.34)
seashell: rdkix.sping.colors.Color  # value = Color(1.00,0.96,0.93)
sienna: rdkix.sping.colors.Color  # value = Color(0.63,0.32,0.18)
silver: rdkix.sping.colors.Color  # value = Color(0.75,0.75,0.75)
skyblue: rdkix.sping.colors.Color  # value = Color(0.53,0.81,0.92)
slateblue: rdkix.sping.colors.Color  # value = Color(0.42,0.35,0.80)
slategray: rdkix.sping.colors.Color  # value = Color(0.44,0.50,0.56)
snow: rdkix.sping.colors.Color  # value = Color(1.00,0.98,0.98)
springgreen: rdkix.sping.colors.Color  # value = Color(0.00,1.00,0.50)
steelblue: rdkix.sping.colors.Color  # value = Color(0.27,0.51,0.71)
tan: rdkix.sping.colors.Color  # value = Color(0.82,0.71,0.55)
teal: rdkix.sping.colors.Color  # value = Color(0.00,0.50,0.50)
thistle: rdkix.sping.colors.Color  # value = Color(0.85,0.75,0.85)
tomato: rdkix.sping.colors.Color  # value = Color(1.00,0.39,0.28)
transparent: rdkix.sping.colors.Color  # value = Color(-1.00,-1.00,-1.00)
turquoise: rdkix.sping.colors.Color  # value = Color(0.25,0.88,0.82)
violet: rdkix.sping.colors.Color  # value = Color(0.93,0.51,0.93)
wheat: rdkix.sping.colors.Color  # value = Color(0.96,0.87,0.70)
white: rdkix.sping.colors.Color  # value = Color(1.00,1.00,1.00)
whitesmoke: rdkix.sping.colors.Color  # value = Color(0.96,0.96,0.96)
yellow: rdkix.sping.colors.Color  # value = Color(1.00,1.00,0.00)
yellowgreen: rdkix.sping.colors.Color  # value = Color(0.60,0.80,0.20)
