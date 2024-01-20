

//Define custom control class
class AirlineCasmOptimizationControl extends og.Control {
	constructor(options) {
		super(options);
	}

	getMainTableId(){
		return "airlineCasmOptimizationTableId";
	}
	
	onadd() {
		//console.log("airline CASM Optimization Results Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "airlineCasmOptimizationMainDivId";
		mainDiv.style = "display: none;";
		mainDiv.classList.add('airlineCasmOptimizationMainDiv');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move - Costs per Available Seat Miles";
		draggableMainDiv.classList.add("draggableDivHeader");
	
		let span = document.createElement('span');
		span.id = "hideId";
		span.innerHTML = "Click to hide";
		// call a function
		span.onclick = clickToHide;
		draggableMainDiv.appendChild(span);
		
		mainDiv.appendChild(draggableMainDiv);
		
		let table = document.createElement('table');
		table.id = this.getMainTableId();
		table.classList.add ('airlineCasmOptimizationTable');
		
		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');

		let th_list = [ 'Airline' , 'Solver Status' , 'Aircraft' , 'assigned', 'Departure', 'Arrival', 'ReducedClimbPower', 
						'Seats', 'Distance (nm)', 'Costs US$' , 'CASM US$' ];
						
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
		dragElement(document.getElementById("airlineCasmOptimizationMainDivId"));
		
	}

	oninit() {
		//console.log("airline CASM Optimization Results Control - oninit");
	}
	
}