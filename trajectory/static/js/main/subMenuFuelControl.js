
import { Control } from "../og/og.es.js";

export class FuelSubMenu extends Control {
	
	constructor(options) {
		super(options);
	}
	
	oninit() {
		//console.log("main Control - oninit");
	}
	
	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "mainSubMenuFuelDivId";
		mainDiv.classList.add('mainControlSubMenu');
		
		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		let row_0 = document.createElement('tr');
				
		let row_0_data_3 = document.createElement('td');
		row_0_data_3.innerHTML = '<div><button id="btnFuelEfficieny" >Fuel Efficiency</button></div>';
		row_0_data_3.title = "click to download the airline Fuel Efficiency computations";
		row_0.appendChild(row_0_data_3);
		
		let row_0_data_4 = document.createElement('td');
		row_0_data_4.innerHTML = '<div><button id="btnFuelPlanner" >Fuel Planner</button></div>';
		row_0_data_4.title = "click to see the Fuel Planner page";
		row_0.appendChild(row_0_data_4);
		
		// ---------------
		tbody.appendChild(row_0);
		
		table.appendChild(tbody);
		mainDiv.appendChild(table);
		
		this.renderer.div.appendChild(mainDiv);
		
		// start hiding this table
		$("#mainSubMenuFuelDivId").hide();
		
	}
}