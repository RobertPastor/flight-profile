
import { SingletonMainClass } from "../main/mainSingletonClass.js";
import { stopBusyAnimation } from "../main/main.js";

document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("Airline Fleet.js is loaded");
	//loadAirlineFleet();
	
}); 

export const SingletonAirlineFleet = (function () {
	
	let instance;

    function createInstance() {
        var object = new AirlineFleet();
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

class AirlineFleet {
	
	constructor() {
		//console.log("AirlineFleet constructor") 
	}

	// 27th May 2023 - add aircraft turn around time in the html table 
	addOneAirlineAircraft( oneAirlineAircraft ) {
	
		$("#tableAirlineFleetId").find('tbody')
			.append($('<tr>')
				.append($('<td>')
					.append( oneAirlineAircraft["Airline"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["AircraftICAOcode"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["AircraftFullName"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["NumberOfAircrafts"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["MaxNumberOfPassengers"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["CostsFlyingHoursDollars"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["CrewCostsFlyingHoursDollars"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["MinimumTakeOffMassKg"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["ReferenceMassKg"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["MaximumTakeOffMassKg"] )
				)
				.append($('<td>')
					.append( oneAirlineAircraft["AircraftTurnAroundTimeMinutes"] )
				)
			);
	}

	addAirlineFleetArray(airlineFleetArray) {
	
		// empty the table
		$('#tableAirlineFleetId tbody').empty();
		for (var airlineFleetId = 0; airlineFleetId < airlineFleetArray.length; airlineFleetId++ ) {
			// insert one airline
			SingletonAirlineFleet.getInstance().addOneAirlineAircraft( airlineFleetArray[airlineFleetId] );
		}
	}

	hideAirlineFleetDiv() {
		
		if ( $('#divAirlineFleetId').is(":visible") ) {
			
			$('#divAirlineFleetId').hide();
			
			document.getElementById("btnAirlineFleet").innerText = "Fleet";
			//document.getElementById("btnAirlineFleet").style.backgroundColor = "yellow";
		}
	}

	initAirlineFleet() {
	
		$('#divAirlineFleetId').hide();
		
		if ( ! document.getElementById("btnAirlineFleet") ) {
			return;
		}
		document.getElementById("btnAirlineFleet").onclick = function () {
			
			//console.log("btnAirlineFleet clicked");
			
			if ( ! $('#divAirlineFleetId').is(":visible") ) {
				
				//hideAllDiv();
				$('#divAirlineFleetId').show();

				// disable the button 
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
				
				// get the name of the airline
				let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "airline/airlineFleet/" + airlineName,
						async : true,
						success: function(data) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							var dataJson = eval(data);		
							var airlineFleetArray = dataJson["airlineFleet"]
							SingletonAirlineFleet.getInstance().addAirlineFleetArray(airlineFleetArray)
							
						},
						error: function(data, status) {
							console.log("Error - show Airline Fleet - status: " + status + " Please contact your admin");
							showMessage ( "Error - Airline Fleet" , data )
						},
						complete : function() {
							stopBusyAnimation();
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);						},
				});

			} else {

				SingletonAirlineFleet.getInstance().hideAirlineFleetDiv();
			}
		}
	}
}