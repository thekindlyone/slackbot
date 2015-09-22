import requests
from creds import *
url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'.format

def get_report(location):
    try:
        r=requests.get(url(location,weatherAPI))
        data=r.json()
        coords='{},{}'.format(data['coord']['lat'],data['coord']['lon'])
        temp=data['main'].get('temp')
        humidity=data['main'].get('humidity')
        temp_min=data['main'].get('temp_min')
        temp_max=data['main'].get('temp_max')
        pressure=data['main'].get('pressure')
        windspeed=data['wind'].get('speed')
        winddir=data['wind'].get('deg')
        name=data['name']
        country=data['sys'].get('country')
        description=', '.join([weather['description'] for weather in data['weather']])
        
        lines = '''City: {}
    Country: {}
    Coords: {}
    Description: {}
    Temperature: {} deg. C
    Min. Temperature: {} deg. C 
    Max. Temperature: {} deg. C
    Humidity: {}%
    Pressure: {} hPa
    Wind Speed: {} m/s
    Wind Direction: {} deg.'''.split('\n')
        
        params=[name,
                country,
                coords,
                description.capitalize(),
                temp,
                temp_min,
                temp_max,
                humidity,
                pressure,
                windspeed,
                winddir]

        report='\n'.join([line.format(param) for line,param in zip(lines,params) if param])

        return report
    except Exception as e:
        print e
        return data

