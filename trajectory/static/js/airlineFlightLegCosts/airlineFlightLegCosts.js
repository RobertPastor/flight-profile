
const SingletonAirlineFlightLegCosts = (function () {
	
	let instance;

    function createInstance() {
        var object = new AirlineFlightLegCosts();
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


class AirlineFlightLegCosts {

	constructor() {
		//console.log("Airline Flight Leg Costs  constructor");
	}

	showFlightLegCostsResults( dataJson ) {

		let aircraftName = $("#airlineAircraftId option:selected").val();
		let route = $("#airlineRouteId option:selected").val();
		
		let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val()
		let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val()
		
		// get the name of the airline
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

		// 30th July 2023 - add requested cruise level and reduced climb power coefficient
		$("#airlineFlightLegCostsTableId")
			.find('tbody')
			.append($('<tr>')

				.append('<td>'+ airlineName +'</td>')
				.append('<td>'+ aircraftName +'</td>')
				.append('<td>'+ dataJson["seats"] +'</td>')
				.append('<td>'+ route.split("-")[0] +'</td>')
				.append('<td>'+ departureRunWay +'</td>')
				.append('<td>'+ route.split("-")[1] +'</td>')
				.append('<td>'+ arrivalRunWay +'</td>')

				.append('<td>'+ dataJson["isAborted"] +'</td>')
				.append('<td>'+ dataJson["takeOffMassKilograms"] +'</td>')
				
				.append('<td>'+ dataJson["cruiseLevelFeet"] +'</td>')
				.append('<td>'+ dataJson["reducedClimbPowerCoeff"] +'</td>')
				
				.append('<td>'+ dataJson["finalMassKilograms"] +'</td>')
				.append('<td>'+ dataJson["massLossFilograms"] +'</td>')
				
				.append('<td>'+ dataJson["fuelCostsDollars"] +'</td>')
				.append('<td>'+ dataJson["flightDurationHours"] +'</td>')
				.append('<td>'+ dataJson["operationalFlyingCostsDollars"] +'</td>')
				.append('<td>'+ dataJson["crewFlyingCostsDollars"] +'</td>')

				.append('<td>'+ dataJson["totalCostsDollars"] +'</td>')
			);
		//console.log("after tableCostsResultsId tbody tr append")
	}

	hideAirlineFlightLegCostsDiv() {
	
		// html elements are defined in AirlineFlightLegCostsControls.js 
		if ( $('#airlineFlightLegCostsMainDivId').is(":visible") ) {
			
			$('#airlineFlightLegCostsMainDivId').hide();

			// change name on the button
			document.getElementById("btnLaunchCosts").innerText = "Profile";
			document.getElementById("btnLaunchCosts").style.backgroundColor = "yellow";
		}
	}

	initFlightLegCosts(flightProfileControl) {
		
		this.flightProfileControl = flightProfileControl;
		
		$('#airlineFlightLegCostsMainDivId').hide();
		
		// btnComputeCostsId
		// listen to the button
		document.getElementById("btnComputeCostsId").onclick = function () {
			
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);

			let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
			let route =  $("#airlineRouteId option:selected").val();
			
			// use the selector of the Flight Profile computation
			let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val();
			let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val();
			
			let elemTOMassKg = document.getElementById('TakeOffMassKgId');
			let elemFL = document.getElementById('requestedFlightLevelId');
			
			// cannot used "this"" keyword in call back
			let reducedClimbPowerCoeffInputId = flightProfileControl.getReducedClimbPowerCoeffInputId();
			let elemReduced = document.getElementById(reducedClimbPowerCoeffInputId);
			let elemReducedValue = 0.0;
			try {
				elemReducedValue = parseFloat(elemReduced.value)
			} catch (error) {
  				// field value is empty
  				elemReducedValue = 0.0
			}
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

			// init progress bar.
			initProgressBar();
			initWorker();
			
			// 17th July 2023 - add reduced climb power coefficient
			/**
			 * @todo - same code as in compute flight profile to launch a computation
			 */
			let data = {
				aircraft : aircraftICAOcode,
				route    : route,
				AdepRwy  : departureRunWay,
				AdesRwy  : arrivalRunWay,
				mass     : elemTOMassKg.value,
				fl       : elemFL.value,
				reduc    : elemReducedValue
			}
			
			$.ajax( {
						method: 'get',
						url :  "trajectory/computeCosts/" + airlineName,
						async : true,
						data :  data,
						success: function(data) {
							
							let dataJson = eval(data);
							if ( dataJson.hasOwnProperty("errors") ) {
								stopBusyAnimation();
								showMessage( "Error" , dataJson["errors"] );
								
							} else {
								
								$("#airlineFlightLegCostsMainDivId").show();
										
								//alert("Data: " + data + "\nStatus: " + status);
								//showMessage( "End of Costs computations" , dataJson )
								SingletonAirlineFlightLegCosts.getInstance().showFlightLegCostsResults( dataJson )
							}
							
							document.getElementById("btnComputeCostsId").disabled = false
													
						},
						error: function(data, status) {
							stopBusyAnimation();
							console.log("Error - compute Costs : " + status + " Please contact your admin");
							showMessage( "Error" , data );
						},
						complete : function() {
							stopBusyAnimation();
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);

						},
				});
		}
	}
	
}