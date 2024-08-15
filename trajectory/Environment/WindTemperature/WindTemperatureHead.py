'''
Created on 9 août 2024

@author: robert

'''

class WindTemperatureHead(object):
    transmissionDay = ""
    transmissionTimeZulu = ""
    measurementDayTimeZulu = ""
    measurementDay = ""
    measurementTimeZulu = ""
    validityDayTimeZulu = ""
    validityDay = ""
    validityTimeZulu = ""
    forUseDayTimeZulu = ""
    forUsePeriodBeginTimeZulu = ""
    forUsePeriodEndTimeZulu = ""
    
    def getTransmissionDay(self):
        return self.transmissionDay
    
    def getTransmissionTimeZulu(self):
        return self.transmissionTimeZulu
    
    def getMeasurementDay(self):
        return self.measurementDay
    
    def getMeasurementTimeZulu(self):
        return self.measurementTimeZulu
    
    def getValidityDay(self):
        return self.validityDay
    
    def getValidityTimeZulu(self):
        return self.validityTimeZulu
    
    def getForUseBeginTimeZulu(self):
        return self.forUsePeriodBeginTimeZulu
    
    def getForUseEndTimeZulu(self):
        return self.forUsePeriodEndTimeZulu

    def analyseTransmissionDates(self, textLine):
        self.transmissionDay = "01"
        self.transmissionTimeZulu = "1200Z"
        textLineArr = str(textLine).split(" ")
        for elem in textLineArr:
            print ( elem )
            if (str(elem).isdigit()):
                print ( "only digits element = {0}".format(elem))
                self.transmissionDay = elem[0:2]
                print ( "measurement day of the month = {0}".format(self.transmissionDay))
                self.transmissionTimeZulu = elem[2:]+ "Z"
                print ( "measurement Zulu time = {0}".format(self.transmissionTimeZulu))
                
    def analyseMeasurementDates(self, textLine):
        length = len("DATA BASED ON ")
        self.measurementDayTimeZulu = textLine[length:]
        print ( "measurement day time = {0}".format(self.measurementDayTimeZulu))
        self.measurementDay = self.measurementDayTimeZulu[0:2]
        print ( "measurement day of the month = {0}".format(self.measurementDay))
        self.measurementTimeZulu = self.measurementDayTimeZulu[2:]
        print ( "measurement time Zulu = {0}".format(self.measurementTimeZulu))
        
    def analyseValidityDates(self, textLine):
        begin = len("VALID ")
        end = begin + 7
        self.validityDayTimeZulu = textLine[begin:end]
        print ( "validity day time = {0}".format(self.validityDayTimeZulu))
        self.validityDay = self.validityDayTimeZulu[0:2]
        print ( "validity day = {0}".format(self.validityDay))
        self.validityTimeZulu = self.validityDayTimeZulu[2:]
        print ( "validity time Zulu = {0}".format(self.validityTimeZulu))
        
    def analyseForUseDates(self , textLine ):
        forUseIndex = str(textLine).index("FOR USE")
        if ( forUseIndex > 0 ):
            begin = forUseIndex + len ( "FOR USE ")
            end = begin + 10
            self.forUseDayTimeZulu = textLine[begin:end]
            print ( "for Use day time Zulu = {0}".format(self.forUseDayTimeZulu))
            self.forUsePeriodBeginTimeZulu = self.forUseDayTimeZulu[0:4] + "Z"
            self.forUsePeriodEndTimeZulu = self.forUseDayTimeZulu[5:10]
        
    
    def analyseHead(self, headLineList ):
        assert ( isinstance ( headLineList , list))
        print (" --- analyse head ----")
        
        for textLine in headLineList:
            if ( str(textLine).startswith("FB")):
                self.analyseTransmissionDates(textLine)
                
            if ( str(textLine).startswith("DATA BASED ON")):
                self.analyseMeasurementDates(textLine)
                
            if ( str(textLine).startswith("VALID")):
                self.analyseValidityDates(textLine)
                self.analyseForUseDates(textLine)


if __name__ == '__main__':
    
    headLineList = []
    headLine = ""
    headLineList.append(headLine)
    headLine = "000"
    headLineList.append(headLine)
    headLine = "FBUS33 KWNO 091357"
    headLineList.append(headLine)
    headLine = "FD3US3"
    headLineList.append(headLine)
    headLine = "DATA BASED ON 091200Z"
    headLineList.append(headLine)
    headLine = "VALID 100000Z   FOR USE 2100-0600Z. TEMPS NEG ABV 24000"
    headLineList.append(headLine)
    
    windTemperatureHead = WindTemperatureHead()
    windTemperatureHead.analyseHead( headLineList )
    
    print ("-----------")
    
    print ("transmission day = {0}".format(windTemperatureHead.getTransmissionDay()))
    print ("measurement day = {0}".format(windTemperatureHead.getMeasurementDay()))
    print ("validity day = {0}".format(windTemperatureHead.getValidityDay()))
    
    print ("-----------")
    
    print ("transmission Time Zulu = {0}".format(windTemperatureHead.getTransmissionTimeZulu()))
    print ("measurement Time Zulu = {0}".format(windTemperatureHead.getMeasurementTimeZulu()))
    print ("validity Time Zulu = {0}".format(windTemperatureHead.getValidityTimeZulu()))
    
    print ( " ---------")
    
    print ("for Use begin time Zulu = {0}".format( windTemperatureHead.getForUseBeginTimeZulu()))
    print ("for Use end time Zulu = {0}".format( windTemperatureHead.getForUseEndTimeZulu()))
    