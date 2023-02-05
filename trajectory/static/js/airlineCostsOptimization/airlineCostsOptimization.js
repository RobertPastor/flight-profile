

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
		console.log("Airline Costs Optimization constructor");
	}
	
	hideAirlineCostsOptimizationDiv() {
		
		console.log("Hide Airline Costs Optimization Main Div");
	
		// html elements are defined in AirlineFlightLegCostsControls.js 
		if ( $('#airlineCostsOptimizationMainDivId').is(":visible") ) {
			
			$('#airlineCostsOptimizationMainDivId').hide();

			// change name on the button
			document.getElementById("btnLaunchCostsOptimization").innerText = "Show Airline Costs Optimization";
			document.getElementById("btnLaunchCostsOptimization").style.backgroundColor = "yellow";
		}
	}
	
	showOneResult( dataJson ) {
		
		$("#airlineCostsOptimizationTableId")
			.find('tbody')
			.append($('<tr>')

				.append('<td>'+ dataJson["airline"] +'</td>')
				.append('<td>'+ dataJson["status"] +'</td>')
				.append('<td>'+ dataJson["aircraft"] +'</td>')
				.append('<td>'+ dataJson["assigned"] +'</td>')
				
				.append('<td>'+ dataJson["Adep"] +'</td>')
				.append('<td>'+ dataJson["Ades"] +'</td>')

			);
		
	}
	
	showCostsResults( optimizationResultsArray ) {
		
		console.log( " show optimization results");
		$('#airlineCostsOptimizationTableId tbody').empty();
		
		for (let resultId = 0; resultId < optimizationResultsArray.length; resultId++ ) {
			
			let oneResult = optimizationResultsArray[resultId];
			SingletonAirlineCostsOptimization.getInstance().showOneResult(oneResult);
		}
	}
	
	initAirlineCostsOptimization() {
	
		console.log( "init Costs Optimization");
	
		$('#airlineCostsMainDivId').hide();
		
		document.getElementById("btnLaunchCostsOptimization").onclick  = function () {
			
			console.log("click on Launch Costs Optimization");
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			// init progress bar.
			initProgressBar();
			initWorker();
			
			$.ajax( {
					method: 'get',
						url :  "airline/getCostsOptimization/" + airlineName,
						async : true,
						success: function(data, status) {
														
							let dataJson = eval(data);
							if ( dataJson.hasOwnProperty("errors") ) {
								stopBusyAnimation();
								showMessage( "Error" , dataJson["errors"] );
								
							} else {
								
								$("#airlineCostsOptimizationMainDivId").show();
										
								//alert("Data: " + data + "\nStatus: " + status);
								//showMessage( "End of Costs computations" , dataJson )
								let resultsArray = dataJson["results"]
								SingletonAirlineCostsOptimization.getInstance().showCostsResults( resultsArray )
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
							document.getElementById("btnLaunchFlightProfile").disabled = false
						}
			});
		}
		
	}
	
}