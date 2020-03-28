from django.templatetags.static import static

from django.conf import settings as conf

from bokeh.models import Div

import pandas as pd

from .models import Commentary


def getCommentary(chartName):

    commentaryText = Commentary.objects.getOne(chartName=chartName).commentary_text

    commentaryDiv = Div(
        text=commentaryText,
        width=conf.COMMENTARY_WIDTH,
        height_policy='min',
        css_classes=['commentary'])

    return commentaryDiv
