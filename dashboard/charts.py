from django.templatetags.static import static

from django.conf import settings as conf

from bokeh.layouts import row, column
from bokeh.models import (CustomJS,
                          DateSlider,
                          Select,
                          ColumnDataSource,
                          HoverTool,
                          Div)

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta, date
import json

from .models import (Website,
                     SocialMedia,
                     Instagram,
                     Facebook,
                     PoliticalParties,
                     LocalAuthorities,
                     BookSales,
                     ActionNetwork)

from . import chartUtils
from . import commentary


def laDeclarationsPlot():

    df = pd.DataFrame(LocalAuthorities.objects.getAll())
    totalLAs = df.shape[0]
    df['dec_month'] = df.declaration_date + pd.offsets.MonthBegin(-1)
    df['dec_yes'] = np.where(df['is_declared'], 1, 0)
    df = df.groupby(['dec_month']).agg({'dec_yes': 'sum'})
    months = pd.date_range(
        start=df.index.min(),
        end=datetime.today(),
        freq=pd.offsets.MonthBegin(1))
    df = df.reindex(months)
    df.dec_yes.fillna(0, inplace=True)
    df['dec_yes_cum'] = df.dec_yes.cumsum()
    df['dec_no_cum'] = totalLAs - df.dec_yes_cum
    df.rename(columns={
        'dec_yes_cum': 'declared',
        'dec_no_cum': 'not_declared'}, inplace=True)
    df['months_date'] = df.index
    df['months'] = df.index
    df.months = df.months_date.dt.strftime('%b %y')

    tooltips = chartUtils.createTooltip([
        ('Declared', 'declared'),
        ('Not delcared', 'not_declared')])

    data = ColumnDataSource(df)

    stackedBarChart = chartUtils.stackedBar(
        data=data,
        x='months',
        y=['declared', 'not_declared'],
        ylabel="Number of Local Authorities",
        tooltips=tooltips)

    commentaryDiv = commentary.getCommentary('la_declared')

    backgroundImageDiv = chartUtils.backgroundImage()

    layout = row(stackedBarChart, commentaryDiv, backgroundImageDiv)

    return layout


def laHexMapPlot():

    # TODO: refactor!

    df = pd.DataFrame(LocalAuthorities.objects.getAll())

    df['target_net_zero_year'] = df['target_net_zero_year'].fillna('')

    start = datetime(2018, 1, 1)
    end = datetime.now()

    declaredFromDate = datetime.now()

    with open(os.path.join(conf.BASE_DIR, 'static/ref/hexmap.geojson'), 'r') as f:
        data = json.load(f)

    # For reasons that aren't clear to me, Bokeh plots
    # the geojson flipped vertically, and every 2nd row
    # needs shifting one more column to the right.
    # So a bit of manual effort needed to sort out

    minR = 1000
    maxR = 0
    for i in range(len(data['features'])):
        r = data['features'][i]['properties']['r']
        if r > maxR:
            maxR = r
        if r < minR:
            minR = r
    n = 0
    for r in range(minR, maxR+1):
        if r % 2 != 0:
            n += 1
        for j in range(len(data['features'])):
            if data['features'][j]['properties']['r'] == r:
                data['features'][j]['properties']['q'] += n

    # Set the colours based on whether they have declared
    q = []
    r = []
    la_name = []
    declared_date = []
    declared_date_str = []
    target_net_zero_year = []
    source = []
    action_plan = []
    color = []
    for i in range(len(data['features'])):
        q.append(data['features'][i]['properties']['q'])
        r.append(data['features'][i]['properties']['r'])

        la_name.append(
            list(df.loc[
                 (df.code == data['features'][i]['properties']['c']),
                 'xr_la_name'])[0])

        decDate = \
            list(df.loc[
                 (df.code == data['features'][i]['properties']['c']),
                 'declaration_date'])[0]
        decDateStr = \
            list(df.loc[
                 (df.code == data['features'][i]['properties']['c']),
                 'declaration_date_str'])[0]

        declared_date.append(decDate)
        declared_date_str.append(decDateStr)

        if decDateStr == 'Not declared':
            color.append(conf.LEMON)
        elif decDate >= declaredFromDate:
            color.append(conf.LEMON)
        else:
            color.append(conf.PINK)

        target_net_zero_year.append(
            list(df.loc[
                (df.code == data['features'][i]['properties']['c']),
                'target_net_zero_year'])[0])

        source.append(
            list(df.loc[
                (df.code == data['features'][i]['properties']['c']),
                'source'])[0])

        action_plan.append(
            list(df.loc[
                (df.code == data['features'][i]['properties']['c']),
                'action_plan'])[0])

    q = np.asarray(q)
    r = np.asarray(r)

    df_LAs = pd.DataFrame({
        'q': q,
        'r': -r,
        'la_name': la_name,
        'declared_date': declared_date,
        'declared_date_str': declared_date_str,
        'target_net_zero_year': target_net_zero_year,
        'source': source,
        'action_plan': action_plan,
        'color': color})

    tooltips = [
        ('la_name'),
        ('Declared Date', 'declared_date_str'),
        ('Net Zero Year', 'target_net_zero_year'),
        ('Source', '/Click for link to data source'),
        ('Action Plan', '/Click for link to action plan'),]

    stickyTooltips = [
        ('la_name'),
        ('Declared Date', 'declared_date_str'),
        ('Net Zero Year', 'target_net_zero_year'),
        ('Source', 'source'),
        ('Action Plan', 'action_plan')]

    data = ColumnDataSource(df_LAs)

    hexMap = chartUtils.hexMap(
        data,
        tooltips=tooltips,
        stickyTooltips=stickyTooltips)

    slider = DateSlider(
        start=datetime(2018, 1, 1),
        end=datetime.now(),
        step=1,
        value=datetime.now())

    callback = CustomJS(
        args=dict(source=data),
        code="""
            var declaredFromDate = cb_obj.value;
            for (var i = 0; i < source.data['declared_date'].length; i++) {
                if (source.data['declared_date_str'][i] == 'Not declared') {
                    source.data['color'][i] = '#F7EE6A'
                } else if (source.data['declared_date'][i] > declaredFromDate) {
                    source.data['color'][i] = '#F7EE6A'
                } else {
                    source.data['color'][i] = '#ED9BC4'
                }
            }
            source.change.emit();
            """)

    slider.js_on_change('value', callback)

    hexMapLayout = column(slider, hexMap)

    commentaryDiv = commentary.getCommentary('map_la_declared')

    backgroundImageDiv = chartUtils.backgroundImage()

    layout = row(hexMapLayout, commentaryDiv, backgroundImageDiv)

    return layout


