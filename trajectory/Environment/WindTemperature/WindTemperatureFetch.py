'''
Created on 23 juil. 2024

@author: robert

https://aviationweather.gov/data/windtemp/?region=bos&fcst=12&level=high
https://www.weather.gov/documentation/services-web-api
https://www.faa.gov/regulationspolicies/handbooksmanuals/aviation/phak/chapter-13-aviation-weather-services

'''

import requests

URL = "https://aviationweather.gov/api/data/windtemp/"

USregions = {
        "all"            : "all",
        "All"            : "all",
        "NorthEast"      : "bos",
        "SouthEast"      : "mia",
        "NorthCentral"   : "chi",
        "SouthCentral"   : "dfw",
        "RockyMountains" : "slc",
        "PacificCoast"   : "sfo",
        "Alaska"         : "alaska",
        "Hawaii"         : "hawaii",
        "WestPacific"    : "other_pac"
    }

ForecastHours = {
        "06-Hour" : "06",
        "06"      : "06",
        "12-Hour" : "12",
        "12"      : "12",
        "24-Hour" : "24",
        "24"      : "24"
    }

Levels = {
        "low" : "low",
        "high": "high"
    }

def fetchWindTemperature(USregion, ForecastHour, Level):
    pass
    weatherDataStrList = []
    if USregion in USregions:
        print ( USregion + " is in US regions dictionary")
        url = URL + "?" + "region=" + USregions[USregion]
        print (url)
        if ForecastHour in ForecastHours:
            print ( ForecastHour + " is in the Forecasts dictionary ")
            url = url + "&" + "fcst=" + ForecastHours[ForecastHour]
            print (url)
            if Level in Levels:
                print ( Level + " is in the Levels dictionary ")
                url = url + "&" + "level=" + Level.lower()
                print ( url )
                
                try:
                    #response = requests.get(url, timeout=16.0, headers={"Accept": "application/geo+json"})
                    response = requests.get(url, timeout=16.0, headers={"Accept": "text/xml"})
                    #response = requests.get(url, timeout=16.0)
                    #rq.raise_for_status()
                    print ( response.status_code )
                    if response.status_code == requests.codes.ok:
                        print ( "answer is OK")
                        #intext = str(response.json())
                        #print ( intext )
                        #print ( response.text )
                        weatherDataStrList = str( response.text ).splitlines()
                        
                        #print ( intext.replace( "True" , "'True'" ) )
                except Exception as err:
                    print ( "Exception = {0}".format(err) )
            
        else:
            print ("Error = unknown Forecast hour = {0}".format(ForecastHour))
    else:
        print ( "Error = unknown US region = {0}".format(USregion) )
    return weatherDataStrList