#!/usr/bin/python2

# Kindle Weather Display
# Matthew Petroff (http://mpetroff.net/)
# September 2012

from xml.dom import minidom
from datetime import datetime

try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen

_ICON = {
    'few': 'rain1',
    'sct': 'rain2',
    'ra': 'rain3',
    'hi_shwrs': 'rain3',
    'raip': 'frozen_rain',
    'skc': 'sunny',
    'bkn': 'partly_sunny',
    'few': 'partly_sunny',
    'sct': 'partly_sunny',
    'ovc': 'cloudy',
    'fg': 'fog',
    'smoke': 'fog',
    'fzra': 'mix',
    'ip': 'hail',
    'mix': 'mix',
    'mix': 'hail',
    'rasn': 'mix',
    'shra': 'rain3',
    'tsra': 'tstorm',
    'sn': 'snow',
    'wind': 'windy',
    'hi_shwrs': 'rain1',
    'fzrara': 'mix',
    'hi_tsra': 'tstorm',
    'ra1': 'rain1',
    'ra': 'rain3',
    'nsvrtsra': 'tornado',
    'dust': 'dusty',
    'mist': 'fog'
}

#
# Download and parse weather data, based on latitude/longitude
#
def getWeather(latitude, longitude):
    # Fetch data (change lat and lon to desired location)
    weather_xml = urlopen('http://graphical.weather.gov/xml/SOAP_server/ndfdSOAPclientByDay.php?whichClient=NDFDgenByDay&lat=' + str(latitude) + '&lon=' + str(longitude) + '&format=24+hourly&numDays=4&Unit=e').read()
    dom = minidom.parseString(weather_xml)

    weather_data = {
        'day_1': {
            'date': '2017-01-01',
            'maximum': -1,
            'minimum': -1,
            'icon': ''
        },
        'day_2': {
            'date': '2017-01-02',
            'maximum': -1,
            'minimum': -1,
            'icon': ''
        },
        'day_3': {
            'date': '2017-01-03',
            'maximum': -1,
            'minimum': -1,
            'icon': ''
        },
        'day_4': {
            'date': '2017-01-04',
            'maximum': -1,
            'minimum': -1,
            'icon': ''
        }
    }

    # Parse temperatures
    xml_temperatures = dom.getElementsByTagName('temperature')
    highs = [None]*4
    lows = [None]*4
    for x, item in enumerate(xml_temperatures):
        for type in ['maximum', 'minimum']:
            if item.getAttribute('type') == type:
                values = item.getElementsByTagName('value')
                for i in range(len(values)):
                    weather_data['day_' + str(i+1)][type] = int(values[i].firstChild.nodeValue)

    # Parse icons
    xml_icons = dom.getElementsByTagName('icon-link')
    icons = [None]*4
    for i in range(len(xml_icons)):
        firstChild = xml_icons[i].firstChild
        if firstChild is not None:
            weather_data['day_' + str(i+1)]['icon'] = _ICON[firstChild.nodeValue.split('/')[-1].split('.')[0].rstrip('0123456789')]

    # Parse dates
    xml_days = dom.getElementsByTagName('start-valid-time')
    for x, item in enumerate(xml_days):
        if x < 4:
            weather_data['day_' + str(x+1)]['date'] = datetime.strptime(item.firstChild.nodeValue[0:10], '%Y-%m-%d')
        else:
            break

    return weather_data
