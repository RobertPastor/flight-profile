
import { Control } from "../og/og.es.js";
    
import { clickToHide } from "../main/main.js";

export const SingletonFlightProfileControlClass = (function () {
	
	let instance;
    function createInstance() {
        var object = new FlightProfileControl();
        return object;
    }
    return {
        getInstance: function () {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();

//Define custom control class
export class FlightProfileControl extends Control {
	constructor(options) {
		super(options);
	}
	
	getMainDivId() {
		this.mainDivId = "flightProfileMainDivId";
		return this.mainDivId;
	}
	
	getReducedClimbPowerCoeffInputId() {
		return "ReducedClimbPowerPercentageInputId";
	}
	
	getReducedClimPowerCoeffInputDefaultValue() {
		return "15";
	}
	
	getBADACheckBoxId() {
		return "BADAcheckboxId";
	}
	
	getWRAPCheckBoxId() {
		return "WRAPcheckboxId";
	}
	/**
	 * as they are radio / toggle buttons only one can be checked
	 */
	getSelectedBadaWrapMode() {
		
		const radioButtons = document.querySelectorAll('input[name="BadaWrap"]');
		for (const radioButton of radioButtons) {
			if (radioButton.checked) {
				console.log(radioButton.value)
				return radioButton.value;
			}
		}
	}
	
	createRowWithAircraftSelector() {
		
		let row = document.createElement('tr');
		let td_1 = document.createElement('td');
		//td.colSpan = "4";
		
		let div_1 = document.createElement('div');
		div_1.id = "aircraftSelectionId";
		div_1.style.textAlign = "center";
		div_1.classList.add("aircraftSelectionClass");
		
		let label_1 = document.createElement("label");
		label_1.innerHTML = "Select the aircraft ->" ;
		div_1.appendChild(label_1);
		
		let select_1 = document.createElement("select");
		select_1.id = "airlineAircraftId";
		select_1.name = "airlineAircraftName";
		select_1.title = "click to change the aircraft";
		div_1.appendChild(select_1);
		
		td_1.appendChild(div_1);
		row.appendChild(td_1);
		
		// reduced climb power settings
		let td_2 = document.createElement('td');
		
		let div_2 = document.createElement('div');
		div_2.id = "reducedClimbPowerSettingsId";
		div_2.style.textAlign = "center";
		
		let label_2 = document.createElement("label");
		label_2.innerHTML = "Enter Reduced Climb Power % ->" ;
		div_2.appendChild(label_2);
		
		let input_1 = document.createElement("input");
		input_1.id = this.getReducedClimbPowerCoeffInputId();
		input_1.maxlength = "6";
		input_1.size = "5";
		input_1.title = "enter a float between 0% power reduction to a max of 15% power reduction" ;
		input_1.value = this.getReducedClimPowerCoeffInputDefaultValue();
		input_1.style.backgroundColor = '#B2BEB5';
		input_1.readOnly = false;

		div_2.appendChild(input_1);

		td_2.appendChild(div_2);
		row.appendChild(td_2);
		
		// select BADA or Wrap
		let td_3 = document.createElement('td');
		
		let div_3 = document.createElement('div');
		div_3.id = "BadaId";
		div_3.style.textAlign = "center";
		
		let label_3 = document.createElement("label");
		label_3.innerHTML = " Legacy -> " ;
		div_3.appendChild(label_3);
		
		// add a checkbox
		let checkboxBADA   = document.createElement('input');
		checkboxBADA.type  = "radio";
		checkboxBADA.name  = "BadaWrap";
		checkboxBADA.value = "BADA";
		checkboxBADA.title = "Tick to select legacy aircraft performances"
		checkboxBADA.id    = this.getBADACheckBoxId();
		
		div_3.appendChild(checkboxBADA);
		td_3.appendChild(div_3);
		row.appendChild(td_3);
		
		// select BADA or Wrap
		let td_4 = document.createElement('td');
		//td_3.colSpan = "2";
		
		let div_4 = document.createElement('div');
		div_4.id = "WrapId";
		div_4.style.textAlign = "center";
		
		let label_4 = document.createElement("label");
		label_4.innerHTML = " WRAP -> " ;
		div_4.appendChild(label_4);
		
		let checkboxWrap   = document.createElement('input');
		checkboxWrap.type  = "radio";
		checkboxWrap.name  = "BadaWrap";
		checkboxWrap.value = "WRAP";
		checkboxWrap.title = "Tick to select WRAP"
		checkboxWrap.id    = this.getWRAPCheckBoxId();
		
		div_4.appendChild(checkboxWrap);
		
		td_4.appendChild(div_4);
		row.appendChild(td_4);
		
		return row;
	}
	
	createRowWithMass() {
		
		let row = document.createElement('tr');
		let td_1 = document.createElement('td');
		td_1.colSpan = "2";

		// ---------- label take off weight
		let div_1 = document.createElement('div');
		div_1.classList.add("horizontal-align-left");
		
		let label_1_2 = document.createElement("label");
		//label_1_2.innerHTML = " Min TakeOff Mass (kg) ->" ;
		label_1_2.innerHTML = " min ->" ;
		div_1.appendChild(label_1_2);
		
		// hidden input with min take off weight KG
		let input_1_1 = document.createElement("input");
		input_1_1.id = "minTakeOffMassKgId" ;
		input_1_1.hidden = false;
		input_1_1.maxlength = "6";
		input_1_1.size = "5";
		input_1_1.title = "min TakeOff Mass (Kg)" ;
		input_1_1.style.backgroundColor = 'yellow';
		input_1_1.readOnly = true;
		div_1.appendChild(input_1_1);
		
		td_1.appendChild(div_1);
		
		// ---------- label take off weight
		let div_2 = document.createElement('div');
		div_2.classList.add("horizontal-align-left");

		let label_1_3 = document.createElement("label");
		label_1_3.innerHTML = " TakeOff Mass (kg) ->" ;
		div_2.appendChild(label_1_3);
		
		let input_1 = document.createElement("input");
		input_1.id = "TakeOffMassKgId" ;
		input_1.maxlength = "6";
		input_1.size = "5";
		input_1.title = "enter the TakeOff mass (kg)" ;
		input_1.style.backgroundColor = '#B2BEB5';

		div_2.appendChild(input_1);
		
		td_1.appendChild(div_2);
		
		// ---------- label take off weight
		let div_3 = document.createElement('div');
		div_3.classList.add("horizontal-align-right");
		
		let label_1_4 = document.createElement("label");
		//label_1_4.innerHTML = " MaxTakeOff Mass (kg) ->" ;
		label_1_4.innerHTML = " max ->" ;
		div_3.appendChild(label_1_4);
		
		// hidden input with max take off weight KG
		let input_1_2 = document.createElement("input");
		input_1_2.id = "maxTakeOffMassKgId" ;
		input_1_2.hidden = false;
		input_1_2.maxlength = "6";
		input_1_2.size = "5";
		input_1_2.title = "max TakeOff Mass (Kg)" ;
		input_1_2.style.backgroundColor = 'yellow';
		input_1_2.readOnly = true;
		
		div_3.appendChild(input_1_2);
		
		td_1.appendChild(div_3);
		row.appendChild(td_1);
		
		// ------------- Requested Flight Level
		let td_2 = document.createElement('td');
		td_2.colSpan = "2";
		
		let div_4 = document.createElement('div');
		div_4.classList.add("horizontal-align-left");
		
		let label_1_5 = document.createElement("label");
		label_1_5.innerHTML = " Requested Flight Level (feet) ->" ;
		div_4.appendChild(label_1_5);
		
		let input_2 = document.createElement("input");
		input_2.id = "requestedFlightLevelId" ;
		input_2.maxlength = "6";
		input_2.size = "5";
		input_2.title = "enter the Requested Flight Level (feet)";
		input_2.style.backgroundColor = '#B2BEB5';

		div_4.appendChild(input_2);
		
		td_2.appendChild(div_4);
		
		let div_5 = document.createElement('div');
		div_5.classList.add("horizontal-align-right");
		
		// hidden input with max fligh level
		
		let label_1_6 = document.createElement("label");
		label_1_6.innerHTML = " max ->" ;
		div_5.appendChild(label_1_6);
		
		let input_2_1 = document.createElement("input");
		input_2_1.id = "maxFlightLevelId" ;
		input_2_1.hidden = false;
		input_2_1.maxlength = "6";
		input_2_1.size = "5";
		input_2_1.title = "max Flight Level (feet)";
		input_2_1.style.backgroundColor = 'yellow';
		input_2_1.readOnly = true;
		div_5.appendChild(input_2_1);
		
		td_2.appendChild(div_5);
		
		row.appendChild(td_2);
		return row;
	}
	
	getAdepICAOcodeInputId() {
		return "fligthProfileControlAdepICAOInputId";
	}
	
	getAdesICAOcodeInputId() {
		return "fligthProfileControlAdesICAOInputId";
	}
	
	// 14th August 2023 - checkbox to select best departure runway
	getBestDepartureRunwayCheckBoxId() {
		return "BestDepartureRunwayCheckBoxId";
	}
	
	// 14th August 2023 - checkbox to select best arrival runway
	getBestArrivalRunwayCheckBoxId() {
		return "BestArrivalRunwayCheckBoxId";
	}
	
	getDirectRouteCheckBoxId() {
		return "DirectRouteCheckBoxId";
	}
	
	createRowWithRouteSelector() {
		
		let row = document.createElement('tr');
		
		let td = document.createElement('td');
		td.colSpan = "4";
		
		let div_1 = document.createElement('div');
		div_1.classList.add("horizontal-align-left");
		
		// input to store ICAO code of the Adep
		let input_1 = document.createElement("input");
		input_1.id     = this.getAdepICAOcodeInputId();
		input_1.hidden = false;
		input_1.maxlength = "5";
		input_1.size = "5";
		input_1.title = "Departure ICAO";
		input_1.style.backgroundColor = 'yellow';
		input_1.readOnly = true;
		
		div_1.appendChild(input_1);
		td.appendChild(div_1);
		
		// route selector

		let div_2 = document.createElement('div');
		div_2.id = "routesSelectionId";
		div_2.classList.add("routesSelectionClass");
		div_2.classList.add("horizontal-align-left");

		let label_2 = document.createElement("label");
		label_2.innerHTML = "Route Selector ->" ;
		div_2.appendChild(label_2);
		
		// route selector
		let select_2 = document.createElement("select");
		select_2.id = "airlineRouteId";
		select_2.name = "airlineRouteName";
		select_2.title = "click to select the route";

		div_2.appendChild(select_2);
		td.appendChild(div_2);
		
		// Ades ICAO code
		let div_3 = document.createElement('div');
		div_3.classList.add("horizontal-align-right");

		// input to store ICAO code of the Ades
		let input_2 = document.createElement("input");
		input_2.id = this.getAdesICAOcodeInputId();
		input_2.hidden = false;
		input_2.maxlength = "5";
		input_2.size = "5";
		input_2.title = "Arrival ICAO";
		input_2.style.backgroundColor = 'yellow';
		input_2.readOnly = true;
		
		div_3.appendChild(input_2);
		td.appendChild(div_3);
		
		// 1st April 2024 - add checkbox to fly direct route
		let div_4 = document.createElement('div');
		div_4.classList.add("horizontal-align-right");
		
		let label_3 = document.createElement("label");
		label_3.innerHTML = "Fly Direct Route ->" ;
		div_4.appendChild(label_3);
		
		// add a checkbox
		let checkboxDirectRoute = document.createElement('input');
		checkboxDirectRoute.type = "checkbox";
		checkboxDirectRoute.name = "DirectRouteCheckBox";
		checkboxDirectRoute.value = "value";
		checkboxDirectRoute.title = "tick to fly direct route"
		checkboxDirectRoute.id    = this.getDirectRouteCheckBoxId();
		
		div_4.appendChild(checkboxDirectRoute);
		td.appendChild(div_4);
		
		row.appendChild(td);
		return row;
	}
	
	/**
	 * 14th August 2023 - add a checkbox to select the Best Runway
	 */
	createRowWithRunwaySelector() {
		
		let row = document.createElement('tr');
		let td_1 = document.createElement('td');
		td_1.colSpan = "2";
		
		let div_3 = document.createElement('div');
		div_3.id = "runWaysSelectionFlightProfileId";
		div_3.classList.add("runWaysSelectionFlightProfileClass");
		
		// add a checkbox
		let checkboxBestDepartureRunway = document.createElement('input');
		checkboxBestDepartureRunway.type = "checkbox";
		checkboxBestDepartureRunway.name = "BestDepartureRunwayCheckBox";
		checkboxBestDepartureRunway.value = "value";
		checkboxBestDepartureRunway.title = "Tick to select best departure runway"
		checkboxBestDepartureRunway.id    = this.getBestDepartureRunwayCheckBoxId();
		
		div_3.appendChild(checkboxBestDepartureRunway);
		
		let label_3 = document.createElement("label");
		label_3.innerHTML = " -> Departure RunWay -> " ;
		div_3.appendChild(label_3);
		
		let select_3   = document.createElement("select");
		select_3.id    = "airlineDepartureRunWayFlightProfileId";
		select_3.name  = "airlineDepartureRunWayFlightProfileName";
		select_3.title = "click to select the Departure runway";

		div_3.appendChild(select_3);
		td_1.appendChild(div_3);
		
		// --------------------
		let td_2 = document.createElement('td');
		td_2.colSpan = "2";
		
		let div_4 = document.createElement('div');
		div_4.id = "runWaysSelectionFlightProfileId";
		div_4.classList.add("runWaysSelectionFlightProfileClass");
		
		// add a checkbox
		let checkboxBestArrivalRunway   = document.createElement('input');
		checkboxBestArrivalRunway.type  = "checkbox";
		checkboxBestArrivalRunway.name  = "BestArrivalRunwayCheckBox";
		checkboxBestArrivalRunway.value = "value";
		checkboxBestArrivalRunway.title = "Tick to select best arrival runway"
		checkboxBestArrivalRunway.id    = this.getBestArrivalRunwayCheckBoxId();
		
		div_4.appendChild(checkboxBestArrivalRunway);
		
		let label_4 = document.createElement("label");
		label_4.innerHTML = " -> Arrival RunWay -> " ;
		div_4.appendChild(label_4);
		
		let select_4   = document.createElement("select");
		select_4.id    = "airlineArrivalRunWayFlightProfileId";
		select_4.name  = "airlineArrivalRunWayFlightProfileName";
		select_4.title = "click to select the Arrival runway";

		div_4.appendChild(select_4);
		
		td_2.appendChild(div_4);
		
		row.appendChild(td_1);
		row.appendChild(td_2);
		return row;
	}
	
	createRowWithButtons() {
		
		let row = document.createElement('tr');
		let td_1 = document.createElement('td');
		td_1.colSpan = "2";
		
		let firstMainDiv = document.createElement('div');
		firstMainDiv.classList.add("rowClass");
		
		let div_5 = document.createElement('div');
		div_5.id = "launchComputeProfileId";
		div_5.classList.add("launchComputeProfileClass");
		div_5.classList.add("colClass");

		// -------------------------------------------
		// first button  - all button added to the same div
		
		let button_5 = document.createElement("button");
		button_5.id = "btnComputeFlightProfileId";
		button_5.innerHTML = "Compute Flight Profile";
		button_5.classList.add("buttonWidth");
		button_5.title = "click to compute the Flight Profile";
		//button_5.disabled = true;
		div_5.appendChild(button_5);
		
		firstMainDiv.appendChild(div_5);
		
		// --------------------
		let div_6 = document.createElement('div');
		div_6.classList.add("horizontal-align-right");
		div_6.classList.add("colClass");

		let button_6 = document.createElement("button");
		button_6.id = "btnComputeCostsId";
		button_6.innerHTML = "Compute Costs";
		button_6.classList.add("buttonWidth");
		button_6.title = "click to compute the Flight leg costs";

		div_6.appendChild(button_6);
		
		firstMainDiv.appendChild(div_6);

		td_1.appendChild(firstMainDiv);
		row.appendChild(td_1);
				
		// ---- second td
		
		let td_2 = document.createElement('td');
		td_2.colSpan = "2";
		
		let secondMainDiv = document.createElement('div');
		secondMainDiv.classList.add("rowClass");

		let div_7 = document.createElement('div');
		div_7.classList.add("horizontal-align-left");
		div_7.classList.add("colClass");

		// --------------------
		// button download state vector
		
		let button_7 = document.createElement("button");
		button_7.id = "btnDownLoadVerticalProfileId";
		button_7.innerHTML = "Download Vertical Profile";
		button_7.classList.add("buttonWidth");
		button_7.title = "click to download an EXCEL file with the Vertical Profile";

		div_7.appendChild(button_7);
		
		secondMainDiv.appendChild( div_7 );

		// --------------------
		// button download XML file
		
		let div_8 = document.createElement('div');
		div_8.classList.add("horizontal-align-right");
		div_8.classList.add("colClass");
		
		let button_8 = document.createElement("button");
		button_8.id = "btnDownLoadKMLfileId";
		button_8.innerHTML = "Download KML";
		button_8.classList.add("buttonWidth");
		button_8.title = "click to download a Keyhole Markup Language file with the compute trajectory";

		div_8.appendChild(button_8);
		
		secondMainDiv.appendChild(div_8);
		td_2.appendChild( secondMainDiv )
		// --------------------
		
		row.appendChild(td_2);
		return row;
	}

	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = this.getMainDivId();
		mainDiv.style = "display: none;";
		mainDiv.classList.add('flightProfileTableDiv');
		
		let draggableMainDiv       = document.createElement('div');
		draggableMainDiv.id        = mainDiv.id  + "Header";
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
				
		// each function returns a row object
		table.appendChild(this.createRowWithAircraftSelector());
		
		table.appendChild(this.createRowWithMass());
		table.appendChild(this.createRowWithRouteSelector());
		table.appendChild(this.createRowWithRunwaySelector());
		table.appendChild(this.createRowWithButtons());
		
		mainDiv.appendChild(table);
		this.renderer.div.appendChild(mainDiv);
		
		// check the BADA checkbox per default
		$('#'+this.getBADACheckBoxId()).prop("checked", true);
		
		// Make the Main Div element draggable:
		dragElement(document.getElementById(this.getMainDivId()));
	}

	oninit() {
		//console.log("flight profile Control - oninit");
	}
};