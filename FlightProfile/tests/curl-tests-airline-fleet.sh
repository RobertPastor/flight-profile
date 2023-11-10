#!/bin/bash

# launch in gitbash
# ensure that the local host is running properly
# extended usage of API
# launch -> . ./curl-tests.sh


# airline URLs

curl -v "http://localhost:8000/airline/airlineFleet/AmericanWings" -o result-001-1.json
curl -v "http://localhost:8000/airline/airlineFleet/EuropeanWings" -o result-001-2.json
curl -v "http://localhost:8000/airline/airlineFleet/IndianWings"   -o result-001-3.json
curl -v "http://localhost:8000/airline/airlineFleet/UnknownWings"  -o result-001-4.json
