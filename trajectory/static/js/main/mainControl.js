

//Define custom control class
class MainControl extends og.Control {
	constructor(options) {
		super(options);
	}

	onadd() {
		//console.log("main Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "mainTableId";
		mainDiv.classList.add('mainTable');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move";
		draggableMainDiv.classList.add("draggableDivHeader");
		mainDiv.appendChild(draggableMainDiv);
						
		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		// ------- 1st row --- progress bar
		let row_0 = document.createElement('tr');
		
		let row_0_data_1 = document.createElement('td');
		row_0_data_1.colSpan = "10";
		
		row_0_data_1.innerHTML = '<div id="workerId" class="w3-container w3-green" style="width:100%"></div>';
		row_0.appendChild(row_0_data_1);
		
		tbody.appendChild(row_0);
		
		// ------- 2nd row --------------
		
		let row_1 = document.createElement('tr');
		
		let row_1_data_1 = document.createElement('td');
		row_1_data_1.colSpan = "3";
		
		let div_1 = document.createElement('div');
		
		let select = document.createElement("select");
		select.id = "airlineSelectId";
		select.title = "click to select an airline";
		select.classList.add('airlineSelect');

		div_1.appendChild(select);
		row_1_data_1.appendChild(div_1);
		row_1.appendChild(row_1_data_1);
		
		let row_1_data_2 = document.createElement('td');
		row_1_data_2.colSpan = "6";
		
		row_1_data_2.innerHTML = '<div class="alignRight"><span>Airline Fleet Management Tool proposed by </span><a href="https://www.appsintellect.org" target="_blank">appsintellect</a></div>';
		row_1.appendChild(row_1_data_2);
		
		let row_1_data_3 = document.createElement('td');
		row_1_data_3.colSpan = "1";
		
		row_1_data_3.classList.add('question_mark_bg')
		row_1_data_3.innerHTML = '<div id="helpId" class="question_mark" title="click to obtain some help" onclick="showHelp()" ></div>';
		row_1.appendChild(row_1_data_3);
		
		tbody.appendChild(row_1);
		
		// --------- 3rd row
		
		let row_2 = document.createElement('tr');
		
		let row_2_data_2 = document.createElement('td');
		row_2_data_2.innerHTML = '<div><button id="btnAirlineFleet" >Fleet</button></div>';
		row_2_data_2.title = "click to see the airline fleet, aircraft, number of seats, hourly costs";
		row_2.appendChild(row_2_data_2);
		
		let row_2_data_3 = document.createElement('td');
		row_2_data_3.innerHTML = '<div><button id="btnAirports" >Airports</button></div>';
		row_2_data_3.title = "click to see the airline airports";
		row_2.appendChild(row_2_data_3);
		
		let row_2_data_4 = document.createElement('td');
		row_2_data_4.innerHTML = '<div><button id="btnAirlineRoutes" >Routes</button></div>';
		row_2_data_4.title = "click to see the routes, way-points, best runway";
		row_2.appendChild(row_2_data_4);
		
		/**
		// 18th September 2022 - airline way points is useless as we can show them for any route
		let row_2_data_5 = document.createElement('td');
		row_2_data_5.innerHTML = '<div><button id="btnWayPoints" >Airline WayPoints</button></div>';
		row_2.appendChild(row_2_data_5);
		**/
		
		let row_2_data_6 = document.createElement('td');
		row_2_data_6.innerHTML = '<div><button id="btnLaunchFlightProfile" >Profile</button></div>';
		row_2_data_6.title = "click to compute a profile, a cost or download an EXCEL profile";
		row_2.appendChild(row_2_data_6);
		
		// 27th January 2023 - Airline costs controls
		let row_2_data_7 = document.createElement('td');
		row_2_data_7.innerHTML = '<div><button id="btnLaunchAirlineCosts" >Costs</button></div>';
		row_2_data_7.title = "click to download an EXCEL costs file";

		row_2.appendChild(row_2_data_7);
		
		// 27th January 2023 - Fleet Assignment based upon costs optimization
		let row_2_data_8 = document.createElement('td');
		row_2_data_8.innerHTML = '<div><button id="btnLaunchCostsOptimization" >Costs Optimization</button></div>';
		row_2_data_8.title = "click to see the best aircraft selection to minimize costs";
		row_2.appendChild(row_2_data_8);
		
		// Costs per Average Seat Miles
		let row_2_data_9 = document.createElement('td');
		row_2_data_9.innerHTML = '<div><button id="btnLaunchCASM" >CASM</button></div>';
		row_2_data_9.title = "click to download an EXCEL Cost per Available Seat Miles file";
		row_2.appendChild(row_2_data_9);
		
		// Costs per Average Seat Miles Optimization
		let row_2_data_10 = document.createElement('td');
		row_2_data_10.innerHTML = '<div><button id="btnLaunchCasmOptimization" >CASM Optimization</button></div>';
		row_2_data_10.title = "click to see the best aircraft selection to minimize Costs per Available Seat Miles"; 
		row_2.appendChild(row_2_data_10);
		
		let row_2_data_11 = document.createElement('td');
		row_2_data_11.innerHTML = '<div><button id="btnLaunchSeatMilesMaximization" >Seats Miles Maximization</button></div>';
		row_2_data_11.title = "click to see the best aircraft selection to minimize Costs per Available Seat Miles"; 
		row_2.appendChild(row_2_data_11);
		
		
		let row_2_data_12 = document.createElement('td');
		
		row_2_data_12.classList.add('question_mark_bg')
		row_2_data_12.innerHTML = '<div id="helpId" class="exclamation_mark" title="click to obtain some configuration information" onclick="showConfiguration()" ></div>';
		row_2.appendChild(row_2_data_12);
		
		tbody.appendChild(row_2);
		
		table.appendChild(tbody);
		mainDiv.appendChild(table);
		
		this.renderer.div.appendChild(mainDiv);
		
		// Make the Main Div element draggable:
		dragElement(document.getElementById("mainTableId"));

	}

	oninit() {
		//console.log("main Control - oninit");
	}
};