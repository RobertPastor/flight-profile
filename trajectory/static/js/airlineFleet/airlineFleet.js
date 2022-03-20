document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("Airline Fleet.js is loaded");
	  loadAirlineFleet();
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
    );
}


function addAirlineFleetArray(airlineFleetArray) {
	
	$('#tableAirlineFleetId tbody').empty();
	for (var airlineFleetId = 0; airlineFleetId < airlineFleetArray.length; airlineFleetId++ ) {
		// insert one waypoint
		addOneAirlineAircraft( airlineFleetArray[airlineFleetId] );
	}
}


function loadAirlineFleet() {
	
	$("#trAirlineFleetId").hide();
	$('#tableAirlineFleetId').hide();
	
	let show = true;
	document.getElementById("btnAirlineFleet").onclick = function () {
		
		if (show) {
			$("#trAirlineFleetId").show();
			$('#tableAirlineFleetId').show();
						
			show = false;
			// change name on the button
			document.getElementById("btnAirlineFleet").innerText = "Hide Airline Fleet";
			$('#tableAirlineRoutesId').show();
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
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirlineFleet").disabled = false
						},
			});

		} else {
			show = true;
			document.getElementById("btnAirlineFleet").innerText = "Show Airline Fleet";
			
			$("#trAirlineFleetId").hide();
			$('#tableAirlineFleetId').hide();
		}
	}
}