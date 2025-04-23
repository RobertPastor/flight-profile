import { initProgressBar , initWorker , stopBusyAnimation } from "../main/main.js";
import { SingletonMainClass } from "../main/mainSingletonClass.js";

export const SingletonFuelEfficiency = (function () {
	
	let instance;
    function createInstance() {
        var object = new AirlineFuelEfficiency();
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


class AirlineFuelEfficiency {

	constructor() {
		//console.log("Airline Fuel Efficiency constructor");
	}
	
	initAirlineFuelEfficiency() {
	
		//console.log( "init Airline Fuel Efficiency");
				
		document.getElementById("btnFuelEfficieny").onclick  = function () {
			
			//console.log( "click Airline Fuel Efficiency");
			
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "airline/airlineFuelEfficiency/" + airlineName;
			let req = new XMLHttpRequest();
			req.open("GET", urlToSend, true);
			req.responseType = "blob";

			req.onload = function (event) {
				
				stopBusyAnimation();
				document.getElementById("btnFuelEfficieny").disabled = false;

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