def partyNetZeroPlot():

    data = PoliticalParties.objects.getAll()

    tooltips = chartUtils.createTooltip([
        ('Target net zero year', 'target_net_zero_year'),
        ('Share of vote', 'vote_pcnt_str')])

    data = ColumnDataSource(data)

    boxPlot = chartUtils.boxPlot(
        data=data,
        y_range=data.data['org_name'],
        cats='org_name',
        whisker_right='latest_year',
        whisker_left='earliest_year',
        box_left='start_year',
        box_right='end_year',
        x_label='Target Net Zero Year',
        tooltips=tooltips)

    commentaryDiv = commentary.getCommentary('political_net_zero')

    backgroundImageDiv = chartUtils.backgroundImage()

    layout = row(boxPlot, commentaryDiv, backgroundImageDiv)

    return layout


def laNetZeroPlot():

    df = pd.DataFrame(LocalAuthorities.objects.getAll())
    df = df.loc[~pd.isnull(df.target_net_zero_year)]
    df = df.groupby(['target_net_zero_year']).size()
    df = df.reset_index(name='count')
    for i in range(int(df.target_net_zero_year.min()),
                   int(df.target_net_zero_year.max())):
        if df.loc[df.target_net_zero_year == i].shape[0] == 0:
            df.loc[-1] = [i, 0]
            df.index = df.index + 1

    df = df.sort_values('target_net_zero_year')
    df.target_net_zero_year = df.target_net_zero_year.astype(int).astype(str)

    tooltips = chartUtils.createTooltip([('Number of Local Authorities', 'count')])

    data = ColumnDataSource(df)

    barChartPlot = chartUtils.barChart(
        data=data,
        x_range=df['target_net_zero_year'],
        cats='target_net_zero_year',
        vals='count',
        x_label='Target Net Zero Year',
        y_label='Number of Local Authorities',
        tooltips=tooltips)

    commentaryDiv = commentary.getCommentary('la_net_zero')

    backgroundImageDiv = chartUtils.backgroundImage()

    layout = row(barChartPlot, commentaryDiv, backgroundImageDiv)

    return layout


def websitePlot():

    tooltips = chartUtils.createTooltip([
        ('date', 'date_str'),
        ('sessions', 'sessions_str')])

    data = ColumnDataSource(Website.objects.getAll())

    lineChart = chartUtils.lineChart(
        data=data,
        x='date',
        y='sessions',
        tooltips=tooltips)

    commentaryDiv = commentary.getCommentary('website_visits')

    backgroundImageDiv = chartUtils.backgroundImage()

    layout = row(lineChart, commentaryDiv, backgroundImageDiv)

    return layout


