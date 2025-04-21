
import { initProgressBar , initWorker , stopBusyAnimation } from "../main/main.js";
import { SingletonMainClass } from "../main/mainSingletonClass.js";

export const SingletonWindTemperature = (function () {
	
	let instance;

    function createInstance() {
        var object = new WindTemperature();
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

class WindTemperature {

	constructor() {
		//console.log("Wind Temperature constructor");
	}
	
	initWindTemperature() {
	
		//console.log( "init Wind Temperature ");
		
		$('#mainSubMenuMeteoDivId').hide();
		
		document.getElementById("btnWindTemperature").onclick  = function () {
			
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "trajectory/windTemperature/" + airlineName;
			let req = new XMLHttpRequest();
			req.open("GET", urlToSend, true);
			req.responseType = "blob";

			req.onload = function (event) {
				
				stopBusyAnimation();
				document.getElementById("btnWindTemperature").disabled = false;

				
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