from django.templatetags.static import static

import pandas as pd


def totalLAs():
    df = pd.read_csv(static('data/local_authorities.csv'))
    total = df.shape[0]
    return total


def laDeclared():
    df = pd.read_csv(static('data/local_authorities.csv'))
    declared = df.loc[~pd.isnull(df.declaration_date)].shape[0]
    return declared


def laNetZero2030():
    df = pd.read_csv(static('data/local_authorities.csv'))
    netZero2030 = df.loc[df.target_net_zero_year <= 2030].shape[0]
    return netZero2030


def maxDailyWebsiteUsers():
    df = pd.read_csv(static('data/website.csv'))
    maxUsers = df.sessions.max()
    return maxUsers
