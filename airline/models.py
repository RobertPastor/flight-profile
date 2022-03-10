from django.db import models

# Create your models here.

class AirlineRoute(models.Model):
    DepartureAirport = models.CharField(max_length = 500)
    DepartureAirportICAOCode = models.CharField(max_length = 50)
    ArrivalAirport = models.CharField(max_length = 500)
    ArrivalAirportICAOCode = models.CharField(max_length = 50)
    
    class Meta:
        unique_together = (('DepartureAirportICAOCode', 'ArrivalAirportICAOCode'),)

    def getDepartureAirportICAOcode(self):
        return self.DepartureAirportICAOCode
    
    def getArrivalAirportICAOcode(self):
        return self.ArrivalAirportICAOCode
    
    def getFlightLegAsString (self):
        return self.DepartureAirportICAOCode + "-" + self.ArrivalAirportICAOCode
    
    def __str__(self):
        return "departure airport= {0} - arrival airport= {1}".format(self.DepartureAirportICAOCode, self.ArrivalAirportICAOCode)
