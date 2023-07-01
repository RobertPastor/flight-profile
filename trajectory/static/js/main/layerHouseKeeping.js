

//Define custom control class
class LayerHouseKeepingControl extends og.Control {
	
	constructor(options) {
		super(options);
	}
	
	oninit() {
		//console.log("main Control - oninit");
	}
	
	getMainDivId() {
		
		return "mainHouseKeepingDivId";
	}

	onadd() {
		//console.log("main Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = this.getMainDivId();
		mainDiv.classList.add('mainTable');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move -> layer house keeping";
		draggableMainDiv.classList.add("draggableDivHeader");
		mainDiv.appendChild(draggableMainDiv);
		
		let table = document.createElement('table');
		table.id = "airlineRoutesTableId";

		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');
		
		let th_list = [ 'Airline' , 'Departure Airport' , 'Destination Airport', 'Remove']
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
		dragElement(document.getElementById(this.getMainDivId()));

		//start with hiding this table
		document.getElementById(this.getMainDivId()).style.visibility = 'hidden';
		
	}
	
}