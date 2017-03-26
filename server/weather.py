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

#
# Geographic location
#

#latitude = 42.243405
#longitude = -70.9407787



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
        #output['day_1']['minimum'] = 72
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
            weather_data['day_' + str(i+1)]['icon'] = firstChild.nodeValue.split('/')[-1].split('.')[0].rstrip('0123456789')
            #icons[i] = firstChild.nodeValue.split('/')[-1].split('.')[0].rstrip('0123456789')

    # Parse dates
    xml_days = dom.getElementsByTagName('start-valid-time')
    for x, item in enumerate(xml_days):
        if x < 4:
            weather_data['day_' + str(x+1)]['date'] = datetime.strptime(item.firstChild.nodeValue[0:10], '%Y-%m-%d')
        else:
            break

    return weather_data

    '''
    nextbus_config = [
        {
            'line': '220',
            'stop': '3611'
        },
        {
            'line': '221',
            'stop': '3651'
        }
    ]

    #
    # Preprocess SVG
    #

    # Open SVG to process
    output = codecs.open('weather-script-preprocess.svg', 'r', encoding='utf-8').read()

    # Insert icons and temperatures
    output = output.replace('ICON_ONE',icons[0])
    output = output.replace('HIGH_ONE',str(highs[0]))
    output = output.replace('LOW_ONE',str(lows[0]))

    for x, config in enumerate(nextbus_config):
        output = output.replace('LINE_' + str(x+1) + '_LABEL', config['line'])
        nextbus_xml = urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=mbta&r=' + config['line'] + '&s=' + config['stop']).read()

        dom = minidom.parseString(nextbus_xml)
        base = dom.getElementsByTagName('predictions')[0]
        stopTitle = base.getAttribute('stopTitle')
        routeTitle = base.getAttribute('routeTitle')
        predictions = dom.getElementsByTagName('prediction')
        predictions.sort(key=lambda x: x.getAttribute('epochTime'))
        for y, prediction in enumerate(predictions):
            datetime.strptime(time.ctime(float(prediction.getAttribute('epochTime')) / 1000), '%a %b %d %H:%M:%S %Y')

            prediction_time = datetime.strptime(time.ctime(float(prediction.getAttribute('epochTime')) / 1000), '%a %b %d %H:%M:%S %Y') #'%-I:%m %p'
            output = output.replace('LINE_' + str(x+1) + '_TIME_' + str(y+1), datetime.strftime(prediction_time, '%-I:%m %p'))
        for z in range(len(predictions) + 1, 2+1):
            output = output.replace('LINE_' + str(x+1) + '_TIME_' + str(z), 'N/A   ')


    '''

    '''
    # Insert days of week
    one_day = datetime.timedelta(days=1)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    output = output.replace('DAY_THREE',days_of_week[(day_one + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(day_one + 3*one_day).weekday()])
    '''

    '''
    # Write output
    codecs.open('weather-script-output.svg', 'w', encoding='utf-8').write(output)
    '''
