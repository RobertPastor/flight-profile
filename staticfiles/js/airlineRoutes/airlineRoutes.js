document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("Airline Routes.js is loaded");
	  $('#tableAirlineRoutesId').hide();

	  loadAirlineRoutes();
}); 


function addOneAirlineRoute( oneAirlineRoute ) {
	
	$("#tableAirlineRoutesId").find('tbody')
    .append($('<tr>')
        .append($('<td>')
            .append( oneAirlineRoute["DepartureAirport"] )
        )
		.append($('<td>')
            .append( oneAirlineRoute["DepartureAirportICAOCode"] )
        )
		.append($('<td>')
            .append( oneAirlineRoute["ArrivalAirport"] )
        )
		.append($('<td>')
            .append( oneAirlineRoute["ArrivalAirportICAOCode"] )
        )
    );
}

function addAirlineRoutes(airlineRoutesArray) {
	
	$('#tableAirlineRoutesId tbody').empty();
	for (var airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
		// insert one waypoint
		addOneAirlineRoute( airlineRoutesArray[airlineRouteId] );
	}
}

function loadAirlineRoutes(globus) {
	
	let show = true;
	$("#trAirlineRoutesId").hide();

	document.getElementById("btnAirlineRoutes").onclick = function () {
		
		if (show) {
			$("#trAirlineRoutesId").show();

			show = false;
			// change name on the button
			document.getElementById("btnAirlineRoutes").innerText = "Hide Airline Routes";
			$('#tableAirlineRoutesId').show();
			// disable the button 
			document.getElementById("btnAirlineRoutes").disabled = true

			// use ajax to get the data 
			$.ajax( {
						method: 'get',
						url :  "airline/airlineRoutes",
						async : true,
						success: function(data, status) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							var dataJson = eval(data);		
							var airlineRoutesArray = dataJson["airlineRoutes"]
							addAirlineRoutes(airlineRoutesArray)
							
						},
						error: function(data, status) {
							console.log("Error - show Airline Routes : " + status + " Please contact your admin");
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirlineRoutes").disabled = false
						},
			});

		} else {

			show = true;
			document.getElementById("btnAirlineRoutes").innerText = "Show Airline Routes";
			
			$("#trAirlineRoutesId").hide();
			$('#tableAirlineRoutesId').hide();
		}
	}
}