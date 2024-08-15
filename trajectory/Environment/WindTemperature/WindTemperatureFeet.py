'''
Created on 26 juil. 2024

@author: robert

FT  3000    6000    9000   12000   18000   24000  30000  34000  39000
https://www.faa.gov/regulationspolicies/handbooksmanuals/aviation/phak/chapter-13-aviation-weather-services

'''

def ExploitFeetLine(feetLine):
    print ( feetLine )
    feetLevels = []
    if str(feetLine).startswith( "FT" ):
        print ( "Feet line starts with FT as expected ")
        feetLine = str(feetLine)[2:]
        print ( feetLine )
        splitArray = str(feetLine).split(" ")
        for elem in splitArray:
            elem = str( elem.strip( ))
            if len ( elem ) > 0:
                print (elem.strip(" "))
                feetLevels.append(elem.strip(" "))
                
    else:
        print ( "Error = Feet line does not start with FT as expected ")
    return feetLevels

if __name__ == '__main__':
    feetLine = "FT  3000    6000    9000   12000   18000   24000  30000  34000  39000"
    feetLevels = ExploitFeetLine(feetLine)
    print ( feetLevels )
    
    print ( "------------------")
    
    feetLine = "FE 3000    6000    9000   12000   18000   24000  30000  34000  39000"
    feetLevels = ExploitFeetLine(feetLine)
    print ( feetLevels )