from django.templatetags.static import static
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.conf import settings as conf

from datetime import datetime, timedelta
import csv
import pandas as pd
import numpy as np


def isDataStale(model):
    dataIsStale = False
    loadHistoryQS = LoadHistory.objects.filter(table_name=model.__name__)
    loadHistoryQS = loadHistoryQS.order_by('-last_load_time')
    lastLoad = loadHistoryQS.values('last_load_time').first()
    if lastLoad is None:
        dataIsStale = True
    elif lastLoad['last_load_time'] + timedelta(hours=conf.HOURS_BETWEEN_DATA_REFRESH) < timezone.now():
        dataIsStale = True
    if dataIsStale:
        print()
        print(model.__name__ + ': refreshing data from source CSV')
    return dataIsStale


def readCSV(model):

    # File can come from S3 or local

    if conf.AWS_ACCESS_KEY_ID == '':
        print(model.__name__ +
              ': no S3 creds found; reading ' +
              model.csv_filename + ' from CSV')
        filePath = conf.LOCAL_DATA_DIR + model.csv_filename + '.csv'
    else:
        print(model.__name__ + ': reading ' + model.csv_filename +
              ' from S3 (' + conf.S3_BUCKET + ')')
        filePath = \
            's3://' + conf.S3_BUCKET + '/' + \
            model.csv_filename + '.csv'

    # Read in pandas to provide robust date parsing, and
    # efficient conversion to Django model-friendly list of dicts

    try:
        df = pd.read_csv(
            filePath,
            parse_dates=model.parse_dates,
            dayfirst=True)
    except (FileNotFoundError, PermissionError) as e:
        print(model.__name__ + ': ERROR opening file. Refreshed aborted')
        conf.DATA_REFRESH_WARNING = True
        df = None

    return df


def df_to_dict(df):

    # Django's bulk create works efficiently with a list of dicts, but
    # unfortunately is can't cope with NaN and NaT values, so we manually
    # replace with None

    data = df.to_dict('records')
    for rec in data:
        for key in rec:
            if pd.isnull(rec[key]):
                rec[key] = None

    return data


def updateDatabase(model, batch):

    try:
        for o in batch:
            # full_clean calls clean_fields(), clean(), validate_unique()
            o.full_clean()
    except ValidationError as e:
        print(model.__name__ + ': ERROR in data. Refreshed aborted: ' +
              str(e.message_dict))
        conf.DATA_REFRESH_WARNING = True
    else:

        # Immediately before creating the new records, delete the old ones

        model.objects.all().delete()

        model.objects.bulk_create(batch)

        # Update the load history so we avoid loading again until next refresh

        (lh, created) = LoadHistory.objects.get_or_create(
            table_name=model.__name__,
            defaults={'last_load_time': timezone.now()})
        lh.last_load_time = timezone.now()
        lh.save()

        print(model.__name__ + ': done')


def convertQuerySetToDict(querySet):
    d = {}
    for i, c in enumerate(querySet):
        if i == 0:
            for key in c:
                d[key] = []
        for key in c:
            d[key].append(c[key])
    return d


def genericRepr(model):
    r = ''
    for fieldName in model._meta.fields:
        fieldName = str(fieldName).split('.')[2]
        r += str(fieldName) + ': ' + str(getattr(model, fieldName)) + '\n'
    return r


class LoadHistory(models.Model):
    table_name = models.TextField(primary_key=True)
    last_load_time = models.DateTimeField()



class LocalAuthoritiesManager(models.Manager):

    def refreshFromCSV(self):
        df = readCSV(self.model)
        if df is not None:
            df.is_declared = np.where(df.is_declared == 'YES', True, False)
            batch = [LocalAuthorities(**row) for row in df_to_dict(df)]
            updateDatabase(self.model, batch)


    def getAll(self):

        if isDataStale(self.model):
            self.refreshFromCSV()

        dataQS = self.model.objects.values()
        data = convertQuerySetToDict(dataQS)

        data['declaration_date_str'] = []
        for i in range(0, len(data['declaration_date'])):
            if data['declaration_date'][i] is None:
                data['declaration_date_str'].append('Not declared')
            else:
                data['declaration_date'][i] = \
                    datetime.combine(data['declaration_date'][i], datetime.min.time())
                data['declaration_date_str'].append(
                    data['declaration_date'][i].strftime('%d %b %Y'))

        return data


