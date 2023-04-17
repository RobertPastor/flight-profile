
//Define custom control class
class AirlineRoutesControl extends og.Control {
	constructor(options) {
		super(options);
	}

	onadd() {
		//console.log("airline Routes Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "airlineRoutesDivId";
		mainDiv.style="display: none;";
		mainDiv.classList.add('airlineRoutesTableDiv');
		
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
		table.id = "airlineRoutesTableId";

		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');
		
		let th_list = [ 'Airline' , 'Departure Airport' , 'Adep', 'Best RunWay', 'Destination Airport', 'Ades', 'Best RunWay', 'Action']
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
		dragElement(document.getElementById("airlineRoutesDivId"));
	}

	oninit() {
		//console.log("airline Routes Control - oninit");
	}
};