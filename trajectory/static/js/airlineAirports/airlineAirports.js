
import { initProgressBar , initWorker , stopBusyAnimation } from "../main/main.js";
import { SingletonMainClass } from "../main/mainSingletonClass.js";
import { Vector , Entity } from "../og/og.es.js";

export const SingletonAirlineAirports = (function () {
	
	let instance;
    function createInstance() {
        let object = new AirlineAirports();
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


export function showRoute( elem ) {
	
	let globus = SingletonAirlineAirports.getInstance().getGlobus();
	
	let layerName = elem.id ;
	let layer = globus.planet.getLayerByName( layerName );
	if (layer) {
		// layer is existing
		if (layer.getVisibility() == true) {
			layer.setVisibility( false );
		} else {
			layer.setVisibility( true );
		}	
	} else {
		// load a route
		//console.log( " layer " + layerName + " is not existing");
		SingletonAirlineAirports.getInstance().queryAirlineRouteWayPoints ( elem.id );
	}
	return false;
}


class AirlineAirports {
	
	constructor() {
		/**
		 * @todo warning this is the same prefix as in airlineRoutes
		 * @todo move this prefix in mainClass.
		 */
		this.LayerNamePrefix = "WayPoints-";
	}
	
	getGlobus() {
		return this.globus;
	}
	
	hideLayer( routeId ) {
		
		let globus = this.globus;
		
		let arr = routeId.split("-");
		if ( Array.isArray(arr) && (arr.length>1)){
			
			let Adep = arr[1];
			//console.log(Adep);
			let Ades = arr[2];
			//console.log(Ades);
				
			let layerName =  this.LayerNamePrefix + Adep + "-" + Ades;
			let layer = globus.planet.getLayerByName( layerName );
			if (layer && (layer.getVisibility() ==  true)) {
				layer.setVisibility( false );
			}
		}
	}
	
	/**
	 * @todo - same function as in airlineairports
	 */
	loadOneRouteWayPoint( layerRouteWayPoints, waypoint ) {
	
		let longitude = 0.0;
		if ( waypoint.hasOwnProperty("Longitude")) {
			longitude = parseFloat(waypoint.Longitude);
		}
		let latitude = 0.0;
		if ( waypoint.hasOwnProperty("Latitude")) {
			latitude = parseFloat(waypoint.Latitude);
		}
		let name = "";
		if ( waypoint.hasOwnProperty("name")) {
			name = waypoint.name;
		}
		
		layerRouteWayPoints.add(new Entity({
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
	
	showRouteWayPoints( airlineRoutesWaypointsArray , layerName ) {
		
		let globus = this.globus;
	
		//console.log("start loading route WayPoints");
		let layerRouteWayPoints = new Vector( layerName , {
				billboard: { 
					src: '/static/trajectory/images/marker.png', 
					color: '#6689db' ,
					width : 4,
					height : 4
					},
				clampToGround: true,
				});
		layerRouteWayPoints.addTo(globus.planet);

		// add the waypoints
		for (let wayPointId = 0; wayPointId < airlineRoutesWaypointsArray.length; wayPointId++ ) {
			// insert one waypoint
			SingletonAirlineAirports.getInstance().loadOneRouteWayPoint( layerRouteWayPoints, airlineRoutesWaypointsArray[wayPointId] );
		}
		// set viewport extent
		SingletonMainClass.getInstance().setExtent( airlineRoutesWaypointsArray );
	}
	
	writeRoutesTableFromToAirport(  departureAirportICAOcode , airlineRoutesArray , position ) {
		
		// modify the div position
		// Update the position of `#div` dynamically
		$('#airlineAirportsRoutesMainDivId').css({
			'position': 'absolute',
			'top': position["y"] - 20, // Leave some margin
			'left': position["x"] - 20 , // Leave some margin
			'display': 'block'
		});
		
		$('#airlineAirportsRoutesMainDivId tbody').empty();
		for (let airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
			// insert one route
			
			let oneAirlineRoute = airlineRoutesArray[airlineRouteId];
			// 25th June 2023 show arrival and departing routs / flight legs
			if ( ( oneAirlineRoute["DepartureAirportICAOCode"] == departureAirportICAOcode ) || 
				 ( oneAirlineRoute["ArrivalAirportICAOCode"]   == departureAirportICAOcode ) ) {
				
				let id = oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"];
				
				// Warning - in the hyperlink TD, the id must start with the name of the layer prefix
				$("#airlineAirportsRoutesMainDivId").find('tbody')
					.append($('<tr>')
						.append($('<td>')
							.append( oneAirlineRoute["Airline"] )
						)
					);
				// arrow to show direction of the flight
				if ( oneAirlineRoute["DepartureAirportICAOCode"] == departureAirportICAOcode ) {
					$("#airlineAirportsRoutesMainDivId").find('tbody').find("tr").last()
							.append($('<td>')
								.append( '<span class="arrow-right" ></span>')
							)
				} else {
					$("#airlineAirportsRoutesMainDivId").find('tbody').find("tr").last()
							.append($('<td>')
								.append( '<span class="arrow-left" ></span>')
							)
				}
					
				$("#airlineAirportsRoutesMainDivId").find('tbody').find("tr").last()
					.append($('<td>')
							.append( '<span> <a id="' + this.LayerNamePrefix + id + '" href="#" onclick="showRoute(this);" >show / hide route</a> </span>'  )
					)
					.append($('<td>')
							.append( oneAirlineRoute["DepartureAirport"] )
					)
					.append($('<td>')
							.append( oneAirlineRoute["DepartureAirportICAOCode"] )
					)
					.append($('<td>')
							.append( oneAirlineRoute["ArrivalAirport"] )
					)
					.append($('<td>')
							.append( oneAirlineRoute["ArrivalAirportICAOCode"] )
					)
			}
		}
	}
	
	// query the server to retrieve the waypoints of the route
	queryAirlineRouteWayPoints( id ) {
		
		let LayerNamePrefix = this.LayerNamePrefix;
	
		let arr = id.split("-");
		let Adep = arr[1];
		let Ades = arr[2];
		
		$.ajax( {
				method: 'get',
				url :  "airline/wayPointsRoute/" + Adep +"/" + Ades,
				async : true,
				success: function(data) {
											
						//alert("Data: " + data + "\nStatus: " + status);
						let dataJson = eval(data);		
						if ( dataJson.hasOwnProperty("airlineRouteWayPoints")) {
							
							let airlineRoutesWaypointsArray = dataJson["airlineRouteWayPoints"];
							let layerName =  LayerNamePrefix + Adep + "-" + Ades;
							//console.log( layerName );
							SingletonAirlineAirports.getInstance().showRouteWayPoints( airlineRoutesWaypointsArray , layerName );
						}
				},
				error: function(data, status) {
					console.log("Error - show Airline Routes : " + status + " Please contact your admin");
					showMessage("Error - Airline Routes", data)
				},
				complete : function() {
					stopBusyAnimation();
					document.getElementById("btnAirlineRoutes").disabled = false
				},
		});
	}
	
	queryRoutesStartingFromAirport ( departureAirportICAOcode , position ) {
		
		// get the name of the airline
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
		
		$.ajax( {
				method: 'get',
				url :  "airline/airlineRoutes/" + airlineName,
				async : true,
				success: function(data) {
								
					//alert("Data: " + data + "\nStatus: " + status);
					let dataJson = eval(data);		
					if ( dataJson.hasOwnProperty("airlineRoutes")) {
						
						let airlineRoutesArray = dataJson["airlineRoutes"]
						SingletonAirlineAirports.getInstance().writeRoutesTableFromToAirport( departureAirportICAOcode, airlineRoutesArray , position );
					}
				},
				error: function(data, status) {
					console.error("Error - show Airline Routes : " + status + " Please contact your admin");
					showMessage("Error - Airline Routes" , data)
				},
				complete : function() {
					stopBusyAnimation();
					document.getElementById("btnAirlineRoutes").disabled = false
				},
		});
	}

	loadOneAirport( airport , showHide ) {
		
		let globus = this.globus;
	
		// get the name of the airline
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

		// need to prefix an airport ICAO code with the airline name 
		// as the same airport might be used by several airlines
		let layerName = airlineName + "-" + airport.AirportICAOcode;
		//console.log( layerName ) ;
		
		let layer = globus.planet.getLayerByName( layerName );
		if (! layer) {
			// layer is not existing
			
			let layerAirport = new Vector(layerName , { clampToGround: true, 	});
			layerAirport.addTo(globus.planet);
			
			let longitude = parseFloat(airport.Longitude);
			let latitude = parseFloat(airport.Latitude);
			let name = airport.AirportName;
			
			layerAirport.add(new Entity({
					lonlat : [longitude, latitude],
					label : SingletonMainClass.getInstance().getStandardOgLabel(name),
					billboard : {
							src: "/static/images/plane.png",
							width: 16,
							height: 16,
							offset: [0, -10]
							}
			}));
			
			layerAirport.events.on("rclick", function (e) {
				//console.log("right click - layer name = " + this.name);
				//console.log("right click - airport name = " + e.pickingObject.label._text);
				
				let position = {}
				position["x"] = e.clientX;
				position["y"] = e.clientY;
				
				// show table with routes starting in this airport
				$("#airlineAirportsRoutesMainDivId").show();
				
				let airportICAOcode = this.name.split("-")[1];
				SingletonAirlineAirports.getInstance().queryRoutesStartingFromAirport( airportICAOcode, position );

			});
			// show airport ICAO code
			layerAirport.events.on("mouseenter", function (e) {
				e.renderer.handler.canvas.style.cursor = "pointer";
				// show ICAO code of the airport
				e.renderer.handler.canvas.title = this.name.split("-")[1];
			});
			// hide airports routes div
			layerAirport.events.on("mouseleave", function (e) {
				e.renderer.handler.canvas.style.cursor = "default";
				e.renderer.handler.canvas.title = "";
				// hide table with routes starting in this airport
				$("#airlineAirportsRoutesMainDivId").hide();
			});
			
		} else {
			// no need to create the layer
			layer.setVisibility(showHide);
		}
	}

	loadAirports( dataJson , showHide ) {
	
		// get all airports
		let airports = eval(dataJson['airports']);

		// add the reservations
		for (let airportId = 0; airportId < airports.length; airportId++ ) {
			// insert one airport
			SingletonAirlineAirports.getInstance().loadOneAirport( airports[airportId] , showHide );
		}
	}

	showHideAllAirports( showHide ) {
			
		// init progress bar.
		initProgressBar();
		initWorker();
		
		// get the name of the airline
		let airlineName = SingletonMainClass.getInstance().getSelectedAirline();

		$.ajax( {
				method: 'get',
				url :  "trajectory/airports/" + airlineName,
				async : true,
				success: function(data) {
					stopBusyAnimation();
					//alert("Data: " + data + "\nStatus: " + status);
					let dataJson = eval(data);
					
					SingletonAirlineAirports.getInstance().loadAirports( dataJson , showHide );	
				},
				error: function(data, status) {
					stopBusyAnimation();
					console.log("Error - show Airports : " + status + " Please contact your admin");
					showMessage ( "Error - show Airports" , data );
				},
				complete : function() {
					stopBusyAnimation();
					SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
				}
		} );
	}

	initAirports(globus) {
	
		// 9th May 2023 - class attributes
		this.globus = globus;
		
		let show = true;
			
		if ( !document.getElementById("btnAirports") ) {
			console.error("bouton Airports is not declared");
			return;
		}
		document.getElementById("btnAirports").onclick = function () {
				
			if (show) {
				show = false;
				document.getElementById("btnAirports").innerText = "Airports";					
				SingletonAirlineAirports.getInstance().showHideAllAirports( true );
				
			} else {
				show = true;
				document.getElementById("btnAirports").innerText = "Airports";
				SingletonAirlineAirports.getInstance().showHideAllAirports( false );
			}
		};
	}
}
