
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

                let progressBar = document.getElementById('workerId');
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

function clickToHide() {
	// span in div and div in div -> hence twice parentNode
	let elem = this.parentNode.parentNode;
	elem.style = "display: none;";
	return false;
}

function hideAllDiv(globus) {
	
	let airlineFleet = SingletonAirlineFleet.getInstance()
	airlineFleet.hideAirlineFleetDiv();
	
	let airlineAirports = SingletonAirlineAirports.getInstance();
	// false means hide
	airlineAirports.showHideAllAirports(globus , false);
	
	let airlineRoutes = SingletonAirlineRoutes.getInstance();
	airlineRoutes.hideAirlineRoutesDiv();
	
	let airlineProfileCosts = SingletonProfileCosts.getInstance();
	airlineProfileCosts.hideFlightProfileDiv();
	
	let airlineFlightLegCosts = SingletonAirlineFlightLegCosts.getInstance();
	airlineFlightLegCosts.hideAirlineFlightLegCostsDiv();
	
	let airlineCosts = SingletonAirlineCosts.getInstance();
	airlineCosts.hideAirlineCostsDiv();
	
	let airlineCostsOptimization = SingletonAirlineCostsOptimization.getInstance();
	airlineCostsOptimization.hideAirlineCostsOptimizationDiv();
	
	let airlineCASM = SingletonAirlineCASM.getInstance();
	airlineCASM.hideAirlineCasmDiv();
	
	let airlineCasmOptimization = SingletonAirlineCasmOptimization.getInstance();
	airlineCasmOptimization.hideAirlineCasmOptimizationDiv();
}

function switchAirlines(globus) {
	
	$( "#airlineSelectId" ).change(function() {
		
		// hide all div created for the other airlines
		hideAllDiv(globus)
		
		stopBusyAnimation()
		
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
	/*
	* fill the selector with the names of the airlines
	*/
	if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {
		airlines.forEach ( function ( airline ) {
			let option = document.createElement("option");
            //option.text = "AmericanWings";
			let select = document.getElementById("airlineSelectId")
			if ( select ) {
				
				let option = document.createElement("option");
                option.text = airline["Name"];
				select.add(option);
			}
		});
	}
}

function initTools(globus, viewExtent) {
			
	// add all controls that are derived from an og control class
	globus.planet.addControl(new MainControl());
	globus.planet.addControl(new HelpControl());
	globus.planet.addControl(new D3Control());
	globus.planet.addControl(new DialogControl());
	
	globus.planet.addControl(new AirlineFleetControl());
	
	// load airline fleet
	let airlineFleet = SingletonAirlineFleet.getInstance()
	airlineFleet.initAirlineFleet();
	
	//console.log("init other tools");
	// contextual menu to show the routes from one right click selected airport 
	globus.planet.addControl(new AirlineAirportsRoutesControl());
	
	// load the airline airports
	let airlineAirports = SingletonAirlineAirports.getInstance();
	airlineAirports.initAirports(globus);
	
	globus.planet.addControl(new AirlineRoutesControl());

	// load the airline routes waypoints
	let airlineRoutes = SingletonAirlineRoutes.getInstance();
	airlineRoutes.initAirlineRoutes(globus);

	let airlineWayPoints = SingletonAirlineWayPoints.getInstance();
	airlineWayPoints.initWayPoints(globus, viewExtent)
	
	// load a flight profile
	//showFlightProfile(globus);
	
	// compute Flight Profile
	globus.planet.addControl(new FlighProfileControl());
	let airlineProfileCosts = SingletonProfileCosts.getInstance();
	airlineProfileCosts.launchFlightProfile(globus);
	
	// compute costs
	// flight profile inputs are shared with flight leg cost controls inputs
	globus.planet.addControl(new AirlineFlightLegCostsResultsControl());
	let airlineFlightLegCosts = SingletonAirlineFlightLegCosts.getInstance()
	airlineFlightLegCosts.initFlightLegCosts();
	
	// airline costs optimization
	globus.planet.addControl(new AirlineCostsControl());
	let airlineCosts = SingletonAirlineCosts.getInstance();
	airlineCosts.initAirlineCosts();
	
	// airline costs optimization
	globus.planet.addControl(new AirlineCostsOptimizationControl());
	let airlineCostsOptimization = SingletonAirlineCostsOptimization.getInstance();
	airlineCostsOptimization.initAirlineCostsOptimization();
	
	// airline CASM
	globus.planet.addControl(new AirlineCasmControl());
	let airlineCASM = SingletonAirlineCASM.getInstance();
	airlineCASM.initAirlineCASM();
	
	// airline CASM Optimization
	globus.planet.addControl(new AirlineCasmOptimizationControl());
	let airlineCasmOptimization = SingletonAirlineCasmOptimization.getInstance();
	airlineCasmOptimization.initAirlineCasmOptimization();
	
	// init download EXCEL Vertical Flight Profile
	initDownloadVerticalProfile();
	
	// now finish by loading the different airlines
	loadAirlines();
	
	// prepare to switch from one airline to the other
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
            "terrain": new og.terrain.GlobusTerrain(),
            "layers": [osm],
            "autoActivated": true,
			"viewExtent" : viewExtent
	});
	
	setTimeout( function() {
		initTools (globus, viewExtent);
	} , 100 );
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
	





