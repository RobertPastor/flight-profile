
var worker = undefined;

window.addEventListener('DOMContentLoaded', () => {
	window.addEventListener("load", ($) => {
			setTimeout( function() {
				init();
			} , 500 );
	});
});

function removeAllChilds (parent) {
    while (parent.lastChild) {
        parent.removeChild(parent.lastChild);
    }
}

function showMessage ( title, message ) {
	
	const dialog = document.getElementById("dialogId");
	if (dialog) {
		removeAllChilds(dialog);
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
}

/**
 * @TODO currently there are two methodes to delete a layer in og
 * this recommandation has been received directly from open globus
 */
//function removeLayer( globus , layerName ) : Promise<boolean> {
function removeLayer( globus , layerName )  {
	
	return new Promise ( (resolve, reject) => {
		try {
			let layerTwo = globus.planet.getLayerByName( layerName );
			if (layerTwo) {
				//console.log("layerTwo is probably existing ...");
				layerTwo._entityCollectionsTree.entityCollection.clear();
				console.log("entity collections cleared !!!");
				resolve(true);
			}
		} catch (err) {
			console.error("2nd method to delete a layer - err = "+ JSON.stringify(err));
			reject(err);
		}
		try {
			let layerOne = globus.planet.getLayerByName( layerName );
			if (layerOne) {
				//console.log("layerOne is probably existing ...");
				let entities = layerOne.getEntities();
				layerOne.removeEntities(entities);
				console.log("entity removed !!!");
				//layerOne.remove();
				resolve(true);
			}
		} catch (err) {
			console.error("1st method to delete og layer - err = "+ JSON.stringify(err));
			reject(err);
		}
	})
}

function stopBusyAnimation(){
	//console.log("stop busy anymation");
	stopWorker();
	initProgressBar();
}

function initProgressBar() {
    // Gets the number of image elements
    //let numberOfSteps = 100;
    let progressBar = document.getElementById('workerId');
    if (progressBar) {
        progressBar.style.width = "0" + '%';
    }
}

function stopWorker() {
	if (worker) {
		worker.terminate();
	}
    worker = undefined;
}

function initWorker() {
	
	if (typeof (Worker) !== "undefined") {
        //console.log("Yes! Web worker is supported !");
        if (typeof (worker) == "undefined") {
            worker = new Worker("/static/js/worker/worker.js");
            worker.onmessage = function (event) {
                let progressBar = document.getElementById('workerId');
				if (progressBar) {
					progressBar.style.width = event.data + '%';
				}
            };
        }
    } else {
		console.error("Sorry! no web worker support ...");
    }
}

/**
 * function used to hide any contextual table
 * using the hide button placed upper right in the table div menu bar
 */
function clickToHide() {
	// span in div and div in div -> hence twice parentNode
	let elem = this.parentNode.parentNode;
	elem.style = "display: none;";
	return false;
}

/**
 * hide all DIVs - use it when an airline is changed
 */
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
	
	let fuelPlanner = SingletonFuelPlanner.getInstance();
	fuelPlanner.hideFuelPlannerDiv();
	
	let metars = SingletonMetars.getInstance();
	metars.hideMetarsDiv();
	
}


function switchAirlines(globus) {
	
	$( "#airlineSelectId" ).change(function() {
		
		// hide all div created for the other airlines
		hideAllDiv(globus);
		stopBusyAnimation();
		
		// selector in the main menu bar
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
		
		/**
		 * airlines data is made available through template index-og.html
		 * @TODO : compute viewport based upon Lat Long of airports
		 * */ 
		if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {

			airlines.forEach ( function ( airline ) {
				
				if (airlineName == airline["Name"] ) {
					
					// airline data made available through template index-og.html
					let MinLongitude = airline["MinLongitudeDegrees"];
					let MinLatitude  = airline["MinLatitudeDegrees"];
					let MaxLongitude = airline["MaxLongitudeDegrees"];
					let MaxLatitude  = airline["MaxLatitudeDegrees"];

					let SouthWest = new og.LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
					let NorthEast = new og.LonLat( parseFloat(MaxLongitude) , parseFloat(MaxLatitude) , parseFloat("0.0") );
					let viewExtent = new og.Extent( SouthWest , NorthEast );

					globus.planet.viewExtent(viewExtent);
				}
			});
		}
    });
}

/**
 * build and fill the airline selector
 */
