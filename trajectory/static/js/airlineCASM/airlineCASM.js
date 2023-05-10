
const SingletonAirlineCASM = (function () {
	
	let instance;

    function createInstance() {
        var object = new AirlineCASM();
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

class AirlineCASM {

	constructor() {
		//console.log("Airline CASM constructor");
	}
	
	hideAirlineCasmDiv() {
	
		// html elements are defined in AirlineCostsControls.js 
		if ( $('#airlineCasmMainDivId').is(":visible") ) {
			
			$('#airlineCasmMainDivId').hide();

			// change name on the button
			document.getElementById("btnLaunchCASM").innerText = "CASM";
			document.getElementById("btnLaunchCASM").style.backgroundColor = "yellow";
		}
	}
	
	showOneAirlineCasmResult( airlineOneCASM ) {
		
		$("#airlineCasmTableId").find('tbody')
				.append($('<tr>')
					.append($('<td>')
						.append( airlineOneCASM["airline"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["airlineAircraft"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["departureAirport"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["arrivalAirport"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["isAborted"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["nbSeats"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["miles"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["totalCostsUSdollars"] )
					)
					.append($('<td>')
						.append( airlineOneCASM["CasmUSdollars"] )
					)
				);
	}

	
	showAirlineCasmResults( airlineCasmArray ) {
		
		console.log( " show airline CASM");
		$('#airlineCasmTableId tbody').empty();
		
		for (let airlineCasmId = 0; airlineCasmId < airlineCasmArray.length; airlineCasmId++ ) {
			
			let oneAirlineCASM = airlineCasmArray[airlineCasmId];
			SingletonAirlineCASM.getInstance().showOneAirlineCasmResult(oneAirlineCASM);
		}
		// set height
		document.getElementById("airlineCasmTableId").style.height = (airlineCasmArray.length * 1)  + "px";

	}
	
	initAirlineCASM() {
	
		//console.log( "init Airline CASM ");
		
		$('#airlineCasmMainDivId').hide();
		
		document.getElementById("btnLaunchCASM").onclick  = function () {
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "airline/getAirlineCasmXlsx/" + airlineName;
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
		
		// btnComputeCostsId
		// listen to the button
		document.getElementById("btnLaunchCASM").ondblclick = function () {
			
			if ( ! $('#airlineCasmMainDivId').is(":visible") ) {
			
				document.getElementById("btnLaunchCASM").disabled = true;
				
				document.getElementById("btnLaunchCASM").innerText = "CASM";
				document.getElementById("btnLaunchCASM").style.backgroundColor = "green";
				
				// get the name of the airline
				let airlineName = $("#airlineSelectId option:selected").val();
				airlineName = encodeURIComponent(airlineName);

				// init progress bar.
				initProgressBar();
				initWorker();
				
				$.ajax({
					method: 'get',
					url :  "airline/getAirlineCASM/" + airlineName,
					async : true,
					success: function(data, status) {
						
						let dataJson = eval(data);
						if ( dataJson.hasOwnProperty("errors") ) {
							stopBusyAnimation();
							showMessage( "Error" , dataJson["errors"] );
						
						} else {
							
							$("#airlineCasmMainDivId").show();
									
							let airlineCasmArray = dataJson["airlineCasmList"]
											
							//alert("Data: " + data + "\nStatus: " + status);
							//showMessage( "End of Costs computations" , dataJson )
							SingletonAirlineCASM.getInstance().showAirlineCasmResults( airlineCasmArray )
							
						}
					},
					error: function(data, status) {
						stopBusyAnimation();
						console.log("Error - airline CASM : " + status + " Please contact your admin");
						showMessage( "Error" , data );
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnLaunchCASM").disabled = false
					}
				});
				
			} else {
				
				SingletonAirlineCASM.getInstance().hideAirlineCasmDiv();
				
			}
		}
	}
}