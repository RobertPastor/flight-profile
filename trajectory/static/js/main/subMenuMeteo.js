
import {
        Control
    } from "../og/og.es.js";
    
    
export class MeteoSubMenu extends Control {

	constructor(options) {
		super(options);
	}
	
	oninit() {
		//console.log("main Control - oninit");
	}
	
	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "mainSubMenuMeteoDivId";
		mainDiv.classList.add('mainControlSubMenu');
		
		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		let row_0 = document.createElement('tr');
				
		let row_0_data_3 = document.createElement('td');
		row_0_data_3.innerHTML = '<div><button id="btnWindTemperature" >Wind Temperature</button></div>';
		row_0_data_3.title = "click to download the Wind Temperature Excel file";
		row_0.appendChild(row_0_data_3);
		
		let row_0_data_4 = document.createElement('td');
		row_0_data_4.innerHTML = '<div><button id="btnMetar" >Metar</button></div>';
		row_0_data_4.title = "click to see the Metar data";
		row_0.appendChild(row_0_data_4);
		
		// ---------------
		tbody.appendChild(row_0);
		
		table.appendChild(tbody);
		mainDiv.appendChild(table);
		
		this.renderer.div.appendChild(mainDiv);
		
		// start hiding this table
		$("#mainSubMenuMeteoDivId").hide();
		
	}
}
