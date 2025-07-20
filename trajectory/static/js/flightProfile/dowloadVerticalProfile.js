
import { initProgressBar , initWorker , stopBusyAnimation } from "../main/main.js";
import { SingletonMainClass } from "../main/mainSingletonClass.js";
import { SingletonFlightProfileControlClass } from "../flightProfile/flightProfileControl.js";


export function initDownloadVerticalProfile(flightProfileControl) {
	
	document.getElementById("btnDownLoadVerticalProfileId").onclick = function () {

		SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
		
		let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();

		let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
		let route =  $("#airlineRouteId option:selected").val();
		
		// use the selector of the Flight Profile computation
		let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val();
		let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val();
		
		let elemTOMassKg = document.getElementById('TakeOffMassKgId');
		let elemFL = document.getElementById('requestedFlightLevelId');
		
		// cannot used "this" keyword in call back
		let reducedClimbPowerCoeffInputId = flightProfileControl.getReducedClimbPowerCoeffInputId();
		let elemReduced = document.getElementById(reducedClimbPowerCoeffInputId);
		
		// get the name of the airline
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

		// init progress bar.
		initProgressBar();
		initWorker();
		
		let urlToSend =  "trajectory/excel/" + airlineName + "/" + BadaWrapMode + "?aircraft=" + aircraftICAOcode;
		urlToSend += "&route=" + route;
		urlToSend += "&adepRwy=" + departureRunWay;
		urlToSend += "&adesRwy=" + arrivalRunWay;
		urlToSend += "&mass=" + elemTOMassKg.value;
		urlToSend += "&fl=" + elemFL.value;
		urlToSend += "&reduc=" + elemReduced.value;
		// 1st April 2024 - direct route
		urlToSend += "&direct=" + document.getElementById(flightProfileControl.getDirectRouteCheckBoxId()).checked
		
		let req = new XMLHttpRequest();
		req.open("GET", urlToSend, true);
		req.responseType = "blob";

		req.onload = function () {
			
			stopBusyAnimation();
			
			let blob = req.response;
			let fileName = req.getResponseHeader("Content-Disposition") //if you have the fileName header available
			fileName = fileName.split("=")[1];
			let link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);
			link.download = fileName;
			link.click();
			
			document.getElementById("btnDownLoadVerticalProfileId").disabled = false;
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);

		 };
		 req.onerror = function (event) {
			console.log("Error in Download Vertical Profile");
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
		 }
		// send the request
		req.send();
	}
}