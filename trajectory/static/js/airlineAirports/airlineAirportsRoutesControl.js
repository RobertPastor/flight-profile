import {
        Control
    } from "../og/og.es.js";
    
    
// Define custom control class
// display a floating table related to the right click on an airport 
export class AirlineAirportsRoutesControl extends Control {
	
	constructor(options) {
		super(options);
	}
	
	getMainDivId() {
		return "airlineAirportsRoutesMainDivId";
	}
	
	getMainTableId() {
		return "airlineAirportsRoutesTableId";
	}

	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "airlineAirportsRoutesMainDivId";
		mainDiv.style="display: none;";
		mainDiv.classList.add('airlineAirportsRoutesMainDiv');
		
		let table = document.createElement('table');
		table.id = this.getMainTableId();
				
		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');
		
		// 8th May 2023 - add hyperlink to show the route
		// 25th June 2023 - show direction of the flight leg
		let th_list = [ 'Airline' , 'direction', 'action' , 'Departure Airport' , 'ICAO', 'Arrival Airport', 'ICAO'];
		th_list.forEach ( function ( element ) {
			let th = document.createElement('th');
			th.innerHTML = element;
			if ( (element == "action") || (element == "direction") ) {
				// sortable no sorting
				th.classList.add("no-sort");
			}
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
		//console.log("airline Airports Routes - oninit");
	}
};