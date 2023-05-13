

//Define custom control class
class FuelPlannerControl extends og.Control {
	
	constructor(options) {
		super(options);
	}

	onadd() {
		//console.log("main Control - onadd");
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "mainFuelPlannerDivId";
		mainDiv.classList.add('mainFuelPlannerDiv');
		mainDiv.style="display: none;";
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move -> Fuel Planner";
		draggableMainDiv.classList.add("draggableDivHeader");
		mainDiv.appendChild(draggableMainDiv);
						
		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		// ------- 1st row --- select the aircraft
		let row_0 = document.createElement('tr');
		let td_0_0 = document.createElement('td');
		
		let div_0_1 = document.createElement('div');
		div_0_1.id = "fuelPlannerAircraftSelectionId";
		div_0_1.classList.add("aircraftSelectionClass");
		
		let label_0_1 = document.createElement("label");
		label_0_1.innerHTML = "Aircraft ->" ;
		div_0_1.appendChild(label_0_1);
		
		let select_0_1 = document.createElement("select");
		select_0_1.id = "fuelPlannerAirlineAircraftSelectId";
		select_0_1.name = "fuelPlannerAirlineAircraftName";
		div_0_1.appendChild(select_0_1);
		
		let label_0_2 = document.createElement("label");
		label_0_2.innerHTML = " ICAO code ->" ;
		div_0_1.appendChild(label_0_2);
		
		let input_0_1 = document.createElement("input");
		input_0_1.id = "fuelPlannerAirlineAircraftICAOcodeId" ;
		input_0_1.maxlength = "4";
		input_0_1.size = "4";
		div_0_1.appendChild(input_0_1);
		
		// ----------------
		// add div to td and then add td to row
		td_0_0.appendChild(div_0_1);
		row_0.appendChild(td_0_0);
		
		// add 1st row to the table
		tbody.appendChild(row_0);
		
		// ---- second row - select the route
		let row_1 = document.createElement('tr');
		let td_1_0 = document.createElement('td');
		
		let div_1_0 = document.createElement('div');
		div_1_0.id = "fuelPlannerRouteSelectionId";
		div_1_0.classList.add("routeSelectionClass");
		
		let label_1_0 = document.createElement("label");
		label_1_0.innerHTML = "Route ->" ;
		div_1_0.appendChild(label_1_0);
		
		let select_1_0 = document.createElement("select");
		select_1_0.id = "fuelPlannerAirlineRouteSelectId";
		select_1_0.name = "fuelPlannerAirlineRouteName";
		div_1_0.appendChild(select_1_0);
		
		let label_1_1 = document.createElement("label");
		label_1_1.innerHTML = " Adep ICAO ->" ;
		div_1_0.appendChild(label_1_1);
		
		let input_1_0 = document.createElement("input");
		input_1_0.id = "fuelPlannerAirlineAdepICAOcodeId" ;
		input_1_0.maxlength = "4";
		input_1_0.size = "4";
		div_1_0.appendChild(input_1_0);
		
		let label_1_2 = document.createElement("label");
		label_1_2.innerHTML = " Ades ICAO ->" ;
		div_1_0.appendChild(label_1_2);
		
		let input_1_1 = document.createElement("input");
		input_1_1.id = "fuelPlannerAirlineAdesICAOcodeId" ;
		input_1_1.maxlength = "4";
		input_1_1.size = "4";
		div_1_0.appendChild(input_1_1);
		
		let label_1_3 = document.createElement("label");
		label_1_3.innerHTML = " Miles ->" ;
		div_1_0.appendChild(label_1_3);
		
		let input_1_2 = document.createElement("input");
		input_1_2.id = "fuelPlannerRouteLengthId" ;
		input_1_2.maxlength = "6";
		input_1_2.size = "6";
		div_1_0.appendChild(input_1_2);

		// add div to td
		td_1_0.appendChild(div_1_0);
		row_1.appendChild(td_1_0);
		
		// add 1st row to the table
		tbody.appendChild(row_1);
		
		// --> table to body
		table.appendChild(tbody);
		mainDiv.appendChild(table);
		
		this.renderer.div.appendChild(mainDiv);
		
		// Make the Main Div element draggable:
		dragElement(document.getElementById("mainFuelPlannerDivId"));
		
		// set Aircraft ICAO code INPUT as read only
		document.getElementById('fuelPlannerAirlineAircraftICAOcodeId').readOnly = true;
		// set Airport departure ICAO code INPUT as read only
		document.getElementById('fuelPlannerAirlineAdepICAOcodeId').readOnly = true;
		// set Airport arrival ICAO code INPUT as read only
		document.getElementById('fuelPlannerAirlineAdesICAOcodeId').readOnly = true;
	}

	oninit() {
		//console.log("main Control - oninit");
	}
	
}