def socialMediaPlot(platform, subtitle):

    # Instagram & Facebook have their own source sheet / model.
    # The rest all sit in a generic "SocialMedia" model
    if platform == 'Instagram':
        df = pd.DataFrame(Instagram.objects.getAll())
        df = df.groupby(['date', 'date_str']).sum().reset_index()
    elif platform == 'Facebook':
        df = pd.DataFrame(Facebook.objects.getAll())
        df = df.groupby(['date', 'date_str']).sum().reset_index()
    else:
        df = pd.DataFrame(SocialMedia.objects.getAll())
        df = df.groupby(['platform', 'date', 'date_str']).sum().reset_index()
        m = (df.platform == platform)
        df = df.loc[m]

    # Bokeh doesn't seem to like taking value/label tuples
    # in a linked dropdown/plot, so we will set our col
    # headings to user-friendly terms  now
    df.rename(columns={'likes': 'Daily likes',
                       'views': 'Daily views',
                       'follows_cum': 'Cumulative follows over time',
                       'likes_cum': 'Cumulative likes over time',
                       'views_cum': 'Cumulative views over time'},
              inplace=True)

    for metric in conf.SOCIAL_MEDIA_DROPDOWN_OPTIONS[platform.lower()]:
        df[metric.replace(' ', '') + '_str'] = df[metric].map('{:,.0f}'.format)

    data = ColumnDataSource(df)

    p = chartUtils.lineChart_figure()

    lines = []
    maxValues = []
    i = -1
    for metric in conf.SOCIAL_MEDIA_DROPDOWN_OPTIONS[platform.lower()]:
        i += 1

        maxValue = max(df[metric]) * 1.05  # Create a little breathing room
        if i==0:
            # Keep the y axis raised above the x axis, otherwise
            # Bokeh will default it back to crossing at 0
            p.y_range.start = -maxValue * 0.05
            p.y_range.end = maxValue
        maxValues.append(maxValue)

        lines.append(chartUtils.lineChart_line(
                p=p,
                data=data,
                x='date',
                y=metric,
                visible=(i==0)))

        tooltips = chartUtils.createTooltip([
            ('Date', 'date_str'),
            (metric, metric.replace(' ', '') + '_str')])

        p.add_tools(HoverTool(renderers=[lines[i]], tooltips=tooltips))

    subtitle = Div(
        text=subtitle,
        width=conf.PLOT_WIDTH,
        css_classes=["tabSubTitle"])

    select = Select(
        width=conf.DROPDOWN_LIST_WIDTH,
        options=conf.SOCIAL_MEDIA_DROPDOWN_OPTIONS[platform.lower()],
        css_classes=["dropdown_list"])

    callback = CustomJS(
        args=dict(lines=lines, y_range=p.y_range, max_values=maxValues),
        code="""
            for (var i = 0; i < lines.length; i++) {
                if (lines[i].name == cb_obj.value) {
                    lines[i].visible = true
                    // keep the y axis 0 raised above the x axis, otherwise
                    // bokeh will default it back to crossing at 0
                    y_range.start = -max_values[i] * 0.05
                    y_range.end = max_values[i]
                } else {
                    lines[i].visible = false
                }
            }
            """)

    select.js_on_change('value', callback)

    commentaryDiv = commentary.getCommentary(platform.lower())

    backgroundImageDiv = chartUtils.backgroundImage()

    lineChartLayout = row(p, commentaryDiv, backgroundImageDiv)

    layout = column(subtitle, select, lineChartLayout)

    return layout


def actionNetworkActivistsPlot():

    tooltips = chartUtils.createTooltip([
        ('date', 'date_str'),
        ('activists', 'cumulative_str')])

    df = pd.DataFrame(ActionNetwork.objects.getAll())
    groupCols = ['date_str', 'date']
    df = df.sort_values('date')

    data = ColumnDataSource(df)

    lineChart = chartUtils.lineChart(
        data=data,
        x='date',
        y='cumulative',
        tooltips=tooltips)

    commentaryDiv = commentary.getCommentary('action_network_activists')

    backgroundImageDiv = chartUtils.backgroundImage()

    layout = row(lineChart, commentaryDiv, backgroundImageDiv)

    return layout


def bookSalesPlot():

    tooltips = chartUtils.createTooltip([
        ('Date', 'date_str'),
        ('Sales', 'sales_str')])

    data = ColumnDataSource(BookSales.objects.getAll())

    lineChart = chartUtils.lineChart(
        data=data,
        x='date',
        y='sales_cum',
        tooltips=tooltips)

    commentaryDiv = commentary.getCommentary('book_sales')

    backgroundImageDiv = chartUtils.backgroundImage()

    layout = row(lineChart, commentaryDiv, backgroundImageDiv)

    return layout
