import {
        Control
    } from "../og/og.es.js";


export class AirlineOptimizationsSubMenu extends Control {
	
	constructor(options) {
		super(options);
	}
	
	oninit() {
		//console.log("main Control - oninit");
	}
	
	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "mainSubMenuOptimizationsDivId";
		mainDiv.classList.add('mainControlSubMenu');
		
		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		// ------- 1st row --- progress bar
		let row_2 = document.createElement('tr');
		
		
		// 27th January 2023 - Fleet Assignment based upon costs optimization
		let row_2_data_8 = document.createElement('td');
		row_2_data_8.innerHTML = '<div><button id="btnLaunchCostsOptimization" >Costs Min</button></div>';
		row_2_data_8.title = "click to see the best aircrafts selection to minimize costs";
		row_2.appendChild(row_2_data_8);
		
		// Costs per Average Seat Miles
		let row_2_data_9 = document.createElement('td');
		row_2_data_9.innerHTML = '<div><button id="btnLaunchCASM" >CASM</button></div>';
		row_2_data_9.title = "click to download an EXCEL file showing Cost per Available Seat Miles";
		row_2.appendChild(row_2_data_9);
		
		// Costs per Average Seat Miles Optimization
		let row_2_data_10 = document.createElement('td');
		row_2_data_10.innerHTML = '<div><button id="btnLaunchCasmOptimization" >CASM Min</button></div>';
		row_2_data_10.title = "click to see the best aircrafts selection to minimize Costs per Available Seat Miles"; 
		row_2.appendChild(row_2_data_10);
		
		let row_2_data_11 = document.createElement('td');
		row_2_data_11.innerHTML = '<div><button id="btnLaunchSeatMilesMaximization" >Seat Miles Max</button></div>';
		row_2_data_11.title = "click to download an EXCEL showing the best aircrafts selection to maximise Seat Miles"; 
		row_2.appendChild(row_2_data_11);
		
		// ---------------
		tbody.appendChild(row_2);
		
		table.appendChild(tbody);
		mainDiv.appendChild(table);
		
		this.renderer.div.appendChild(mainDiv);
		
		// start hiding this table
		$("#mainSubMenuOptimizationsDivId").hide();
	}
}
		