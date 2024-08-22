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
from trajectory.Environment.WindTemperature.WeatherStationClass import WeatherStation


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

    row = row + 1
    writeReadMeRow(wsReadMe, row, "Wind Speed" , styleLavender , "expressed in Knots", styleEntete)
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Wind Direction" , styleLavender , "expressed in Degrees from True North", styleEntete)
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Temperature" , styleLavender , "expressed in Degrees Celsius", styleEntete)

    wsReadMe.autofit()
    
def writeRawData(workbook, request, airlineName , windTemperatureList):
    assert ( isinstance ( windTemperatureList , list))
    wsRawData = workbook.add_worksheet("Raw Data")
    styleData = workbook.add_format({'bold': False, 'border': True})
    row = 0
    for textLine in windTemperatureList:
        wsRawData.write(row , 0 , textLine , styleData)
        row = row + 1
        
    wsRawData.autofit()
    
    
def writeWeatherStationDataDetails(worksheet, row, windTemperatureList, numberOfLevels, styleData):
    assert ( isinstance ( windTemperatureList , list))
    feetLineFound = False
    for textLine in windTemperatureList:
        if feetLineFound:
            row = row + 1
            weatherStation = WeatherStation() 
            weatherStation.ExploitStationData(textLine, numberOfLevels)
            worksheet.write(row, 0 , weatherStation.getStationName() , styleData )
            #worksheet.write(row, 1 , weatherStation.getStationsFirstLevel() , styleData )
            col = 1
            for stationDataLevel in weatherStation.getStationLevels():
                worksheet.write(row, col , stationDataLevel , styleData )
                col = col + 1
            
        if ( str(textLine).startswith("FT")):
            feetLineFound = True
            
def writeWeatherStationTemperatureDataDetails(worksheet, row, windTemperatureList, numberOfLevels, styleData):
    assert ( isinstance ( windTemperatureList , list))
    feetLineFound = False
    for textLine in windTemperatureList:
        if feetLineFound:
            row = row + 1
            weatherStation = WeatherStation() 
            weatherStation.ExploitStationData(textLine, numberOfLevels)
            worksheet.write(row, 0 , weatherStation.getStationName() , styleData )
            #worksheet.write(row, 1 , weatherStation.getStationsFirstLevel() , styleData )
            col = 1
            for stationTemperatureDataLevel in weatherStation.getStationTemperatureLevels():
                worksheet.write(row, col , stationTemperatureDataLevel , styleData )
                col = col + 1
            
        if ( str(textLine).startswith("FT")):
            feetLineFound = True
            
            
def writeWeatherStationWindDirectionDataDetails(worksheet, row, windTemperatureList, numberOfLevels, styleData):
    assert ( isinstance ( windTemperatureList , list))
    feetLineFound = False
    for textLine in windTemperatureList:
        if feetLineFound:
            row = row + 1
            weatherStation = WeatherStation() 
            weatherStation.ExploitStationData(textLine, numberOfLevels)
            worksheet.write(row, 0 , weatherStation.getStationName() , styleData )
            #worksheet.write(row, 1 , weatherStation.getStationsFirstLevel() , styleData )
            col = 1
            for stationWindDirectionDataLevel in weatherStation.getStationWindDirectionLevels():
                worksheet.write(row, col , stationWindDirectionDataLevel , styleData )
                col = col + 1
            
        if ( str(textLine).startswith("FT")):
            feetLineFound = True
            
def writeWeatherStationWindSpeedDataDetails(worksheet, row, windTemperatureList, numberOfLevels, styleData):
    assert ( isinstance ( windTemperatureList , list))
    feetLineFound = False
    for textLine in windTemperatureList:
        if feetLineFound:
            row = row + 1
            weatherStation = WeatherStation() 
            weatherStation.ExploitStationData(textLine, numberOfLevels)
            worksheet.write(row, 0 , weatherStation.getStationName() , styleData )
            #worksheet.write(row, 1 , weatherStation.getStationsFirstLevel() , styleData )
            col = 1
            for stationWindSpeedDataLevel in weatherStation.getStationWindSpeedLevels():
                worksheet.write(row, col , stationWindSpeedDataLevel , styleData )
                col = col + 1
            
        if ( str(textLine).startswith("FT")):
            feetLineFound = True
    
            
def writeFeetHeader(worksheet, style, windTemperatureList):
    weatherStationFeet = WeatherStationFeet()
    feetLevels = weatherStationFeet.readTextLines(windTemperatureList)
    row = 0
    col = 0
    worksheet.write(row, 0 , "FEET", style)
    ''' write a Feet only row '''
    for feetLevel in feetLevels:
        col = col + 1
        worksheet.write(row, col , str(feetLevel), style)
    return len(feetLevels)
    
def writeWeatherStationData(workbook, request, airlineName , windTemperatureList):
    assert ( isinstance ( windTemperatureList , list))
    wsWeatherStationData = workbook.add_worksheet("Weather Station Data")
    styleData = workbook.add_format({'bold': False, 'border':True})
    styleHeader = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})

    feetLevelsLength = writeFeetHeader(wsWeatherStationData, styleHeader, windTemperatureList)
    ''' write the weather stations data '''
    row = 0
    writeWeatherStationDataDetails(wsWeatherStationData , row , windTemperatureList , feetLevelsLength, styleData)
    wsWeatherStationData.autofit()
    
def writeWindSpeedData(workbook, request, airlineName , windTemperatureList):
    assert ( isinstance ( windTemperatureList , list))
    wsWindSpeedData = workbook.add_worksheet("Wind Speed Data")
    styleData = workbook.add_format({'bold': False, 'border':True})
    styleHeader = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    feetLevelsLength = writeFeetHeader(wsWindSpeedData, styleHeader, windTemperatureList)
    row = 0
    writeWeatherStationWindSpeedDataDetails(wsWindSpeedData, row , windTemperatureList , feetLevelsLength, styleData)
    wsWindSpeedData.autofit()
    
    
def writeWindDirectionData(workbook, request, airlineName , windTemperatureList):
    assert ( isinstance ( windTemperatureList , list))
    wsWindDirectionData = workbook.add_worksheet("Wind Direction Data")
    styleData = workbook.add_format({'bold': False, 'border':True})
    styleHeader = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    feetLevelsLength = writeFeetHeader(wsWindDirectionData, styleHeader, windTemperatureList)
    row = 0
    writeWeatherStationWindDirectionDataDetails(wsWindDirectionData, row , windTemperatureList , feetLevelsLength, styleData)
    wsWindDirectionData.autofit()
    
def writeTemperatureData(workbook, request, airlineName , windTemperatureList):
    assert ( isinstance ( windTemperatureList , list))
    wsTemperatureData = workbook.add_worksheet("Temperature Data")
    styleData = workbook.add_format({'bold': False, 'border':True})
    styleHeader = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    feetLevelsLength = writeFeetHeader(wsTemperatureData, styleHeader, windTemperatureList)
    row = 0
    writeWeatherStationTemperatureDataDetails(wsTemperatureData, row , windTemperatureList , feetLevelsLength, styleData)
    wsTemperatureData.autofit()

def createExcelWorkbook(memoryFile, request, airlineName, windTemperatureList):
    ''' create the workbook '''
    wb = Workbook(memoryFile)
    ''' write the readme sheet '''
    writeReadMe(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    writeRawData(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    writeWeatherStationData(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    writeWindSpeedData(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    writeWindDirectionData(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
    writeTemperatureData(workbook=wb, request=request, airlineName=airlineName, windTemperatureList=windTemperatureList)
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
        
    