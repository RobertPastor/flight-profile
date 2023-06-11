
document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("compute flight profile js is loaded");
	 
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	$("#launchComputeId").hide();

}); 

const SingletonProfileCosts = (function () {
	
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




class AirlineProfileCosts {
	
	constructor() {
		//console.log("Airline Profile Costs constructor") 
	}
	
	populateAircraftPerformance ( aircraftPerformanceData ) {
		
		let elemTOMassKg = document.getElementById('TakeOffMassKgId');
		let elemMinTOMassKg = document.getElementById('minTakeOffMassKgId');
		let elemMaxTOMassKg = document.getElementById('maxTakeOffMassKgId');
		
		elemTOMassKg.value    = aircraftPerformanceData["acMaxTakeOffWeightKg"];
		elemMinTOMassKg.value = aircraftPerformanceData["acMinTakeOffWeightKg"];
		elemMaxTOMassKg.value = aircraftPerformanceData["acMaxTakeOffWeightKg"];
		
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
		let elemTOMassKg = document.getElementById('TakeOffMassKgId');
		let elemMinTOMassKg = document.getElementById('minTakeOffMassKgId');
		let elemMaxTOMassKg = document.getElementById('maxTakeOffMassKgId');
		
		let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
		//console.log(aircraftICAOcode);
		
		// set Max TakeOff Mass
		for (let index = 0; index < airlineAircraftsArray.length; index++) {
			if ( airlineAircraftsArray[index]["airlineAircraftICAOcode"] == aircraftICAOcode ) {
				elemTOMassKg.value = airlineAircraftsArray[index]["acMaxTakeOffWeightKg"];
				elemMinTOMassKg.value = airlineAircraftsArray[index]["acMinTakeOffWeightKg"];
				elemMaxTOMassKg.value = airlineAircraftsArray[index]["acMaxTakeOffWeightKg"];
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

	populateAirlineRoutesFlightProfileSelector( airlineRoutesArray ) {
	
		// trComputeFlightProfileId
		$("#trComputeFlightProfileId").show();
		// routesSelectionId
		$("#routesSelectionId").show();
		
		// empty the selector
		$('#airlineRouteId').empty()

		for (let index = 0; index < airlineRoutesArray.length; index++) {
			let airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
			let airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
			$('#airlineRouteId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
		}
	}

	loadOneFlightProfileWayPoint( layerWayPoints, waypoint ) {
	
		let longitude = parseFloat(waypoint.Longitude);
		let latitude = parseFloat(waypoint.Latitude);
		let name = waypoint.name;
		
		layerWayPoints.add(new og.Entity({
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
						width: 16,
						height: 16,
						offset: [0, -2]
						}
		}));
	}

	loadFlightProfileWayPoints( layerWayPoints, dataJson) {
	
		// get all waypoints
		let waypoints = eval(dataJson['waypoints']);

		// add the waypoints
		for (let wayPointId = 0; wayPointId < waypoints.length; wayPointId++ ) {
			// insert one waypoint
			SingletonProfileCosts.getInstance().loadOneFlightProfileWayPoint( layerWayPoints, waypoints[wayPointId] );
		}
	}

	loadFlightProfileOneAirport( layerAirports, airport ) {
	
		let longitude = parseFloat(airport.Longitude);
		let latitude = parseFloat(airport.Latitude);
		let name = airport.AirportName;
		
		layerAirports.add(new og.Entity({
				lonlat: [longitude, latitude],
				label: {
						text: name,
						outline: 0.77,
						outlineColor: "rgba(255,255,255,.4)",
						size: 12,
						color: "black",
						offset: [10, -2]
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
	
		let ellipsoid = new og.Ellipsoid(6378137.0, 6356752.3142);
		
		let latitude = parseFloat(placeMark["latitude"])
		let longitude = parseFloat(placeMark["longitude"])
		let height = parseFloat(placeMark["height"])
		
		let lonlat = new og.LonLat(longitude, latitude , 0.);
		//coordinate above Bochum to allow a upwards direction of ray
		let lonlatAir = new og.LonLat(longitude, latitude , height);
		
		//coordinates of Bochum in Cartesian
		let cart = ellipsoid.lonLatToCartesian(lonlat);
		let cartAir = ellipsoid.lonLatToCartesian(lonlatAir);
		
		if ( placeMark["name"].length > 0 ) {
			let offset = [10, 10]
			if ( placeMark["name"].includes("turn") || placeMark["name"].includes("climb") || placeMark["name"].includes("touch") ) {
				offset = [10, -20]
			} 
			// alternate place
			if ( placeMark["name"].includes("ground") || placeMark["name"].includes("slope") || placeMark["name"].includes("takeOff") ) {
				offset = [10, +20]
			}
			
			rayLayer.add(new og.Entity({
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
		
		rayLayer.add ( new og.Entity({
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
		removeLayer( globus , finalLayerName );
		
		let layerKML = new og.layer.KML( finalLayerName , {
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

	deleteCreateRayLayer(globus , layerName ) {
	
		let finalLayerName = "Rays-" + layerName;
		removeLayer( globus , finalLayerName );

		//polygonOffsetUnits is needed to hide rays behind globe
		let rayLayer = new og.layer.Vector( finalLayerName , { polygonOffsetUnits: 0 });
		rayLayer.addTo(globus.planet);
		return rayLayer;
	}


	displayD3LineChart( arrayAltitudeMSLtime ) {
	
		let verticalProfile = new VerticalProfile();
		verticalProfile.displayVerticalProfile (arrayAltitudeMSLtime);
		
	}

	populateAirlineRunWaysFlightProfileSelector( airlineRunWaysArray ) {
	
		$("#tableFlightProfileId").show();
		$("#trComputeFlightProfileId").show();
		
		// empty the selector
		$('#airlineDepartureRunWayFlightProfileId').empty()
		
		for ( let index = 0 ; index < airlineRunWaysArray.length ; index++) {
			
			let route = $("#airlineRouteId option:selected").val();
			
			//console.log(route)
			//console.log( airlineRunWaysArray[index]["airlineAirport"] )
			
			if ( route.split("-")[0] == airlineRunWaysArray[index]["airlineAirport"]) {
				
				//console.log( "runway -> " + airlineRunWaysArray[index]["airlineRunWayName"] + " ---> for airport -> " + airlineRunWaysArray[index]["airlineAirport"] )
			
				let airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"]
				let airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading"
				$('#airlineDepartureRunWayFlightProfileId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
			}
		}
		
		// empty the selector
		$('#airlineArrivalRunWayFlightProfileId').empty()
		
		for ( let index = 0 ; index < airlineRunWaysArray.length ; index++) {
			
			let route = $("#airlineRouteId option:selected").val();
			
			//console.log(route)
			//console.log( airlineRunWaysArray[index]["airlineAirport"] )
			
			if ( route.split("-")[1] == airlineRunWaysArray[index]["airlineAirport"]) {
				
				//console.log( "runway -> " + airlineRunWaysArray[index]["airlineRunWayName"] + " ---> for airport -> " + airlineRunWaysArray[index]["airlineAirport"] )

				let airlineRunWayKey = airlineRunWaysArray[index]["airlineRunWayName"]
				let airlineRunWayName = airlineRunWaysArray[index]["airlineRunWayName"] + " -> " + airlineRunWaysArray[index]["airlineRunWayTrueHeadindDegrees"] + " degrees True Heading"
				$('#airlineArrivalRunWayFlightProfileId').append('<option value="' + airlineRunWayKey + '">' + airlineRunWayName + '</option>');
			}
		}
	}

	hideFlightProfileDiv() {
	
		if ( $('#flightProfileMainDivId').is(":visible") ) {
			
			$("#flightProfileMainDivId").hide();
			
			//document.getElementById("btnLaunchFlightProfile").disabled = true
			document.getElementById("btnLaunchFlightProfile").innerText = "Profile";
			//document.getElementById("btnLaunchFlightProfile").style.backgroundColor = "yellow";
			
		}
	}

	launchFlightProfile(globus) {
	
		this.globus = globus ;
		globus.planet.events.on("layeradd", function (e) {
			
			//console.log("layeradd event");
			if (e.pickingObject instanceof og.Layer) {
				console.log(e.pickingObject.name);
			}
			stopBusyAnimation();
		});
		
		//console.log( "compute flight profile ");
		
		/**
		let layerFlightProfileWayPoints = new og.layer.Vector("FlightProfileWayPoints", {
				billboard: { 
					src: '/static/trajectory/images/marker.png', 
					color: '#6689db' ,
					width : 4,
					height : 4
					},
				clampToGround: true,
				});
		layerFlightProfileWayPoints.addTo(globus.planet);
		*/
		
		// listen to change to the aircraft Mass
		document.getElementById("TakeOffMassKgId").addEventListener('change', function (evt) {
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
		document.getElementById("requestedFlightLevelId").addEventListener('change', function (evt) {
			let elemFL = document.getElementById('requestedFlightLevelId');
			let FLvalue = elemFL.value;
			//console.log(elemFL.value);
			let elemMaxFL = document.getElementById('maxFlightLevelId');
			
				if ( ! Number.isInteger(+(FLvalue)) ) {
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
		
				
		// listen to select route change
		$( "#airlineRouteId" ).change(function() {
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			//console.log( "Handler for airlineRouteId selection change called." );
			$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName,
						async : true,
						success: function(data, status) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);
							// airlineAircrafts
							SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] );
							
							$("#btnLaunchCosts").show();
							
						},
						error: function(data, status) {
							stopBusyAnimation();
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage( "Error - Launch Flight Profile" , eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false
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
				
				// define in the main.js
				hideAllDiv(globus);
				
				$('#flightProfileMainDivId').show();
				
				// change name on the button
				document.getElementById("btnLaunchFlightProfile").innerText = "Profile";
				//document.getElementById("btnLaunchFlightProfile").style.backgroundColor = "green";
				
				// get the name of the airline
				let airlineName = $("#airlineSelectId option:selected").val();
				airlineName = encodeURIComponent(airlineName);

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "trajectory/launchFlightProfile/" + airlineName,
						async : true,
						success: function(data, status) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);
							// airlineAircrafts
							SingletonProfileCosts.getInstance().populateAircraftFlightProfileSelector( dataJson["airlineAircrafts"] );
							SingletonProfileCosts.getInstance().populateAirlineRoutesFlightProfileSelector( dataJson["airlineRoutes"] );
							SingletonProfileCosts.getInstance().populateAirlineRunWaysFlightProfileSelector( dataJson["airlineRunWays"] );

							$("#launchComputeId").show();
							
						},
						error: function(data, status) {
							console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
							showMessage("Error - launch Flight Profile", eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnLaunchFlightProfile").disabled = false;
						},
				});
			} else {

				//document.getElementById("btnLaunchFlightProfile").disabled = true
				document.getElementById("btnLaunchFlightProfile").innerText = "Profile";
				//document.getElementById("btnLaunchFlightProfile").style.backgroundColor = "yellow";

				$('#flightProfileMainDivId').hide();
			}
		} 
		
		/**
		* Monitor the change of Aircraft
		**/
		document.getElementById("airlineAircraftId").onchange = function () {
			
			console.log ("select aircraft changed");
			let aircraftICAOcode = $("#airlineAircraftId option:selected").val();
			console.log(aircraftICAOcode);
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);
			
			// init progress bar.
			initProgressBar();
			initWorker();
			
			$.ajax({
						method: 'get',
						url :  "trajectory/getAircraft/" + airlineName,
						async : true,
						data: 'aircraft=' + aircraftICAOcode,
						success: function(data, status) {
							
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
		* monitor the button used to launch the profile computation
		**/
		let once = false;
		//document.getElementById("btnComputeFlightProfileId").disabled = true
		document.getElementById("btnComputeFlightProfileId").onclick = function () {
		
			//console.log ("button compte flight profile pressed");
		
			document.getElementById("btnComputeFlightProfileId").disabled = true
			
			let aircraft = $("#airlineAircraftId option:selected").val();
			let route =  $("#airlineRouteId option:selected").val();
			
			let departureRunWay = $("#airlineDepartureRunWayFlightProfileId option:selected").val();
			let arrivalRunWay = $("#airlineArrivalRunWayFlightProfileId option:selected").val();
			
			let elemTOMassKg = document.getElementById('TakeOffMassKgId');
			let elemFL = document.getElementById('requestedFlightLevelId');
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);
			
			let data = 'aircraft=' + aircraft
			data += '&route=' + route
			data += '&AdepRwy=' + departureRunWay
			data += '&AdesRwy=' + arrivalRunWay
			data += '&mass=' + elemTOMassKg.value;
			data += '&fl=' + elemFL.value;
			// init progress bar.
			initProgressBar();
			initWorker();
			
			$.ajax({
						method:  'get',
						url   :  "trajectory/computeFlightProfile/" + airlineName,
						async :  true,
						data  :  data ,
						success: function(data, status) {
							
							let dataJson = eval(data);
							if ( dataJson.hasOwnProperty("errors") ) {
								stopBusyAnimation();
								showMessage( "Error" , dataJson["errors"] );
								
							} else {
								// create layers does also a delete layer if name found
								let layerKML = SingletonProfileCosts.getInstance().deleteCreateKMLLayer(globus , route);
								let rayLayer = SingletonProfileCosts.getInstance().deleteCreateRayLayer(globus , route);
								
								// convert JSON to XML
								let x2js = new X2JS();
								let xml = x2js.js2xml(dataJson["kmlXMLjson"]);
								
								let parser = new DOMParser();
								let xmlDoc = parser.parseFromString(xml, "text/xml");
								
								layerKML.addKmlFromXml(  xmlDoc ,  null ,  null );
								
								// add rays to Rays layer
								SingletonProfileCosts.getInstance().addRays( rayLayer , dataJson["placeMarks"] );
								
								let arrayAltitudeMSLtime = dataJson["csvAltitudeMSLtime"];
								SingletonProfileCosts.getInstance().displayD3LineChart(arrayAltitudeMSLtime);
								
								showMessage("Information" , "Double Click in the vertical profile to return to the map") 
								
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
	}
}