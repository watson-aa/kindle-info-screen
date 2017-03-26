import weather
import nextbus
import codecs
from datetime import datetime

# CONFIG
_LATITUDE = 42.243405
_LONGITUDE = -70.9407787

_NEXTBUS_AGENCY = 'mbta'
_NEXTBUS_LINE1 = '220'
_NEXTBUS_STOP1 = '3611'
_NEXTBUS_LINE2 = '221'
_NEXTBUS_STOP2 = '3651'


def generate_image():
    weather_data = weather.getWeather(_LATITUDE, _LONGITUDE)
    nextbus_data = []
    nextbus_data.append(nextbus.getPredictions(_NEXTBUS_AGENCY, _NEXTBUS_LINE1, _NEXTBUS_STOP1))
    nextbus_data.append(nextbus.getPredictions(_NEXTBUS_AGENCY, _NEXTBUS_LINE2, _NEXTBUS_STOP2))

    # Open SVG to process
    svg = codecs.open('preprocess.svg', 'r', encoding='utf-8').read()

    # insert weather
    svg = svg.replace('ICON_ONE', weather_data['day_1']['icon'])
    svg = svg.replace('HIGH_ONE', str(weather_data['day_1']['maximum']))
    svg = svg.replace('LOW_ONE', str(weather_data['day_1']['minimum']))

    # insert bus predictions
    for x in range(1,3):
        svg = svg.replace('LINE_' + str(x) + '_LABEL', nextbus_data[x-1]['route'])
        for y in range(1,3):
            #print nextbus_data[x-1]['predictions'][y-1]['datetime']
            #prediction_time = datetime.strptime(nextbus_data[x-1]['predictions'][y-1]['datetime'], '%Y-%m-%d %H:%M:%S')
            if len(nextbus_data[x-1]['predictions']) >= y:
                prediction_time = datetime.strftime(nextbus_data[x-1]['predictions'][y-1]['datetime'], '%-I:%M %p')
                svg = svg.replace('LINE_' + str(x) + '_TIME_' + str(y), prediction_time)
            else:
                svg = svg.replace('LINE_' + str(x) + '_TIME_' + str(y), 'N/A')

    codecs.open('output.svg', 'w', encoding='utf-8').write(svg)


if __name__ == "__main__":
    generate_image()
