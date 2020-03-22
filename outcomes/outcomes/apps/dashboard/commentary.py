from django.templatetags.static import static
from .models import Commentary

from bokeh.models import Div

import pandas as pd

from .Conf import conf


def getCommentary(chartName):

    commentaryText = Commentary.objects.get(chart_name=chartName).commentary_text

    commentaryDiv = Div(
        text=commentaryText,
        width=conf.commentary_width,
        height=conf.commentary_height,
        css_classes=['commentary'])

    return commentaryDiv
