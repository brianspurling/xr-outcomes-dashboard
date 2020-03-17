from django.templatetags.static import static

import pandas as pd
import numpy as np
import os
import boto3

from .Conf import conf

def loadCSV(filename, parse_dates=None):

    if conf.AWS_ACCESS_KEY_ID == '':

        print('No S3 creds found; reading ' + filename + ' from CSV')

        df = pd.read_csv(
            static('data/' + filename),
            parse_dates=parse_dates,
            dayfirst=True)

    else:

        print('Reading ' + filename + ' from S3 (' + conf.S3_BUCKET + ')')

        df = pd.read_csv(
            's3://' + conf.S3_BUCKET + '/' + filename + '.csv',
            parse_dates=parse_dates,
            dayfirst=True)

    return df


def processSocialMediaData(df, platform):

    m = (df.platform == platform)

    # We either get daily figures or cumulative figures from source, so
    # we calculate what we don't have
    if df.loc[m].follows_cum.sum() == 0:
        df.loc[m, 'follows_cum'] = df.loc[m].follows.cumsum()
    if df.loc[m].likes_cum.sum() == 0:
        df.loc[m, 'likes_cum'] = df.loc[m].likes.cumsum()
    if df.loc[m].views_cum.sum() == 0:
        df.loc[m, 'views_cum'] = df.loc[m].views.cumsum()

    # For the reverse of cumsum() we need to do a diff, then
    # set first value to 0
    # This is only valid if you have daily stats from _the beginning
    # of time_ in the source data, otherwise the cumulation doesn't
    # start from the right value and is incorrect. Hiding this data
    # is controlled by the dashboard configuration
    if df.loc[m, 'follows'].sum() == 0 and df.loc[m, 'follows_cum'].sum() != 0:
        df.loc[m, 'follows'] = df.loc[m].follows_cum.diff().fillna(0)
        firstValIndex = list(df.index[m & (df.follows != 0) & ~pd.isnull(df.follows)])[0]
        lastValIndex = list(df.index[m & (df.follows != 0) & ~pd.isnull(df.follows)])[-1]
        df.loc[firstValIndex, 'follows'] = 0
        df.loc[lastValIndex, 'follows'] = 0
    if df.loc[m, 'likes'].sum() == 0 and df.loc[m, 'likes_cum'].sum() != 0:
        df.loc[m, 'likes'] = df.loc[m].likes_cum.diff().fillna(0)
        firstValIndex = list(df.index[m & (df.likes != 0) & ~pd.isnull(df.likes)])[0]
        lastValIndex = list(df.index[m & (df.likes != 0) & ~pd.isnull(df.likes)])[-1]
        df.loc[firstValIndex, 'likes'] = 0
        df.loc[lastValIndex, 'likes'] = 0
    if df.loc[m, 'views'].sum() == 0 and df.loc[m, 'views_cum'].sum() != 0:
        df.loc[m, 'views'] = df.loc[m].views_cum.diff().fillna(0)
        firstValIndex = list(df.index[m & (df.views != 0) & ~pd.isnull(df.views)])[0]
        lastValIndex = list(df.index[m & (df.views != 0) & ~pd.isnull(df.views)])[-1]
        df.loc[firstValIndex, 'views'] = 0
        df.loc[lastValIndex, 'views'] = 0

    # Bokeh doesn't seem to like taking value/label tuples
    # in a linked dropdown/plot, so we will set our col
    # headings to user-friendly terms  now
    df.rename(columns={'follows': 'Daily follows',
                       'likes': 'Daily likes',
                       'views': 'Daily views',
                       'follows_cum': 'Cumulative follows over time',
                       'likes_cum': 'Cumulative likes over time',
                       'views_cum': 'Cumulative views over time'},
              inplace=True)

    df = df.loc[m]

    return df
