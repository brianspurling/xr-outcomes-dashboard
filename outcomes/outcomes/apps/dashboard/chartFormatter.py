import math

from .Conf import conf


def formatPlot(p,
               hideAxes=False,
               isHorizontal=False,
               rotateXAxisLabels=False,
               isBarChart=False):

    formatPlotArea(p, isBarChart=isBarChart)

    formatAxes(p, isHorizontal=isHorizontal, isBarChart=isBarChart)

    formatAxesTicks(
        p,
        isHorizontal=isHorizontal,
        rotateXAxisLabels=rotateXAxisLabels)

    formatAxesLabels(p)

    if hideAxes:
        formatAxesHidden(p)


def formatPlotArea(p, isBarChart=False):

    p.toolbar_location = None
    p.background_fill_color = None
    p.border_fill_color = None
    p.outline_line_color = None
    p.grid.grid_line_color = None

    # Two attributes for height depending on plot type
    try:
        p.frame_height = conf.plot_height
    except AttributeError:
        p.height = conf.plot_height

    p.plot_width = conf.plot_width

    if not isBarChart:
         p.min_border_left = conf.chart_min_border_left
         p.min_border_right = conf.chart_min_border_right
         p.min_border_top = conf.chart_min_border_top


def formatAxesHidden(p):
    p.axis.axis_line_width = 0
    p.axis.axis_line_color = None
    p.axis.axis_label_text_color = None
    p.axis.major_label_text_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = '0pt'


def formatAxes(p, isHorizontal=False, isBarChart=False):

    p.axis.axis_line_width = conf.axis_line_width
    p.axis.axis_line_cap = conf.axis_line_cap

    if isHorizontal and isBarChart:
        p.y_range.range_padding = conf.chart_range_padding
    elif isBarChart:
        p.x_range.range_padding = conf.chart_range_padding


def formatAxesTicks(p, isHorizontal=False, rotateXAxisLabels=False):

    # We format some axes values dependent on chart orientation
    if isHorizontal:
        cat_axis = p.yaxis
        val_axis = p.xaxis
    else:
        cat_axis = p.xaxis
        val_axis = p.yaxis

    p.axis.minor_tick_line_color = None

    # All axes

    p.axis.minor_tick_line_color = None
    p.axis.major_tick_line_color = None

    p.axis.major_label_standoff = conf.major_label_standoff

    p.axis.major_label_text_font = conf.major_label_text_font
    p.axis.major_label_text_font_style = conf.major_label_text_font_style
    p.axis.major_label_text_font_size = conf.major_label_text_font_size
    p.axis.major_label_text_color = conf.major_label_text_color

    if rotateXAxisLabels:
        p.xaxis.major_label_orientation = math.pi/4

    # Specific axis

    val_axis.major_tick_line_cap = conf.major_tick_line_cap
    val_axis.major_tick_line_width = conf.major_tick_line_width
    val_axis.major_tick_out = conf.major_tick_out


def formatAxesLabels(p):

    p.axis.axis_label_standoff = conf.axis_label_standoff

    p.axis.axis_label_text_font = conf.axis_label_text_font
    p.axis.axis_label_text_font_style = conf.axis_label_text_font_style
    p.axis.axis_label_text_color = conf.axis_label_text_color
    p.axis.axis_label_text_font_size = conf.axis_label_text_font_size
