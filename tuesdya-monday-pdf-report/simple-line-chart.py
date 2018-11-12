# "Line with markers (serious)"
# from reportlab.lib.colors import purple, PCMYKColor, black, pink, green, blue
# from reportlab.graphics.charts.lineplots import LinePlot
# from reportlab.graphics.charts.legends import LineLegend
# from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
# from reportlab.lib.validators import Auto
# from reportlab.graphics.widgets.markers import makeMarker
# from reportlab.pdfbase.pdfmetrics import stringWidth, EmbeddedType1Face, registerTypeFace, Font, registerFont
# from reportlab.graphics.charts.axes import XValueAxis, YValueAxis, AdjYValueAxis, NormalDateXValueAxis
#
# class SmileyMarkerChart(_DrawingEditorMixin,Drawing):
#     '''
#     Chart Features
#     ==============
#
#     This chart is closely related to the 'silly' line chart
#     with markers. The key attributes that have changed are:
#
#     - **chart.lines.symbol.kind** was changed from 'FilledCross' to 'Smiley'
#     - **chart.lines.symbol.size** was changed from 5 to 15
#     - **chart.lines.symbol.angle** was changed from 45 to 0 in order
#     to prevent the smiley faces from being rotated
#     - **legend.columnMaximum** was changed from 1 to 2, forcing the
#     legend into a single stacked column
#     - **legend.y** was increased to push the legend up
#     - **legend.x** was increased to move it to the right across the chart
#     '''
#     def __init__(self,width=258,height=150,*args,**kw):
#         Drawing.__init__(self,width,height,*args,**kw)
#         # font
#         fontName = 'Helvetica'
#         fontSize = 7
#         # chart
#         self._add(self,LinePlot(),name='chart',validate=None,desc=None)
#         self.chart.y                = 16
#         self.chart.x                = 32
#         self.chart.width            = 212
#         self.chart.height           = 90
#         # line styles
#         self.chart.lines.strokeWidth     = 0
#         self.chart.lines.symbol= makeMarker('FilledSquare')
#         # x axis
#         self.chart.xValueAxis = NormalDateXValueAxis()
#         self.chart.xValueAxis.labels.fontName          = fontName
#         self.chart.xValueAxis.labels.fontSize          = fontSize-1
#         self.chart.xValueAxis.forceEndDate             = 1
#         self.chart.xValueAxis.forceFirstDate           = 1
#         self.chart.xValueAxis.labels.boxAnchor      ='autox'
#         self.chart.xValueAxis.xLabelFormat          = '{d}-{MMM}'
#         self.chart.xValueAxis.maximumTicks          = 5
#         self.chart.xValueAxis.minimumTickSpacing    = 0.5
#         self.chart.xValueAxis.niceMonth             = 0
#         self.chart.xValueAxis.strokeWidth           = 1
#         self.chart.xValueAxis.loLLen                = 5
#         self.chart.xValueAxis.hiLLen                = 5
#         self.chart.xValueAxis.gridEnd               = self.width
#         self.chart.xValueAxis.gridStart             = self.chart.x-10
#         # y axis
#         #self.chart.yValueAxis = AdjYValueAxis()
#         self.chart.yValueAxis.visibleGrid           = 1
#         self.chart.yValueAxis.visibleAxis=0
#         self.chart.yValueAxis.labels.fontName       = fontName
#         self.chart.yValueAxis.labels.fontSize       = fontSize -1
#         self.chart.yValueAxis.labelTextFormat       = '%0.2f%%'
#         self.chart.yValueAxis.strokeWidth           = 0.25
#         self.chart.yValueAxis.visible               = 1
#         self.chart.yValueAxis.labels.rightPadding   = 5
#         #self.chart.yValueAxis.maximumTicks          = 6
#         self.chart.yValueAxis.rangeRound            ='both'
#         self.chart.yValueAxis.tickLeft              = 7.5
#         self.chart.yValueAxis.minimumTickSpacing    = 0.5
#         self.chart.yValueAxis.maximumTicks          = 8
#         self.chart.yValueAxis.forceZero             = 0
#         self.chart.yValueAxis.avoidBoundFrac = 0.1
#         # legend
#         self._add(self,LineLegend(),name='legend',validate=None,desc=None)
#         self.legend.fontName         = fontName
#         self.legend.fontSize         = fontSize
#         self.legend.alignment        ='right'
#         self.legend.dx           = 5
#         # sample data
#         self.chart.data = [[(19010706, 1), (19010806, 2), (19010906, 3.2999999999999998), (19011006, 3.29), (19011106, 3.3399999999999999), (19011206, 3.4100000000000001), (19020107, 3.3700000000000001), (19020207, 3.3700000000000001), (19020307, 3.3700000000000001), (19020407, 3.5), (19020507, 3.6200000000000001), (19020607, 3.46), (19020707, 3.3900000000000001)],
#                            [(19010706, 10), (19010806, 3.1200000000000001), (19010906, 3.1400000000000001), (19011006, 3.1400000000000001), (19011106, 3.1699999999999999), (19011206, 3.23), (19020107, 3.1899999999999999), (19020207, 3.2000000000000002), (19020307, 3.1899999999999999), (19020407, 3.3100000000000001), (19020507, 3.4300000000000002), (19020607, 3.29), (19020707, 3.2200000000000002)]]
#         self.chart.lines[0].strokeColor = PCMYKColor(0,100,100,40,alpha=100)
#         self.chart.lines[1].strokeColor = PCMYKColor(100,0,90,50,alpha=100)
#         self.chart.xValueAxis.strokeColor             = PCMYKColor(100,60,0,50,alpha=100)
#         self.legend.colorNamePairs = [(PCMYKColor(0,100,100,40,alpha=100), 'Bovis Homes'), (PCMYKColor(100,0,90,50,alpha=100), 'HSBC Holdings')]
#         self.chart.lines.symbol.x           = 0
#         self.chart.lines.symbol.strokeWidth = 0
#         self.chart.lines.symbol.arrowBarbDx = 5
#         self.chart.lines.symbol.strokeColor = PCMYKColor(0,0,0,0,alpha=100)
#         self.chart.lines.symbol.fillColor   = None
#         self.chart.lines.symbol.arrowHeight = 5
#         self.legend.dxTextSpace    = 7
#         self.legend.boxAnchor      = 'nw'
#         self.legend.subCols.dx        = 0
#         self.legend.subCols.dy        = -2
#         self.legend.subCols.rpad      = 0
#         self.legend.columnMaximum  = 1
#         self.legend.deltax         = 1
#         self.legend.deltay         = 0
#         self.legend.dy             = 5
#         self.legend.y              = 135
#         self.legend.x              = 120
#         self.chart.lines.symbol.kind        = 'FilledCross'
#         self.chart.lines.symbol.size        = 5
#         self.chart.lines.symbol.angle       = 45
#
# SmileyMarkerChart().save(formats=['pdf'],outDir='.',fnRoot=None)
from reportlab.graphics.charts.axes import NormalDateXValueAxis
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from random import randint
from datetime import date, timedelta
import main.database as maria

