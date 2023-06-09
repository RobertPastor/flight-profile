

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
		
		let span = document.createElement('span');
		span.id = "hideId";
		span.innerHTML = "Click to hide";
		// call a function
		span.onclick = clickToHide;
		draggableMainDiv.appendChild(span);
		
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
		label_0_2.innerHTML = " ICAO ->" ;
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
		label_1_1.innerHTML = " Adep ->" ;
		div_1_0.appendChild(label_1_1);
		
		let input_1_0 = document.createElement("input");
		input_1_0.id = "fuelPlannerAirlineAdepICAOcodeId" ;
		input_1_0.maxlength = "4";
		input_1_0.size = "4";
		div_1_0.appendChild(input_1_0);
		
		let label_1_2 = document.createElement("label");
		label_1_2.innerHTML = " Ades ->" ;
		div_1_0.appendChild(label_1_2);
		
		let input_1_1 = document.createElement("input");
		input_1_1.id = "fuelPlannerAirlineAdesICAOcodeId" ;
		input_1_1.maxlength = "4";
		input_1_1.size = "4";
		div_1_0.appendChild(input_1_1);
		
		let label_1_3 = document.createElement("label");
		label_1_3.innerHTML = " Great Circle Miles ->" ;
		div_1_0.appendChild(label_1_3);
		
		let input_1_2 = document.createElement("input");
		input_1_2.id = "fuelPlannerRouteLengthId" ;
		input_1_2.maxlength = "6";
		input_1_2.size = "6";
		div_1_0.appendChild(input_1_2);

		// add div to td
		td_1_0.appendChild(div_1_0);
		row_1.appendChild(td_1_0);
		
		// add second row to the table
		tbody.appendChild(row_1);
		
		//=========================================
		// third row
		let row_2 = document.createElement('tr');
		let td_2_0 = document.createElement('td');
		
		// div
		
		let div_2_0 = document.createElement('div');
		div_2_0.id = "fuelPlannerWeightId";
		
		// minimum mass
		let label_2_0 = document.createElement("label");
		label_2_0.innerHTML = " Min Mass (Kg) ->" ;
		div_2_0.appendChild(label_2_0);

		let input_2_0 = document.createElement("input");
		input_2_0.id = "fuelPlannerMinimumMassId" ;
		input_2_0.maxlength = "6";
		input_2_0.size = "6";
		div_2_0.appendChild(input_2_0);
		
		// max payload
		let label_2_1 = document.createElement("label");
		label_2_1.innerHTML = " Max PayLoad (Kg) ->" ;
		div_2_0.appendChild(label_2_1);

		let input_2_1 = document.createElement("input");
		input_2_1.id = "fuelPlannerMaxPayLoadMassId" ;
		input_2_1.maxlength = "6";
		input_2_1.size = "6";
		div_2_0.appendChild(input_2_1);
		
		// max mass
		let label_2_2 = document.createElement("label");
		label_2_2.innerHTML = " Max Mass (Kg) ->" ;
		div_2_0.appendChild(label_2_2);

		let input_2_2 = document.createElement("input");
		input_2_2.id = "fuelPlannerMaximumMassId" ;
		input_2_2.maxlength = "6";
		input_2_2.size = "6";
		div_2_0.appendChild(input_2_2);
		
		// add div to td
		td_2_0.appendChild(div_2_0);
		row_2.appendChild(td_2_0);
		// add  row to the table tbody
		tbody.appendChild(row_2);
		
		// ================== fourth row =================
		let row_3 = document.createElement('tr');
		let td_3_0 = document.createElement('td');
		
		// create div
		let div_3_0 = document.createElement('div');
		div_3_0.id = "fuelPlannerTakeOffId";
		
		//---------------------------------
		// takeoff mass
		let label_3_0 = document.createElement("label");
		label_3_0.innerHTML = " TakeOff Mass (Kg) ->" ;
		div_3_0.appendChild(label_3_0);

		let input_3_0 = document.createElement("input");
		input_3_0.id = "fuelPlannerTakeOffMassId" ;
		input_3_0.maxlength = "6";
		input_3_0.size = "6";
		div_3_0.appendChild(input_3_0);
		
		// ------------
		// leg duration
		let label_3_1 = document.createElement("label");
		label_3_1.innerHTML = " Leg Duration (sec) ->" ;
		div_3_0.appendChild(label_3_1);

		let input_3_1 = document.createElement("input");
		input_3_1.id = "fuelPlannerLegDurationId" ;
		input_3_1.maxlength = "6";
		input_3_1.size = "6";
		div_3_0.appendChild(input_3_1);
		
		// ------------
		// leg length
		let label_3_2 = document.createElement("label");
		label_3_2.innerHTML = " Leg Length (miles) ->" ;
		div_3_0.appendChild(label_3_2);

		let input_3_2 = document.createElement("input");
		input_3_2.id = "fuelPlannerLegLengthId" ;
		input_3_2.maxlength = "6";
		input_3_2.size = "6";
		div_3_0.appendChild(input_3_2);
		
		// ------------
		// trip fuel 
		let label_3_3 = document.createElement("label");
		label_3_3.innerHTML = " Trip Fuel (kg) ->" ;
		div_3_0.appendChild(label_3_3);

		let input_3_3 = document.createElement("input");
		input_3_3.id = "fuelPlannerFuelBurnId" ;
		input_3_3.maxlength = "6";
		input_3_3.size = "6";
		div_3_0.appendChild(input_3_3);
		
		// one hour reserve
		let label_3_4 = document.createElement("label");
		label_3_4.innerHTML = " One Hour Reserve Fuel (kg) ->" ;
		div_3_0.appendChild(label_3_4);

		let input_3_4 = document.createElement("input");
		input_3_4.id = "fuelPlannerFuelOneHourReserveFuelId" ;
		input_3_4.maxlength = "6";
		input_3_4.size = "6";
		div_3_0.appendChild(input_3_4);
		
		// add div to td
		td_3_0.appendChild(div_3_0);
		row_3.appendChild(td_3_0);

		// add  row to the table tbody
		tbody.appendChild(row_3);
		
		// ================== next row
		let row_4 = document.createElement('tr');
		let td_4_0 = document.createElement('td');
		
		// create div
		let div_4_0 = document.createElement('div');
		div_4_0.id = "fuelPlannerOptimalTakeOffId";
		
		//---------------------------------
		// takeoff mass
		let label_4_0 = document.createElement("label");
		label_4_0.innerHTML = " Optimal TakeOff Mass ===> Min Mass + 80% of PayLoad + Trip Fuel + Reserve Fuel (kg) --->" ;
		div_4_0.appendChild(label_4_0);

		let input_4_0 = document.createElement("input");
		input_4_0.id = "fuelPlannerOptimalTakeOffMassId" ;
		input_4_0.maxlength = "6";
		input_4_0.size = "6";
		div_4_0.appendChild(input_4_0);
		
		//---------------------------------
		// link to the fuel planner website
		//let label_4_1 = document.createElement("label");
		//label_4_1.innerHTML = " See Fuel Planner --->" ;
		//div_4_0.appendChild(label_4_1);
		
		// link to fuel planner
		//let label_4_2 = document.createElement("span");
		//label_4_2.innerHTML = ' <a href="http://fuelplanner.com/" target="_blank">Fuel Planner</a> ' ;
		//div_4_0.appendChild(label_4_2);
		
		// add div to td
		td_4_0.appendChild(div_4_0);
		row_4.appendChild(td_4_0);

		// add  row to the table tbody
		tbody.appendChild(row_4);
		
		
		// =================
		// --> table to tbody
		table.appendChild(tbody);
		// --> add table to main div
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
		// set Route Length Miles as read only
		document.getElementById('fuelPlannerRouteLengthId').readOnly = true;
		// Minimum Mass 
		document.getElementById('fuelPlannerMinimumMassId').readOnly = true;
		document.getElementById('fuelPlannerMaximumMassId').readOnly = true;
		document.getElementById('fuelPlannerMaxPayLoadMassId').readOnly = true;
		
		document.getElementById('fuelPlannerTakeOffMassId').readOnly = true;
		document.getElementById('fuelPlannerLegDurationId').readOnly = true;
		document.getElementById('fuelPlannerLegLengthId').readOnly = true;
		document.getElementById('fuelPlannerFuelBurnId').readOnly = true;
		document.getElementById('fuelPlannerFuelOneHourReserveFuelId').readOnly = true;
		document.getElementById('fuelPlannerOptimalTakeOffMassId').readOnly = true;
		

	}

	oninit() {
		//console.log("main Control - oninit");
	}
	
}