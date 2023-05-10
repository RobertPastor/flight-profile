
//Define custom control class
class AirlineAirportsRoutesControl extends og.Control {
	constructor(options) {
		super(options);
	}

	onadd() {
		//console.log("airline Airports Routes - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "airlineAirportsRoutesMainDivId";
		mainDiv.style="display: none;";
		mainDiv.classList.add('airlineAirportsRoutesMainDiv');
		
		let table = document.createElement('table');
		table.id = "airlineAirportsRoutesTableId";
		
		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');
		
		// 8th May 2023 - add hyperlink to show the route
		let th_list = [ 'Airline' , 'action' , 'Departure Airport' , 'ICAO', 'Arrival Airport', 'ICAO']
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
		
		// --------------------
		
		this.renderer.div.appendChild(mainDiv);
	}
	
	oninit() {
		//console.log("airline Airports Routes - oninit");
	}
};