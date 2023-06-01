
document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("Down Load Vertical Profile is loaded");
	
}); 

function initDownloadVerticalProfile() {
	
	document.getElementById("btnDownLoadVerticalProfileId").onclick = function () {

		document.getElementById("btnDownLoadVerticalProfileId").disabled = true;

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
		
		let data = {
			aircraft : aircraftICAOcode,
			route    : route,
			AdepRwy  : departureRunWay,
			AdesRwy  : arrivalRunWay,
			mass     : elemTOMassKg.value,
			fl       : elemFL.value
		}
		
		let urlToSend =  "trajectory/excel/" + airlineName + "?ac=" + aircraftICAOcode;
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
			fileName = fileName.split("=")[1]
			let link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);
			link.download = fileName;
			link.click();
			
			document.getElementById("btnDownLoadVerticalProfileId").disabled = false;

		 };
		 req.onerror = function (event) {
			console.log("Error in Download Vertical Profile");
		 }
		// send the request
		req.send();

	}
}