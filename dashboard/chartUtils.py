from django.templatetags.static import static

from django.conf import settings as conf

from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter, DataRange1d, Div
from bokeh.models.glyphs import HexTile

from datetime import datetime, date, timedelta
import random

from . import chartFormatter


def barChart(data,
             x_range,
             cats,
             vals,
             x_label,
             y_label,
             tooltips):

    # Primary Plot Creation

    p = figure(
        x_range=x_range,
        tools=conf.TOOLS,
        tooltips=tooltips)

    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = y_label

    p.vbar(
        source=data,
        x=cats,
        top=vals,
        width=conf.BAR_WIDTH,
        line_color=conf.BAR_BORDER_COLOR,
        line_width=conf.BAR_BORDER_WIDTH,
        fill_color=conf.PINK)

    chartFormatter.formatPlot(p, rotateXAxisLabels=True, isBarChart=True)

    return p


def stackedBar(data, x, y, ylabel, tooltips):

    p = figure(
        x_range=data.data[x].tolist(),
        tools=conf.TOOLS,
        tooltips=tooltips)

    p.yaxis.axis_label = ylabel

    p.vbar_stack(
        source=data,
        stackers=y,
        x=x,
        width=0.7,
        line_color=conf.BAR_BORDER_COLOR,
        line_width=conf.BAR_BORDER_WIDTH,
        fill_color=[conf.LEMON, conf.PINK])

    # Bespoke formatting for this chart

    chartFormatter.formatPlot(
        p,
        rotateXAxisLabels=True,
        isBarChart=True)

    return p


def hexMap(data, tooltips):

    glyph = HexTile(
        q="q",
        r="r",
        aspect_scale=1.1,
        orientation='pointytop',
        size=1,
        fill_color='color',
        line_color=conf.WHITE)

    p = figure(tools=conf.TOOLS, tooltips=createTooltip(tooltips))

    p.match_aspect = True

    p.add_glyph(data, glyph)

    chartFormatter.formatPlot(p, hideAxes=True) #, setPlotSize=False)

    return p


def boxPlot(data,
            y_range,
            cats,
            whisker_left,
            whisker_right,
            box_left,
            box_right,
            x_label,
            tooltips):

    # Primary Plot Creation
    p = figure(
        y_range=y_range,
        tools=conf.TOOLS,
        tooltips=tooltips)

    p.xaxis.axis_label = x_label

    # Whiskers
    p.segment(
        source=data,
        x0=whisker_left,
        y0=cats,
        x1=whisker_right,
        y1=cats,
        line_color=conf.WHISKER_LINE_COLOR,
        line_width=conf.WHISKER_LINE_WIDTH,
        line_cap=conf.WHISKER_LINE_CAP)

    # Boxes
    p.hbar(
        source=data,
        y=cats,
        height=0.7,
        left=box_left,
        right=box_right,
        fill_color=conf.BOX_FILL_COLOR,
        line_color=conf.BOX_LINE_COLOR,
        line_cap=conf.BOX_LINE_CAP,
        line_width=conf.BOX_LINE_WIDTH)

    chartFormatter.formatPlot(p, isHorizontal=True, isBarChart=True)

    return p


def lineChart_figure(tooltips=None):

    start = datetime.strptime(
        conf.START_DATE_OF_TIME_SERIES, '%Y-%m-%d')
    end = datetime.today() - timedelta(days = 1)

    p = figure(
        x_axis_type='datetime',
        x_range=DataRange1d(start=start, end=end),
        tools=conf.TOOLS,
        tooltips=tooltips)

    p.xaxis.formatter = \
        DatetimeTickFormatter(
            days=["%d %m"],
            months=["%b %y"])

    p.yaxis.formatter = \
        NumeralTickFormatter(format="#,###")

    chartFormatter.formatPlot(p)

    return p


def lineChart_line(p, data, x, y, visible=True):

    # TODO: I would like to put the three formatting options above into
    # formatPlot with everything else, but it doesn't seem possible to
    # access the line glyph post creation. Closest I got was this:
    # https://github.com/bokeh/bokeh/issues/1790, but that doesn't seem
    # to work anymore

    l = p.line(
        source=data,
        x=x,
        y=y,
        line_color=conf.CHART_LINE_COLOR,
        line_width=conf.CHART_LINE_WIDTH_THIN,
        line_cap=conf.CHART_LINE_CAP,
        name=y,
        visible=visible)

    return l

def lineChart(data, x, y, tooltips):

    p = lineChart_figure(tooltips)

    l = lineChart_line(p, data, x, y)

    return p


def createTooltip(labelValuePairs):

    html = ''
    html += '<div style="background-color: ' + conf.WHITE + '">'
    html += '<table>'
    for labelValuePair in labelValuePairs:

        # Normally we get a label/value tuple, but sometimes it's just the
        # value, in which case we put it in a full width row of the tooltip
        # table
        if type(labelValuePair) is tuple:
            label = labelValuePair[0].lower()
            if label != '':
                label = label + ': '

            html += '<tr>'
            html += '<td class="tooltip_label">'
            html += label
            html += '</td>'
            html += '<td class="tooltip_value">'
            html += '@' + labelValuePair[1]
            html += '</td>'
            html += '</tr>'
        else:
            html += '<tr>'
            html += '<td colspan="2" class="tooltip_value">'
            html += '@' + labelValuePair
            html += '</td>'
            html += '</tr>'
    html += '</table>'
    html += '</div>'

    return html


def backgroundImage():

    d1 = Div(
        text='''<div class="background_image_div" style="left:-''' +
             str(conf.DASHBOARD_WIDTH - random.randint(0, 400)) +
             '''px;"><img src="''' +
             static('images/' + conf.BG_IMG_URLS[random.randint(0, len(conf.BG_IMG_URLS)-1)]) +
             '''" class="background_image"></div>''')
    return d1
