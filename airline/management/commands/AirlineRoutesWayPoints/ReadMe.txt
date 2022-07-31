
Use the following site to retrieve a route
http://rfinder.asalink.net/free/ 

Use the html table with name of the route points and Latitude and longitude , and paste the content in an EXCEL file
using a SPACE separator.

In the latitude and longitude columns replace single ' with \'

create a new column and apply following EXCEL formulae

=CONCAT("{'Name'"; ":'"; A1; "',"; "'Latitude':'"; B1; "','Longitude':'"; C1;"'}, \")

with an input such as 
YNKEE	N40°29\'00.90"	W073°50\'57.17"

you should obtain the following column content

{'Name':'YNKEE','Latitude':'N40°29\'00.90"','Longitude':'W073°50\'57.17"'},


extract from http://rfinder.asalink.net/free/  with flight ceiling of FL390

ID      FREQ   TRK   DIST   Coords                       Name/Remarks
KJFK             0      0   N40°38'23.74" W073°46'43.29" JOHN F KENNEDY INTL
YNKEE          203     10   N40°29'00.90" W073°50'57.17" YNKEE
CREEL          103     14   N40°26'50.50" W073°33'10.67" CREEL
RIFLE           76     47   N40°41'24.17" W072°34'54.89" RIFLE
HTO     113.6   46     18   N40°55'08.38" W072°19'00.13" HAMPTON
PARCH           44     14   N41°05'57.21" W072°07'14.66" PARCH
TRAIT           44     14   N41°17'04.75" W071°55'03.35" TRAIT
PVD     115.6   44     34   N41°43'27.63" W071°25'46.70" PROVIDENCE
BOS     112.7   32     43   N42°21'26.82" W070°59'22.37" BOSTON
COPLY           71     21   N42°29'52.21" W070°33'28.56" COPLY
SCUPP           72     16   N42°36'11.01" W070°13'49.34" SCUPP
CANAL           72     10   N42°40'08.51" W070°01'21.75" CANAL
TUSKY           72    143   N43°33'53.99" W067°00'00.00" TUSKY
OMSAT           73    665   N47°00'00.00" W052°00'00.00" OMSAT
47N050W         78     87   N47°30'00.00" W050°00'00.00" 4730N05000W
49N040W         78    415   N49°30'00.00" W040°00'00.00" 4930N04000W
51N030W         77    400   N51°30'00.00" W030°00'00.00" 5130N03000W
52N020W         84    374   N52°30'00.00" W020°00'00.00" 5230N02000W
LIMRI          102    186   N52°00'00.00" W015°00'00.00" LIMRI
XETBO           93     37   N52°00'00.00" W014°00'00.00" XETBO
DOLIP           92     74   N52°00'00.00" W012°00'00.00" DOLIP
LINRA          111     77   N51°34'47.00" W010°01'55.99" LINRA
LESLU          116     84   N51°00'00.00" W008°00'00.00" LESLU
INSUN          120     73   N50°23'43.00" W006°19'23.99" INSUN
LND     114.2  121     31   N50°08'10.99" W005°38'13.00" LAND'S END
NAKID          123     47   N49°42'54.00" W004°37'22.99" NAKID
ANNET           99     24   N49°39'04.99" W004°00'05.00" ANNET
UVSUV           95     91   N49°29'16.99" W001°40'27.99" UVSUV
INGOR           96     56   N49°21'52.00" W000°15'00.00" INGOR
LUKIP           94     29   N49°18'56.99" E000°29'46.99" LUKIP
LFPG           101     83   N49°00'35.09" E002°32'52.15" PARIS CHARLES DE GAULLE