
import { stopBusyAnimation , initProgressBar , initWorker } from "./main.js";

window.addEventListener('load', (event) => { 
       
	//console.log("Download Pdf Presentation is loaded");
	stopBusyAnimation();
	
}); 


export function initDownloadPdfPresentation() {
	
		// init progress bar.
		initProgressBar();
		initWorker();
		
		let urlToSend =  "pdf/downloadPresentation/";
		
		let req = new XMLHttpRequest();
		req.open("GET", urlToSend, true);
		req.responseType = "blob";

		req.onload = function () {
			
			stopBusyAnimation();
			
			let blob = req.response;
			let fileName = req.getResponseHeader("Content-Disposition") //if you have the fileName header available
			// split filename to keep the part after the equal sign
			fileName = fileName.split("=")[1];
			//console.log ( fileName );
			let link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);
			link.download = fileName;
			link.click();
			
		 };
		 req.onerror = function () {
			 
			stopBusyAnimation();
			console.log("Error in Download Pdf Presentation");
		 }
		// send the request
		req.send();
}