db = maria.MySQLDatabase()
action = ['insert', 'update', 'delete']
sql_insert = """select DATE_FORMAT(event_date, '%Y-%m-%d %H:%00:00') AS 'Logged Time', count(logging_id) AS 'Total {act} Transaction'
                from LOGGING_EVENTS
                where event_type='{action}'
                group by UNIX_TIMESTAMP(event_date) DIV 3600"""

result = map(lambda item: db.select(sql_insert.format(action=item, act=item.capitalize())), action)

# result = map(lambda item: db.select(sql_insert.format(action=item)), action)
part_user_desc = [field[0] for field in db.mycursor.description]
# print db.select(sql_insert)

print part_user_desc
print result

#Generate some testdata
# data = [
#     [(x,randint(90,100)) for x in range(0,2001,100)],
#     [(x,randint(30,80)) for x in range(0,2001,100)],
#     [(x,randint(5,20)) for x in range(0,2001,100)],
#     ]

# Create the drawing and the lineplot
drawing = Drawing(400, 200)
lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp._inFill = 1
lp.data = result
for i in range(len(result)):
    lp.lines[i].strokeColor = colors.toColor('hsl(%s,80%%,40%%)'%(i*60))

fontName = 'Helvetica'
fontSize = 7

lp.xValueAxis = NormalDateXValueAxis()
lp.xValueAxis.labels.fontName          = fontName
lp.xValueAxis.labels.fontSize          = fontSize-1
lp.xValueAxis.forceEndDate             = 1
lp.xValueAxis.forceFirstDate           = 1
lp.xValueAxis.labels.boxAnchor      ='autox'
lp.xValueAxis.xLabelFormat          = '{d}-{MMM}'
lp.xValueAxis.maximumTicks          = 5
lp.xValueAxis.minimumTickSpacing    = 0.5
lp.xValueAxis.niceMonth             = 0
lp.xValueAxis.strokeWidth           = 1
lp.xValueAxis.loLLen                = 5
lp.xValueAxis.hiLLen                = 5
# lp.xValueAxis.gridEnd               = self.width
# lp.xValueAxis.gridStart             = self.chart.x-10

# Specify where the labels should be
# lp.xValueAxis.valueSteps = [5, 500, 1402, 1988]
# Create a formatter that takes the value and format it however you like.
# def formatter(val):
#     #return val
#     #return 'x=%s'%val
#     return (date(2010,1,1) + timedelta(val)).strftime('%Y-%m-%d')

# Use the formatter
# lp.xValueAxis.labelTextFormat = formatter(result)
drawing.add(lp)

from reportlab.graphics import renderPDF
renderPDF.drawToFile(drawing, 'example.pdf', 'lineplot with dates')