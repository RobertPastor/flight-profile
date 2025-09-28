
import { initProgressBar , initWorker , stopBusyAnimation , removeLayer , showMessage } from "../main/main.js";
import { Ellipsoid , Entity , LonLat , KML , Vector } from "../og/og.es.js";
import { SingletonMainClass } from "../main/mainSingletonClass.js";
import { SingletonOgLayerCleaner } from "../ogLayerCleaner/ogLayerCleaner.js";
import { SingletonFlightProfileControlClass } from "../flightProfile/flightProfileControl.js";

import { VerticalProfile } from "./verticalProfile.js";

document.addEventListener('DOMContentLoaded', () => { 
       	 
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	$("#launchComputeId").hide();

}); 

export const SingletonProfileCosts = (function () {
	
	let instance;
    function createInstance() {
        let object = new AirlineProfileCosts();
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


// Profile and Costs
class AirlineProfileCosts {
	
	constructor() {
		//console.log("Airline Profile Costs constructor") 
	}
	
	populateAircraftPerformance ( aircraftPerformanceData ) {
		
		let elemTOMassKg = document.getElementById('TakeOffMassKgId');
		let elemMinTOMassKg = document.getElementById('minTakeOffMassKgId');
		let elemMaxTOMassKg = document.getElementById('maxTakeOffMassKgId');
		
		// 16th July 2023 - initial default mass = reference mass
		elemTOMassKg.value = "0";
		if ( aircraftPerformanceData.hasOwnProperty("acReferenceTakeOffWeightKg")) {
			elemTOMassKg.value = aircraftPerformanceData["acReferenceTakeOffWeightKg"];
		}
		elemMinTOMassKg.value = "0";
		if ( aircraftPerformanceData.hasOwnProperty("acMinTakeOffWeightKg")) {
			elemMinTOMassKg.value = aircraftPerformanceData["acMinTakeOffWeightKg"];
		}
		elemMaxTOMassKg.value = "0";
		if ( aircraftPerformanceData.hasOwnProperty("acMaxTakeOffWeightKg")) {
			elemMaxTOMassKg.value = aircraftPerformanceData["acMaxTakeOffWeightKg"];
			//console.log(elemMaxTOMassKg.value);
		}
		
		let elemFL = document.getElementById('requestedFlightLevelId');
		elemFL.value = aircraftPerformanceData["acMaxOpAltitudeFeet"];
		
		let elemMaxFL = document.getElementById('maxFlightLevelId');
		elemMaxFL.value = aircraftPerformanceData["acMaxOpAltitudeFeet"];
	}

	populateAircraftFlightProfileSelector( airlineAircraftsArray ) {
	
		// trComputeFlightProfileId
		$("#trComputeFlightProfileId").show();
		// aircraftSelectionId
		$("#aircraftSelectionId").show();
		
		// empty the selector
		$('#airlineAircraftId').empty()

		for (let index = 0; index < airlineAircraftsArray.length; index++) {
		  $('#airlineAircraftId').append('<option value="' + airlineAircraftsArray[index]["airlineAircraftICAOcode"] + '">' + airlineAircraftsArray[index]["airlineAircraftFullName"] + '</option>');
		}
		
		// set takeoff Mass
		let elemTOMassKg    = document.getElementById('TakeOffMassKgId');
		let elemMinTOMassKg = document.getElementById('minTakeOffMassKgId');
		let elemMaxTOMassKg = document.getElementById('maxTakeOffMassKgId');
		
		let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
		
		// set Max TakeOff Mass
		for (let index = 0; index < airlineAircraftsArray.length; index++) {
			if ( airlineAircraftsArray[index]["airlineAircraftICAOcode"] == aircraftICAOcode ) {
				// 1st July 2023 - show reference mass
				elemTOMassKg.value = airlineAircraftsArray[index]["acReferenceTakeOffWeightKg"];
				elemMinTOMassKg.value = airlineAircraftsArray[index]["acMinTakeOffWeightKg"];
				elemMaxTOMassKg.value = airlineAircraftsArray[index]["acMaxTakeOffWeightKg"];
				//console.log(elemMaxTOMassKg.value);
			}
		}
		
		let elemMaxFL = document.getElementById('maxFlightLevelId');
		
		// set Max Flight Level
		let elemFL = document.getElementById('requestedFlightLevelId');
		for (let index = 0; index < airlineAircraftsArray.length; index++) {
			if ( airlineAircraftsArray[index]["airlineAircraftICAOcode"] == aircraftICAOcode ) {
				elemFL.value = airlineAircraftsArray[index]["acMaxOpAltitudeFeet"];
				elemMaxFL.value = airlineAircraftsArray[index]["acMaxOpAltitudeFeet"];
			}
		}
	}
	
	setAirportsICAOcode() {
		
		let selectedRoute = $("#airlineRouteId option:selected").val();

		// get Input Id
		let inputId = this.flightProfileControl.getAdepICAOcodeInputId();
		let inputElement = document.getElementById(inputId);
		inputElement.value = selectedRoute.split("-")[0];
			
		inputId = this.flightProfileControl.getAdesICAOcodeInputId();
		inputElement = document.getElementById(inputId);
		inputElement.value = selectedRoute.split("-")[1];
		
	}

	populateAirlineRoutesFlightProfileSelector( airlineRoutesArray ) {
	
		// trComputeFlightProfileId
		$("#trComputeFlightProfileId").show();
		// routesSelectionId defined in FlightProfileControl
		$("#routesSelectionId").show();
		
		// 18th June 2023 - create a list of departure and arrival airports
		this.routes = [];
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
		
		// empty the selector
		$('#airlineRouteId').empty();

		for (let index = 0; index < airlineRoutesArray.length; index++) {
			
			let airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
			let airlineRouteKey  = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
			$('#airlineRouteId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
			
			// this.routes is used further ... please see below
			this.routes.push({ "airline" : airlineName , 
								"aDep"   : airlineRoutesArray[index]["DepartureAirportICAOCode"] , 
								"aDes"   : airlineRoutesArray[index]["ArrivalAirportICAOCode"]
								});
			
		}
		// the next function is using this.routes object
		this.setAirportsICAOcode();
	}

	loadOneFlightProfileWayPoint( layerWayPoints, waypoint ) {
	
		let longitude = 0.0;
		if (waypoint.hasOwnProperty("Longitude")) {
			longitude = parseFloat(waypoint.Longitude);
		}
		let latitude = 0.0;
		if (waypoint.hasOwnProperty("Latitude")) {
			latitude = parseFloat(waypoint.Latitude);
		}
		let name = "";
		if (waypoint.hasOwnProperty("name")) {
			name = parseFloat(waypoint.name);
		}
		
		layerWayPoints.add(new Entity({
				lonlat: [longitude, latitude],
				label: {
						text: name,
						outline: 0.77,
						outlineColor: "rgba(255,255,255,.4)",
						size: 12,
						color: "black",
						offset: [0, -2]
						},
				billboard: {
						src: "/static/images/marker.png",
						width: 12,
						height: 12,
						offset: [0, -2]
						}
		}));
	}

	loadFlightProfileWayPoints( layerWayPoints, dataJson) {
	
		// get all waypoints
		let waypoints = [];
		if ( dataJson.hasOwnProperty('waypoints')) {
			waypoints = eval(dataJson['waypoints']);
		}
		// add the waypoints
		for (let wayPointId = 0; wayPointId < waypoints.length; wayPointId++ ) {
			// insert one waypoint
			SingletonProfileCosts.getInstance().loadOneFlightProfileWayPoint( layerWayPoints, waypoints[wayPointId] );
		}
	}

	loadFlightProfileOneAirport( layerAirports, airport ) {
	
		let longitude = 0.0;
		if (airport.hasOwnProperty("Longitude")) {
			longitude = parseFloat(airport.Longitude);
		}
		let latitude = 0.0;
		if (airport.hasOwnProperty("Latitude")) {
			latitude = parseFloat(airport.Latitude);
		}
		let name = "";
		if (airport.hasOwnProperty("AirportName")) {
			name = airport.AirportName;
		}
		
		layerAirports.add(new Entity({
				lonlat: [longitude, latitude],
				label: {
						text: name,
						outline: 0.77,
						outlineColor: "rgba(255,255,255,.4)",
						size: 12,
						color: "black",
						offset: [-100, -2]
						},
				billboard: {
						src: "/static/images/plane.png",
						width: 16,
						height: 16,
						offset: [0, 32]
						}
		}));
	}

	loadOneRay( rayLayer, placeMark ) {
	
		/**
		 * @TODO get these constants from og
		 */ 
		let ellipsoid = new Ellipsoid(6378137.0, 6356752.3142);
		
		let latitude = 0.0;
		if ( placeMark.hasOwnProperty("latitude")) {
			latitude = parseFloat(placeMark["latitude"]);
		}

		let longitude = 0.0;
		if ( placeMark.hasOwnProperty("longitude")) {
			longitude = parseFloat(placeMark["longitude"]);
		}
		
		let height = 0.0;
		if ( placeMark.hasOwnProperty("height")) {
			height = parseFloat(placeMark["height"]);
		}
		
		let lonlat = new LonLat(longitude, latitude , 0.0);
		//coordinate above Bochum to allow a upwards direction of ray
		let lonlatAir = new LonLat(longitude, latitude , height);
		
		//coordinates of Bochum in Cartesian
		let cart = ellipsoid.lonLatToCartesian(lonlat);
		let cartAir = ellipsoid.lonLatToCartesian(lonlatAir);
		
		if ( placeMark["name"].length > 0 ) {
			let offset = [10, 10];
			if ( placeMark["name"].includes("turn") || placeMark["name"].includes("climb") || placeMark["name"].includes("touch") ) {
				offset = [10, -20];
			} 
			// alternate place
			if ( placeMark["name"].includes("ground") || placeMark["name"].includes("slope") || placeMark["name"].includes("takeOff") ) {
				offset = [10, +20];
			}
			rayLayer.add(new Entity({
				cartesian : cartAir,
				label: {
						text: placeMark["name"],
						outline: 0.77,
						outlineColor: "rgba(255,255,255,.4)",
						size: 12,
						color: "black",
						offset: offset
						}
			}));
		}
		// create a ray
		rayLayer.add ( new Entity({
				ray: {
					startPosition: cart,
					endPosition: cartAir,
					length: height,
					startColor: "blue",
					endColor: "green",
					thickness: 5
				}
			})
		);
	}

	addRays ( rayLayer , placeMarks ) {
		// add the waypoints
		for (let placeMarkId = 0; placeMarkId < placeMarks.length; placeMarkId++ ) {
			// insert one waypoint
			SingletonProfileCosts.getInstance().loadOneRay( rayLayer, placeMarks[placeMarkId] );
		}
	}

	deleteCreateKMLLayer(globus , layerName ) {
	
		let finalLayerName = "FlightProfile-" + layerName ;
		/**
		 * @TODO removeLayer defined in the main.js
		 */
		removeLayer( globus , finalLayerName );
		
		let layerKML = new KML( finalLayerName , {
			billboard: { 
				src: '/static/images/move_down_icon.png', 
				color: '#6689db' ,
				width : 4,
				height : 4
				},
			color: '#6689db'
		} ) ;
		layerKML.addTo(globus.planet);
		return layerKML;
	}
	
	/**
	 * unique way to define a global layer name for all airlines
	 * @TODO warning = not applicable if several identical Adep Ades routes for one airline
	 */
	getLayerPrefix() {
		// get the name of the airline
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
		return "Rays" + "-" + airlineName;
	}
	
	/**
	 * called when a new Ray Layer has to be created or a new layer with the same Adep Ades.
	 */
	deleteCreateRayLayer( globus , route ) {
		
		//console.log ( route );
		let layerPrefix = SingletonProfileCosts.getInstance().getLayerPrefix();
	
		// route format = "Adep"+"-"+"Ades"
		let layerName = layerPrefix + "-" + route;
		//console.log( layerName );
		
		/**
		 * @TODO removeLayer to use Promise !!!
		 * removeLayer defined in the main.js
		 */
		let ogLayer = globus.planet.getLayerByName( layerName );
		if ( ogLayer ) {
			removeLayer( globus , layerName );
		}

		//polygonOffsetUnits is needed to hide rays behind globe
		let rayLayer = new Vector( layerName , { polygonOffsetUnits: 0 });
		rayLayer.addTo(globus.planet);
		
		// add layer to the House Keeping class
		// get the name of the airline
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
				
		// add layer to the og Cleaner table
		SingletonOgLayerCleaner.getInstance().addLayer( layerName , airlineName , route.split("-")[0] , route.split("-")[1]);
		
		return rayLayer;
	}

	// using D3 library - display a vertical profile
	displayD3LineChart( arrayAltitudeMSLtime ) {
	
		let verticalProfile = new VerticalProfile();
		verticalProfile.displayVerticalProfile (arrayAltitudeMSLtime);
	}
	
	populateBestDepartureRunway(airlineRoutesArray) {
		
		$('#airlineDepartureRunWayFlightProfileId').empty();
				
		for ( let index = 0 ; index < airlineRoutesArray.length ; index++) {
				
				let route = $("#airlineRouteId option:selected").val();
				if ( ( route.split("-")[0] == airlineRoutesArray[index]["DepartureAirportICAOCode"] )
					&& ( route.split("-")[1] == airlineRoutesArray[index]["ArrivalAirportICAOCode"] ) ) {
					
					// fill only one option è> the best runway -> BestDepartureRunway
					let airlineRunWayKey = airlineRoutesArray[index]["BestDepartureRunway"];
					$('#airlineDepartureRunWayFlightProfileId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayKey + '</option>');
				}
		}
	}
	
	populateBestArrivalRunway( airlineRoutesArray ) {
		
		$('#airlineArrivalRunWayFlightProfileId').empty();
					
		for ( let index = 0 ; index < airlineRoutesArray.length ; index++) {
			
				let route = $("#airlineRouteId option:selected").val();
				if ( ( route.split("-")[0] == airlineRoutesArray[index]["DepartureAirportICAOCode"] )
					&& ( route.split("-")[1] == airlineRoutesArray[index]["ArrivalAirportICAOCode"] ) ) {
					
					// fill only one option è> the best arrival runway -> BestDepartureRunway
					let airlineRunWayKey = airlineRoutesArray[index]["BestArrivalRunway"];
					$('#airlineArrivalRunWayFlightProfileId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayKey + '</option>');

				}
		}
	}

	// 15th August 2023 - use checkbox to use only the Best Departure or arrival runway
	populateAirlineRunWaysFlightProfileSelector( airlineRunWaysArray , airlineRoutesArray ) {
	
		$("#tableFlightProfileId").show();
		$("#trComputeFlightProfileId").show();
		
		// empty the departure runway selector
		$('#airlineDepartureRunWayFlightProfileId').empty();
		
		let departureRunwayCheckBoxId = this.flightProfileControl.getBestDepartureRunwayCheckBoxId();
		if ( $("#"+departureRunwayCheckBoxId).is(":checked") ) {
			
			this.populateBestDepartureRunway(airlineRoutesArray);
			
		} else {
			
			for ( let index = 0 ; index < airlineRunWaysArray.length ; index++) {
			
				let route = $("#airlineRouteId option:selected").val();
				if ( route.split("-")[0] == airlineRunWaysArray[index]["airlineAirport"]) {
								
					let airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"];
					let airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading";
					$('#airlineDepartureRunWayFlightProfileId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
				}
			}
		}
		
		// empty the arrival runway selector
		$('#airlineArrivalRunWayFlightProfileId').empty();
		
		let arrivalRunwayCheckBoxId = this.flightProfileControl.getBestArrivalRunwayCheckBoxId();
		if ( $("#"+arrivalRunwayCheckBoxId).is(":checked") ) {
			this.populateBestArrivalRunway( airlineRoutesArray );
		} else {
			
			for ( let index = 0 ; index < airlineRunWaysArray.length ; index++) {
				
				let route = $("#airlineRouteId option:selected").val();
				if ( route.split("-")[1] == airlineRunWaysArray[index]["airlineAirport"]) {
					
					let airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"];
					let airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading";
					$('#airlineArrivalRunWayFlightProfileId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
				}
			}
		}
	}

	hideFlightProfileDiv() {
		if ( $('#flightProfileMainDivId').is(":visible") ) {
			$("#flightProfileMainDivId").hide();
		}
	}
	
	// main entry point - called from main.js
	launchFlightProfile(globus , flightProfileControl) {
	
		this.globus = globus;
		this.flightProfileControl = flightProfileControl;
		
		/**
		 * globus.planet.events.on("layeradd", function (e) {
		*  if (e.pickingObject instanceof og.Layer) {
		*		console.log(e.pickingObject.name);
		*	}
		*	stopBusyAnimation();
		*});
		**/
		
		// 14th August 2023 - Listen to change in the Best Runway selection checkbox
		let departureRunwayCheckBoxId = this.flightProfileControl.getBestDepartureRunwayCheckBoxId();
		document.getElementById( departureRunwayCheckBoxId ).addEventListener('change', function () {
						
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
			let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();

			//console.log( "Handler for airlineRouteId selection change called." );
			$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName + "/" + BadaWrapMode,
						async : true,
						success: function(data) {
										
							let dataJson = eval(data);
							// airlineRunWays
							if ( dataJson.hasOwnProperty( "airlineRunWays" ) && dataJson.hasOwnProperty( "airlineRoutes" ) ) {
								SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] , dataJson["airlineRoutes"]);
							}
						},
						error: function(data, status) {
							stopBusyAnimation();
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage( "Error - Launch Flight Profile" , eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false;
						},
				});
		});
		
		// 14th August 2023 - Listen to change in the Best Runway selection checkbox
		let arrivalRunwayCheckBoxId = this.flightProfileControl.getBestArrivalRunwayCheckBoxId();
		document.getElementById( arrivalRunwayCheckBoxId ).addEventListener('change', function () {
						
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
			let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();

			//console.log( "Handler for airlineRouteId selection change called." );
			$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName + "/" + BadaWrapMode,
						async : true,
						success: function(data) {
										
							let dataJson = eval(data);
							// airlineRunWays
							if ( dataJson.hasOwnProperty( "airlineRunWays" ) && dataJson.hasOwnProperty( "airlineRoutes" ) ) {
								SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] , dataJson["airlineRoutes"] );
							}
						},
						error: function(data, status) {
							stopBusyAnimation();
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage( "Error - Launch Flight Profile" , eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false;
						},
				});
		});
		
		// 16th July 2023 - listen to Reduced Climb Power settings changes
		let reducedClimbPowerCoeffInputId = this.flightProfileControl.getReducedClimbPowerCoeffInputId();
		document.getElementById(reducedClimbPowerCoeffInputId).addEventListener('change', function () {
			
			// Warning : cannot use this inside a call-back
			let elemDefaultMaxValue = flightProfileControl.getReducedClimPowerCoeffInputDefaultValue();
			
			let elemReducedClimbPowerCoeffInput = document.getElementById(reducedClimbPowerCoeffInputId);
			let elemValue = elemReducedClimbPowerCoeffInput.value;
			if ( ( ! Number.isInteger(+(elemValue)) ) || ( elemValue.length == 0) ) {
				showMessage("Reduced Climb Power Error" , "Reduced Climb Power Coeff must be an integer");
				elemReducedClimbPowerCoeffInput.value = elemDefaultMaxValue;
			} else {
				if ( elemValue > parseInt( elemDefaultMaxValue ) ) {
					showMessage ("Reduced Climb Power Percentage Error" , "Reduced Climb Power Percentage must be lower or equal to " + elemDefaultMaxValue )
					elemReducedClimbPowerCoeffInput.value = elemDefaultMaxValue;
				} else {
					if ( elemValue < parseInt ( 0.0 ) ) {
						showMessage ("Reduced Climb Power Percentage Error" , "Reduced Climb Power Percentage must be greater or equal to 0.0" )
						elemReducedClimbPowerCoeffInput.value = elemDefaultMaxValue;
					}
				}
			}
		});
		
		// listen to change to the aircraft Mass
		document.getElementById("TakeOffMassKgId").addEventListener('change', function () {
			
			let elemTOMassKg = document.getElementById('TakeOffMassKgId');
			//console.log(elemTOMassKg.value);
			let massValue = elemTOMassKg.value;
			let elemMinTOMassKg = document.getElementById('minTakeOffMassKgId');
			let elemMaxTOMassKg = document.getElementById('maxTakeOffMassKgId');
			
			if ( ! Number.isInteger(+(elemTOMassKg.value)) ) {
				showMessage("Take Off Mass Error" , "Take Off Mass KG must be an integer");
				elemTOMassKg.value = elemMaxTOMassKg.value;
			} else {
				if ( massValue > parseInt( elemMaxTOMassKg.value ) ) {
					showMessage ("Take Off Mass Error" , "Take Off Mass Kg must be lower or equal to " + elemMaxTOMassKg.value )
					elemTOMassKg.value = elemMaxTOMassKg.value;
				} else {
					if ( massValue < parseInt ( elemMinTOMassKg.value ) ) {
						showMessage ("Take Off Mass Error", "Take Off Mass Kg must be greater or equal to " + elemMinTOMassKg.value )
						elemTOMassKg.value = elemMaxTOMassKg.value;
					}
				}
			}
		});
		
		// listen to change to requested flight level
		document.getElementById("requestedFlightLevelId").addEventListener('change', function () {
			let elemFL = document.getElementById('requestedFlightLevelId');
			let FLvalue = elemFL.value;
			//console.log(elemFL.value);
			let elemMaxFL = document.getElementById('maxFlightLevelId');
			
			if ( ( ! Number.isInteger(+(FLvalue)) ) || ( FLvalue.length == 0 ) ) {
				showMessage("Flight Level Error" , "Flight Level must be an integer");
					elemFL.value = elemMaxFL.value;
			} else {
				if ( FLvalue > parseInt( elemMaxFL.value ) ) {
						showMessage ("Flight Level Error" ,  "Flight Level must be lower than " + elemMaxFL.value );
						elemFL.value = elemMaxFL.value;
				} 
				if ( FLvalue < parseInt( "0" ) ) {
						showMessage ("Flight Level Error" ,  "Flight Level must be greater than 0" );
						elemFL.value = elemMaxFL.value;
				} 
			}
		});
		
		// listen to the route change selector
		$( "#airlineRouteId" ).change(function() {
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
			let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();

			//console.log( "Handler for airlineRouteId selection change called." );
			$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName + "/" + BadaWrapMode,
						async : true,
						success: function(data) {
										
							let dataJson = eval(data);
							// airlineRunWays
							if ( dataJson.hasOwnProperty( "airlineRunWays" ) && dataJson.hasOwnProperty( "airlineRoutes" ) ) {
								SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] , dataJson["airlineRoutes"] );
							}
							// each time the route selector changes, it is needed to update the inputs with the ICAO codes
							SingletonProfileCosts.getInstance().setAirportsICAOcode();
							$("#btnLaunchCosts").show();
							
						},
						error: function(data, status) {
							stopBusyAnimation();
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage( "Error - Launch Flight Profile" , eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false;
						},
				});
		});
		
		$("#flightProfileMainDivId").hide();
		/**
		* monitor the button used to show the table with the inputs
		* it allows only to choose the aircraft, the route before clicking to launch the profile computation
		**/
		if ( ! document.getElementById("btnLaunchFlightProfile") ) {
			return;
		}
		document.getElementById("btnLaunchFlightProfile").onclick = function () {

			if ( ! $('#flightProfileMainDivId').is(":visible") ) {
				
				$('#flightProfileMainDivId').show();
								
				// get the name of the airline
				let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
				
				// disable all buttons
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
				let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName + "/" + BadaWrapMode,
						async : true,
						success: function(data) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);
							// airlineAircrafts
							if ( dataJson.hasOwnProperty( "airlineAircrafts" ) 
								&& dataJson.hasOwnProperty( "airlineRoutes" ) 
								&& dataJson.hasOwnProperty( "airlineRunWays" )) {
								
								SingletonProfileCosts.getInstance().populateAircraftFlightProfileSelector( dataJson["airlineAircrafts"] );
								SingletonProfileCosts.getInstance().populateAirlineRoutesFlightProfileSelector( dataJson["airlineRoutes"] );
								
								SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] , dataJson["airlineRoutes"] );
								
								$("#launchComputeId").show();
							}
						},
						error: function(data, status) {
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage("Error - launch Flight Profile", eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false;
							// enable all buttons
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
						},
				});
			} else {
				$('#flightProfileMainDivId').hide();
			}
		} 
		
		/**
		* Monitor the change of Aircraft
		**/
		document.getElementById("airlineAircraftId").onchange = function () {
			
			let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
			let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();

			// init progress bar.
			initProgressBar();
			initWorker();
			
			$.ajax({
						method: 'get',
						url :  "trajectory/aircraft" ,
						async : true,
						data: 'aircraft=' + aircraftICAOcode + "&" + "BadaWrap=" + BadaWrapMode,
						success: function(data) {
							
							let dataJson = eval(data);
							if ( dataJson.hasOwnProperty("errors") ) {
								stopBusyAnimation();
								showMessage( "Error" , dataJson["errors"] );
								
							} else {
								//alert("Data: " + data + "\nStatus: " + status);
								let dataJson = eval(data);
								// airlineAircrafts
								SingletonProfileCosts.getInstance().populateAircraftPerformance( dataJson );
							}
						},
						error: function(data, status) {
							stopBusyAnimation();
							alert("Error - compute Flight Profile: " + status + " Please contact your admin");
							showMessage( "Error" , eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnComputeFlightProfileId").disabled = false;
						}
			});
		}
		
		/**
		 * monitor the radio button used to switch from BADA to WRAP
		 * radio button id are defined in Flight Profile Control
		 **/
		let BADAcheckboxId = SingletonFlightProfileControlClass.getInstance().getBADACheckBoxId();
		document.getElementById(BADAcheckboxId).addEventListener('click', function(){
			
			//console.log("radio button Bada has been clicked");
			
				// get the name of the airline
				let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
				
				// disable all buttons
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
				let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();
				
				initProgressBar();
				initWorker();

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName + "/" + BadaWrapMode,
						async : true,
						success: function(data) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);
							// airlineAircrafts
							if ( dataJson.hasOwnProperty( "airlineAircrafts" ) 
								&& dataJson.hasOwnProperty( "airlineRoutes" ) 
								&& dataJson.hasOwnProperty( "airlineRunWays" )) {
								
								SingletonProfileCosts.getInstance().populateAircraftFlightProfileSelector( dataJson["airlineAircrafts"] );
								SingletonProfileCosts.getInstance().populateAirlineRoutesFlightProfileSelector( dataJson["airlineRoutes"] );
								
								SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] , dataJson["airlineRoutes"] );
								
								$("#launchComputeId").show();
							}
						},
						error: function(data, status) {
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage("Error - launch Flight Profile", eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false;
							// enable all buttons
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
						},
				});
			
		});
		
		
		let WRAPcheckboxId = SingletonFlightProfileControlClass.getInstance().getWRAPCheckBoxId();
		document.getElementById(WRAPcheckboxId).addEventListener('click', function(){
			
			// disable the Reduced climb performance
			let ReducedClimbPowerInputId  = SingletonFlightProfileControlClass.getInstance().getReducedClimbPowerCoeffInputId();
			$("#"+ ReducedClimbPowerInputId ).prop('disabled', true);

			//console.log("radio button Wrap has been clicked");
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
				
			// disable all buttons
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
			let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();
			
			initProgressBar();
			initWorker();

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName + "/" + BadaWrapMode,
						async : true,
						success: function(data) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);
							// airlineAircrafts
							if ( dataJson.hasOwnProperty( "airlineAircrafts" ) 
								&& dataJson.hasOwnProperty( "airlineRoutes" ) 
								&& dataJson.hasOwnProperty( "airlineRunWays" )) {
								
								SingletonProfileCosts.getInstance().populateAircraftFlightProfileSelector( dataJson["airlineAircrafts"] );
								SingletonProfileCosts.getInstance().populateAirlineRoutesFlightProfileSelector( dataJson["airlineRoutes"] );
								
								SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] , dataJson["airlineRoutes"] );
								
								$("#launchComputeId").show();
							}
						},
						error: function(data, status) {
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage("Error - launch Flight Profile", eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false;
							// enable all buttons
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
							
							let ReducedClimbPowerInputId  = SingletonFlightProfileControlClass.getInstance().getReducedClimbPowerCoeffInputId();
							$("#"+ ReducedClimbPowerInputId ).prop('disabled', false);
						},
				});
		});
		
		
		/**
		* monitor the button used to launch the profile computation
		**/
		//document.getElementById("btnComputeFlightProfileId").disabled = true
		document.getElementById("btnComputeFlightProfileId").onclick = function () {
				
			document.getElementById("btnComputeFlightProfileId").disabled = true;
			SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
			
			let BadaWrapMode = SingletonFlightProfileControlClass.getInstance().getSelectedBadaWrapMode();
			
			let aircraft = $("#airlineAircraftId option:selected").val();
			let route =  $("#airlineRouteId option:selected").val();
			
			let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val();
			let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val();
			
			let elemTOMassKg = document.getElementById('TakeOffMassKgId');
			let elemFL = document.getElementById('requestedFlightLevelId');
			
			// cannot used this keyword in call back
			let reducedClimbPowerCoeffInputId = flightProfileControl.getReducedClimbPowerCoeffInputId();
			let elemReduced = document.getElementById(reducedClimbPowerCoeffInputId);
			
			// get the name of the airline
			let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
			
			let data = 'aircraft=' + aircraft;
			data += '&route='   + route;
			data += '&adepRwy=' + departureRunWay;
			data += '&adesRwy=' + arrivalRunWay;
			data += '&mass='    + elemTOMassKg.value;
			data += '&fl='      + elemFL.value;
			// 17th July 2023 - add reduced climb power coefficient
			data += '&reduc='   + elemReduced.value;
			
			// 1st April 2024 - fly direct route
			data += "&direct=" + document.getElementById(flightProfileControl.getDirectRouteCheckBoxId()).checked;
			
			// init progress bar.
			initProgressBar();
			initWorker();
			
			$.ajax({
						method:  'get',
						url   :  "trajectory/computeFlightProfile/" + airlineName + "/" + BadaWrapMode,
						async :  true,
						data  :  data ,
						success: function(data) {
							
							let dataJson = eval(data);
							if ( dataJson.hasOwnProperty("errors") ) {
								
								stopBusyAnimation();
								showMessage( "Error" , dataJson["errors"] );
								
							} else {
								// create layers - performs also a delete layer if layer name found
								let layerKML = SingletonProfileCosts.getInstance().deleteCreateKMLLayer(globus , route);
								let rayLayer = SingletonProfileCosts.getInstance().deleteCreateRayLayer(globus , route);
								
								// convert JSON to XML
								let x2js = new X2JS();
								if ( dataJson.hasOwnProperty( "kmlXMLjson" )) {
									
									let xml = x2js.js2xml(dataJson["kmlXMLjson"]);
								
									let parser = new DOMParser();
									let xmlDoc = parser.parseFromString(xml, "text/xml");
									
									// add Kml From Xml add to open globus
									try {
										// need to create a Pull Request to openglobus to add this function
										layerKML.addKmlFromXml(  xmlDoc ,  null ,  null );
									} catch (err) {
										showMessage("Error - add KML from XML" , JSON.stringify(err) );
									}
								}
								
								// add rays to Rays layer
								if ( dataJson.hasOwnProperty( "placeMarks" )) {
									SingletonProfileCosts.getInstance().addRays( rayLayer , dataJson["placeMarks"] );
								}
								// display the 3D vertical profile
								if ( dataJson.hasOwnProperty( "csvAltitudeMSLtime" )) {
									let arrayAltitudeMSLtime = dataJson["csvAltitudeMSLtime"];
									SingletonProfileCosts.getInstance().displayD3LineChart(arrayAltitudeMSLtime);
									//showMessage("Information" , "Double Click in the vertical profile to return to the map");
								}
							}
						},
						error: function(data, status) {
							stopBusyAnimation();
							alert("Error - compute Flight Profile: " + status + " Please contact your admin");
							showMessage( "Error" , eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
						}
				});
		}
	}
}