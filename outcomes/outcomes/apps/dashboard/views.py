from django.shortcuts import render
from bokeh.embed import components
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import column

from . import kpis
from . import charts

def dashboard(request):

    kpi_totalLAs = kpis.totalLAs()
    kpi_laDeclared = kpis.laDeclared()
    kpi_laNetZero2030 = kpis.laNetZero2030()
    kpis_maxDailyWebsiteUsers = '{:,}'.format(kpis.maxDailyWebsiteUsers())

    p_laDecs = charts.laDeclarationsPlot()
    p_laHexMap = charts.laHexMapPlot()
    p_partyNetZero = charts.partyNetZeroPlot()
    p_laNetZero = charts.laNetZeroPlot()
    p_website = charts.websitePlot()
    p_bookSales = charts.bookSalesPlot()

    p_twitter = Panel(child=charts.socialMediaPlot('Twitter'), title='Twitter')
    p_facebook = Panel(child=charts.socialMediaPlot('Facebook'), title='Facebook')
    p_youTube = Panel(child=charts.socialMediaPlot('YouTube'), title='YouTube')
    socialMediaTabs = Tabs(tabs=[p_twitter, p_facebook, p_youTube], css_classes=['chart_tabs'])

    plots = {
        'la_decs_plot': p_laDecs,
        'la_hex_map_plot': p_laHexMap,
        'party_net_zero_plot': p_partyNetZero,
        'la_net_zero_plot': p_laNetZero,
        'website_plot': p_website,
        'social_media_tabs': socialMediaTabs,
        'book_sales_plot': p_bookSales
    }

    script, plotDivs = components(plots)

    return render(
        request,
        'dashboard.html',
        {'script': script,

         'kpi_total_las': kpi_totalLAs,
         'kpi_las_declared': kpi_laDeclared,
         'kpi_las_with_2030_net_zero': kpi_laNetZero2030,
         'kpi_max_website_users': kpis_maxDailyWebsiteUsers,

         'la_decs_title': 'LOCAL AUTHORITIES DECLARING A CLIMATE EMERGENCY',
         'la_decs_plot': plotDivs['la_decs_plot'],

         'la_hex_map_title': 'MAP OF DECLARED LOCAL AUTHORITIES',
         'la_hex_map_plot': plotDivs['la_hex_map_plot'],

         'party_party_net_zero_title': 'POLITICAL NET ZERO TARGETS',
         'party_party_net_zero_plot': plotDivs['party_net_zero_plot'],

         'la_net_zero_title': 'LA NET ZERO TARGETS',
         'la_net_zero_plot': plotDivs['la_net_zero_plot'],

         'website_title': 'WEBSITE VISITS',
         'website_plot': plotDivs['website_plot'],

         'social_media_title': 'SOCIAL MEDIA',
         'social_media_tabs': plotDivs['social_media_tabs'],

         'book_sales_title': 'SALES OF ‘THIS IS NOT A DRILL‘',
         'book_sales_plot': plotDivs['book_sales_plot']
         })
