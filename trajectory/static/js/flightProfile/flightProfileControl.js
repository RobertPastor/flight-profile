


//Define custom control class
class FlighProfileControl extends og.Control {
	constructor(options) {
		super(options);
	}
	
	getMainDivId() {
		this.mainDivId = "flightProfileMainDivId";
		return this.mainDivId;
	}

	onadd() {
		//console.log("flight profile Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = this.getMainDivId();
		mainDiv.style = "display: none;";
		mainDiv.classList.add('flightProfileTableDiv');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move -> Flight Profile Computation";
		draggableMainDiv.classList.add("draggableDivHeader");
		
		let span = document.createElement('span');
		span.id = "hideId";
		span.innerHTML = "Click to hide";
		// call a function
		span.onclick = clickToHide;
		draggableMainDiv.appendChild(span);
		
		mainDiv.appendChild(draggableMainDiv);
		
		let table = document.createElement('table');
		table.id = "flightProfileTableId";
		
		let row_1 = document.createElement('tr');
		let td = document.createElement('td');
		
		// ------------------
		
		let div_1 = document.createElement('div');
		div_1.id = "aircraftSelectionId";
		div_1.classList.add("aircraftSelectionClass");
		
		let label_1_1 = document.createElement("label");
		label_1_1.innerHTML = "Aircraft ->" ;
		div_1.appendChild(label_1_1);
		
		let select_1 = document.createElement("select");
		select_1.id = "airlineAircraftId";
		select_1.name = "airlineAircraftName";
		div_1.appendChild(select_1);
		
		// ---------- label take off weight
		
		let label_1_2 = document.createElement("label");
		//label_1_2.innerHTML = " Min TakeOff Mass (kg) ->" ;
		label_1_2.innerHTML = " ->" ;
		div_1.appendChild(label_1_2);
		
		// hidden input with min take off weight KG
		let input_1_1 = document.createElement("input");
		input_1_1.id = "minTakeOffMassKgId" ;
		input_1_1.hidden = false;
		input_1_1.maxlength = "6";
		input_1_1.size = "3";
		input_1_1.title = "minimal TakeOff Mass (Kg)" ;
		input_1_1.readOnly = true;
		div_1.appendChild(input_1_1);
		
		let label_1_3 = document.createElement("label");
		label_1_3.innerHTML = " TakeOff Mass (kg) ->" ;
		div_1.appendChild(label_1_3);
		
		let input_1 = document.createElement("input");
		input_1.id = "TakeOffMassKgId" ;
		input_1.maxlength = "5";
		input_1.size = "3";
		input_1.title = "insert here the TakeOff mass (kg)" ;
		div_1.appendChild(input_1);
		
		let label_1_4 = document.createElement("label");
		//label_1_4.innerHTML = " MaxTakeOff Mass (kg) ->" ;
		label_1_4.innerHTML = " ->" ;
		div_1.appendChild(label_1_4);
		
		// hidden input with max take off weight KG
		let input_1_2 = document.createElement("input");
		input_1_2.id = "maxTakeOffMassKgId" ;
		input_1_2.hidden = false;
		input_1_2.maxlength = "6";
		input_1_2.size = "3";
		input_1_2.title = "maximal TakeOff Mass (Kg)" ;
		input_1_2.readOnly = true;
		div_1.appendChild(input_1_2);
		
		// ------------- Requested Flight Level
		
		let label_1_5 = document.createElement("label");
		label_1_5.innerHTML = "Requested Flight Level (feet) ->" ;
		div_1.appendChild(label_1_5);
		
		let input_2 = document.createElement("input");
		input_2.id = "requestedFlightLevelId" ;
		input_2.maxlength = "3";
		input_2.size = "3";
		input_2.title = "insert here the requested flight level (feet)";
		div_1.appendChild(input_2);
		
		// hidden input with max fligh level
		
		let label_1_6 = document.createElement("label");
		label_1_6.innerHTML = " ->" ;
		div_1.appendChild(label_1_6);
		
		let input_2_1 = document.createElement("input");
		input_2_1.id = "maxFlightLevelId" ;
		input_2_1.hidden = false;
		input_2_1.maxlength = "3";
		input_2_1.size = "3";
		input_2_1.title = "max Flight Level (feet)";
		input_2_1.readOnly = true;
		div_1.appendChild(input_2_1);
		
		td.appendChild(div_1);
		
		// ---------------
		
		let div_2 = document.createElement('div');
		div_2.id = "routesSelectionId";
		div_2.classList.add("routesSelectionClass");
		
		let label_2 = document.createElement("label");
		label_2.innerHTML = "Route ->" ;
		div_2.appendChild(label_2);
		
		// route selector
		let select_2 = document.createElement("select");
		select_2.id = "airlineRouteId";
		select_2.name = "airlineRouteName";

		div_2.appendChild(select_2);
		
		td.appendChild(div_2);

		// --------------------
		
		let div_3 = document.createElement('div');
		div_3.id = "runWaysSelectionFlightProfileId";
		div_3.classList.add("runWaysSelectionFlightProfileClass");
		
		let label_3 = document.createElement("label");
		label_3.innerHTML = "Departure RunWay -> " ;
		div_3.appendChild(label_3);
		
		let select_3 = document.createElement("select");
		select_3.id = "airlineDepartureRunWayFlightProfileId";
		select_3.name = "airlineDepartureRunWayFlightProfileName";

		div_3.appendChild(select_3);
		td.appendChild(div_3);
		
		// --------------------
					
		let div_4 = document.createElement('div');
		div_4.id = "runWaysSelectionFlightProfileId";
		div_4.classList.add("runWaysSelectionFlightProfileClass");
		
		let label_4 = document.createElement("label");
		label_4.innerHTML = "Arrival RunWay -> " ;
		div_4.appendChild(label_4);
		
		let select_4 = document.createElement("select");
		select_4.id = "airlineArrivalRunWayFlightProfileId";
		select_4.name = "airlineArrivalRunWayFlightProfileName";

		div_4.appendChild(select_4);
		
		td.appendChild(div_4);
		
		// --------------------

		let div_5 = document.createElement('div');
		div_5.id = "launchComputeProfileId";
		div_5.classList.add("launchComputeProfileClass");

		// -------------------------------------------
		// first button  - all button added to the same div
		
		let button_5 = document.createElement("button");
		button_5.id = "btnComputeFlightProfileId";
		button_5.innerHTML = "Compute Flight Profile";
		div_5.appendChild(button_5);

		// --------------------
		
		let button_6 = document.createElement("button");
		button_6.id = "btnComputeCostsId";
		button_6.innerHTML = "Compute Costs";
		div_5.appendChild(button_6);
		
		// --------------------
		// button down load state vector
		
		let button_7 = document.createElement("button");
		button_7.id = "btnDownLoadVerticalProfileId";
		button_7.innerHTML = "Download Vertical Profile";
		div_5.appendChild(button_7);
		
		// --------------------
		// button download XML file
		
		let button_8 = document.createElement("button");
		button_8.id = "btnDownLoadKMLfileId";
		button_8.innerHTML = "Download KML";
		div_5.appendChild(button_8);

		// add div with all buttons to the TD
		td.appendChild(div_5);
		
		// --------------------
		
		row_1.appendChild(td);
		table.appendChild(row_1);
		mainDiv.appendChild(table);
		this.renderer.div.appendChild(mainDiv);
		
		// Make the Main Div element draggable:
		dragElement(document.getElementById(this.getMainDivId()));
	}

	oninit() {
		//console.log("flight profile Control - oninit");
	}
};