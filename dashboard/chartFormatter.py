from django.conf import settings as conf

import math


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
        p.frame_height = conf.PLOT_HEIGHT
    except AttributeError:
        p.height = conf.PLOT_HEIGHT

    p.plot_width = conf.PLOT_WIDTH

    if not isBarChart:
         p.min_border_left = conf.CHART_MIN_BORDER_LEFT
         p.min_border_right = conf.CHART_MIN_BORDER_RIGHT
         p.min_border_top = conf.CHART_MIN_BORDER_TOP


def formatAxesHidden(p):
    p.axis.axis_line_width = 0
    p.axis.axis_line_color = None
    p.axis.axis_label_text_color = None
    p.axis.major_label_text_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = '0pt'


def formatAxes(p, isHorizontal=False, isBarChart=False):

    p.axis.axis_line_width = conf.AXIS_LINE_WIDTH
    p.axis.axis_line_cap = conf.AXIS_LINE_CAP

    if isHorizontal and isBarChart:
        p.y_range.range_padding = conf.CHART_RANGE_PADDING
    elif isBarChart:
        p.x_range.range_padding = conf.CHART_RANGE_PADDING


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

    p.axis.major_label_standoff = conf.MAJOR_LABEL_STANDOFF

    p.axis.major_label_text_font = conf.MAJOR_LABEL_TEXT_FONT
    p.axis.major_label_text_font_style = conf.MAJOR_LABEL_TEXT_FONT_STYLE
    p.axis.major_label_text_font_size = conf.MAJOR_LABEL_TEXT_SIZE
    p.axis.major_label_text_color = conf.MAJOR_LABEL_TEXT_COLOR

    if rotateXAxisLabels:
        p.xaxis.major_label_orientation = math.pi/4

    # Specific axis

    val_axis.major_tick_line_cap = conf.MAJOR_TICK_LINE_CAP
    val_axis.major_tick_line_width = conf.MAJOR_TICK_LINE_WIDTH
    val_axis.major_tick_out = conf.MAJOR_TICK_OUT


def formatAxesLabels(p):

    p.axis.axis_label_standoff = conf.AXIS_LABEL_STANDOFF

    p.axis.axis_label_text_font = conf.AXIS_LABEL_TEXT_FONT
    p.axis.axis_label_text_font_style = conf.AXIS_LABEL_TEXT_FONT_STYLE
    p.axis.axis_label_text_color = conf.AXIS_LABEL_TEXT_COLOR
    p.axis.axis_label_text_font_size = conf.AXIS_LABEL_TEXT_FONT_SIZE
