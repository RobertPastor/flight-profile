

//Define custom control class
		class AirlineFleetControl extends og.Control {
            constructor(options) {
                super(options);
            }

            onadd() {
				//console.log("airline Fleet Control - onadd");
				
				let mainDiv = document.createElement('div');
				mainDiv.id = "divAirlineFleetId";
				mainDiv.style="display: none;";
				mainDiv.classList.add('airlineFleetTableDiv');
				
				let table = document.createElement('table');
				table.id = "tableAirlineFleetId";

				let thead = document.createElement('thead');
				let row_1 = document.createElement('tr');
				
				let th_list = [ 'Aircraft ICAO Code' , 'Aircraft Full Name', 'Number of Aircrafts', 'Max Number of Passengers', 'Flying Costs per Hour (US Dollars)', 'Crew Costs per Hour (US Dollars)']
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
            }

            oninit() {
                //console.log("airline Fleet Control - oninit");
            }
        };