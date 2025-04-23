import { stopBusyAnimation , showMessage } from "../main/main.js";
import { SingletonMainClass } from "../main/mainSingletonClass.js";

export const SingletonFuelPlanner = (function () {
	
	let instance;

    function createInstance() {
        let object = new FuelPlanner();
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

class FuelPlanner {
	
	constructor() {
		//console.log("Fuel Planner constructor");
	}
	
	getGlobus() {
		return this.globus;
	}
	
	setAircraftWeightsInput() {
		
		let airlineAircraftsArray =	this.airlineAircraftsArray;
		
		// selected aircraft
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();

		for (let index = 0; index < airlineAircraftsArray.length; index++) {
			
			let acICAOcode = airlineAircraftsArray[index]["airlineAircraftICAOcode"]
			if ( acICAOcode == aircraftSelectorICAOcode ) {
			
				// find the inputs
				let acMinWeightKg = document.getElementById('fuelPlannerMinimumMassId');
				let acMaxWeightKg = document.getElementById('fuelPlannerMaximumMassId');
				let acPayLoadKg = document.getElementById('fuelPlannerMaxPayLoadMassId');
				
				acMinWeightKg.value = airlineAircraftsArray[index]["acMinTakeOffWeightKg"];
				acMaxWeightKg.value = airlineAircraftsArray[index]["acMaxTakeOffWeightKg"];
				acPayLoadKg.value = airlineAircraftsArray[index]["acMaxPayLoadKg"];
			
			}
		}
	}
	
	populateAircraftWeightInputs ( airlineAircraftsArray ) {
		
		this.airlineAircraftsArray = airlineAircraftsArray;
		SingletonFuelPlanner.getInstance().setAircraftWeightsInput();
	}
	
	populateAircraftFlightProfileSelector( airlineAircraftsArray ) {
	
		// aircraftSelectionId
		$("#fuelPlannerAircraftSelectionId").show();
		
		// empty the selector
		$('#fuelPlannerAirlineAircraftSelectId').empty()

		for (let index = 0; index < airlineAircraftsArray.length; index++) {
			
		  $('#fuelPlannerAirlineAircraftSelectId').append('<option value="' + airlineAircraftsArray[index]["airlineAircraftICAOcode"] + '">' + airlineAircraftsArray[index]["airlineAircraftFullName"] + '</option>');
		
		}
		SingletonFuelPlanner.getInstance().setAircraftICAOcodeInput();
	}
	
	setAircraftICAOcodeInput(  ) {
		
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();
		
		// set aircraft ICAO code in the read only input
		let acICAOcode = document.getElementById('fuelPlannerAirlineAircraftICAOcodeId');
		acICAOcode.value = aircraftSelectorICAOcode;
	}
	
	populateAirlineRoutesFlightProfileSelector( airlineRoutesArray ) {
		
		this.airlineRoutesArray = airlineRoutesArray;
	
		// empty the selector
		$('#fuelPlannerAirlineRouteSelectId').empty()

		for (let index = 0; index < airlineRoutesArray.length; index++) {
			let airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
			let airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
			$('#fuelPlannerAirlineRouteSelectId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
		}
		
		SingletonFuelPlanner.getInstance().setRouteAirportsICAOcode();
		SingletonFuelPlanner.getInstance().setRouteLengthMiles();
	}
	
	setRouteLengthMiles() {
		
		let airlineRoutesArray = this.airlineRoutesArray;
		
		// route selecor 
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		for (let index = 0; index < airlineRoutesArray.length; index++) {
			
			let airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
			if ( routeSelector == airlineRouteKey) {
				
				let routeLength = document.getElementById('fuelPlannerRouteLengthId');
				routeLength.value = airlineRoutesArray[index]["RouteLengthMiles"];
			}
		}
	}
	
	setRouteAirportsICAOcode() {
		
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		
		// set aircraft ICAO code in the read only input
		let adepICAOcode = document.getElementById('fuelPlannerAirlineAdepICAOcodeId');
		adepICAOcode.value = routeSelector.split("-")[0];
		
		let adesICAOcode = document.getElementById('fuelPlannerAirlineAdesICAOcodeId');
		adesICAOcode.value = routeSelector.split("-")[1];
		
	}
	
	hideFuelPlannerDiv() {
		$('#mainFuelPlannerDivId').hide();
	}
	
	setAircraftTakeOffMassInput( ) {
		
		let airlineAircraftPerformanceArray = this.airlineAircraftPerformanceArray ;
		
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();

		for (let index = 0; index < airlineAircraftPerformanceArray.length; index++) {
			
			if ( ( aircraftSelectorICAOcode == airlineAircraftPerformanceArray[index]["Aircraft"] ) && 
			     (  routeSelector           == airlineAircraftPerformanceArray[index]["Route"] ) ) {
					 
				let takeOffMassKg = document.getElementById('fuelPlannerTakeOffMassId');
				takeOffMassKg.value = airlineAircraftPerformanceArray[index]["TakeOffMassKg"];
				
			}
		}
	}
	
	setFlightLegDurationInput( ) {
		
		let airlineAircraftPerformanceArray = this.airlineAircraftPerformanceArray ;
		
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();

		for (let index = 0; index < airlineAircraftPerformanceArray.length; index++) {
			
			if ( ( aircraftSelectorICAOcode == airlineAircraftPerformanceArray[index]["Aircraft"] ) && 
			     (  routeSelector           == airlineAircraftPerformanceArray[index]["Route"] ) ) {
					 
				let flightLegDurationSeconds = document.getElementById('fuelPlannerLegDurationId');
				flightLegDurationSeconds.value = airlineAircraftPerformanceArray[index]["LegDurationSec"];
				
				let hoursMinutes = airlineAircraftPerformanceArray[index]["LegDurationSec"];
				hoursMinutes = Math.floor( hoursMinutes / 3600.0 ) + " Hours " + Math.floor( ( (hoursMinutes / 3600.0) - Math.floor( hoursMinutes / 3600.0 ) ) * 60.0 ) + " Minutes" ;
				flightLegDurationSeconds.title = hoursMinutes ;
			}
		}
	}
	
	setFlightLegLengthInput( ) {
		
		let airlineAircraftPerformanceArray = this.airlineAircraftPerformanceArray ;
		
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();

		for (let index = 0; index < airlineAircraftPerformanceArray.length; index++) {
			
			if ( ( aircraftSelectorICAOcode == airlineAircraftPerformanceArray[index]["Aircraft"] ) && 
			     (  routeSelector           == airlineAircraftPerformanceArray[index]["Route"] ) ) {
					 
				let flightLegLength = document.getElementById('fuelPlannerLegLengthId');
				flightLegLength.value = airlineAircraftPerformanceArray[index]["LegLengthMiles"];
				
			}
		}
	}
	
	setLegFuelBurnInput() {
		
		let airlineAircraftPerformanceArray = this.airlineAircraftPerformanceArray ;
		
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();

		for (let index = 0; index < airlineAircraftPerformanceArray.length; index++) {
			
			if ( ( aircraftSelectorICAOcode == airlineAircraftPerformanceArray[index]["Aircraft"] ) && 
			     (  routeSelector           == airlineAircraftPerformanceArray[index]["Route"] ) ) {
					 
				let flightLegFuelBurn = document.getElementById('fuelPlannerFuelBurnId');
				flightLegFuelBurn.value = airlineAircraftPerformanceArray[index]["TripFuelBurnKg"];
				
			}
		}
	}
	
	setOneHourReserveFuelInput() {
		
		let airlineAircraftPerformanceArray = this.airlineAircraftPerformanceArray ;
		
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();

		for (let index = 0; index < airlineAircraftPerformanceArray.length; index++) {
			
			if ( ( aircraftSelectorICAOcode == airlineAircraftPerformanceArray[index]["Aircraft"] ) && 
			     (  routeSelector           == airlineAircraftPerformanceArray[index]["Route"] ) ) {
					 
				let OneHourReserveFuelMass = document.getElementById('fuelPlannerFuelOneHourReserveFuelId');
				OneHourReserveFuelMass.value = airlineAircraftPerformanceArray[index]["OneHourReserveFuelKg"];
				
			}
		}
	}
	
	setOptimalTakeOffMassInput() {
		
		let airlineAircraftPerformanceArray = this.airlineAircraftPerformanceArray ;
		
		let routeSelector = $("#fuelPlannerAirlineRouteSelectId option:selected").val();
		let aircraftSelectorICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();

		for (let index = 0; index < airlineAircraftPerformanceArray.length; index++) {
			
			if ( ( aircraftSelectorICAOcode == airlineAircraftPerformanceArray[index]["Aircraft"] ) && 
			     (  routeSelector           == airlineAircraftPerformanceArray[index]["Route"] ) ) {
					 
				let OptimalTakeOffMass = document.getElementById('fuelPlannerOptimalTakeOffMassId');
				OptimalTakeOffMass.value = airlineAircraftPerformanceArray[index]["OptimalTakeOffMassKg"];
				
			}
		}
	}
	
	populateAircraftLegPerformance( airlineAircraftPerformanceArray ) {
		
		this.airlineAircraftPerformanceArray = airlineAircraftPerformanceArray;
		SingletonFuelPlanner.getInstance().setAircraftTakeOffMassInput();
		SingletonFuelPlanner.getInstance().setFlightLegDurationInput();
		SingletonFuelPlanner.getInstance().setFlightLegLengthInput();
		SingletonFuelPlanner.getInstance().setLegFuelBurnInput();
		SingletonFuelPlanner.getInstance().setOneHourReserveFuelInput();
		SingletonFuelPlanner.getInstance().setOptimalTakeOffMassInput();
	}
	
	initFuelPlanner( globus ) {
		
		this.globus = globus;
		// listen to the button defined in MainSubMenuFuel.js
		document.getElementById("btnFuelPlanner").onclick = function () {

			if ( ! $('#mainFuelPlannerDivId').is(":visible") ) {
			
				$('#mainFuelPlannerDivId').show();
				
				// get the name of the airline
				let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
				
				// disable the button
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "trajectory/fuelPlanner/" + airlineName,
						async : true,
						success: function(data) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);
							// airlineAircrafts
							SingletonFuelPlanner.getInstance().populateAircraftFlightProfileSelector( dataJson["airlineAircrafts"] );
							SingletonFuelPlanner.getInstance().populateAirlineRoutesFlightProfileSelector( dataJson["airlineRoutes"] );
							SingletonFuelPlanner.getInstance().populateAircraftWeightInputs( dataJson["airlineAircrafts"] );
							SingletonFuelPlanner.getInstance().populateAircraftLegPerformance( dataJson["aircraftPerformance"] );
						},
						error: function(data, status) {
							console.log("Error - Fuel Planner: " + status + " Please contact your admin");
							showMessage("Error - Fuel Planner", eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
						},
				});
				
			} else {
				$('#mainFuelPlannerDivId').hide();
			}
		}
		
		/**
		* Monitor the change of Aircraft
		**/
		document.getElementById("fuelPlannerAirlineAircraftSelectId").onchange = function () {
			
			//console.log ("selected aircraft changed");
			//let aircraftICAOcode = $("#fuelPlannerAirlineAircraftSelectId option:selected").val();
			//console.log(aircraftICAOcode)
			
			SingletonFuelPlanner.getInstance().setAircraftICAOcodeInput();
			SingletonFuelPlanner.getInstance().setAircraftWeightsInput();
			SingletonFuelPlanner.getInstance().setAircraftTakeOffMassInput();
			SingletonFuelPlanner.getInstance().setFlightLegDurationInput();
			SingletonFuelPlanner.getInstance().setFlightLegLengthInput();
			SingletonFuelPlanner.getInstance().setLegFuelBurnInput();
			SingletonFuelPlanner.getInstance().setOneHourReserveFuelInput();
			SingletonFuelPlanner.getInstance().setOptimalTakeOffMassInput();
		}
		
		// Listen to the change to the routeEvents
		document.getElementById("fuelPlannerAirlineRouteSelectId").onchange = function () {

			SingletonFuelPlanner.getInstance().setRouteAirportsICAOcode();
			SingletonFuelPlanner.getInstance().setRouteLengthMiles();
			SingletonFuelPlanner.getInstance().setAircraftTakeOffMassInput();
			SingletonFuelPlanner.getInstance().setFlightLegDurationInput();
			SingletonFuelPlanner.getInstance().setFlightLegLengthInput();
			SingletonFuelPlanner.getInstance().setLegFuelBurnInput();
			SingletonFuelPlanner.getInstance().setOneHourReserveFuelInput();
			SingletonFuelPlanner.getInstance().setOptimalTakeOffMassInput();
		}
	}
}
