from django.templatetags.static import static

from .models import Website, LocalAuthorities

import pandas as pd


def totalLAs():
    data = LocalAuthorities.objects.getAll()
    total = len(data['code'])
    return total


def laDeclared():
    df = pd.DataFrame(LocalAuthorities.objects.getAll())
    declared = df.loc[~pd.isnull(df.declaration_date)].shape[0]
    return declared


def laNetZero2030():
    df = pd.DataFrame(LocalAuthorities.objects.getAll())
    netZero2030 = df.loc[df.target_net_zero_year <= 2030].shape[0]
    return netZero2030


def maxDailyWebsiteUsers():
    df = pd.DataFrame(Website.objects.getAll())
    maxUsers = df.sessions.max()
    return maxUsers
