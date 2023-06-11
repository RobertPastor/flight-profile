

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
		draggableMainDiv.innerHTML = "Click here to move -> Main navigation bar";
		draggableMainDiv.classList.add("draggableDivHeader");
		mainDiv.appendChild(draggableMainDiv);
		
		let span = document.createElement('span');
		span.id = "PdfPresentationId";
		span.innerHTML = "<a title='download a pdf presentation' id='linkDownloadPdfPresentationId' class='download' href='#' onclick='initDownloadPdfPresentation()' ></a>";
		draggableMainDiv.appendChild(span);
						
		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		// ------- 1st row --- progress bar
		let row_0 = document.createElement('tr');
		
		let row_0_data_1 = document.createElement('td');
		row_0_data_1.colSpan = "11";
		row_0_data_1.innerHTML = '<div id="workerId" class="w3-container progressBar" style="width:100%"></div>';
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
		
		let row_1_data_3 = document.createElement('td');
		row_1_data_3.colSpan = "7";
		
		row_1_data_3.innerHTML = '<div class="alignRight"><span>Airline Fleet Management Tool proposed by </span><a href="https://www.appsintellect.org" target="_blank">appsintellect</a></div>';
		row_1.appendChild(row_1_data_3);
		
		let row_1_data_4 = document.createElement('td');
		row_1_data_4.colSpan = "1";
		
		row_1_data_4.classList.add('question_mark_bg')
		row_1_data_4.innerHTML = '<div id="helpId" class="question_mark" title="click to obtain some help" onclick="showHelp()" ></div>';
		row_1.appendChild(row_1_data_4);
		
		tbody.appendChild(row_1);
		
		// --------- 3rd row
		
		let row_2 = document.createElement('tr');
		
		let row_2_data_2 = document.createElement('td');
		row_2_data_2.innerHTML = '<div><button id="btnAirlineFleet" >Fleet</button></div>';
		row_2_data_2.title = "click to see the airline fleet, aircraft, number of seats, hourly costs";
		row_2.appendChild(row_2_data_2);
		
		let row_2_data_3 = document.createElement('td');
		row_2_data_3.innerHTML = '<div><button id="btnAirports" >Airports</button></div>';
		row_2_data_3.title = "click to see the airline airports and the waypoints";
		row_2.appendChild(row_2_data_3);
		
		let row_2_data_4 = document.createElement('td');
		row_2_data_4.innerHTML = '<div><button id="btnAirlineRoutes" >Routes</button></div>';
		row_2_data_4.title = "click to see the routes, way-points, best runway";
		row_2.appendChild(row_2_data_4);
		
		// 8th June 2023 - SID STAR
		//let row_2_data_5 = document.createElement('td');
		//row_2_data_5.innerHTML = '<div><button id="btnSidStar" >SID/STAR</button></div>';
		//row_2.appendChild(row_2_data_5);
		
		
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
		row_2_data_8.innerHTML = '<div><button id="btnLaunchCostsOptimization" >Costs Min</button></div>';
		row_2_data_8.title = "click to see the best aircraft selection to minimize costs";
		row_2.appendChild(row_2_data_8);
		
		// Costs per Average Seat Miles
		let row_2_data_9 = document.createElement('td');
		row_2_data_9.innerHTML = '<div><button id="btnLaunchCASM" >CASM</button></div>';
		row_2_data_9.title = "click to download an EXCEL Cost per Available Seat Miles file";
		row_2.appendChild(row_2_data_9);
		
		// Costs per Average Seat Miles Optimization
		let row_2_data_10 = document.createElement('td');
		row_2_data_10.innerHTML = '<div><button id="btnLaunchCasmOptimization" >CASM Min</button></div>';
		row_2_data_10.title = "click to see the best aircraft selection to minimize Costs per Available Seat Miles"; 
		row_2.appendChild(row_2_data_10);
		
		let row_2_data_11 = document.createElement('td');
		row_2_data_11.innerHTML = '<div><button id="btnLaunchSeatMilesMaximization" >Seat Miles Max</button></div>';
		row_2_data_11.title = "click to see the best aircraft selection to minimize Costs per Available Seat Miles"; 
		row_2.appendChild(row_2_data_11);
		
		let row_2_data_12 = document.createElement('td');
		row_2_data_12.innerHTML = '<div><button id="btnLaunchFuelPlanner" >Fuel Planner</button></div>';
		row_2_data_12.title = "click to support computing aircraft takeoff weight while estimating the needed fuel"; 
		row_2.appendChild(row_2_data_12);
		
		// 13th May 2023 - add fuel planner
		let row_2_data_13 = document.createElement('td');
		row_2_data_13.classList.add('question_mark_bg')
		row_2_data_13.innerHTML = '<div id="helpId" class="exclamation_mark" title="click to obtain some configuration information" onclick="showConfiguration()" ></div>';
		row_2.appendChild(row_2_data_13);
		
		// ---------------
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