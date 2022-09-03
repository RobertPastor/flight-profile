document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("Airline Fleet.js is loaded");
	//loadAirlineFleet();
	
}); 

function addOneAirlineAircraft( oneAirlineAircraft ) {
	
	$("#tableAirlineFleetId").find('tbody')
		.append($('<tr>')
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
				.append( "Crew costs not yet implemented" )
			)
		);
}


function addAirlineFleetArray(airlineFleetArray) {
	
	// empty the table
	$('#tableAirlineFleetId tbody').empty();
	for (var airlineFleetId = 0; airlineFleetId < airlineFleetArray.length; airlineFleetId++ ) {
		// insert one airline
		addOneAirlineAircraft( airlineFleetArray[airlineFleetId] );
	}
}


function initAirlineFleet() {
	
	$('#divAirlineFleetId').hide();
	$('#tableAirlineFleetId').hide();
	
	let show = true;
	if ( ! document.getElementById("btnAirlineFleet") ) {
		return;
	}
	document.getElementById("btnAirlineFleet").onclick = function () {
		
		//console.log("btnAirlineFleet clicked");
		
		if (show) {
			
			$('#divAirlineFleetId').show();
			$('#tableAirlineFleetId').show();
						
			show = false;
			// change name on the button
			document.getElementById("btnAirlineFleet").innerText = "Hide Airline Fleet";
			document.getElementById("btnAirlineFleet").style.backgroundColor = "green";

			// disable the button 
			document.getElementById("btnAirlineFleet").disabled = true

			// use ajax to get the data 
			$.ajax( {
						method: 'get',
						url :  "airline/airlineFleet",
						async : true,
						success: function(data, status) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							var dataJson = eval(data);		
							var airlineFleetArray = dataJson["airlineFleet"]
							addAirlineFleetArray(airlineFleetArray)
							
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
			show = true;
			document.getElementById("btnAirlineFleet").innerText = "Show Airline Fleet";
			document.getElementById("btnAirlineFleet").style.backgroundColor = "yellow";

			$('#divAirlineFleetId').hide();
			$('#tableAirlineFleetId').hide();
		}
	}
}