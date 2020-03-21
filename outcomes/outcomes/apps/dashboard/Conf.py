from django.conf import settings

from configobj import ConfigObj
import os


class Conf():

    def __init__(self):
        pass

    def loadConfig(self):
        configFilePath = os.path.join(settings.BASE_DIR, 'outcomes/apps/dashboard/config.ini')
        self.confDict = dict(**ConfigObj(configFilePath))
        for var in self.confDict:
            setattr(Conf, var, self.confDict[var])

        # We get our S3 creds from 1. environment variables, 2. config.ini
        # If neither, set to None (and app will attempt to load from CSV)
        if 'AWS_ACCESS_KEY_ID' not in os.environ or 'AWS_SECRET_ACCESS_KEY' not in os.environ or 'S3_BUCKET' not in os.environ:

            if hasattr(self, 'AWS_ACCESS_KEY_ID') and hasattr(self, 'AWS_SECRET_ACCESS_KEY') and hasattr(self, 'S3_BUCKET'):

                os.environ["AWS_ACCESS_KEY_ID"] = self.AWS_ACCESS_KEY_ID
                os.environ["AWS_SECRET_ACCESS_KEY"] = self.AWS_SECRET_ACCESS_KEY
                os.environ["S3_BUCKET"] = self.S3_BUCKET

            else:

                os.environ["AWS_ACCESS_KEY_ID"] = ''
                os.environ["AWS_SECRET_ACCESS_KEY"] = ''
                os.environ["S3_BUCKET"] = ''

        self.AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
        self.AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
        self.S3_BUCKET = os.environ["S3_BUCKET"]

        self.WARNINGS = []

        self.start_date_of_time_series = '2019-01-01'

        self.logo_filename = 'XR-logo-RGB-Black-Linear.png'

        ################
        # Chart Config #
        ################

        self.SOCIAL_MEDIA_DROPDOWN_OPTIONS = {
            'twitter': [
                'Cumulative follows over time',
                # 'Cumulative likes over time',
                #'Daily follows',
                'Daily likes'],
            'facebook': [
                'Cumulative follows over time',
                # 'Cumulative likes over time'
                #'Daily follows',
                'Daily likes'],
            'youtube': [
                # 'Cumulative follows over time'
                # 'Cumulative views over time'
                'Daily follows',
                'Daily views'],
        }

        self.BG_IMG_URLS = [
            'skull-charcoal-sad.png',
            'skull-charcoal.svg',
            'output-onlinepngtools (0).png',
            'output-onlinepngtools (1).png',
            'output-onlinepngtools (2).png',
            'output-onlinepngtools (3).png',
            'output-onlinepngtools (4).png',
            'output-onlinepngtools (5).png',
            'output-onlinepngtools (6).png',
            'output-onlinepngtools (8).png',
            'output-onlinepngtools (9).png']

        ####################
        # Chart Formatting #
        ####################

        self.font_crimson_text = 'Crimson Text'
        self.font_content_default = self.font_crimson_text

        self.white = 'white'
        self.black = 'black'
        self.pink = '#ED9BC4'
        self.green = '#14AA37'
        self.lemon = '#F7EE6A'

        self.tools = ''  # Or a list of tool names

        self.dashboard_width = 1000

        self.plot_width = 800
        self.plot_height = 400

        self.commentary_width = 280
        self.commentary_height = 400

        # Axes lines are the main x and y lines

        self.axis_line_width = 14
        self.axis_line_cap = 'round'

        # Axes labels are the titles on each axis

        self.axis_label_standoff = 20
        self.axis_label_text_font = self.font_content_default
        self.axis_label_text_font_style = 'bold'
        self.axis_label_text_color = self.black
        self.axis_label_text_font_size = '16pt'

        self.chart_min_border_left = 110  # Enough for space for largest line chart y axis labels
        self.chart_min_border_right = 25  # Just enough to avoid last x axis label being cut
        self.chart_min_border_top =  25   # as above

        # Major and minor ticks & labels are the scale on each axis

        self.major_tick_line_cap = 'round'
        self.major_tick_line_width = 7
        self.major_tick_out = 13

        self.major_label_standoff = 20
        self.major_label_text_font = self.font_content_default
        self.major_label_text_font_style = 'normal'
        self.major_label_text_font_size = '15pt'
        self.major_label_text_color = self.black

        self.major_tick_line_cap = 'round'
        self.major_tick_line_width = 7
        self.major_tick_out = 13

        # The data series for line charts

        self.chart_line_colour = self.pink
        self.chart_line_width_thin = 7
        self.chart_line_cap = 'round'

        # The data series for bar charts

        self.bar_border_color = self.white
        self.bar_border_width = 2
        self.fill_color = [conf.lemon, conf.pink]
        self.bar_width = 0.7  # # Bar chart column width (defines gap between)
        self.chart_range_padding = 0.05

        # The data series for box and whisker

        self.whisker_line_color = self.pink
        self.whisker_line_width = 14
        self.whisker_line_cap = 'round'
        self.box_fill_color = self.lemon
        self.box_line_color = self.lemon
        self.box_line_cap = 'round'
        self.box_line_width = 5

        # Other
        self.dropdown_list_width = 260

# We instantiate the class immediately so all
# modules can import the same object
conf = Conf()
conf.loadConfig()
