"""
piddleSVG

This module implements an SVG PIDDLE canvas.
In other words, this is a PIDDLE backend that renders into a
SVG file.

Bits have been shamelessly cobbled from piddlePDF.py and/or
piddlePS.py

Greg Landrum (greglandrum@earthlink.net) 3/10/2000
"""
from __future__ import annotations
from math import acos
from math import acosh
from math import asin
from math import asinh
from math import atan
from math import atan2
from math import atanh
from math import ceil
from math import comb
from math import copysign
from math import cos
from math import cosh
from math import degrees
from math import dist
from math import erf
from math import erfc
from math import exp
from math import expm1
from math import fabs
from math import factorial
from math import floor
from math import fmod
from math import frexp
from math import fsum
from math import gamma
from math import gcd
from math import hypot
from math import isclose
from math import isfinite
from math import isinf
from math import isnan
from math import isqrt
from math import ldexp
from math import lgamma
from math import log
from math import log10
from math import log1p
from math import log2
from math import modf
from math import perm
from math import pow
from math import prod
from math import radians
from math import remainder
from math import sin
from math import sinh
from math import sqrt
from math import tanh
from math import trunc
from rdkix.sping.PDF import pdfmetrics
import rdkix.sping.colors
from rdkix.sping.colors import Color
from rdkix.sping.colors import HexColor
import rdkix.sping.pid
from rdkix.sping.pid import AffineMatrix
from rdkix.sping.pid import Canvas
from rdkix.sping.pid import Font
from rdkix.sping.pid import StateSaver
from rdkix.sping.pid import getFileObject
__all__ = ['AffineMatrix', 'Canvas', 'Color', 'Font', 'HexColor', 'SVGCanvas', 'SVG_HEADER', 'StateSaver', 'acos', 'acosh', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'ceil', 'chartreuse', 'chocolate', 'cm', 'comb', 'copysign', 'coral', 'cornflower', 'cornsilk', 'cos', 'cosh', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'dashtest', 'deeppink', 'deepskyblue', 'degrees', 'dimgray', 'dist', 'dodgerblue', 'e', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'figureArc', 'figureCurve', 'figureLine', 'firebrick', 'floor', 'floralwhite', 'fmod', 'forestgreen', 'frexp', 'fsum', 'fuchsia', 'gainsboro', 'gamma', 'gcd', 'getFileObject', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'hypot', 'inch', 'indianred', 'indigo', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'ivory', 'keyBksp', 'keyClear', 'keyDel', 'keyDown', 'keyEnd', 'keyHome', 'keyLeft', 'keyPgDn', 'keyPgUp', 'keyRight', 'keyTab', 'keyUp', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'ldexp', 'lemonchiffon', 'lgamma', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'log', 'log10', 'log1p', 'log2', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'modControl', 'modShift', 'modf', 'nan', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'pdfmetrics', 'peachpuff', 'perm', 'peru', 'pi', 'pink', 'plum', 'pow', 'powderblue', 'prod', 'purple', 'radians', 'red', 'remainder', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'sin', 'sinh', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'sqrt', 'steelblue', 'tan', 'tanh', 'tau', 'teal', 'test', 'test2', 'testit', 'thistle', 'tomato', 'transparent', 'trunc', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
class SVGCanvas(rdkix.sping.pid.Canvas):
    def _FormArcStr(self, x1, y1, x2, y2, theta1, extent):
        """
         Forms an arc specification for SVG
        
            
        """
    def _FormFontStr(self, font):
        """
         form what we hope is a valid SVG font string.
              Defaults to 'sansserif'
              This should work when an array of font faces are passed in.
            
        """
    def __init__(self, size = (300, 300), name = 'SVGCanvas', includeXMLHeader = True, extraHeaderText = ''):
        ...
    def _drawStringOneLine(self, line, x, y, fontStr, svgColor, **kwargs):
        ...
    def _findExternalFontName(self, font):
        """
        Attempts to return proper font name.
                PDF uses a standard 14 fonts referred to
                by name. Default to self.defaultFont('Helvetica').
                The dictionary allows a layer of indirection to
                support a standard set of sping.pid font names.
        """
    def _initOutput(self, includeXMLHeader = True, extraHeaderText = ''):
        ...
    def clear(self):
        ...
    def drawArc(self, x1, y1, x2, y2, theta1 = 0, extent = 360, edgeColor = None, edgeWidth = None, fillColor = None, dash = None, **kwargs):
        ...
    def drawCurve(self, x1, y1, x2, y2, x3, y3, x4, y4, edgeColor = None, edgeWidth = None, fillColor = ..., closed = 0, dash = None, **kwargs):
        ...
    def drawEllipse(self, x1, y1, x2, y2, edgeColor = None, edgeWidth = None, fillColor = ..., dash = None, **kwargs):
        ...
    def drawFigure(self, partList, edgeColor = None, edgeWidth = None, fillColor = None, closed = 0, dash = None, **kwargs):
        """
        drawFigure(partList) -- draws a complex figure
            partlist: a set of lines, curves, and arcs defined by a tuple whose
            first element is one of figureLine, figureArc, figureCurve
            and whose remaining 4, 6, or 8 elements are parameters.
        """
    def drawImage(self, image, x1, y1, x2 = None, y2 = None, **kwargs):
        """
        
              to the best of my knowledge, the only real way to get an image
              into SVG is to read it from a file.  So we'll save out to a PNG
              file, then set a link to that in the SVG.
            
        """
    def drawLine(self, x1, y1, x2, y2, color = None, width = None, dash = None, **kwargs):
        """
        Draw a straight line between x1,y1 and x2,y2.
        """
    def drawPolygon(self, pointlist, edgeColor = None, edgeWidth = None, fillColor = ..., closed = 0, dash = None, **kwargs):
        """
        drawPolygon(pointlist) -- draws a polygon
            pointlist: a list of (x,y) tuples defining vertices
            
        """
    def drawString(self, s, x, y, font = None, color = None, angle = 0, **kwargs):
        ...
    def flush(self):
        ...
    def fontAscent(self, font = None):
        ...
    def fontDescent(self, font = None):
        ...
    def save(self, file = None, format = None):
        """
        Hand hand this either a file= <filename> or
            file = <an open file object>.  By default, I've made the fomrat extension be
            .svg.  By default it saves the file to "self.name" + '.svg' 
        """
    def stringWidth(self, s, font = None):
        """
        Return the logical width of the string if it were drawn     in the current font (defaults to self.font).
        """
    def text(self):
        ...
def _ColorToSVG(color):
    """
     convenience function for converting a sping.pid color to an SVG color
    
      
    """
def _PointListToSVG(points, dupFirst = 0):
    """
     convenience function for converting a list of points to a string
          suitable for passing to SVG path operations
    
      
    """
def dashtest():
    ...
def test():
    ...
def test2():
    ...
def testit(canvas, s, x, y, font = None):
    ...
SVG_HEADER: str = '<?xml version="1.0" encoding="iso-8859-1"?>\n'
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
e: float = 2.718281828459045
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
inf: float  # value = inf
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
nan: float  # value = nan
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
pi: float = 3.141592653589793
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
tau: float = 6.283185307179586
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
