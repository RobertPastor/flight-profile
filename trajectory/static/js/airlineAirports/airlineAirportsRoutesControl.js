
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
								
		let th_list = [ 'Airline' , 'Departure Airport' , 'Departure ICAO Code', 'Arrival Airport', 'Arrival ICAO Code']
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