function loadAirlinesSelector() {
	/*
	* fill the selector with the names of the airlines
	* Warning : the airlines array is loaded in the index-og.html -> see Django templates area 
	*/
	if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {
		airlines.forEach ( function ( airline ) {
			let select = document.getElementById("airlineSelectId");
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
	if	(globus){
		
		globus.planet.addControl(new MainControl());
		globus.planet.addControl(new AirlineRoutesAirwaysSubMenu());
		globus.planet.addControl(new AirlineOptimizationsSubMenu());
		
		// control to display help or configuration information
		globus.planet.addControl(new HelpControl());
		
		// control used to draw a vertical profile
		globus.planet.addControl(new D3Control());
		
		// control used to display a message to the user
		globus.planet.addControl(new DialogControl());
		
		let airlineFleetControl = new AirlineFleetControl();
		globus.planet.addControl(airlineFleetControl);
		
		// load airline fleet
		let airlineFleet = SingletonAirlineFleet.getInstance();
		airlineFleet.initAirlineFleet();
		
		// contextual menu to show the routes from one right click selected airport 
		let airlineAirportsRoutesControl = new AirlineAirportsRoutesControl();
		globus.planet.addControl(airlineAirportsRoutesControl);
		
		// load the airline airports
		let airlineAirports = SingletonAirlineAirports.getInstance();
		airlineAirports.initAirports(globus);
		
		// table allowing to see the Routes 
		let airlineRoutesControl = new AirlineRoutesControl();
		globus.planet.addControl(airlineRoutesControl);
	
		// load the airline routes 
		let airlineRoutes = SingletonAirlineRoutes.getInstance();
		airlineRoutes.initAirlineRoutes(globus);
	
		// load the airline routes waypoints
		let airlineWayPoints = SingletonAirlineWayPoints.getInstance();
		airlineWayPoints.initWayPoints(globus, viewExtent);
		
		// compute Flight Profile
		let flightProfileControl = new FlightProfileControl();
		globus.planet.addControl(flightProfileControl);
		
		// compute profile and costs for each route and runways selection
		let airlineProfileCosts = SingletonProfileCosts.getInstance();
		airlineProfileCosts.launchFlightProfile(globus, flightProfileControl);
		
		// compute costs
		// flight profile inputs are shared with flight leg cost controls inputs
		let airlineFlightLegCostsResultsControl = new AirlineFlightLegCostsResultsControl()
		globus.planet.addControl(airlineFlightLegCostsResultsControl);
		
		let airlineFlightLegCosts = SingletonAirlineFlightLegCosts.getInstance();
		airlineFlightLegCosts.initFlightLegCosts(flightProfileControl);
		
		// airline costs optimization
		globus.planet.addControl(new AirlineCostsControl());
		let airlineCosts = SingletonAirlineCosts.getInstance();
		airlineCosts.initAirlineCosts();
		
		// airline costs optimization
		let airlineCostsOptimizationControl = new AirlineCostsOptimizationControl()
		globus.planet.addControl(airlineCostsOptimizationControl);
		
		let airlineCostsOptimization = SingletonAirlineCostsOptimization.getInstance();
		airlineCostsOptimization.initAirlineCostsOptimization();
		
		// airline CASM
		let airlineCasmControl = new AirlineCasmControl();
		globus.planet.addControl(airlineCasmControl);
		
		let airlineCASM = SingletonAirlineCASM.getInstance();
		// need to call this init function to listen to button
		airlineCASM.initAirlineCASM();
		
		// airline CASM Optimization
		let airlineCasmOptimizationControl = new AirlineCasmOptimizationControl();
		globus.planet.addControl(airlineCasmOptimizationControl);
		
		let airlineCasmOptimization = SingletonAirlineCasmOptimization.getInstance();
		airlineCasmOptimization.initAirlineCasmOptimization();
		
		// 6th May 2023 Seat Miles Maximization
		let airlineSeatMilesMaximization = SingletonAirlineSeatMiles.getInstance();
		airlineSeatMilesMaximization.initAirlineSeatsMilesMaximization();
		
		// 13th May 2023 - Fuel Planner
		globus.planet.addControl(new FuelPlannerControl());
		let fuelPlanner = SingletonFuelPlanner.getInstance();
		fuelPlanner.initFuelPlanner(globus);
		
		// 1st July 2023 - add Layer Housekeeping
		let ogLayerCleanerControl = new OgLayerCleanerControl();
		globus.planet.addControl(ogLayerCleanerControl);
		
		let ogLayerCleaner = SingletonOgLayerCleaner.getInstance();
		ogLayerCleaner.init(globus, ogLayerCleanerControl);
		
		// init listener for downloading EXCEL Vertical Flight Profile
		initDownloadVerticalProfile(flightProfileControl);
		
		// 24th June 2023 - init listener for downloading KML file
		initDownloadKMLfile(flightProfileControl);
		
		// 8th June 2023 - SID STAR
		let sidStar = SingletonSidStar.getInstance();
		sidStar.initSidStar(globus);
		
		// now finish by loading the different airlines
		loadAirlinesSelector();
		
		// prepare to switch from one airline to the other
		switchAirlines(globus);
		
		// 29th September 2023 - 
		let metarsOgControl = new MetarsOgControl();
		globus.planet.addControl( metarsOgControl );
		
		let metar = SingletonMetars.getInstance();
		metar.initMetars( globus , metarsOgControl )
		
		// 29th September 2023 - init listener to Metars button
		
		// show the airports
		SingletonAirlineAirports.getInstance().showHideAllAirports( true );
		
		// 19th July 2023 Main Singleton Class
		new SingletonMainClass.getInstance().init(globus);
		
		// 1st October 2023 - sortable
		let airlineFleetTable = document.getElementById(airlineFleetControl.getMainTableDivId());
		airlineFleetTable.classList.add('sortable');
		
		let airlineRoutesTable = document.getElementById(airlineRoutesControl.getMainTableDivId());
		airlineRoutesTable.classList.add('sortable');
		
		let airlineCostsOptimizationTable = document.getElementById(airlineCostsOptimizationControl.getMainTableDivId());
		airlineCostsOptimizationTable.classList.add('sortable');
		
		let airlineCasmTable = document.getElementById(airlineCasmControl.getMainTableDivId());
		airlineCasmTable.classList.add('sortable');
		
		let airlineCasmOptimizationTable = document.getElementById(airlineCasmOptimizationControl.getMainTableDivId());
		airlineCasmOptimizationTable.classList.add('sortable');
		
		let airlineFlightLegCostsResultsTable =  document.getElementById(airlineFlightLegCostsResultsControl.getMainTableDivId());
		airlineFlightLegCostsResultsTable.classList.add('sortable');
		
		let metarsTable =  document.getElementById(metarsOgControl.getMainTableDivId());
		metarsTable.classList.add('sortable');
	}
}


function initMain(viewExtent) {
	// 10th September 2023 - use .de OSM instance
	var osm = new og.layer.XYZ("OpenStreetMap", {
            isBaseLayer: true,
            url: "https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png",
            visibility: true,
            attribution: 'Data @ OpenStreetMap contributors, ODbL'
    });
	
    // a HTMLDivElement whose id is `globus`
    var globus = new og.Globe({
            "target": "globusDivId", 
            "name": "Earth",
            "terrain": new og.terrain.GlobusTerrain(),
            "layers": [osm],
            "autoActivated": true,
			"viewExtent" : viewExtent,
			"controls": [
				new og.control.MouseNavigation({ autoActivate: true }),
                new og.control.KeyboardNavigation({ autoActivate: true }),
                new og.control.EarthCoordinates({ autoActivate: true, center: false , type: 1}),
                new og.control.ZoomControl({ autoActivate: true }),
                new og.control.CompassButton()                
                ]
	});
	initTools (globus, viewExtent);
}


function init() {
	
	// Warning : the airlines object is loaded in the index-og.html
		  
	//let airlineList = JSON.parse('{{ airlines|escapejs }}');
	if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {
				
		let airline = airlines[0];
		let MinLongitude = airline["MinLongitudeDegrees"];
		let MaxLongitude = airline["MaxLongitudeDegrees"];

		let MinLatitude = airline["MinLatitudeDegrees"];
		let MaxLatitude = airline["MaxLatitudeDegrees"];
		
		let SouthWest  = new og.LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
		let NorthEast  = new og.LonLat( parseFloat(MaxLongitude), parseFloat(MaxLatitude) , parseFloat("0.0") );
		let viewExtent = new og.Extent( SouthWest , NorthEast );
	
		setTimeout( function() {
			initMain(viewExtent);
		} , 500 );
	}
}
	

