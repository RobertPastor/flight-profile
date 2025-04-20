import { initProgressBar , initWorker } from "../main/main.js";

export const SingletonAirlineSeatMiles = (function () {
	
	let instance;

    function createInstance() {
        var object = new AirlineSeatsMilesMaximization();
        return object;
    }

    return {
        getInstance: function () {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();


class AirlineSeatsMilesMaximization {

	constructor() {
		//console.log("Airline Seat Miles Maximization constructor");
	}
	
	initAirlineSeatsMilesMaximization() {
	
		//console.log( "init Airline CASM ");
		
		$('#airlineCasmMainDivId').hide();
		
		document.getElementById("btnLaunchSeatMilesMaximization").onclick  = function () {
			
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "airline/getAirlineSeatMilesXlsx/" + airlineName;
			let req = new XMLHttpRequest();
			req.open("GET", urlToSend, true);
			req.responseType = "blob";

			req.onload = function (event) {
				
				stopBusyAnimation();
				document.getElementById("btnLaunchSeatMilesMaximization").disabled = false;

				
				let blob = req.response;
				let fileName = req.getResponseHeader("Content-Disposition") //if you have the fileName header available
				// name starts with attachment followed by a EQUAL sign and the file name
				fileName = fileName.split("=")[1];
				let link = document.createElement('a');
				link.href = window.URL.createObjectURL(blob);
				link.download = fileName;
				link.click();
				
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
				
			 };
			 req.onerror = function (event) {
				console.log("Error in Download EXCEL Costs");
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
			 }
			// send the request
			req.send();
			
		}
	}
	
}