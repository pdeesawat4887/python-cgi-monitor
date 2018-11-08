"Legend with text wrapping"
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.pdfbase.pdfmetrics import stringWidth, EmbeddedType1Face, registerTypeFace, Font, registerFont
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.lib.colors import PCMYKColor, Color

class PieChart07(_DrawingEditorMixin,Drawing):
    '''
        Chart Features
        --------------

        - The legend text is wrapped and the extra wrapped text goes below the first line.

        - The maximum number of rows in the legend is four, then the legend moves to the right
        to start a new column of rows.
    '''
    def __init__(self,width=155,height=138,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        fontName = 'Helvetica'
        fontSize = 6
        self._add(self,Pie(),name='pie',validate=None,desc=None)
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        colors= [PCMYKColor(40,0,7,40,alpha=100), PCMYKColor(0,12,9,87,alpha=100), PCMYKColor(30,0,6,33,alpha=100), PCMYKColor(0,4,4,69,alpha=100), PCMYKColor(21,0,5,25,alpha=100), PCMYKColor(0,2,2,52,alpha=100)]
        self.pie.data              = [30.600000000000001, 8.5, 39.299999999999997, 7.7000000000000002, 11.6, 2.2000000000000002]
        self.pie.sameRadii=1
        for i in range(len(self.pie.data)): self.pie.slices[i].fillColor = colors[i]
        self.pie.slices.strokeColor              = PCMYKColor(0,0,0,0)
        self.pie.slices.strokeWidth              = 0.5
        self.legend.alignment                    ='right'
        self.legend.fontName         = fontName
        self.legend.fontSize         = fontSize
        self.legend.dx               = 6.5
        self.legend.dy               = 6.5
        self.legend.yGap             = 0
        self.legend.deltax           = 10
        self.legend.deltay           = 10
        self.legend.strokeColor      = PCMYKColor(0,0,0,0)
        self.legend.strokeWidth     = 0
        self.legend.columnMaximum    = 4
        self.width       = 400
        self.height      = 200
        self.legend.y              = 100
        self.legend.boxAnchor      = 'c'
        self.legend.x              = 325
        self.pie.x                = 25
        self.pie.y                = 25
        self.pie.height           = 150
        self.pie.width            = 150
        self.pie.slices[0].fillColor             = PCMYKColor(23,51,0,4,alpha=100)
        self.pie.slices[1].fillColor             = PCMYKColor(0,100,100,40,alpha=100)
        self.pie.slices[5].fillColor             = PCMYKColor(0,61,22,25,alpha=100)
        self.pie.slices[2].fillColor             = PCMYKColor(100,60,0,50,alpha=100)
        self.pie.slices[3].fillColor             = PCMYKColor(100,0,90,50,alpha=100)
        self.pie.slices[4].fillColor             = PCMYKColor(66,13,0,22,alpha=100)
        self.legend.colorNamePairs = [(PCMYKColor(23,51,0,4,alpha=100), u'Europe: 30.6'), (PCMYKColor(0,100,100,40,alpha=100), u'Japan: 8.5'), (PCMYKColor(100,60,0,50,alpha=100), u'US/Canada: 39.3'), (PCMYKColor(100,0,90,50,alpha=100), u'Asia ex Japan: 7.7'), (PCMYKColor(66,13,0,22,alpha=100), u'Latin\nAmerica/Other: 11.6'), (PCMYKColor(0,61,22,25,alpha=100), u'Australia/New\nZealand: 2.2')]

if __name__=="__main__": #NORUNTESTS
    PieChart07().save(formats=['pdf'],outDir='.',fnRoot='Help')