
import { initProgressBar , initWorker } from "../main/main.js";


export const SingletonAirlineCasmOptimization = (function () {
	
	let instance;

    function createInstance() {
        var object = new AirlineCasmOptimization();
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

class AirlineCasmOptimization {
	
	constructor() {
		//console.log("Airline CASM optimization constructor");
	}
	
	hideAirlineCasmOptimizationDiv() {
	
		// html elements are defined in AirlineCostsControls.js 
		if ( $('#airlineCasmOptimizationMainDivId').is(":visible") ) {
			
			$('#airlineCasmOptimizationMainDivId').hide();

			// change name on the button
			document.getElementById("btnLaunchCasmOptimization").innerText = "CASM Min";
			//document.getElementById("btnLaunchCasmOptimization").style.backgroundColor = "yellow";
		}
	}
	
	showOneResult( dataJson ) {
		
		$("#airlineCasmOptimizationTableId")
			.find('tbody')
			.append($('<tr>')

				.append('<td>'+ dataJson["airline"] +'</td>')
				.append('<td>'+ dataJson["status"] +'</td>')
				.append('<td>'+ dataJson["aircraft"] +'</td>')
				.append('<td>'+ dataJson["assigned"] +'</td>')
				
				.append('<td>'+ dataJson["Adep"] +'</td>')
				.append('<td>'+ dataJson["Ades"] +'</td>')
				
				.append('<td>'+ dataJson["ReducedClimbPowerCoeff"] +'</td>')
				
				.append('<td>'+ dataJson["Seats"] +'</td>')
				.append('<td>'+ dataJson["Miles"] +'</td>')
				.append('<td>'+ dataJson["Costs"] +'</td>')
				.append('<td>'+ dataJson["CASM"] +'</td>')

			);
	}
	
	showCasmResults( optimizationResultsArray ) {
		
		//console.log( " show optimization results");
		$('#airlineCasmOptimizationTableId tbody').empty();
		
		for (let resultId = 0; resultId < optimizationResultsArray.length; resultId++ ) {
			
			let oneResult = optimizationResultsArray[resultId];
			SingletonAirlineCasmOptimization.getInstance().showOneResult(oneResult);
		}
	}
	
	initAirlineCasmOptimization() {
		
		//console.log( "init CASM Optimization");
		// listen to the button
		document.getElementById("btnLaunchCasmOptimization").onclick = function () {
			
			if ( ! $('#airlineCasmOptimizationMainDivId').is(":visible") ) {
				
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
								
				// get the name of the airline
				let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

				// init progress bar.
				initProgressBar();
				initWorker();
				
				$.ajax( {
					method: 'get',
					url :  "airline/getAirlineCasmOptimization/" + airlineName,
					async : true,
					success: function(data) {
						
						let dataJson = eval(data);
						if ( dataJson.hasOwnProperty("errors") ) {
							
							stopBusyAnimation();
							showMessage( "Error" , dataJson["errors"] );
						
						} else {
							
							$("#airlineCasmOptimizationMainDivId").show();
							let resultsArray = dataJson["results"];
							SingletonAirlineCasmOptimization.getInstance().showCasmResults( resultsArray );
						}
					},
					error: function(data, status) {
						stopBusyAnimation();
						console.log("Error - compute CASM Optimization : " + status + " Please contact your admin");
						showMessage( "Error" , data );
					},
					complete : function() {
						stopBusyAnimation();
						SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
					}
				});
				
			} else {
				
				SingletonAirlineCasmOptimization.getInstance().hideAirlineCasmOptimizationDiv();
			}
		}
	}
}