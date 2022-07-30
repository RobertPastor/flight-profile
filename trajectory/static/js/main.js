
var worker = undefined;

document.addEventListener('DOMContentLoaded', () => {
	//console.log("DOM content loaded");
	init();
});

function showMessage ( title, message ) {
	
	const dialog = document.getElementById("dialogId");
	removeAllChilds(dialog)
	$("#dialogId")
			.dialog({
				autoOpen: false,
				title: ( typeof title === 'string' ? title : JSON.stringify(title)),
				modal: true,
				hide: "puff",
				show : "slide",
				height: 200 ,
				buttons: {
					OK: function() {
					  $( this ).dialog( "close" );
					}
				  }			   
            })
			.html(typeof message === 'string' ? message : JSON.stringify(message))
			.dialog('open'); 
}

function removeLayer( globus , layerName ) {
	
	try {
		let layer = globus.planet.getLayerByName( layerName );
		if (layer) {
			
			let entities = layer.getEntities();
			layer.removeEntities(entities);
			layer.remove();
		}
	} catch (err) {
		console.log("layer is probably not existing")
	}
}

function stopBusyAnimation(){
	//console.log("stop busy anymation");
	stopWorker();
	initProgressBar();
}

function initProgressBar() {
    // Gets the number of image elements
    var numberOfSteps = 100;
    var progressBar = document.getElementById('workerId');
    if (progressBar) {
        progressBar.style.width = "0" + '%';
    }
}

function stopWorker() {
	if (worker) {
		worker.terminate();
	}
    worker = undefined;
    //console.log("worker is stopped !!!");
    // hide the progress bars
}

function initWorker() {
	
	if (typeof (Worker) !== "undefined") {
        //console.log("Yes! Web worker is supported !");
        // Some code.....
        if (typeof (worker) == "undefined") {
            worker = new Worker("/static/js/worker/worker.js");
            worker.onmessage = function (event) {
				
				//console.log(`message received - ${event.data}`);

                var progressBar = document.getElementById('workerId');
				if (progressBar) {
					progressBar.style.width = event.data + '%';
					//progressBar.innerText = event.data + '%';
				}
            };
        }
    } else {
        // Sorry! No Web Worker support..
		console.log("Sorry! no web worker support ...");
    }
}

function initTools(globus, viewExtent) {
			
	//console.log("init other tools");
	// load the airline airports
	airports(globus);
			
	// load the airline routes waypoints
	wayPoints(globus, viewExtent)
			
	// load a flight profile
	showFlightProfile(globus);
			
	// compute Flight Profile
	launchFlightProfile(globus);
	
	// load routes
	loadAirlineRoutes(globus);
	
	$('#bodyDivOverlayId').show();
}

function initMain(viewExtent) {
	//console.log("init Main ");
	
	var osm = new og.layer.XYZ("OpenStreetMap", {
            isBaseLayer: true,
            url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            visibility: true,
            attribution: 'Data @ OpenStreetMap contributors, ODbL'
    });
	
    // a HTMLDivElement which its id is `globus`
    var globus = new og.Globe({
            "target": "globusDivId", 
            "name": "Earth",
            "terrain": new og.terrain.GlobusTerrain(),
            "layers": [osm],
            "autoActivated": true,
			"viewExtent" : viewExtent
	});
	
	setTimeout( function() {
		initTools (globus, viewExtent);
	} , 1500 );
	
}


function init() {
	//console.log("init");

	//$( window ).on( "load", function () {
	//the event occurred
		  
	// hide the overlay
	$('#bodyDivOverlayId').hide();
		  
	let MinLongitude = "-130.0";
	let MinLatitude = "25.0";
	let MaxLongitude = "-70.0";
	let MaxLatitude = "50.0";
	let SouthWest = new og.LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
	let NorthEast = new og.LonLat( parseFloat(MaxLongitude), parseFloat(MaxLatitude) , parseFloat("0.0") );
	let viewExtent = new og.Extent( SouthWest , NorthEast );
	
	setTimeout( function() {
		initMain(viewExtent);
	} , 500 );
		
}
	





