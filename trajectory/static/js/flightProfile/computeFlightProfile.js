
document.addEventListener('DOMContentLoaded', (event) => { 
       
	console.log("compute flight profile js is loaded");
	 
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	$("#launchComputeId").hide();

}); 

function populateAircraftSelector( airlineAircraftsArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeFlightProfileId").show();
	// aircraftSelectionId
	$("#aircraftSelectionId").show();

	for (var index = 0; index < airlineAircraftsArray.length; index++) {
      $('#airlineAircraftId').append('<option value="' + airlineAircraftsArray[index]["airlineAircraftICAOcode"] + '">' + airlineAircraftsArray[index]["airlineAircraftFullName"] + '</option>');
	}
}

function populateAirlineRoutesSelector( airlineRoutesArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeFlightProfileId").show();
	// routesSelectionId
	$("#routesSelectionId").show();

	for (var index = 0; index < airlineRoutesArray.length; index++) {
		var airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
		var airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
		$('#airlineRouteId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
	}
}

function loadOneFlightProfileWayPoint( layerWayPoints, waypoint ) {
	
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

function loadFlightProfileWayPoints( layerWayPoints, dataJson) {
	
	// get all waypoints
	var waypoints = eval(dataJson['waypoints']);

	// add the waypoints
	for (var wayPointId = 0; wayPointId < waypoints.length; wayPointId++ ) {
		// insert one waypoint
		loadOneFlightProfileWayPoint( layerWayPoints, waypoints[wayPointId] );
	}
}

function loadFlightProfileOneAirport( layerAirports, airport ) {
	
	let longitude = parseFloat(airport.Longitude);
	var latitude = parseFloat(airport.Latitude);
	var name = airport.AirportName;
	
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

function loadOneRay( rayLayer, placeMark ) {
	
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
		if ( placeMark["name"].startsWith("turn") || placeMark["name"].startsWith("ground-run") 
			|| placeMark["name"].startsWith("climb-ramp") ) {
			offset = [10, -20]
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

function addRays ( rayLayer , placeMarks ) {
	
	// add the waypoints
	for (var placeMarkId = 0; placeMarkId < placeMarks.length; placeMarkId++ ) {
		// insert one waypoint
		loadOneRay( rayLayer, placeMarks[placeMarkId] );
	}
}

function launchFlightProfile(globus) {
	
	console.log( "compute flight profile ");
	
	let layerKML = new og.layer.KML( "FlightProfile" , {
		billboard: { 
			src: '/static/images/move_down_icon.png', 
			color: '#6689db' ,
			width : 4,
			height : 4
			},
		color: '#6689db'
	} ) ;
	layerKML.addTo(globus.planet);
	
	//polygonOffsetUnits is needed to hide rays behind globe
	let rayLayer = new og.layer.Vector("rays", { polygonOffsetUnits: 0 });
	rayLayer.addTo(globus.planet);
	
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
	    
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	
	let show = true;
	document.getElementById("btnLaunchFlightProfile").onclick = function () {

		if (show) {
			show = false;
			document.getElementById("btnLaunchFlightProfile").disabled = true

			// use ajax to get the data 
			$.ajax( {
					method: 'get',
					url :  "trajectory/launchFlightProfile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						// airlineAircrafts
						populateAircraftSelector( dataJson["airlineAircrafts"] );
						populateAirlineRoutesSelector( dataJson["airlineRoutes"] );
						
						$("#launchComputeId").show();
						
					},
					error: function(data, status) {
						console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnLaunchFlightProfile").disabled = false
					},
			});
		} 
	} 
	
	//document.getElementById("btnComputeFlightProfile").disabled = true
	document.getElementById("btnComputeFlightProfile").onclick = function () {
	
		console.log ("button compte flight profile pressed");
	
		document.getElementById("btnComputeFlightProfile").disabled = true
		let aircraft = $("#airlineAircraftId option:selected").val()
		let route =  $("#airlineRouteId option:selected").val()
		$.ajax( {
					method: 'get',
					url :  "trajectory/computeFlightProfile",
					async : true,
					data: 'aircraft=' + aircraft + '&route=' + route ,
					success: function(data, status) {
						
						var dataJson = eval(data);
						console.log( dataJson["kmlURL"] );
						layerKML.addKmlFromUrl( url = dataJson["kmlURL"] );
						addRays( rayLayer , dataJson["placeMarks"] );
						setTimeout(
							function(){ 
								stopWorker(); 
							}
						, 10000);
						
						/*
						let entities = layerFlightProfileWayPoints.getEntities();
						if ( Array.isArray(entities) && ( entities.length > 0 ) ) {
							layerFlightProfileWayPoints.removeEntities(entities) 
						}
						
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						loadFlightProfileWayPoints(layerFlightProfileWayPoints, dataJson)
						
						// load departure airport
						loadFlightProfileOneAirport( layerFlightProfileWayPoints, dataJson["departureAirport"] )
						loadFlightProfileOneAirport( layerFlightProfileWayPoints, dataJson["arrivalAirport"] )
						
						*/
						
					},
					error: function(data, status) {
						console.log("Error - compute Flight Profile: " + status + " Please contact your admin");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnComputeFlightProfile").disabled = false
					},
			});
	}
}