class LocalAuthorities(models.Model):

    csv_filename = 'local_authorities'
    parse_dates = ['declaration_date']

    code = models.TextField()
    ons_la_name = models.TextField()
    xr_la_name = models.TextField()
    is_declared = models.BooleanField()
    declaration_date = models.DateField(blank=True, null=True)
    target_net_zero_year = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    objects = LocalAuthoritiesManager()

    def __repr__(self):
        return genericRepr(self)


class PoliticalPartiesManager(models.Manager):

    def refreshFromCSV(self):
        df = readCSV(self.model)
        if df is not None:
            df.is_political_org = np.where(df.is_political_org == 'YES', True, False)
            batch = [PoliticalParties(**row) for row in df_to_dict(df)]
            updateDatabase(self.model, batch)

    def getAll(self):

        if isDataStale(self.model):
            self.refreshFromCSV()

        dataQS = self.model.objects.order_by('-target_net_zero_year').values()
        data = convertQuerySetToDict(dataQS)

        data['start_year'] = []
        data['end_year'] = []
        data['vote_pcnt_str'] = []
        for i in range(0, len(data['date_call_made'])):
            data['date_call_made'][i] = \
                datetime.combine(data['date_call_made'][i], datetime.min.time())
            data['start_year'].append(
                data['target_net_zero_year'][i] - 0.5)
            data['end_year'].append(
                data['target_net_zero_year'][i] + 0.5)
            data['vote_pcnt_str'].append(
                str(round(data['vote_pcnt'][i],1)) + '%')

        return data


class PoliticalParties(models.Model):

    csv_filename = 'political_parties'
    parse_dates = ['date_call_made']

    org_name = models.TextField()
    is_political_org = models.BooleanField()
    date_call_made = models.DateField()
    target_net_zero_year = models.IntegerField()
    earliest_year = models.IntegerField()
    latest_year = models.IntegerField()
    vote_pcnt = models.FloatField()

    objects = PoliticalPartiesManager()

    def __repr__(self):
        return genericRepr(self)


class SocialMediaManager(models.Manager):

    def refreshFromCSV(self):
        df = readCSV(self.model)
        if df is not None:
            batch = [SocialMedia(**row) for row in df_to_dict(df)]
            updateDatabase(self.model, batch)

    def getAll(self):

        if isDataStale(self.model):
            self.refreshFromCSV()

        dataQS = self.model.objects.order_by('platform', 'date').values()
        data = convertQuerySetToDict(dataQS)

        data['date_str'] = []
        for i in range(0, len(data['date'])):
            data['date'][i] = \
                datetime.combine(data['date'][i], datetime.min.time())
            data['date_str'].append(
                data['date'][i].strftime('%d %b %Y'))

        return data


class SocialMedia(models.Model):

    csv_filename = 'social_media'
    parse_dates = ['date']

    platform = models.TextField()
    account_id = models.TextField()
    date = models.DateField()
    follows = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    follows_cum = models.IntegerField(blank=True, null=True)
    likes_cum = models.IntegerField(blank=True, null=True)
    views_cum = models.IntegerField(blank=True, null=True)

    objects = SocialMediaManager()

    def __repr__(self):
        return genericRepr(self)


class InstagramManager(models.Manager):

    def refreshFromCSV(self):
        df = readCSV(self.model)
        if df is not None:
            batch = [Instagram(**row) for row in df_to_dict(df)]
            updateDatabase(self.model, batch)

    def getAll(self):

        if isDataStale(self.model):
            self.refreshFromCSV()

        dataQS = self.model.objects.order_by('date').values()
        data = convertQuerySetToDict(dataQS)

        data['date_str'] = []
        for i in range(0, len(data['date'])):
            data['date'][i] = \
                datetime.combine(data['date'][i], datetime.min.time())
            data['date_str'].append(
                data['date'][i].strftime('%d %b %Y'))

        return data


class Instagram(models.Model):

    csv_filename = 'instagram'
    parse_dates = ['date']

    date = models.DateField()
    follows_cum = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)

    objects = InstagramManager()

    def __repr__(self):
        return genericRepr(self)


