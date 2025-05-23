
import {
        Control
    } from "../og/og.es.js";
    
    
//Define custom control class
export class OgLayerCleanerControl extends Control {
	
	constructor(options) {
		super(options);
	}
	
	oninit() {
		//console.log("main Control - oninit");
	}
	
	getMainDivId() {
		
		return "mainHouseKeepingDivId";
	}
	
	getMainTableId() {
		return "ogLayerCleanerTableId";
	}

	onadd() {
		//console.log("main Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = this.getMainDivId();
		mainDiv.classList.add('mainTable');
		mainDiv.classList.add('layerCleaner');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move -> layer cleaner";
		draggableMainDiv.classList.add("draggableDivHeader");
		mainDiv.appendChild(draggableMainDiv);
		
		let table = document.createElement('table');
		table.id = this.getMainTableId();

		let thead = document.createElement('thead');
		let row_1 = document.createElement('tr');
		
		let th_list = [ 'Airline' , 'Departure' , 'Destination', 'Layer' , 'Action'];
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