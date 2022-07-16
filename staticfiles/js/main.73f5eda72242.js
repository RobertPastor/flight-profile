
var worker = undefined;

document.addEventListener('DOMContentLoaded', (event) => {
    //the event occurred
		  
	// hide the overlay
	$('#bodyDivOverlayId').hide();
		  
	let MinLongitude = -130.
	let MinLatitude = 25.
	let MaxLongitude = -70.
	let MaxLatitude = 50.
	let viewExtent = [MinLongitude , MinLatitude, MaxLongitude, MaxLatitude]
	setTimeout( function() {
			initMain(viewExtent);
		} , 1500 );
})

function initTools(globus, viewExtent) {
	
	$('#bodyDivOverlayId').show();
			
			// load the airline airports
			airports(globus);
			
			// load the airline routes waypoints
			wayPoints(globus, viewExtent)
			
			// load a flight profile
			showFlightProfile(globus);
			
			// compute Flight Profile
			launchFlightProfile(globus);
	
}

function initMain(viewExtent) {
	console.log("init Main ");
	let osm = new og.layer.XYZ("OpenStreetMap", {
            isBaseLayer: true,
            url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            visibility: true,
            attribution: 'Data @ OpenStreetMap contributors, ODbL'
    });
	    
    // a HTMLDivElement which its id is `globus`
    let globus = new og.Globe({
            "target": "globus", 
            "name": "Earth",
            "terrain": new og.terrain.GlobusTerrain(),
            "layers": [osm],
            "autoActivated": true,
            "viewExtent": viewExtent
    });
	
	setTimeout( function() {
			initTools (globus, viewExtent);
		} , 	500 );
		
	
	globus.planet.events.on("layeradd", function (e) {
		
		console.log("layeradd event");
		if (e.pickingObject instanceof og.Layer) {
            console.log(e.pickingObject.name);
        }
    });
}

function stopBusyAnimation(){
	console.log("stop busy anymation");
	stopWorker();
	initProgressBar();
}


function initProgressBar() {
    // Gets the number of image elements
    var numberOfSteps = 100;
    var progressBar = document.getElementById('workerId');
    if (progressBar) {
        //progressBar.style.width = "0" + '%';
    }
}

function stopWorker() {
	if (worker) {
		worker.terminate();
	}
    worker = undefined;
    console.log("worker is stopped !!!");
    // hide the progress bars
}


function initWorker() {
	
	if (typeof (Worker) !== "undefined") {
        console.log("Yes! Web worker is supported !");
        // Some code.....
        if (typeof (worker) == "undefined") {
            worker = new Worker("/static/js/worker/worker.js");
            worker.onmessage = function (event) {
				
				//console.log(`message received - ${event.data}`);

                var progressBar = document.getElementById('workerId');
				//if (progressBar) {
				//	progressBar.style.width = event.data + '%';
				//	progressBar.innerText = event.data + '%';
				//}
            };
        }
    } else {
        // Sorry! No Web Worker support..
		console.log("Sorry! no web worker support ...");
    }
}


