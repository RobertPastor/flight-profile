'''
Created on 23 juil. 2024

@author: robert

https://aviationweather.gov/data/windtemp/?region=bos&fcst=12&level=high

The forecasts are made twice a day based on the
radio-sonde upper air observations taken at 0000Z and 1200Z

Altitudes through 12,000 feet are classified as true altitudes,
while altitudes 18,000 feet and above are classified as
altitudes and are termed flight levels

'''

import logging
logger = logging.getLogger(__name__)
import io
from datetime import datetime 
from xlsxwriter import Workbook
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


from trajectory.Environment.WindTemperature.WindTemperatureFetch import fetchWindTemperature
from trajectory.Environment.WindTemperature.WindTemperatureHeader import WindTemperatureHeader
from trajectory.Environment.WindTemperature.WindTemperatureFeet import WeatherStationFeet


def writeReadMeRow(worksheet, row, headerStr , styleHeader, dataStr,  styleData):
    worksheet.write(row, 0 , headerStr, styleHeader)
    worksheet.write(row, 1 , dataStr, styleData)
    

def writeReadMe(workbook, request, airlineName, windTemperatureList):

    wsReadMe = workbook.add_worksheet("ReadMe")
    styleEntete = workbook.add_format({'bold': False, 'border':True})
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    windTemperatureHeader = WindTemperatureHeader()
    windTemperatureHeader.analyseHeader( windTemperatureList )
    
    row = 0
    writeReadMeRow(wsReadMe, row, "Airline Services" , styleLavender , "Wind and Temperature aloft", styleEntete)
    
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Transmission day" , styleLavender , windTemperatureHeader.getTransmissionDay(), styleEntete)
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Measurement day" , styleLavender , windTemperatureHeader.getMeasurementDay(), styleEntete)
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Validity day" , styleLavender , windTemperatureHeader.getValidityDay(), styleEntete)
    
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Transmission Time (Zulu)" , styleLavender , windTemperatureHeader.getTransmissionTimeZulu(), styleEntete)
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Measurement Time (Zulu)" , styleLavender , windTemperatureHeader.getMeasurementTimeZulu(), styleEntete)
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Validity Time (Zulu)" , styleLavender , windTemperatureHeader.getValidityTimeZulu(), styleEntete)
    
    row = row + 1
    writeReadMeRow(wsReadMe, row, "For Use Begin Time (Zulu)" , styleLavender , windTemperatureHeader.getForUseBeginTimeZulu(), styleEntete)
    row = row + 1
    writeReadMeRow(wsReadMe, row, "For Use End Time (Zulu)" , styleLavender , windTemperatureHeader.getForUseEndTimeZulu(), styleEntete)

    
    wsReadMe.autofit()
    
def writeRawData(workbook, request, airlineName , windTemperatureList):
    assert ( isinstance ( windTemperatureList , list))
    wsRawData = workbook.add_worksheet("Raw Data")
    styleData = workbook.add_format({'bold': False, 'border':True})
    row = 0
    for textLine in windTemperatureList:
        wsRawData.write(row , 0 , textLine , styleData)
        row = row + 1
        
    wsRawData.autofit()
    
def writeWeatherStationData(workbook, request, airlineName , windTemperatureList):
    assert ( isinstance ( windTemperatureList , list))
    wsWeatherStationData = workbook.add_worksheet("Weather Station Data")
    styleData = workbook.add_format({'bold': False, 'border':True})
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})

    weatherStationFeet = WeatherStationFeet()
    feetLevels = weatherStationFeet.readTextLines(windTemperatureList)
    row = 0
    col = 0
    wsWeatherStationData.write(row, 0 , "FT", styleLavender)
    for feetLevel in feetLevels:
        col = col + 1
        wsWeatherStationData.write(row, col , str(feetLevel), styleLavender)
        
    wsWeatherStationData.autofit()

def createExcelWorkbook(memoryFile, request, airlineName, windTemperatureList):
    ''' create the workbook '''
    wb = Workbook(memoryFile)
    ''' write the readme sheet '''
    writeReadMe(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    writeRawData(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    writeWeatherStationData(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    return wb


@csrf_protect
def getWindTemperatureExcel(request, airlineName):
    
    logger.setLevel(logging.INFO)
    logging.info ("get Wind Temperature - for airline = {0}".format(airlineName))
        
    if (request.method == 'GET'):
        logger.debug ( "=========== create output files  =========== " )
        
        windTemperatureList = fetchWindTemperature(USregion="All", ForecastHour="12-Hour", Level="low")
                    
        ''' Robert - python2 to python 3 '''
        memoryFile = io.BytesIO() # create a file-like object 
                        
        # warning : we get strings from the URL query
        wb = createExcelWorkbook(memoryFile, request, airlineName, windTemperatureList)
                                
        ''' create Excel Output sheet using an existing workbook '''
        #flightPath.createStateVectorOutputSheet(wb) 
        wb.close()
                                
        filename = 'WindTemperature-{}.xlsx'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                                #print filename
                                
        response = HttpResponse( memoryFile.getvalue() )
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8'
        #response['Content-Type'] = 'application/vnd.ms-excel'
        response["Content-Transfer-Encoding"] = "binary"
        response['Set-Cookie'] = 'fileDownload=true; path=/'
        response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=filename)
        response['Content-Length'] = memoryFile.tell()
        return response    
    
    else:
        logger.debug ('expecting a GET - received something else = {0}'.format(request.method))
        response_data = {'errors' : 'expecting a GET - received something else = {0}'.format(request.method)}
        return JsonResponse(response_data)
        

if __name__ == '__main__':

    USregion = "All"
    ForecastHour = "12-Hour"
    Level = "low"
    
    weatherDataList = fetchWindTemperature(USregion , ForecastHour, Level)
    lineNumber = 1
    for weatherDataLine in weatherDataList:
        print ( "line number = {0} - weatherDataLine = {1}".format( str(lineNumber) , weatherDataLine ) )
        lineNumber = lineNumber + 1
        
    