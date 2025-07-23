
to upgrade 
# python manage.py AirlineFleetDatabaseLoad

#  pip install pyyaml
#  pip install matplotlib
#  pip install scipy

python manage.py AirlineFleetDatabaseLoad
linux-6.5.0-1022-aws-x86_64-with-debian-bullseye-sid
airline fleet database exists
Bada aircraft database read correctly = True
/home/airlineservices/flight-profile/airline/management/commands/AirlineFleet/AirlineFleet.xlsx
Index is: 0
--> row --> Airline                                AmericanWings
Aircraft ICAO                                   A320
Aircraft                                 Airbus A320
In service                                         5
Orders                                           NaN
Passengers Delta One                             NaN
Passengers First Class                          16.0
Passengers Premium Select                        NaN
Passengers Delta Confort Plus                   18.0
Passengers Main Cabin                          123.0
Passengers Total                                 157
Costs per flying hours dollars                  2840
Crew Costs per flying hours dollars             1657
TurnAround Time Minutes                           25
Refs                                            [35]
Notes                                            NaN
Name: 0, dtype: object
Airbus A320
aircraft = A320 - of airline = AmericanWings is already existing
Index is: 1
--> row --> Airline                                                                   AmericanWings
Aircraft ICAO                                                                      A332
Aircraft                                                                Airbus A330-200
In service                                                                            5
Orders                                                                              NaN
Passengers Delta One                                                               34.0
Passengers First Class                                                              NaN
Passengers Premium Select                                                           NaN
Passengers Delta Confort Plus                                                      32.0
Passengers Main Cabin                                                             168.0
Passengers Total                                                                    234
Costs per flying hours dollars                                                     3300
Crew Costs per flying hours dollars                                                1857
TurnAround Time Minutes                                                              35
Refs                                                                               [40]
Notes                                  To be retrofitted with Premium Select seats.[41]
Name: 1, dtype: object
Airbus A330-200
aircraft = A332 - of airline = AmericanWings is already existing
Index is: 2
--> row --> Airline                                 AmericanWings
Aircraft ICAO                                    B738
Aircraft                               Boeing 737-800
In service                                          5
Orders                                            NaN
Passengers Delta One                              NaN
Passengers First Class                           16.0
Passengers Premium Select                         NaN
Passengers Delta Confort Plus                    36.0
Passengers Main Cabin                           108.0
Passengers Total                                  160
Costs per flying hours dollars                   3010
Crew Costs per flying hours dollars              1557
TurnAround Time Minutes                            25
Refs                                             [51]
Notes                                             NaN
Name: 2, dtype: object
Boeing 737-800
aircraft = B738 - of airline = AmericanWings is already existing
Index is: 3
--> row --> Airline                                                                    AmericanWings
Aircraft ICAO                                                                       B739
Aircraft                                                                Boeing 737-900ER
In service                                                                             1
Orders                                                                              29.0
Passengers Delta One                                                                 NaN
Passengers First Class                                                              20.0
Passengers Premium Select                                                            NaN
Passengers Delta Confort Plus                                                       21.0
Passengers Main Cabin                                                              139.0
Passengers Total                                                                     180
Costs per flying hours dollars                                                      3050
Crew Costs per flying hours dollars                                                 1557
TurnAround Time Minutes                                                               25
Refs                                                                                [52]
Notes                                  29 used aircraft to enter service from 2022.[2...
Name: 3, dtype: object
Boeing 737-900ER
aircraft = B739 - of airline = AmericanWings is new in the database
Boeing 737-900ER-B739
AmericanWings
Boeing 737-900ER
Index is: 4
--> row --> Airline                                AmericanWings
Aircraft ICAO                                   A319
Aircraft                                 Airbus A319
In service                                         5
Orders                                           NaN
Passengers Delta One                             NaN
Passengers First Class                           NaN
Passengers Premium Select                        NaN
Passengers Delta Confort Plus                    NaN
Passengers Main Cabin                            NaN
Passengers Total                                 150
Costs per flying hours dollars                  2780
Crew Costs per flying hours dollars             1457
TurnAround Time Minutes                           25
Refs                                             NaN
Notes                                            NaN
Name: 4, dtype: object
Airbus A319
aircraft = A319 - of airline = AmericanWings is new in the database
Airbus A319-A319
AmericanWings
Airbus A319
Index is: 5
--> row --> Airline                                 AmericanWings
Aircraft ICAO                                    A20N
Aircraft                               Airbus A320neo
In service                                          5
Orders                                            NaN
Passengers Delta One                              NaN
Passengers First Class                            NaN
Passengers Premium Select                         NaN
Passengers Delta Confort Plus                     NaN
Passengers Main Cabin                             NaN
Passengers Total                                  180
Costs per flying hours dollars                   2780
Crew Costs per flying hours dollars              1457
TurnAround Time Minutes                            25
Refs                                              NaN
Notes                                             NaN
Name: 5, dtype: object
Airbus A320neo
aircraft = A20N - of airline = AmericanWings is new in the database
Airbus A320neo-A20N
AmericanWings
Airbus A320neo
Index is: 6
--> row --> Airline                                EuropeanWings
Aircraft ICAO                                   A320
Aircraft                                 Airbus A320
In service                                         7
Orders                                           NaN
Passengers Delta One                             NaN
Passengers First Class                          16.0
Passengers Premium Select                        NaN
Passengers Delta Confort Plus                   18.0
Passengers Main Cabin                          123.0
Passengers Total                                 157
Costs per flying hours dollars                  2840
Crew Costs per flying hours dollars             1607
TurnAround Time Minutes                           25
Refs                                            [35]
Notes                                            NaN
Name: 6, dtype: object
Airbus A320
aircraft = A320 - of airline = EuropeanWings is already existing
Index is: 7
--> row --> Airline                                                                   EuropeanWings
Aircraft ICAO                                                                      A332
Aircraft                                                                Airbus A330-200
In service                                                                            8
Orders                                                                              NaN
Passengers Delta One                                                               34.0
Passengers First Class                                                              NaN
Passengers Premium Select                                                           NaN
Passengers Delta Confort Plus                                                      32.0
Passengers Main Cabin                                                             168.0
Passengers Total                                                                    234
Costs per flying hours dollars                                                     3300
Crew Costs per flying hours dollars                                                1807
TurnAround Time Minutes                                                              35
Refs                                                                               [40]
Notes                                  To be retrofitted with Premium Select seats.[41]
Name: 7, dtype: object
Airbus A330-200
aircraft = A332 - of airline = EuropeanWings is already existing
Index is: 8
--> row --> Airline                                 EuropeanWings
Aircraft ICAO                                    B738
Aircraft                               Boeing 737-800
In service                                          9
Orders                                            NaN
Passengers Delta One                              NaN
Passengers First Class                           16.0
Passengers Premium Select                         NaN
Passengers Delta Confort Plus                    36.0
Passengers Main Cabin                           108.0
Passengers Total                                  160
Costs per flying hours dollars                   3010
Crew Costs per flying hours dollars              1507
TurnAround Time Minutes                            25
Refs                                             [51]
Notes                                             NaN
Name: 8, dtype: object
Boeing 737-800
aircraft = B738 - of airline = EuropeanWings is already existing
Index is: 9
--> row --> Airline                                                                    EuropeanWings
Aircraft ICAO                                                                       B739
Aircraft                                                                Boeing 737-900ER
In service                                                                            10
Orders                                                                              29.0
Passengers Delta One                                                                 NaN
Passengers First Class                                                              20.0
Passengers Premium Select                                                            NaN
Passengers Delta Confort Plus                                                       21.0
Passengers Main Cabin                                                              139.0
Passengers Total                                                                     180
Costs per flying hours dollars                                                      3050
Crew Costs per flying hours dollars                                                 1507
TurnAround Time Minutes                                                               25
Refs                                                                                [52]
Notes                                  29 used aircraft to enter service from 2022.[2...
Name: 9, dtype: object
Boeing 737-900ER
aircraft = B739 - of airline = EuropeanWings is new in the database
Boeing 737-900ER-B739
EuropeanWings
Boeing 737-900ER
Index is: 10
--> row --> Airline                                EuropeanWings
Aircraft ICAO                                   A319
Aircraft                                 Airbus A319
In service                                         5
Orders                                           NaN
Passengers Delta One                             NaN
Passengers First Class                           NaN
Passengers Premium Select                        NaN
Passengers Delta Confort Plus                    NaN
Passengers Main Cabin                            NaN
Passengers Total                                 150
Costs per flying hours dollars                  2780
Crew Costs per flying hours dollars             1457
TurnAround Time Minutes                           25
Refs                                             NaN
Notes                                            NaN
Name: 10, dtype: object
Airbus A319
aircraft = A319 - of airline = EuropeanWings is new in the database
Airbus A319-A319
EuropeanWings
Airbus A319
Index is: 11
--> row --> Airline                                 EuropeanWings
Aircraft ICAO                                    A20N
Aircraft                               Airbus A320neo
In service                                          5
Orders                                            NaN
Passengers Delta One                              NaN
Passengers First Class                            NaN
Passengers Premium Select                         NaN
Passengers Delta Confort Plus                     NaN
Passengers Main Cabin                             NaN
Passengers Total                                  180
Costs per flying hours dollars                   2780
Crew Costs per flying hours dollars              1457
TurnAround Time Minutes                            25
Refs                                              NaN
Notes                                             NaN
Name: 11, dtype: object
Airbus A320neo
aircraft = A20N - of airline = EuropeanWings is new in the database
Airbus A320neo-A20N
EuropeanWings
Airbus A320neo
Index is: 12
--> row --> Airline                                IndianWings
Aircraft ICAO                                 A320
Aircraft                               Airbus A320
In service                                      12
Orders                                         NaN
Passengers Delta One                           NaN
Passengers First Class                        16.0
Passengers Premium Select                      NaN
Passengers Delta Confort Plus                 18.0
Passengers Main Cabin                        123.0
Passengers Total                               157
Costs per flying hours dollars                2840
Crew Costs per flying hours dollars           1517
TurnAround Time Minutes                         25
Refs                                          [35]
Notes                                          NaN
Name: 12, dtype: object
Airbus A320
aircraft = A320 - of airline = IndianWings is already existing
Index is: 13
--> row --> Airline                                                                     IndianWings
Aircraft ICAO                                                                      A332
Aircraft                                                                Airbus A330-200
In service                                                                           13
Orders                                                                              NaN
Passengers Delta One                                                               34.0
Passengers First Class                                                              NaN
Passengers Premium Select                                                           NaN
Passengers Delta Confort Plus                                                      32.0
Passengers Main Cabin                                                             168.0
Passengers Total                                                                    234
Costs per flying hours dollars                                                     3300
Crew Costs per flying hours dollars                                                1617
TurnAround Time Minutes                                                              35
Refs                                                                               [40]
Notes                                  To be retrofitted with Premium Select seats.[41]
Name: 13, dtype: object
Airbus A330-200
aircraft = A332 - of airline = IndianWings is already existing
Index is: 14
--> row --> Airline                                   IndianWings
Aircraft ICAO                                    B738
Aircraft                               Boeing 737-800
In service                                         14
Orders                                            NaN
Passengers Delta One                              NaN
Passengers First Class                           16.0
Passengers Premium Select                         NaN
Passengers Delta Confort Plus                    36.0
Passengers Main Cabin                           108.0
Passengers Total                                  160
Costs per flying hours dollars                   3010
Crew Costs per flying hours dollars              1407
TurnAround Time Minutes                            25
Refs                                             [51]
Notes                                             NaN
Name: 14, dtype: object
Boeing 737-800
aircraft = B738 - of airline = IndianWings is already existing
Index is: 15
--> row --> Airline                                                                      IndianWings
Aircraft ICAO                                                                       B739
Aircraft                                                                Boeing 737-900ER
In service                                                                            15
Orders                                                                              29.0
Passengers Delta One                                                                 NaN
Passengers First Class                                                              20.0
Passengers Premium Select                                                            NaN
Passengers Delta Confort Plus                                                       21.0
Passengers Main Cabin                                                              139.0
Passengers Total                                                                     180
Costs per flying hours dollars                                                      3050
Name: 0, dtype: object
Crew Costs per flying hours dollars                                                 1407
TurnAround Time Minutes                                                               25
Refs                                                                                [52]
Notes                                  29 used aircraft to enter service from 2022.[2...
Name: 15, dtype: object
Boeing 737-900ER
aircraft = B739 - of airline = IndianWings is new in the database
Boeing 737-900ER-B739
IndianWings
Boeing 737-900ER
Index is: 16
--> row --> Airline                                IndianWings
Aircraft ICAO                                 A319
Aircraft                               Airbus A319
In service                                       5
Orders                                         NaN
Passengers Delta One                           NaN
Passengers First Class                         NaN
Passengers Premium Select                      NaN
Passengers Delta Confort Plus                  NaN
Passengers Main Cabin                          NaN
Passengers Total                               150
Costs per flying hours dollars                2780
Crew Costs per flying hours dollars           1457
TurnAround Time Minutes                         25
Refs                                           NaN
Notes                                          NaN
Name: 16, dtype: object
Airbus A319
aircraft = A319 - of airline = IndianWings is new in the database
Airbus A319-A319
IndianWings
Airbus A319
Index is: 17
--> row --> Airline                                   IndianWings
Aircraft ICAO                                    A20N
Aircraft                               Airbus A320neo
In service                                          5
Orders                                            NaN
Passengers Delta One                              NaN
Passengers First Class                            NaN
Passengers Premium Select                         NaN
Passengers Delta Confort Plus                     NaN
Passengers Main Cabin                             NaN
Passengers Total                                  180
Costs per flying hours dollars                   2780
Crew Costs per flying hours dollars              1457
TurnAround Time Minutes                            25
Refs                                              NaN
Notes                                             NaN
Name: 17, dtype: object
Airbus A320neo
aircraft = A20N - of airline = IndianWings is new in the database
Airbus A320neo-A20N
IndianWings
Airbus A320neo
read airline fleet database result = True
(airlineservices) 20:07 ~/flight-profile (master)$ 