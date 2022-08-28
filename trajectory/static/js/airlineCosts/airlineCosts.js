
document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("Airline Costs is loaded");
	launchCostsComputation();
	
}); 


function populateAircraftCostsSelector( airlineAircraftsArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeCostsId").show();
	
	// aircraftSelectionId
	$("#aircraftSelectionCostsId").show();
	
	$('#airlineAircraftCostsId').empty()

	for (var index = 0; index < airlineAircraftsArray.length; index++) {
      $('#airlineAircraftCostsId').append('<option value="' + airlineAircraftsArray[index]["airlineAircraftICAOcode"] + '">' + airlineAircraftsArray[index]["airlineAircraftFullName"] + '</option>');
	}
}

function populateAirlineRoutesCostsSelector( airlineRoutesArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeCostsId").show();
	// routesSelectionId
	$("#routesSelectionCostsId").show();
	
	// empty the selector before filling it again
	$('#airlineRouteCostsId').empty()

	for (var index = 0; index < airlineRoutesArray.length; index++) {
		var airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
		var airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
		$('#airlineRouteCostsId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
	}
}

function populateAirlineRunWaysCostsSelector( airlineRunWaysArray ) {
	
	$("#tableCostsId").show();
	$("#trComputeCostsId").show();
	
	// empty the selector
	$('#airlineDepartureRunWayCostsId').empty()
	
	for ( var index = 0 ; index < airlineRunWaysArray.length ; index++) {
		
		let route = $("#airlineRouteCostsId option:selected").val();
		
		//console.log(route)
		//console.log( airlineRunWaysArray[index]["airlineAirport"] )
		
		if ( route.split("-")[0] == airlineRunWaysArray[index]["airlineAirport"]) {
			
			//console.log( "runway -> " + airlineRunWaysArray[index]["airlineRunWayName"] + " ---> for airport -> " + airlineRunWaysArray[index]["airlineAirport"] )
		
			var airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"]
			var airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading"
			$('#airlineDepartureRunWayCostsId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
		}
	}
	
	// empty the selector
	$('#airlineArrivalRunWayCostsId').empty()
	
	for ( var index = 0 ; index < airlineRunWaysArray.length ; index++) {
		
		let route = $("#airlineRouteCostsId option:selected").val();
		
		//console.log(route)
		//console.log( airlineRunWaysArray[index]["airlineAirport"] )
		
		if ( route.split("-")[1] == airlineRunWaysArray[index]["airlineAirport"]) {
			
			//console.log( "runway -> " + airlineRunWaysArray[index]["airlineRunWayName"] + " ---> for airport -> " + airlineRunWaysArray[index]["airlineAirport"] )

			var airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"]
			var airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading"
			$('#airlineArrivalRunWayCostsId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
		}
	}
}

function showCostsResults( dataJson ) {

	let aircraftName = $("#airlineAircraftCostsId option:selected").html()
	let route =  $("#airlineRouteCostsId option:selected").val()
	let departureRunWay = $("#airlineDepartureRunWayCostsId option:selected").val()
	let arrivalRunWay = $("#airlineArrivalRunWayCostsId option:selected").val()
	
	//console.log("before tableCostsResultsId tbody tr append")
	$("#tableCostsResultsId")
	.find('tbody')
    .append($('<tr>')

		.append('<td>'+ aircraftName +'</td>')
		.append('<td>'+ dataJson["seats"] +'</td>')
		.append('<td>'+ route.split("-")[0] +'</td>')
		.append('<td>'+ departureRunWay +'</td>')
		.append('<td>'+ route.split("-")[1] +'</td>')
		.append('<td>'+ arrivalRunWay +'</td>')

		.append('<td>'+ dataJson["isAborted"] +'</td>')
		.append('<td>'+ dataJson["initialMassKilograms"] +'</td>')
		.append('<td>'+ dataJson["finalMassKilograms"] +'</td>')
		.append('<td>'+ dataJson["massLossFilograms"] +'</td>')
		
		.append('<td>'+ dataJson["fuelCostsDollars"] +'</td>')
		.append('<td>'+ dataJson["flightDurationHours"] +'</td>')
		.append('<td>'+ dataJson["operationalFlyingCostsDollars"] +'</td>')
		.append('<td>'+ dataJson["totalCostsDollars"] +'</td>')
	);
	//console.log("after tableCostsResultsId tbody tr append")

}


function launchCostsComputation() {
	
	$('#tableCostsId').hide();
	$("#trComputeCostsResultsHeaderId").hide()

	$("#trComputeCostsId").hide();
	$("#aircraftSelectionCostsId").hide();
	$("#routesSelectionCostsId").hide();
	
	// listen to the route selector changes
	$( "#airlineRouteCostsId" ).change(function() {
		//console.log( "Handler for airlineRouteCostsId selection change called." );
		// for the begin of the computation we use the same URL route as the Flight Profile computation
		$.ajax( {
					method: 'get',
					url :  "trajectory/launchFlightProfile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						// airlineAircrafts
						populateAirlineRunWaysCostsSelector( dataJson["airlineRunWays"] );
						
						$("#btnLaunchCosts").show();
						
					},
					error: function(data, status) {
						console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnLaunchFlightProfile").disabled = false
					},
			});
	});
	
	let show = true;
	
	/**
	* monitor the button used to show the table with the inputs
	* it allows only to choose the aircraft, the route before clicking to launch the profile computation
	* the button is defined in /flight-profile/trajectory/templates/index-og.html
	**/
	if ( !document.getElementById("btnLaunchCosts") ) {
		return;
	}
	document.getElementById("btnLaunchCosts").onclick = function () {
		
		if (show) {
			show = false;
			$('#tableCostsId').show();
			$('#tableCostsResultsId').show();
			
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
						
						$("#btnLaunchCosts").show();
						
					},
					error: function(data, status) {
						console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
						showMessage("Error" , eval(data) ) 
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnLaunchFlightProfile").disabled = false
					},
			});

		} else {
			show = true;
			$('#tableCostsId').hide();
			$('#tableCostsResultsId').hide();

			// change name on the button
			document.getElementById("btnLaunchCosts").innerText = "Show Compute Costs";
			document.getElementById("btnLaunchCosts").style.backgroundColor = "yellow";
		}
	}
	
	// btnComputeCostsId
	document.getElementById("btnComputeCostsId").onclick = function () {
		
		document.getElementById("btnComputeCostsId").disabled = true
		
		let aircraftICAOcode = $("#airlineAircraftCostsId option:selected").val()
		let route =  $("#airlineRouteCostsId option:selected").val()
		let departureRunWay = $("#airlineDepartureRunWayCostsId option:selected").val()
		let arrivalRunWay = $("#airlineArrivalRunWayCostsId option:selected").val()

		// init progress bar.
		initProgressBar();
		initWorker();
		
		
		data = {
			aircraft : aircraftICAOcode,
			route    : route,
			AdepRwy  : departureRunWay,
			AdesRwy  : arrivalRunWay
		}
		
		$.ajax( {
					method: 'get',
					url :  "trajectory/computeCosts",
					async : true,
					data :  data,
					success: function(data, status) {
						
						let dataJson = eval(data);
						if ( dataJson.hasOwnProperty("errors") ) {
							stopBusyAnimation();
							showMessage( "Error" , dataJson["errors"] );
							
						} else {
							
							$("#trComputeCostsResultsHeaderId").show()
									
							//alert("Data: " + data + "\nStatus: " + status);
							//showMessage( "End of Costs computations" , dataJson )
							showCostsResults( dataJson )
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
					},
			});
		
	}

	
}