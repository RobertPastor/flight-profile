
// Define custom control class
// display a floating table related to the right click on an airport 
class MetarsOgControl extends og.Control {
	constructor(options) {
		super(options);
	}
	
	getMainDivId() {
		return "airportsMetarsMainDivId";
	}
	
	getMainTableId(){
		return "airportsMetarsTableId";
	}
	
	oninit() {
	}

	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = this.getMainDivId();
		mainDiv.classList.add('metarsOgControlMainDiv');

		mainDiv.style="display: none;";
		mainDiv.classList.add('airportsMetarsMainDiv');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move - Metar";
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
		
		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');
		
		// 26th September 2023 - show METARs for each airport
		let th_list = [ 'ICAO' , 'Airport Name', 'Date Time UTC' , 'Metar Type' , 'Temperature Celsius', 'Dew Point Celsius', 
						'Wind Speed Kt' , 'Wind Direction Compass' , 'Wind Direction Degrees' , 'Wind Gust Kt', 'Sea Level Pressure Hpa'];
						
		th_list.forEach ( function ( element ) {
			let th = document.createElement('th');
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
		dragElement(document.getElementById("airportsMetarsMainDivId"));
	}
	
}