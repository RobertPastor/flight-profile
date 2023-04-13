
# ensure that DEBUG constant is set to False

open /flight-profile/FlightProfile/settings.py
and set DEBUG = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# perform git push

# log on python anywhere

https://eu.pythonanywhere.com/user/airlineservices/
account = airlineservices
password = same as usual

## open the bash console



## search the virtual environment

ls -al .virtualenvs/airlineservices

## activate the virtual environment -> check the virtual env name in the prompt

17:44 ~ $ source .virtualenvs/airlineservices/bin/activate
(airlineservices) 17:44 ~ $ 

## move to the git folder -> check the branch master in the prompt

(airlineservices) 17:46 ~ $ cd flight-profile/
(airlineservices) 17:46 ~/flight-profile (master)$ 

## perform a git pull

## sometimes , when local changes (on pythonanywhere) are seeing... -> git reset --hard

(airlineservices) 18:31 ~/flight-profile (master)$ git pull
Updating 0f733d3..3d2be0c
Fast-forward
 .gitignore                                                                           |   3 +-
 ReadMe-Extend-Routes.md                                                              | 301 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 ReadMe-Push-Pull.md                                                                  |  33 ++++++++++
 README.md => ReadMe.md                                                               |   0
 airline/management/commands/AirlineRoutes/AirlineRoutesAirportsDepartureArrival.xlsx | Bin 10617 -> 10718 bytes
 airline/management/commands/AirlineRoutes/AirlineRoutesAirportsReader.py             | 155 -----------------------------------------------
 airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-KJFK-LFPG.xlsx       | Bin 5954 -> 9684 bytes
 airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VABB-VECC.xlsx       | Bin 0 -> 10455 bytes
 airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VOMM-VIJP.xlsx       | Bin 0 -> 10329 bytes
 airline/management/commands/AirlineRoutesWayPoints/ReadMe.txt                        |   2 +
 airline/management/commands/AirlineRoutesWayPoints/WayPoints.xlsx                    | Bin 18925 -> 26034 bytes
 trajectory/management/commands/WayPoints/WayPoints-old.xls                           | Bin 63488 -> 0 bytes
 trajectory/management/commands/WayPoints/WayPoints.xlsx                              | Bin 18925 -> 19777 bytes
 13 files changed, 338 insertions(+), 156 deletions(-)
 create mode 100644 ReadMe-Extend-Routes.md
 create mode 100644 ReadMe-Push-Pull.md
 rename README.md => ReadMe.md (100%)
 delete mode 100644 airline/management/commands/AirlineRoutes/AirlineRoutesAirportsReader.py
 create mode 100644 airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VABB-VECC.xlsx
 create mode 100644 airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VOMM-VIJP.xlsx
 delete mode 100644 trajectory/management/commands/WayPoints/WayPoints-old.xls
(airlineservices) 18:31 ~/flight-profile (master)$ 

## move to the web tab 
https://eu.pythonanywhere.com/user/airlineservices/webapps/#tab_id_airlineservices_eu_pythonanywhere_com

## perform reload

## upgrade xlsxwriter

(airlineservices) 20:49 ~/flight-profile (master)$ pip install xlsxwriter --upgrade
Looking in links: /usr/share/pip-wheels
Requirement already satisfied: xlsxwriter in /home/airlineservices/.virtualenvs/airlineservices/lib/python3.7/site-packages (3.0.3)
Collecting xlsxwriter
  Downloading XlsxWriter-3.0.9-py3-none-any.whl (152 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 152.8/152.8 kB 4.0 MB/s eta 0:00:00
Installing collected packages: xlsxwriter
  Attempting uninstall: xlsxwriter
    Found existing installation: XlsxWriter 3.0.3
    Uninstalling XlsxWriter-3.0.3:
      Successfully uninstalled XlsxWriter-3.0.3
Successfully installed xlsxwriter-3.0.9
(airlineservices) 20:52 ~/flight-profile (master)$ 




