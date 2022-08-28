


//Define custom control class
		class FlighProfileControl extends og.Control {
            constructor(options) {
                super(options);
            }

            onadd() {
				//console.log("flight profile Control - onadd");
				
				let mainDiv = document.createElement('div');
				mainDiv.id = "flightProfileMainDivId";
				mainDiv.style="display: none;";
				mainDiv.classList.add('flightProfileTableDiv');
				
				let table = document.createElement('table');
				table.id = "flightProfileTableId";
				
				let row_1 = document.createElement('tr');
				let td = document.createElement('td');
				
				// ------------------
				
				let div_1 = document.createElement('div');
				div_1.id = "aircraftSelectionId";
				div_1.classList.add("aircraftSelectionClass");
				
				let label_1 = document.createElement("label");
				label_1.innerHTML = "Select an aircraft ->" ;
				div_1.appendChild(label_1);
				
				let select_1 = document.createElement("select");
				select_1.id = "airlineAircraftId";
				select_1.name = "airlineAircraftName";
				div_1.appendChild(select_1);

				td.appendChild(div_1);
				
				// ---------------
				
				let div_2 = document.createElement('div');
				div_2.id = "routesSelectionId";
				div_2.classList.add("routesSelectionClass");
				
				let label_2 = document.createElement("label");
				label_2.innerHTML = "Select an route ->" ;
				div_2.appendChild(label_2);
				
				let select_2 = document.createElement("select");
				select_2.id = "airlineRouteId";
				select_2.name = "airlineRouteName";

				div_2.appendChild(select_2);
				
				td.appendChild(div_2);

				// --------------------
				
				let div_3 = document.createElement('div');
				div_3.id = "runWaysSelectionFlightProfileId";
				div_3.classList.add("runWaysSelectionFlightProfileClass");
				
				let label_3 = document.createElement("label");
				label_3.innerHTML = "Select a Departure RunWay -> " ;
				div_3.appendChild(label_3);
				
				let select_3 = document.createElement("select");
				select_3.id = "airlineDepartureRunWayFlightProfileId";
				select_3.name = "airlineDepartureRunWayFlightProfileName";

				div_3.appendChild(select_3);
				
				td.appendChild(div_3);
				
				// --------------------
							
				let div_4 = document.createElement('div');
				div_4.id = "runWaysSelectionFlightProfileId";
				div_4.classList.add("runWaysSelectionFlightProfileClass");
				
				let label_4 = document.createElement("label");
				label_4.innerHTML = "Select an Arrival RunWay -> " ;
				div_4.appendChild(label_4);
				
				let select_4 = document.createElement("select");
				select_4.id = "airlineArrivalRunWayFlightProfileId";
				select_4.name = "airlineArrivalRunWayFlightProfileName";

				div_4.appendChild(select_4);
				
				td.appendChild(div_4);
				
				// --------------------

				let div_5 = document.createElement('div');
				div_5.id = "launchComputeId";
				div_5.classList.add("launchComputeClass");

				let label_5 = document.createElement("label");
				label_5.innerHTML = "Click to launch the profile computation -> " ;
				div_5.appendChild(label_5);
				
				let button = document.createElement("button");
				button.id = "btnComputeFlightProfileId";
				button.innerHTML = "Compute Flight Profile";
				div_5.appendChild(button);

				td.appendChild(div_5);

				// --------------------
				
				row_1.appendChild(td);
				table.appendChild(row_1);
				mainDiv.appendChild(table);
                this.renderer.div.appendChild(mainDiv);
            }

            oninit() {
                //console.log("flight profile Control - oninit");
            }
        };