class WebsiteManager(models.Manager):

    def refreshFromCSV(self):
        df = readCSV(self.model)
        if df is not None:
            batch = [Website(**row) for row in df_to_dict(df)]
            updateDatabase(self.model, batch)

    def getAll(self):

        if isDataStale(self.model):
            self.refreshFromCSV()

        dataQS = self.model.objects.order_by('date').values()
        data = convertQuerySetToDict(dataQS)

        data['date_str'] = []
        data['sessions_str'] = []
        for i in range(0, len(data['date'])):
            data['date'][i] = \
                datetime.combine(data['date'][i], datetime.min.time())
            data['date_str'].append(
                data['date'][i].strftime('%d %b %Y'))
            data['sessions_str'].append(
                '{:,.0f}'.format(data['sessions'][i]))

        return data


class Website(models.Model):

    csv_filename = 'website'
    parse_dates = ['date']

    domain = models.TextField()
    date = models.DateField()
    page_views = models.IntegerField()
    sessions = models.IntegerField()

    objects = WebsiteManager()

    def __repr__(self):
        return genericRepr(self)


class ActionNetworkManager(models.Manager):

    def refreshFromCSV(self):
        df = readCSV(self.model)
        if df is not None:
            batch = [ActionNetwork(**row) for row in df_to_dict(df)]
            updateDatabase(self.model, batch)

    def getAll(self):

        if isDataStale(self.model):
            self.refreshFromCSV()

        dataQS = self.model.objects.order_by('date').values()
        data = convertQuerySetToDict(dataQS)

        data['date_str'] = []
        data['daily_str'] = []
        data['cumulative_str'] = []
        for i in range(0, len(data['date'])):
            data['date'][i] = \
                datetime.combine(data['date'][i], datetime.min.time())
            data['date_str'].append(
                data['date'][i].strftime('%d %b %Y'))
            data['daily_str'].append(
                '{:,.0f}'.format(data['daily'][i]))
            data['cumulative_str'].append(
                '{:,.0f}'.format(data['cumulative'][i]))

        return data


class ActionNetwork(models.Model):

    csv_filename = 'action_network'
    parse_dates = ['date']

    date = models.DateField()
    daily = models.IntegerField()
    cumulative = models.IntegerField()

    objects = ActionNetworkManager()

    def __repr__(self):
        return genericRepr(self)


class BookSalesManager(models.Manager):

    def refreshFromCSV(self):
        df = readCSV(self.model)
        if df is not None:
            batch = [BookSales(**row) for row in df_to_dict(df)]
            updateDatabase(self.model, batch)

    def getAll(self):

        if isDataStale(self.model):
            self.refreshFromCSV()

        dataQS = self.model.objects.order_by('date').values()
        data = convertQuerySetToDict(dataQS)

        data['date_str'] = []
        data['sales_str'] = []
        data['sales_cum'] = []
        sales = 0
        for i in range(0, len(data['date'])):
            data['date'][i] = \
                datetime.combine(data['date'][i], datetime.min.time())
            data['date_str'].append(
                data['date'][i].strftime('%d %b %Y'))
            data['sales_str'].append(
                '{:,.0f}'.format(data['sales'][i]))

            sales = sales + data['sales'][i]
            data['sales_cum'].append(sales)


        return data


class BookSales(models.Model):

    csv_filename = 'book_sales'
    parse_dates = ['date']

    date = models.DateField()
    sales = models.IntegerField()

    objects = BookSalesManager()

    def __repr__(self):
        return genericRepr(self)


class CommentaryManager(models.Manager):

    def getAll(self):

        dataQS = self.model.objects.values()
        data = convertQuerySetToDict(dataQS)

        return data

    def getOne(self, chartName):

        return self.model.objects.get(chart_name=chartName)


class Commentary(models.Model):
    csv_filename = 'commentary'
    chart_name = models.TextField(primary_key=True)
    commentary_text = models.TextField(blank=False, max_length=550)
    objects = CommentaryManager()

    def __str__(self):
        return self.chart_name

    def __repr__(self):
        return genericRepr(self)
