$(document).ready( function () {
	setTimeout(function () {
		if ( document.getElementById("airlineCostsTableId") ) {
			console.log("element table with id " + airlineCostsTableId + " is existing");
		}
	}, 500 );
} );



//Define custom control class
class AirlineCostsControl extends og.Control {
	constructor(options) {
		super(options);
	}

	onadd() {
		//console.log("airline Optimization Results Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "airlineCostsMainDivId";
		mainDiv.style = "display: none;";
		mainDiv.classList.add('airlineCostsMainDiv');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move";
		draggableMainDiv.classList.add("draggableDivHeader");
		
		let span = document.createElement('span');
		span.id = "hideId";
		span.innerHTML = "Click to hide";
		// call a function
		span.onclick = clickToHide;
		draggableMainDiv.appendChild(span);
		
		mainDiv.appendChild(draggableMainDiv);
		
		let table = document.createElement('table');
		table.id = "airlineCostsTableId";
		table.classList.add ('airlineCostsTable');
		
		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');

		let th_list = [ 'Airline' , 'Aircraft' , 'Departure', 'Arrival', 'Is Aborted', 'takeOff Mass Kg' ,
						'Final Mass Kg', 'Flight Duration Hours' , 'fuelCostUS$' , 'operationCostsUS$' , 
						'crewCostsUS$' , 'totalCostsUS$' ];
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
		dragElement(document.getElementById("airlineCostsMainDivId"));
		
		// set datatable
		//$('#airlineCostsTableId').DataTable();
	}

	oninit() {
		//console.log("airline Optimization Results Control - oninit");
	}
};