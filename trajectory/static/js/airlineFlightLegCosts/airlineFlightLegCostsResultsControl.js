
//Define custom control class
		class AirlineFlightLegCostsResultsControl extends og.Control {
            constructor(options) {
                super(options);
            }

            onadd() {
				//console.log("airline Costs Results Control - onadd");
				
				let mainDiv = document.createElement('div');
				mainDiv.id = "airlineFlightLegCostsMainDivId";
				mainDiv.style="display: none;";
				mainDiv.classList.add('airlineFlightLegCostsMainDiv');
				
				let draggableMainDiv = document.createElement('div');
				draggableMainDiv.id = mainDiv.id  + "Header";
				draggableMainDiv.innerHTML = "Click here to move";
				draggableMainDiv.classList.add("draggableDivHeader");
				mainDiv.appendChild(draggableMainDiv);
				
				let table = document.createElement('table');
				table.id = "airlineFlightLegCostsTableId";
				
				let thead = document.createElement('thead');
				let row_1 = document.createElement('tr');

				let th_list = [ 'Airline' , 'Aircraft' , 'Seats', 'Adep', 'RunWay', 'Ades', 'RunWay', 'Is Aborted', 'Initial Mass Kg' ,
								'Final Mass Kg', 'Lost Mass Kg', 'Fuel Costs US$', 'Flight Duration Hours', 'Flying Costs US$', 'Crew Costs US$', 'Total Costs US$' ];
				let th = undefined;
				th_list.forEach ( function ( element ) {
					th = document.createElement('th');
					th.innerHTML = element;
					row_1.appendChild(th);
				});

				thead.appendChild(row_1);
				table.appendChild(thead);

				// --------------------
				let tbody = document.createElement('tbody');
				table.appendChild(tbody);

				mainDiv.appendChild(table);
				this.renderer.div.appendChild(mainDiv);
				
				// Make the Main Div element draggable:
				dragElement(document.getElementById("airlineFlightLegCostsMainDivId"));
            }

            oninit() {
                //console.log("airline Costs Results Control - oninit");
            }
        };