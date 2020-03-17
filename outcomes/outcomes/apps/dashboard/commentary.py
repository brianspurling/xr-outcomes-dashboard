from django.templatetags.static import static

from bokeh.models import Div

import pandas as pd

from .Conf import conf


def getCommentary(chartName):

    df = pd.read_csv(static('data/commentary.csv'))

    commentaryText = \
        df.loc[df.chart_name == chartName, 'commentary_text'].values[0]

    commentaryDiv = Div(
        text=commentaryText,
        width=conf.commentary_width,
        height=conf.commentary_height,
        css_classes=['commentary'])

    return commentaryDiv
