from __future__ import annotations
from math import cos
from math import sin
import os as os
from rdkix.sping.PDF.pidPDF import PDFCanvas
from rdkix.sping.PDF.pidPDF import test
import rdkix.sping.colors
from rdkix.sping.colors import Color
from rdkix.sping.colors import HexColor
from rdkix.sping import pagesizes
from rdkix.sping.pid import AffineMatrix
from rdkix.sping.pid import Canvas
from rdkix.sping.pid import Font
from rdkix.sping.pid import StateSaver
from rdkix.sping.pid import getFileObject
from .pdfdoc import *
from .pdfgen import *
from .pdfgeom import *
from .pdfmetrics import *
from .pdfutils import *
from .pidPDF import *
__all__ = ['AffineMatrix', 'Canvas', 'Color', 'DEFAULT_PAGE_SIZE', 'Font', 'HexColor', 'PDFCanvas', 'StateSaver', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'cm', 'coral', 'cornflower', 'cornsilk', 'cos', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'figureArc', 'figureCurve', 'figureLine', 'firebrick', 'floralwhite', 'font_face_map', 'forestgreen', 'fuchsia', 'gainsboro', 'getFileObject', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'inch', 'indianred', 'indigo', 'ivory', 'keyBksp', 'keyClear', 'keyDel', 'keyDown', 'keyEnd', 'keyHome', 'keyLeft', 'keyPgDn', 'keyPgUp', 'keyRight', 'keyTab', 'keyUp', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'modControl', 'modShift', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'os', 'pagesizes', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'pdfdoc', 'pdfgen', 'pdfgeom', 'pdfmetrics', 'pdfutils', 'peachpuff', 'peru', 'pi', 'pidPDF', 'pink', 'plum', 'powderblue', 'ps_font_map', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'sin', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'test', 'thistle', 'tomato', 'transparent', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
DEFAULT_PAGE_SIZE: tuple = (595.275590551181, 841.8897637795275)
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
font_face_map: dict = {'serif': 'times', 'sansserif': 'helvetica', 'monospaced': 'courier', 'arial': 'helvetica'}
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
pi: float = 3.141592653589793
pink: rdkix.sping.colors.Color  # value = Color(1.00,0.75,0.80)
plum: rdkix.sping.colors.Color  # value = Color(0.87,0.63,0.87)
powderblue: rdkix.sping.colors.Color  # value = Color(0.69,0.88,0.90)
ps_font_map: dict = {('times', 0, 0): 'Times-Roman', ('times', 1, 0): 'Times-Bold', ('times', 0, 1): 'Times-Italic', ('times', 1, 1): 'Times-BoldItalic', ('courier', 0, 0): 'Courier', ('courier', 1, 0): 'Courier-Bold', ('courier', 0, 1): 'Courier-Oblique', ('courier', 1, 1): 'Courier-BoldOblique', ('helvetica', 0, 0): 'Helvetica', ('helvetica', 1, 0): 'Helvetica-Bold', ('helvetica', 0, 1): 'Helvetica-Oblique', ('helvetica', 1, 1): 'Helvetica-BoldOblique', ('symbol', 0, 0): 'Symbol', ('symbol', 1, 0): 'Symbol', ('symbol', 0, 1): 'Symbol', ('symbol', 1, 1): 'Symbol', ('zapfdingbats', 0, 0): 'ZapfDingbats', ('zapfdingbats', 1, 0): 'ZapfDingbats', ('zapfdingbats', 0, 1): 'ZapfDingbats', ('zapfdingbats', 1, 1): 'ZapfDingbats'}
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
