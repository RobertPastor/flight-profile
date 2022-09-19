
var worker = undefined;

document.addEventListener('DOMContentLoaded', () => {
	//console.log("DOM content loaded");
	init();
});


function removeAllChilds (parent) {
    while (parent.lastChild) {
        parent.removeChild(parent.lastChild);
    }
}

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
		let layerOne = globus.planet.getLayerByName( layerName );
		if (layerOne) {
			
			let entities = layerOne.getEntities();
			layerOne.removeEntities(entities);
			layerOne.remove();
		}
	} catch (err) {
		console.log(JSON.stringify(err));
		console.log("layerOne is probably not existing anymore...");
	}
	try {
		let layerTwo = globus.planet.getLayerByName( layerName );
		if (layerTwo) {
			
			layerTwo._entityCollectionsTree.entityCollection.clear();
		}
	} catch (err) {
		console.log(JSON.stringify(err));
		console.log("layerTwo is probably not existing anymore...");
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

function switchAirlines(globus) {
	
	$( "#airlineSelectId" ).change(function() {

		let airlineName = $("#airlineSelectId option:selected").val();
		
		if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {

			airlines.forEach ( function ( airline ) {
				
				if (airlineName == airline["Name"] ) {
					
					let MinLongitude = airline["MinLongitudeDegrees"]
					let MinLatitude = airline["MinLatitudeDegrees"]
					let MaxLongitude = airline["MaxLongitudeDegrees"]
					let MaxLatitude = airline["MaxLatitudeDegrees"]

					let SouthWest = new og.LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
					let NorthEast = new og.LonLat( parseFloat(MaxLongitude), parseFloat(MaxLatitude) , parseFloat("0.0") );
					let viewExtent = new og.Extent( SouthWest , NorthEast );

					globus.planet.viewExtent(viewExtent);
				
				}
			})
		}
  
    });
}

function loadAirlines() {
	
	if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {
		
		airlines.forEach ( function ( airline ) {
			
			let option = document.createElement("option");
            option.text = "AmericanWings";
			let select = document.getElementById("airlineSelectId")
			if ( select ) {
				
				let option = document.createElement("option");
                option.text = airline["Name"];
				select.add(option);
				
			}
		});
	}
}

function hideAllDiv() {
	hideAirlineFleetDiv();
	hideAirlineRoutesDiv();
	hideFlightProfileDiv();
	hideAirlineCostsDiv();
}

function initTools(globus, viewExtent) {
			
	globus.planet.addControl(new MainControl());
	globus.planet.addControl(new HelpControl());
	globus.planet.addControl(new D3Control());
	globus.planet.addControl(new DialogControl());
	
	globus.planet.addControl(new AirlineFleetControl());
	// load airline fleet
	initAirlineFleet();
	
	globus.planet.addControl(new AirlineRoutesControl());
	// load routes
	initAirlineRoutes(globus);
	
	//console.log("init other tools");
	// load the airline airports
	// need to do it after the show airports button is defined in MainControl
	initAirports(globus);
	
	// load the airline routes waypoints
	initWayPoints(globus, viewExtent)
	
	// load a flight profile
	//showFlightProfile(globus);
	
	// compute Flight Profile
	globus.planet.addControl(new FlighProfileControl());
	launchFlightProfile(globus);
	
	// compute Flight Profile
	globus.planet.addControl(new AirlineCostsControl());
	globus.planet.addControl(new AirlineCostsResultsControl());
	initCostsComputation();
	
	loadAirlines();
	switchAirlines(globus);
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
            "terrain": new og.terrain.EmptyTerrain(),
            "layers": [osm],
            "autoActivated": true,
			"viewExtent" : viewExtent
	});
	
	setTimeout( function() {
		initTools (globus, viewExtent);
	} , 500 );
}


function init() {
	//console.log("init");

	//$( window ).on( "load", function () {
	//the event occurred
		  
	//let airlineList = JSON.parse('{{ airlines|escapejs }}');
	if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {
		
		//console.log("receive Airline list");
		
		let airline = airlines[0]
		let MinLongitude = airline["MinLongitudeDegrees"]
		let MinLatitude = airline["MinLatitudeDegrees"]
		let MaxLongitude = airline["MaxLongitudeDegrees"]
		let MaxLatitude = airline["MaxLatitudeDegrees"]
		
		let SouthWest = new og.LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
		let NorthEast = new og.LonLat( parseFloat(MaxLongitude), parseFloat(MaxLatitude) , parseFloat("0.0") );
		let viewExtent = new og.Extent( SouthWest , NorthEast );
	
		setTimeout( function() {
			initMain(viewExtent);
		} , 500 );
	}
		
}
	





