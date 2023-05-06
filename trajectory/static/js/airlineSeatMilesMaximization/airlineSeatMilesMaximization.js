const SingletonAirlineSeatMiles = (function () {
	
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
		console.log("Airline Seat Miles Maximization constructor");
	}
	
	initAirlineSeatsMilesMaximization() {
	
		console.log( "init Airline CASM ");
		
		$('#airlineCasmMainDivId').hide();
		
		document.getElementById("btnLaunchSeatMilesMaximization").onclick  = function () {
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			// init progress bar.
			initProgressBar();
			initWorker();
			
			let urlToSend =  "airline/getAirlineSeatMilesXlsx/" + airlineName;
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
				
			 };
			 req.onerror = function (event) {
				console.log("Error in Download EXCEL Costs");
			 }
			// send the request
			req.send();
			
		}
	}
	
}