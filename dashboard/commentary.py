from django.templatetags.static import static

from django.conf import settings as conf

from bokeh.models import Div

from django.core.exceptions import ObjectDoesNotExist

import pandas as pd

from .models import Commentary


def getCommentary(chartName):

    try:
        commentaryText = \
            Commentary.objects.getOne(chartName=chartName).commentary_text
    except ObjectDoesNotExist as e:
        commentaryText = None
        commentaryClass = 'commentary-missing'
    else:
        commentaryDiv = commentaryDiv = Div()
        commentaryClass = 'commentary'

    commentaryDiv = Div(
        text=commentaryText,
        width=conf.COMMENTARY_WIDTH,
        height_policy='min',
        max_height=conf.COMMENTARY_MAX_HEIGHT,
        css_classes=[commentaryClass])

    return commentaryDiv
