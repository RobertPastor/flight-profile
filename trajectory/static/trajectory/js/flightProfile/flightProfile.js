
var worker = undefined;

document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("KML flight profile js is loaded");
}); 

function stopBusyAnimation(){
	console.log("stop busy anymation");
}

var imagesIndex = 0;

function updateProgress() {
    var progressBar = document.getElementById('progressId');
    progressBar.value = String(imagesIndex++);
    var progressValue = document.getElementById('progressVal');
    if (progressValue != undefined) {
        progressValue.innerHTML = String(imagesIndex);
    }
}

function initProgressBar() {
    // Gets the number of image elements
    var numberOfSteps = 100;
    var progressBar = document.getElementById('progressId');
    if (progressBar != undefined) {
        progressBar.max = String(numberOfSteps);
    }
}

function stopWorker() {
    worker.terminate();
    worker = undefined;
    console.log("worker is stopped !!!");
    // hide the progress bars
    
    //$("#workerId").hide();
    //$("#progressId").hide();
}

function initWorker() {
	
	if (typeof (Worker) !== "undefined") {
        console.log("Yes! Web worker is supported !");
        // Some code.....
        if (typeof (worker) == "undefined") {
            worker = new Worker("/static/trajectory/js/worker/worker.js");
            worker.onmessage = function (event) {

                var workerProgressBar = document.getElementById('workerId');
                workerProgressBar.value = event.data;

                var workerProgressValue = document.getElementById('workerVal');
                workerProgressValue.innerHTML = event.data;
            };
        }
    } else {
        // Sorry! No Web Worker support..
		console.log("Sorry! no web worker support ...");
    }
}

function flightprofile(globus) {
	
	console.log("start flight profile");
	let layerKML = new og.layer.KML( "FlightProfile" , {
		billboard: { 
			src: '/static/trajectory/images/move_down_icon.png', 
			color: '#6689db' ,
			width : 4,
			height : 4
			},
		color: '#6689db'
	} ) ;
	layerKML.addTo(globus.planet);
	    
	let first = true;
	let show = true;
	document.getElementById("btnFlightProfile").onclick = function () {
		
		if (show) {
			show = false;
			document.getElementById("btnFlightProfile").innerText = "Hide Flight Profile";
			if (first) {
				first = false
				document.getElementById("btnFlightProfile").disabled = true

				// init progress bar.
				initProgressBar();
				initWorker();
				
				// use ajax to get the data 
				$.ajax( {
					method: 'get',
					url :  "trajectory/flightprofile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						console.log( dataJson["kmlURL"] );
						layerKML.addKmlFromUrl( url = dataJson["kmlURL"] );
						setTimeout(stopWorker(), 3000);
						
					},
					error: function(data, status) {
						console.log("Error - delete old bookings: " + status + " SVP veuillez contactez votre administrateur");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnFlightProfile").disabled = false
					},
				} );
				
			} else {
				layerKML.setVisibility(true);
			}
		} else {
			show = true;
			document.getElementById("btnFlightProfile").innerText = "Show Flight Profile";
			layerKML.setVisibility(false);
		}
	};
}