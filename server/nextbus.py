#!/usr/bin/python2

from xml.dom import minidom
from datetime import datetime
import time

try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen

def getPredictions(agency, line, stop):
    nextbus_data = {
        'agency': '',
        'route': '',
        'stop': '',
        'predictions': []
    }

    base_url = 'http://webservices.nextbus.com/service/publicXMLFeed'
    nextbus_xml = urlopen(base_url + '?command=predictions&a=' + agency + '&r=' + line + '&s=' + stop).read()
    dom = minidom.parseString(nextbus_xml)
    base = dom.getElementsByTagName('predictions')[0]
    if base is not None:
        nextbus_data['agency'] = base.getAttribute('agencyTitle')
        nextbus_data['route'] = base.getAttribute('routeTitle')
        nextbus_data['stop'] = base.getAttribute('stopTitle')

    predictions = dom.getElementsByTagName('prediction')
    # sort by time
    predictions.sort(key=lambda x: x.getAttribute('epochTime'))

    for y, prediction in enumerate(predictions):
        tmp_prediction = {}

        datetime.strptime(time.ctime(float(prediction.getAttribute('epochTime')) / 1000), '%a %b %d %H:%M:%S %Y')
        tmp_prediction['datetime'] = datetime.strptime(time.ctime(float(prediction.getAttribute('epochTime')) / 1000), '%a %b %d %H:%M:%S %Y') #'%-I:%m %p'
        tmp_prediction['seconds'] = int(prediction.getAttribute('seconds'))
        tmp_prediction['minutes'] = int(prediction.getAttribute('minutes'))
        nextbus_data['predictions'].append(tmp_prediction)

    return nextbus_data
