
import { initProgressBar , initWorker } from "../main/main.js";

export function initDownloadKMLfile(flightProfileControl) {
	
	let buttonId = "btnDownLoadKMLfileId";
	// temporary issue between kml versions local and python anywhere
	//document.getElementById(buttonId).disabled = true;
	
	try {
		document.getElementById(buttonId).onclick = function () {
	
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
	
			let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
			let route =  $("#airlineRouteId option:selected").val();
			
			// use the selector of the Flight Profile computation
			let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val();
			let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val();
			
			let elemTOMassKg = document.getElementById('TakeOffMassKgId');
			let elemFL = document.getElementById('requestedFlightLevelId');
			
			// cannot used this keyword in call back
			let reducedClimbPowerCoeffInputId = flightProfileControl.getReducedClimbPowerCoeffInputId();
			let elemReduced = document.getElementById(reducedClimbPowerCoeffInputId);
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
	
			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "trajectory/kml/" + airlineName + "?aircraft=" + aircraftICAOcode;
			urlToSend += "&route=" + route;
			urlToSend += "&adepRwy=" + departureRunWay;
			urlToSend += "&adesRwy=" + arrivalRunWay;
			urlToSend += "&mass=" + elemTOMassKg.value;
			urlToSend += "&fl=" + elemFL.value;
			urlToSend += "&reduc=" + elemReduced.value;
			// 1st April 2024 - fly direct route
			urlToSend += "&direct=" + document.getElementById(flightProfileControl.getDirectRouteCheckBoxId()).checked;
			
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
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);

			 };
			 req.onerror = function (event) {
				 console.error("Error in Download KML file");
				 console.error(JSON.stringify(event));
				 SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);

			 }
			// send the request
			req.send();
		}
	} catch (error) {
  		console.error(error);
	}
}