

const SingletonAirlineCostsOptimization = (function () {
	
	let instance;

    function createInstance() {
        var object = new AirlineCostsOptimization();
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


class AirlineCostsOptimization {

	constructor() {
		//console.log("Airline Routes constructor");
	}

	hideAirlineOptimizationCostsDiv() {
	
		// html elements are defined in AirlineCostsControls.js 
		if ( $('#airlineOptimizationMainDivId').is(":visible") ) {
			
			$('#airlineOptimizationMainDivId').hide();

			// change name on the button
			document.getElementById("btnLaunchCostsOptimization").innerText = "Show Costs Optimization";
			document.getElementById("btnLaunchCostsOptimization").style.backgroundColor = "yellow";
		}
	}
	
	showOneCostOptimizationResult( airlineOneCostOptimization ) {
		
		$("#airlineOptimizationResultsTableId").find('tbody')
				.append($('<tr>')
					.append($('<td>')
						.append( airlineOneCostOptimization["airline"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["airlineAircraft"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["departureAirport"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["arrivalAirport"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["isAborted"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["takeOffMassKg"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["finalMassKg"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["flightDurationHours"] )
					)

				);
		
	}


	showCostsOptimizationResults( airlineCostsArray ) {
		
		console.log( " show airline costs");
		$('#airlineOptimizationResultsTableId tbody').empty();
		
		for (let airlineCostId = 0; airlineCostId < airlineCostsArray.length; airlineCostId++ ) {
			
			let oneAirlineCostOptimization = airlineCostsArray[airlineCostId];
			SingletonAirlineCostsOptimization.getInstance().showOneCostOptimizationResult(oneAirlineCostOptimization);
		}
		
	}


	initCostsOptimization() {
	
		console.log( "init Costs Optimization");
	
		$('#airlineCostsMainDivId').hide();
		
		// btnComputeCostsId
		// listen to the button
		document.getElementById("btnLaunchCostsOptimization").onclick = function () {
			
			document.getElementById("btnLaunchCostsOptimization").disabled = true;
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			// init progress bar.
			initProgressBar();
			initWorker();
			
			$.ajax( {
					method: 'get',
						url :  "airline/getAirlineCosts/" + airlineName,
						async : true,
						success: function(data, status) {
							
							let dataJson = eval(data);
							if ( dataJson.hasOwnProperty("errors") ) {
								stopBusyAnimation();
							showMessage( "Error" , dataJson["errors"] );
							
						} else {
							
							$("#airlineOptimizationMainDivId").show();
							
							let airlineCostsArray = dataJson["airlineCostsList"]
									
							//alert("Data: " + data + "\nStatus: " + status);
							//showMessage( "End of Costs computations" , dataJson )
							SingletonAirlineCostsOptimization.getInstance().showCostsOptimizationResults( airlineCostsArray )
						}
						
						document.getElementById("btnLaunchCostsOptimization").disabled = false
												
					},
					error: function(data, status) {
						stopBusyAnimation();
						console.log("Error - compute Costs : " + status + " Please contact your admin");
						showMessage( "Error" , data );
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnLaunchFlightProfile").disabled = false
					},
			});
		}
	}
	
}