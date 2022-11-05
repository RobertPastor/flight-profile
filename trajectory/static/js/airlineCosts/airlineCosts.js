
document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("Airline Costs is loaded");
	
}); 


function showCostsResults( dataJson ) {

    let aircraftName = $("#airlineAircraftId option:selected").val();
	let route = $("#airlineRouteId option:selected").val();
	
	let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val()
	let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val()
	
	// get the name of the airline
	let airlineName = $("#airlineSelectId option:selected").val();
	airlineName = encodeURIComponent(airlineName);

	//console.log("before tableCostsResultsId tbody tr append")
	
	$("#airlineCostsResultsTableId")
		.find('tbody')
		.append($('<tr>')

			.append('<td>'+ airlineName +'</td>')
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
			.append('<td>'+ dataJson["crewFlyingCostsDollars"] +'</td>')

			.append('<td>'+ dataJson["totalCostsDollars"] +'</td>')
		);
	//console.log("after tableCostsResultsId tbody tr append")

}

function hideAirlineCostsDiv() {
	
	if ( $('#airlineCostsMainDivId').is(":visible") ) {
		
		$('#airlineCostsMainDivId').hide();
		$("#airlineCostsResultsMainDivId").hide();

		// change name on the button
		document.getElementById("btnLaunchCosts").innerText = "Show Profile / Costs";
		document.getElementById("btnLaunchCosts").style.backgroundColor = "yellow";
	}
}

function initCostsComputation() {
	
	$('#airlineCostsMainDivId').hide();
	
	
	// btnComputeCostsId
	// listen to the button
	document.getElementById("btnComputeCostsId").onclick = function () {
		
		document.getElementById("btnComputeCostsId").disabled = true
		
		let aircraftICAOcode = $("#airlineAircraftId option:selected").val()
		let route =  $("#airlineRouteId option:selected").val()
		
		// use the selector of the Flight Profile computation
		let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val()
		let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val()
		
		// get the name of the airline
		let airlineName = $("#airlineSelectId option:selected").val();
		airlineName = encodeURIComponent(airlineName);

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
					url :  "trajectory/computeCosts/" + airlineName,
					async : true,
					data :  data,
					success: function(data, status) {
						
						let dataJson = eval(data);
						if ( dataJson.hasOwnProperty("errors") ) {
							stopBusyAnimation();
							showMessage( "Error" , dataJson["errors"] );
							
						} else {
							
							$("#airlineCostsResultsMainDivId").show();
									
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