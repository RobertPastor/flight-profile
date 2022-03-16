
document.addEventListener('DOMContentLoaded', (event) => { 
       
	console.log("compute flight profile js is loaded");
	 
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	$("#launchComputeId").hide();

}); 

function populateAircraftSelector( airlineAircraftsArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeFlightProfileId").show();
	// aircraftSelectionId
	$("#aircraftSelectionId").show();

	for (var index = 0; index < airlineAircraftsArray.length; index++) {
      $('#airlineAircraftId').append('<option value="' + airlineAircraftsArray[index]["airlineAircraftICAOcode"] + '">' + airlineAircraftsArray[index]["airlineAircraftFullName"] + '</option>');
	}
}

function populateAirlineRoutesSelector( airlineRoutesArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeFlightProfileId").show();
	// routesSelectionId
	$("#routesSelectionId").show();

	for (var index = 0; index < airlineRoutesArray.length; index++) {
		var airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
		var airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
		$('#airlineRouteId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
	}
}

function computeFlightProfile(globus) {
	
	console.log( "compute flight profile ");
	
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	
	let show = true;
	document.getElementById("btnComputeFlightProfile").onclick = function () {

		if (show) {
			show = false;
			document.getElementById("btnComputeFlightProfile").disabled = true

			// use ajax to get the data 
			$.ajax( {
					method: 'get',
					url :  "trajectory/computeFlightProfile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						// airlineAircrafts
						populateAircraftSelector( dataJson["airlineAircrafts"] );
						populateAirlineRoutesSelector( dataJson["airlineRoutes"] );
						
						$("#launchComputeId").show();
						
					},
					error: function(data, status) {
						console.log("Error - delete old bookings: " + status + " SVP veuillez contactez votre administrateur");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnShowFlightProfile").disabled = false
					},
			});
			
		} 
	} 
	
}