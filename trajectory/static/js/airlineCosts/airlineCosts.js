

const SingletonAirlineCosts = (function () {
	
	let instance;

    function createInstance() {
        var object = new AirlineCosts();
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


class AirlineCosts {

	constructor() {
		//console.log("Airline Costs constructor");
	}

	hideAirlineCostsDiv() {
	
		// html elements are defined in AirlineCostsControls.js 
		if ( $('#airlineCostsMainDivId').is(":visible") ) {
			
			$('#airlineCostsMainDivId').hide();

			// change name on the button
			document.getElementById("btnLaunchAirlineCosts").innerText = "Costs";
			document.getElementById("btnLaunchAirlineCosts").style.backgroundColor = "yellow";
		}
	}
	
	showOneAirlineCostsResult( airlineOneCostOptimization ) {
		
		$("#airlineCostsTableId").find('tbody')
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
					.append($('<td>')
						.append( airlineOneCostOptimization["fuelCostsUSdollars"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["operationalCostsUSdollars"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["crewCostsUSdollars"] )
					)
					.append($('<td>')
						.append( airlineOneCostOptimization["totalCostsUSdollars"] )
					)
				);
	}

	showAirlineCostsResults( airlineCostsArray ) {
		
		console.log( " show airline costs");
		$('#airlineCostsTableId tbody').empty();
		
		for (let airlineCostId = 0; airlineCostId < airlineCostsArray.length; airlineCostId++ ) {
			
			let oneAirlineCostOptimization = airlineCostsArray[airlineCostId];
			SingletonAirlineCosts.getInstance().showOneAirlineCostsResult(oneAirlineCostOptimization);
		}
		// set height
		document.getElementById("airlineCostsTableId").style.height = (airlineCostsArray.length * 1)  + "px";

	}


	initAirlineCosts() {
	
		console.log( "init Costs Optimization");
	
		$('#airlineCostsMainDivId').hide();
		
		// btnComputeCostsId
		// listen to the button
		document.getElementById("btnLaunchAirlineCosts").onclick  = function () {
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "airline/getAirlineCostsXlsx/" + airlineName;
			let req = new XMLHttpRequest();
			req.open("GET", urlToSend, true);
			req.responseType = "blob";

			req.onload = function (event) {
				
				stopBusyAnimation();
				
				let blob = req.response;
				let fileName = req.getResponseHeader("Content-Disposition") //if you have the fileName header available
				fileName = fileName.split("=")[1]
				let link = document.createElement('a');
				link.href = window.URL.createObjectURL(blob);
				link.download = fileName;
				link.click();
				
			 };
			 req.onerror = function (event) {
				console.log("Error in Download EXCEL Costs");
			 }
			// send the request
			req.send();
			
		}
		
		document.getElementById("btnLaunchAirlineCosts").ondblclick = function () {
			
			if ( ! $('#airlineCostsMainDivId').is(":visible") ) {
			
				document.getElementById("btnLaunchAirlineCosts").disabled = true;
				
				document.getElementById("btnLaunchAirlineCosts").innerText = "Costs";
				document.getElementById("btnLaunchAirlineCosts").style.backgroundColor = "green";
				
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
								
									$("#airlineCostsMainDivId").show();
									
									let airlineCostsArray = dataJson["airlineCostsList"]
											
									//alert("Data: " + data + "\nStatus: " + status);
									//showMessage( "End of Costs computations" , dataJson )
									SingletonAirlineCosts.getInstance().showAirlineCostsResults( airlineCostsArray )
								}
							
								document.getElementById("btnLaunchAirlineCosts").disabled = false
													
							},
							error: function(data, status) {
								stopBusyAnimation();
								console.log("Error - compute Costs : " + status + " Please contact your admin");
								showMessage( "Error" , data );
							},
							complete : function() {
								stopBusyAnimation();
								document.getElementById("btnLaunchAirlineCosts").disabled = false
							}
				});
			} else {
				
				SingletonAirlineCosts.getInstance().hideAirlineCostsDiv();
				
			}
	    }
	}
}