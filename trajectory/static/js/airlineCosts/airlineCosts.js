
document.addEventListener('DOMContentLoaded', (event) => { 
       
	console.log("Airline Costs is loaded");
	setTimeout( function () {
		launchCostsComputation();
	} , 500 )
}); 


function populateAircraftCostsSelector( airlineAircraftsArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeCostsId").show();
	// aircraftSelectionId
	$("#aircraftSelectionCostsId").show();

	for (var index = 0; index < airlineAircraftsArray.length; index++) {
      $('#airlineAircraftCostsId').append('<option value="' + airlineAircraftsArray[index]["airlineAircraftICAOcode"] + '">' + airlineAircraftsArray[index]["airlineAircraftFullName"] + '</option>');
	}
}

function populateAirlineRoutesCostsSelector( airlineRoutesArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeCostsId").show();
	// routesSelectionId
	$("#routesSelectionCostsId").show();

	for (var index = 0; index < airlineRoutesArray.length; index++) {
		var airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
		var airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
		$('#airlineRouteCostsId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
	}
}

function populateAirlineRunWaysCostsSelector( airlineRunWaysArray ) {
	
	$("#tableCostsId").show();
	$("#trComputeCostsId").show();
	
	for ( var index = 0 ; index < airlineRunWaysArray.length ; index++) {
		
		let route = $("#airlineRouteCostsId option:selected").val();
		
		//console.log(route)
		//console.log( airlineRunWaysArray[index]["airlineAirport"] )
		
		if ( route.split("-")[0] == airlineRunWaysArray[index]["airlineAirport"]) {
			
			console.log( "runway -> " + airlineRunWaysArray[index]["airlineRunWayName"] + " ---> for airport -> " + airlineRunWaysArray[index]["airlineAirport"] )
		
			var airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"]
			var airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading"
			$('#airlineDepartureRunWayCostsId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
		}
	}
	
	for ( var index = 0 ; index < airlineRunWaysArray.length ; index++) {
		
		let route = $("#airlineRouteCostsId option:selected").val();
		
		//console.log(route)
		//console.log( airlineRunWaysArray[index]["airlineAirport"] )
		
		if ( route.split("-")[1] == airlineRunWaysArray[index]["airlineAirport"]) {
			
			console.log( "runway -> " + airlineRunWaysArray[index]["airlineRunWayName"] + " ---> for airport -> " + airlineRunWaysArray[index]["airlineAirport"] )

			var airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"]
			var airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading"
			$('#airlineArrivalRunWayCostsId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
		}
	}
	
	// listen to select change
	$( "#airlineRouteCostsId" ).change(function() {
		alert( "Handler for airlineRouteCostsId selection change called." );
	});
}


function launchCostsComputation() {
	
	$('#tableCostsId').hide();

	$("#trComputeCostsId").hide();
	$("#aircraftSelectionCostsId").hide();
	$("#routesSelectionCostsId").hide();
	
	let show = true;
	
		/**
	* monitor the button used to show the table with the inputs
	* it allows only to choose the aircraft, the route before clicking to launch the profile computation
	**/
	document.getElementById("btnLaunchCosts").onclick = function () {
		
		if (show) {
			show = false;
			$('#tableCostsId').show();
			$("#trComputeCostsId").show();
			$("#aircraftSelectionCostsId").show();
			$("#routesSelectionCostsId").show();
			
			// change name on the button
			document.getElementById("btnLaunchCosts").innerText = "Hide Compute Costs";
			document.getElementById("btnLaunchCosts").style.backgroundColor = "green";
			
						// use ajax to get the data 
			$.ajax( {
					method: 'get',
					url :  "trajectory/launchFlightProfile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						// airlineAircrafts
						populateAircraftCostsSelector( dataJson["airlineAircrafts"] );
						populateAirlineRoutesCostsSelector( dataJson["airlineRoutes"] );
						populateAirlineRunWaysCostsSelector( dataJson["airlineRunWays"] );
						
						$("#launchComputeId").show();
						
					},
					error: function(data, status) {
						console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnLaunchFlightProfile").disabled = false
					},
			});


			
			
		} else {
			show = true;
			$('#tableCostsId').hide();
			
			// change name on the button
			document.getElementById("btnLaunchCosts").innerText = "Show Compute Costs";
			document.getElementById("btnLaunchCosts").style.backgroundColor = "yellow";


		}
	}
	
}