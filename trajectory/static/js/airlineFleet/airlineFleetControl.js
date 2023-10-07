

//Define custom control class
		class AirlineFleetControl extends og.Control {
            constructor(options) {
                super(options);
            }
            
            getMainTableDivId() {
				return "tableAirlineFleetId";
			}

            onadd() {
				//console.log("airline Fleet Control - onadd");
				
				let mainDiv = document.createElement('div');
				mainDiv.id = "divAirlineFleetId";
				mainDiv.style="display: none;";
				mainDiv.classList.add('airlineFleetTableDiv');
				
				let draggableMainDiv = document.createElement('div');
				draggableMainDiv.id = mainDiv.id  + "Header";
				draggableMainDiv.innerHTML = "Click here to move -> Airline Fleet Configuration";
				draggableMainDiv.classList.add("draggableDivHeader");
				
				let span = document.createElement('span');
				span.id = "hideId";
				span.innerHTML = "Click to hide";
				// call a function
				span.onclick = clickToHide;
				draggableMainDiv.appendChild(span);
		
				mainDiv.appendChild(draggableMainDiv);
				
				let table = document.createElement('table');
				table.id = this.getMainTableDivId();

				let thead = document.createElement('thead');
				let row_1 = document.createElement('tr');
				
				let th_list = [ 'Airline' , 'Aircraft ICAO Code' , 'Aircraft Full Name', 
								'Number of Aircrafts', 'Number of Seats', 
								'Flying Costs per Hour (US$)', 'Crew Costs per Hour (US$)',
								'Min TakeOff Mass (kg)' , 'Reference Mass (kg)' , 'Max TakeOff Mass (kg)',
								'Aircraft Turn Around Time (mn)'];
								
				let th = undefined;
				th_list.forEach ( function ( element ) {
					th = document.createElement('th');
					th.innerHTML = element;
					row_1.appendChild(th);
				});
				
				thead.appendChild(row_1);
				table.appendChild(thead);
				
				let tbody = document.createElement('tbody');
				table.appendChild(tbody);
				mainDiv.appendChild(table);
                
                this.renderer.div.appendChild(mainDiv);
				
				// Make the Main Div element draggable:
				dragElement(document.getElementById("divAirlineFleetId"));
				
				// use jquery datatable
				//let fleetTable = new DataTable('#tableAirlineFleetId');
            }

            oninit() {
                //console.log("airline Fleet Control - oninit");
            }
        };