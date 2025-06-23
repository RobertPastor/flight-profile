
import {
        Globe,
        GlobusRgbTerrain,
        control,
        LonLat,
        Extent,
        OpenStreetMap
    } from "../og/og.es.js";
    
import { MainControl } from "./mainControl.js";
import { AirlineRoutesAirwaysSubMenu } from "./subMenuAirwaysControl.js";
import { AirlineOptimizationsSubMenu } from "./subMenuOptimizations.js";
import { FuelSubMenu } from "./subMenuFuelControl.js";
import { MeteoSubMenu } from "./subMenuMeteo.js";
import { HelpControl } from "../help/helpControl.js";
import { D3Control } from "../d3/d3Control.js";
import { DialogControl } from "./dialogControl.js";
import { AirlineFleetControl } from "../airlineFleet/airlineFleetControl.js";
import { AirlineAirportsRoutesControl } from "../airlineAirports/airlineAirportsRoutesControl.js"; 
import { AirlineRoutesControl} from "../airlineRoutes/airlineRoutesControl.js";
import { FlightProfileControl } from "../flightProfile/flightProfileControl.js";
import { AirlineFlightLegCostsResultsControl } from "../airlineFlightLegCosts/airlineFlightLegCostsResultsControl.js";
import { AirlineCostsControl } from "../airlineCosts/airlineCostsControl.js";
import { AirlineCostsOptimizationControl } from "../airlineCostsOptimization/airlineCostsOptimizationControl.js";
import { AirlineCasmControl } from "../airlineCASM/airlineCasmControl.js";
import { AirlineCasmOptimizationControl } from "../airlineCasmOptimization/airlineCasmOptimizationControl.js";
import { FuelPlannerControl } from "../fuelPlanner/fuelPlannerControl.js";
import { OgLayerCleanerControl } from "../ogLayerCleaner/ogLayerCleanerControl.js";
import { MetarsOgControl } from "../metars/metarsOgControl.js";

import { SingletonAirlineFleet } from "../airlineFleet/airlineFleet.js";
import { SingletonAirlineAirports } from "../airlineAirports/airlineAirports.js";
import { SingletonAirlineWayPoints } from "../airlineWayPoints/airlineWayPoints.js";
import { SingletonAirlineRoutes } from "../airlineRoutes/airlineRoutes.js";
import { SingletonAirlineCosts } from "../airlineCosts/airlineCosts.js";
import { SingletonProfileCosts } from "../flightProfile/computeFlightProfile.js";
import { SingletonAirlineFlightLegCosts } from "../airlineFlightLegCosts/airlineFlightLegCosts.js";
import { SingletonAirlineCostsOptimization } from "../airlineCostsOptimization/airlineCostsOptimization.js";
import { SingletonAirlineCASM } from "../airlineCASM/airlineCASM.js";
import { SingletonAirlineCasmOptimization } from "../airlineCasmOptimization/airlineCasmOptimization.js";
import { SingletonFuelPlanner } from "../fuelPlanner/fuelPlanner.js";
import { SingletonMetars } from "../metars/metars.js";
import { SingletonAirlineSeatMiles } from "../airlineSeatMilesMaximization/airlineSeatMilesMaximization.js";
import { SingletonSidStar } from "../SidStar/SidStar.js";
import { SingletonWindTemperature } from "../windTemperature/windTemperature.js";
import { SingletonMainClass } from "./mainSingletonClass.js";
import { SingletonFuelEfficiency } from "../fuelPlanner/fuelEfficiency.js";
import { SingletonOgLayerCleaner } from "../ogLayerCleaner/ogLayerCleaner.js";

import { initDownloadVerticalProfile } from "../flightProfile/dowloadVerticalProfile.js";
import { initDownloadKMLfile } from "../flightProfile/downloadKMLfile.js";
    
var worker = undefined;

window.addEventListener('DOMContentLoaded', () => {
	window.addEventListener("load", ($) => {
			setTimeout( function() {
				
				// call init function after a certain amount of milliseconds
				init();
				
			} , 500 );
	});
});

export function removeAllChilds (parent) {
    while (parent.lastChild) {
        parent.removeChild(parent.lastChild);
    }
}

