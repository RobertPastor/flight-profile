


function initDownloadKMLfile() {
	
	let buttonId = "btnDownLoadKMLfileId";
	try {
		document.getElementById(buttonId).onclick = function () {
	
			document.getElementById(buttonId).disabled = true;
	
			let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
			let route =  $("#airlineRouteId option:selected").val();
			
			// use the selector of the Flight Profile computation
			let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val();
			let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val();
			
			let elemTOMassKg = document.getElementById('TakeOffMassKgId');
			let elemFL = document.getElementById('requestedFlightLevelId');
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);
	
			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "trajectory/kml/" + airlineName + "?ac=" + aircraftICAOcode;
			urlToSend += "&route=" + route;
			urlToSend += "&adepRwy=" + departureRunWay;
			urlToSend += "&adesRwy=" + arrivalRunWay;
			urlToSend += "&mass=" + elemTOMassKg.value;
			urlToSend += "&fl=" + elemFL.value;
			
			let req = new XMLHttpRequest();
			req.open("GET", urlToSend, true);
			req.responseType = "blob";
	
			req.onload = function (event) {
				
				stopBusyAnimation();
				
				let blob = req.response;
				let fileName = req.getResponseHeader("Content-Disposition") //if you have the fileName header available
				// filename starts with attachment followed by an EQUAL signe
				if ( fileName ) {
					
					fileName = fileName.split("=")[1];
					let link = document.createElement('a');
					link.href = window.URL.createObjectURL(blob);
					link.download = fileName;
					link.click();
				} else {
					console.error(JSON.stringify(req.status + " - " + req.statusText));
					console.error("fileName is null - " + JSON.stringify(event));
				}
				
				// enable button again
				document.getElementById(buttonId).disabled = false;
	
			 };
			 req.onerror = function (event) {
				 console.error("Error in Download KML file");
				 console.error(JSON.stringify(event));
			 }
			// send the request
			req.send();
		}
	} catch (error) {
  		console.error(error);
	}
}