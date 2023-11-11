#!/bin/bash

# launch in gitbash
# ensure that the local host is running properly
# extended usage of API
# launch -> . ./curl-tests.sh


# airline URLs

curl -v "http://localhost:8000/airline/airlineFleet/AmericanWings" -o results/airlineFleet-AmericanWings-1.json
curl -v "http://localhost:8000/airline/airlineFleet/EuropeanWings" -o results/airlineFleet-EuropeanWings-2.json
curl -v "http://localhost:8000/airline/airlineFleet/IndianWings"   -o results/airlineFleet-IndianWings-3.json
curl -v "http://localhost:8000/airline/airlineFleet/UnknownWings"  -o results/airlineFleet-UnknownWings-4.json
