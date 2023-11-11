#!/bin/bash

# launch in gitbash
# ensure that the local host is running properly
# extended usage of API
# launch -> . ./curl-tests.sh


# trajectory URLs


curl -v "http://localhost:8000/trajectory/computeCosts/AmericanWings?aircraft=A320&route=KATL-KLAX&AdepRwy=08L&AdesRwy=06L&mass=64000&fl=39000&reduc=15"  -o results/computeCosts-002.json