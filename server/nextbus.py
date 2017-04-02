#!/usr/bin/python2

from xml.dom import minidom
from datetime import datetime, time
#import time

try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen

def findClosestStop(stops, stop):
    if len(stops) == 0:
        return None
    elif len(stops) == 1:
        return stops[0]
    elif len(stops) == 2:
        # is everyone a happy number?
        if stop.isdigit() and stop[0].isdigit() and stop[1].isdigit():
            # who has the smallest difference?
            if abs(int(stops[0]) - int(stop)) < abs(int(stops[1]) - int(stop)):
                return stops[0]
            else:
                return stops[1]

    mid = int(len(stops)/2 + .5)

    if stops[mid] == stop:
        return stop
    elif stops[mid] < stop:
        return findClosestStop(stops[mid:], stop)
    else:
        return findClosestStop(stops[0:mid], stop)

def isTodaysSchedule(route):
    dow = datetime.strftime(datetime.now(), '%A')

    if ((dow in ['Saturday', 'Sunday'] and route.getAttribute('serviceClass') == dow) or \
        (dow not in ['Saturday', 'Sunday'] and route.getAttribute('serviceClass') != dow)):
        return True
    else:
        return False


def getSchedule(agency, line, stop, direction):
    nextbus_data = {
        'agency': agency,
        'route': line,
        'stop': '',
        'schedule': []
    }

    base_url = 'http://webservices.nextbus.com/service/publicXMLFeed'
    nextbus_xml = urlopen(base_url + '?command=schedule&a=' + agency + '&r=' + line).read()
    dom = minidom.parseString(nextbus_xml)

    # get the closest stop (assuming sane sorting), because not all stops are represented
    arr_stops = []
    for route in dom.getElementsByTagName('route'):
        if route.getAttribute('direction') == direction and isTodaysSchedule(route):
            for header in route.getElementsByTagName('header'):
                for s in header.getElementsByTagName('stop'):
                    arr_stops.append(s.getAttribute('tag'))

    arr_stops = sorted(set(arr_stops))
    closest_stop = findClosestStop(arr_stops, stop)

    # Now, let's get the schedule for this stop
    schedule = []
    for route in dom.getElementsByTagName('route'):
        if route.getAttribute('direction') == direction and isTodaysSchedule(route):
            for tr in route.getElementsByTagName('tr'):
                for s in tr.getElementsByTagName('stop'):
                    if s.getAttribute('tag') == closest_stop:
                        schedule.append(s.firstChild.nodeValue)
    schedule = sorted(set(schedule))

    nextbus_data['stop'] = closest_stop
    nextbus_data['schedule'] = schedule

    return nextbus_data


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
        tmp_prediction['datetime'] = datetime.strptime(time.ctime(float(prediction.getAttribute('epochTime')) / 1000), '%a %b %d %H:%M:%S %Y')
        tmp_prediction['seconds'] = int(prediction.getAttribute('seconds'))
        tmp_prediction['minutes'] = int(prediction.getAttribute('minutes'))
        nextbus_data['predictions'].append(tmp_prediction)

    return nextbus_data
