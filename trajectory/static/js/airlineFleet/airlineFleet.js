document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("Airline Fleet.js is loaded");
	//loadAirlineFleet();
	
}); 

const SingletonAirlineFleet = (function () {
	
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
			document.getElementById("btnAirlineFleet").style.backgroundColor = "yellow";
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
				
				hideAllDiv();
				$('#divAirlineFleetId').show();
							
				// change name on the button
				document.getElementById("btnAirlineFleet").innerText = "Fleet";
				document.getElementById("btnAirlineFleet").style.backgroundColor = "green";

				// disable the button 
				document.getElementById("btnAirlineFleet").disabled = true
				
				// get the name of the airline
				let airlineName = $("#airlineSelectId option:selected").val();
				airlineName = encodeURIComponent(airlineName);

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "airline/airlineFleet/" + airlineName,
						async : true,
						success: function(data, status) {
										
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
							document.getElementById("btnAirlineFleet").disabled = false
						},
				});

			} else {

				SingletonAirlineFleet.getInstance().hideAirlineFleetDiv();
			}
		}
	}
}