export function showMessage ( title, message ) {
	
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
export function removeLayer( globus , layerName )  {
	
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

export function stopBusyAnimation(){
	//console.log("stop busy anymation");
	stopWorker();
	initProgressBar();
}

export function initProgressBar() {
    // Gets the number of image elements
    //let numberOfSteps = 100;
    let progressBar = document.getElementById('workerId');
    if (progressBar) {
        progressBar.style.width = "0" + '%';
    }
}

export function stopWorker() {
	if (worker) {
		worker.terminate();
	}
    worker = undefined;
}

export function initWorker() {
	
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
export function clickToHide() {
	// span in div and div in div -> hence twice parentNode
	let elem = this.parentNode.parentNode;
	elem.style = "display: none;";
	return false;
}

/**
 * hide all DIVs - use it when an airline is changed
 */
export function hideAllDiv(globus) {
	
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
		 * @TODO : compute viewport based upon Lat Long of airline airports airports
		 * */ 
		if ( airlines && Array.isArray( airlines ) && ( airlines.length > 0 ) ) {

			airlines.forEach ( function ( airline ) {
				
				if (airlineName == airline["Name"] ) {
					
					// airline data made available through template index-og.html
					let MinLongitude = airline["MinLongitudeDegrees"];
					let MinLatitude  = airline["MinLatitudeDegrees"];
					let MaxLongitude = airline["MaxLongitudeDegrees"];
					let MaxLatitude  = airline["MaxLatitudeDegrees"];

					let SouthWest = new LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
					let NorthEast = new LonLat( parseFloat(MaxLongitude) , parseFloat(MaxLatitude) , parseFloat("0.0") );
					let viewExtent = new Extent( SouthWest , NorthEast );

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

/**
 * initialize og.Controls
 */
function initTools(globus, viewExtent) {
			
	// add all controls that are derived from an og control class
	if	(globus){
		
		globus.planet.addControl(new MainControl());
		
		globus.planet.addControl(new AirlineRoutesAirwaysSubMenu());
		globus.planet.addControl(new AirlineOptimizationsSubMenu());
		globus.planet.addControl(new FuelSubMenu());
		// 22nd August 2024 
		globus.planet.addControl(new MeteoSubMenu());
		
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
		
		// 30th December 2023 - Fuel Efficiency
		let fuelEfficiency = SingletonFuelEfficiency.getInstance();
		fuelEfficiency.initAirlineFuelEfficiency();
		
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
		
		// 23rd August 2024 - Wind Temperature
		let windTemperature = SingletonWindTemperature.getInstance();
		windTemperature.initWindTemperature();
		
		// now finish by loading the different airlines
		loadAirlinesSelector();
		
		// prepare to switch from one airline to the other
		switchAirlines(globus);
		
		// 29th September 2023 - 
		let metarsOgControl = new MetarsOgControl();
		globus.planet.addControl( metarsOgControl );
		
		let metar = SingletonMetars.getInstance();
		metar.initMetars( globus , metarsOgControl );
		
		// 29th September 2023 - init listener to Metars button
		
		// show the airports
		SingletonAirlineAirports.getInstance().showHideAllAirports( true );
		
		// 19th July 2023 Main Singleton Class
		new SingletonMainClass.getInstance().init(globus);
		
		// 1st October 2023 - sortable
		let airlineFleetTable = document.getElementById(airlineFleetControl.getMainTableId());
		airlineFleetTable.classList.add('sortable');
		
		let airlineRoutesTable = document.getElementById(airlineRoutesControl.getMainTableId());
		airlineRoutesTable.classList.add('sortable');
		
		let airlineCostsOptimizationTable = document.getElementById(airlineCostsOptimizationControl.getMainTableId());
		airlineCostsOptimizationTable.classList.add('sortable');
		
		let airlineCasmTable = document.getElementById(airlineCasmControl.getMainTableId());
		airlineCasmTable.classList.add('sortable');
		
		let airlineCasmOptimizationTable = document.getElementById(airlineCasmOptimizationControl.getMainTableId());
		airlineCasmOptimizationTable.classList.add('sortable');
		
		let airlineFlightLegCostsResultsTable = document.getElementById(airlineFlightLegCostsResultsControl.getMainTableId());
		airlineFlightLegCostsResultsTable.classList.add('sortable');
		
		let metarsTable = document.getElementById(metarsOgControl.getMainTableId());
		metarsTable.classList.add('sortable');
		
		let airlineAirportsRoutesTable = document.getElementById(airlineAirportsRoutesControl.getMainTableId());
		airlineAirportsRoutesTable.classList.add('sortable');
		
	}
}

function initMain(viewExtent) {
	// 10th September 2023 - use .de OSM instance
	let osm = new OpenStreetMap();
	
    // a HTMLDivElement whose id is `globus`
    //"resourcesSrc": "/static/js/og/res"
    
	var globus = new Globe({
            target: "globusDivId", 
            name: "Earth",
            terrain: new GlobusRgbTerrain(),
            layers: [osm],
            autoActivated: true,
            viewExtent : viewExtent,
            controls: [
				new control.MouseNavigation({ autoActivate: true }),
                new control.KeyboardNavigation({ autoActivate: true }),
                new control.EarthCoordinates({ autoActivate: true, center: false , type: 1}),
                new control.ZoomControl({ autoActivate: true }),
                new control.CompassButton()
                ],
            fontsSrc: "/static/js/og/fonts",
            resourcesSrc: "/static/js/og/res"
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
		
		let SouthWest  = new LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
		let NorthEast  = new LonLat( parseFloat(MaxLongitude), parseFloat(MaxLatitude) , parseFloat("0.0") );
		let viewExtent = new Extent( SouthWest , NorthEast );
	
		setTimeout( function() {
			initMain(viewExtent);
			// check if firefox is used
			if (navigator.userAgent.indexOf("Firefox") == -1 ) { 
					showMessage("Browser usage" , "Please envisage using FireFox to see the globe map");
			}
				
		} , 500 );
	}
}


