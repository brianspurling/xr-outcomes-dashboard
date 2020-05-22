import environ
env = environ.Env()
environ.Env.read_env()  # reads the .env file

HOURS_BETWEEN_DATA_REFRESH = env.float('HOURS_BETWEEN_DATA_REFRESH', default=24)

GA_TRACKING_ID = env('GA_TRACKING_ID')

START_DATE_OF_TIME_SERIES = '2018-12-01'

LOGO_FILENAME = 'xr_logo.png'

LOCAL_DATA_DIR = '../data/'

# This is updated to True by Models and used in UI to display warning to user
DATA_REFRESH_WARNING = False

MISSING_COMMENTARY_TEXT = 'Commentary for this chart is missing'

################
# Chart Config #
################

SOCIAL_MEDIA_DROPDOWN_OPTIONS = {
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
    'instagram': [
        # 'Cumulative follows over time'
        # 'Cumulative views over time'
        'Daily follows',
        'Daily likes'],
}

BG_IMG_URLS = [
    'human_skull_sad.png',
    'human_skull.svg',
    'butterfly.png',
    'bird_01.png',
    'animal_skull_01.png',
    'bird_02.png',
    'hour_glass.png',
    'animal_skull_02.png',
    'plant.png',
    'bee.png',
    'eye.png']

####################
# Chart Formatting #
####################

FONT_CRIMSON_TEXT = 'Crimson Text'
FONT_CONTENT_DEFAULT = FONT_CRIMSON_TEXT

WHITE = 'white'
BLACK = 'black'
PINK = '#ED9BC4'
GREEN = '#14AA37'
LEMON = '#F7EE6A'

TOOLS = ''  # Default no Bokeh tools on the charts

DASHBOARD_WIDTH = 1000

PLOT_WIDTH = 800
PLOT_HEIGHT = 400

COMMENTARY_WIDTH = 280
COMMENTARY_MAX_HEIGHT = 500

# Axes lines are the main x and y lines

AXIS_LINE_WIDTH = 14
AXIS_LINE_CAP = 'round'

# Axes labels are the titles on each axis

AXIS_LABEL_STANDOFF = 20
AXIS_LABEL_TEXT_FONT = FONT_CONTENT_DEFAULT
AXIS_LABEL_TEXT_FONT_STYLE = 'bold'
AXIS_LABEL_TEXT_COLOR = BLACK
AXIS_LABEL_TEXT_FONT_SIZE = '16pt'

CHART_MIN_BORDER_LEFT = 110  # Enough for space for largest line chart y axis labels
CHART_MIN_BORDER_RIGHT = 25  # Just enough to avoid last x axis label being cut
CHART_MIN_BORDER_TOP =  25   # as above

# Major and minor ticks & labels are the scale on each axis

MAJOR_TICK_LINE_CAP = 'round'
MAJOR_TICK_LINE_WIDTH = 7
MAJOR_TICK_OUT = 13

MAJOR_LABEL_STANDOFF = 20
MAJOR_LABEL_TEXT_FONT = FONT_CONTENT_DEFAULT
MAJOR_LABEL_TEXT_FONT_STYLE = 'normal'
MAJOR_LABEL_TEXT_SIZE = '15pt'
MAJOR_LABEL_TEXT_COLOR = BLACK

# The data series for line charts

CHART_LINE_COLOR = PINK
CHART_LINE_WIDTH_THIN = 7
CHART_LINE_CAP = 'round'

# The data series for bar charts

BAR_BORDER_COLOR = WHITE
BAR_BORDER_WIDTH = 2
FILL_COLOUR = [LEMON, PINK]
BAR_WIDTH = 0.7  # # Bar chart column width (defines gap between)
CHART_RANGE_PADDING = 0.05

# The data series for box and whisker

WHISKER_LINE_COLOR = PINK
WHISKER_LINE_WIDTH = 14
WHISKER_LINE_CAP = 'round'
BOX_FILL_COLOR = LEMON
BOX_LINE_COLOR = LEMON
BOX_LINE_CAP = 'round'
BOX_LINE_WIDTH = 5

# Other
DROPDOWN_LIST_WIDTH = 260
