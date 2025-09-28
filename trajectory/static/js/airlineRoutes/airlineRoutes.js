
import { SingletonMainClass } from "../main/mainSingletonClass.js";
import { SingletonSidStar } from "../SidStar/SidStar.js";
import { stopBusyAnimation , showMessage } from "../main/main.js";
import { Entity , Vector } from "../og/og.es.js";

export const SingletonAirlineRoutes = (function () {
	
	let instance;
    function createInstance() {
        var object = new AirlineRoutes();
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

/**
 * same function used to show or hide a Sid Star
 */
export function showHideSidStarRoute( elem ) {
	
	let globus = SingletonAirlineRoutes.getInstance().getGlobus();
	
	let layerName = elem.id ;
	layerName = layerName.replaceAll("/", "-");
	let layer = globus.planet.getLayerByName( layerName );
	if (layer) {
		if (layer.getVisibility() == false) {
			layer.setVisibility(true);
			try {
				// load a SID STAR from backend
				SingletonSidStar.getInstance().queryServer ( elem.name );
			} catch (err) {
				console.error( JSON.stringify(err));
			}
		} else {
			SingletonSidStar.getInstance().hideLayer(layerName);
		}
	} else {
		// load a Sid Star route
		try {
			// load a SID STAR from backend
			SingletonSidStar.getInstance().queryServer ( elem.name );
		} catch (err) {
			console.error( JSON.stringify(err));
		}
	}
	return false;
}


class AirlineRoutes {
	
	constructor( ) {
		//console.log("Airline Routes constructor");
		/**
		 * @todo this is the same prefix as in the AirlineAirports constructor
		 * */
		this.LayerNamePrefix = "WayPoints-";
		this.LayerSidPrefix = "Sid-";
		this.LayerStarPrefix = "Star-";
		this.LayerWayPoints = {};
	}
	
	getGlobus() {
		return this.globus;
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
		// add the waypoint
		layerRouteWayPoints.add(new Entity({
				lonlat: [longitude, latitude],
				label: SingletonMainClass.getInstance().getStandardOgLabel(name),
				billboard: {
						src: "/static/images/marker.png",
						width: 12,
						height: 12,
						offset: [0, -2]
						}
		}));
	}

	loadRouteWayPoints(  airlineRoutesWaypointsArray , layerName ) {
		
		let globus = this.globus;
		let layerRouteWayPoints = new Vector( layerName , {
				billboard: { 
					src: '/static/trajectory/images/marker.png', 
					color: '#6689db' ,
					width : 4,
					height : 4
					},
				clampToGround: true,
				});
		layerRouteWayPoints.addTo( globus.planet );

		// add the waypoints
		for (let wayPointId = 0; wayPointId < airlineRoutesWaypointsArray.length; wayPointId++ ) {
			// insert one waypoint
			SingletonAirlineRoutes.getInstance().loadOneRouteWayPoint( layerRouteWayPoints, airlineRoutesWaypointsArray[wayPointId] );
		}
		SingletonMainClass.getInstance().setExtent(airlineRoutesWaypointsArray);
		// 22nd July 2023 - store the wayPoints array
		this.LayerWayPoints[layerName] = airlineRoutesWaypointsArray;
	}
	
	// write in the table the best departure runway and the best arrival runway
	loadBestRunway( Adep, Ades, isAdep, AdepAdesRunWay ) {
		
		if (isAdep) {
			let elemTdAdepRwy = document.getElementById('tdAdepRwyId-'+Adep+'-'+Ades);
			elemTdAdepRwy.innerHTML = AdepAdesRunWay;
		} else {
			let elemTdAdesRwy = document.getElementById('tdAdesRwyId-'+Adep+'-'+Ades);
			elemTdAdesRwy.innerHTML = AdepAdesRunWay;
		}
	}

	// query the server to retrieve the waypoints of the route
	loadOneAirlineRoute( id ) {
		
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
						if ( dataJson.hasOwnProperty("errors") ) {
							
							showMessage("Error - Airline Routes", data)
							
						} else {
							
							let airlineRoutesWaypointsArray = dataJson["airlineRouteWayPoints"];
							let layerName =  LayerNamePrefix + Adep + "-" + Ades;
							SingletonAirlineRoutes.getInstance().loadRouteWayPoints( airlineRoutesWaypointsArray , layerName );
									
							// 3rd April 2023 - add best runways
							if ( dataJson.hasOwnProperty("bestAdepRunway")) {
								
								let AdepRunWay = dataJson["bestAdepRunway"];
								// true means Adep and false means Ades
								SingletonAirlineRoutes.getInstance().loadBestRunway( Adep , Ades , true, AdepRunWay);
							}
							if ( dataJson.hasOwnProperty("bestAdesRunway")) {
							
								let AdesRunWay = dataJson["bestAdesRunway"];
								// true means Adep and false means Ades
								SingletonAirlineRoutes.getInstance().loadBestRunway( Adep , Ades , false, AdesRunWay);
							}
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

	showHideWayPoints( domElement ) {
	
		let id = domElement.id ;
		//console.log( id );
		let arr = id.split("-");
		if ( Array.isArray(arr) && (arr.length>1)) {

			let Adep = arr[1];
			//console.log(Adep)
			let Ades = arr[2];
			//console.log(Ades)
				
			let layerName =  this.LayerNamePrefix + Adep + "-" + Ades;
			let globus = this.globus;
			let layer = globus.planet.getLayerByName( layerName );
			if (layer) {
				// layer is existing
				if (layer.getVisibility() ==  true) {
					document.getElementById(id).value = "Show";
					layer.setVisibility( false );
				} else {
					document.getElementById(id).value = "Hide";
					layer.setVisibility( true );
					if ( this.LayerWayPoints.hasOwnProperty(layerName)) {
						let wayPointsArray = this.LayerWayPoints[layerName];
						if ( wayPointsArray ) {
							SingletonMainClass.getInstance().setExtent( wayPointsArray );
						}
					}
				}
			} else {
				//console.log(id)
				document.getElementById(id).value = "Hide";
				SingletonAirlineRoutes.getInstance().loadOneAirlineRoute( id );
			}
		}
	}
	
	configureRoutesWayPointsButton( oneAirlineRoute ) {
		
		let globus = this.globus;
		
		let elemTdAdepRwy = document.getElementById('tdAdepRwyId');
		elemTdAdepRwy.id = "tdAdepRwyId-"+oneAirlineRoute["DepartureAirportICAOCode"]+ "-" +oneAirlineRoute["ArrivalAirportICAOCode"];
		
		let elemTdAdesRwy = document.getElementById('tdAdesRwyId');
		elemTdAdesRwy.id = "tdAdesRwyId-"+oneAirlineRoute["DepartureAirportICAOCode"]+ "-" +oneAirlineRoute["ArrivalAirportICAOCode"];
	
		let elemTd = document.getElementById('tdButtonId');
		elemTd.id = "tdButtonId-"+oneAirlineRoute["DepartureAirportICAOCode"]+ "-" +oneAirlineRoute["ArrivalAirportICAOCode"];
		
		let elemButton = document.getElementById('buttonRouteId');
		elemButton.id = "buttonRouteId-"+oneAirlineRoute["DepartureAirportICAOCode"]+ "-" +oneAirlineRoute["ArrivalAirportICAOCode"];
		
		let layerName = this.LayerNamePrefix + oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"];
		let layer = globus.planet.getLayerByName( layerName );
		if (layer) {
			// layer is existing
			if (layer.getVisibility() == false) {
				document.getElementById(elemButton.id).value = "Hide";
				layer.setVisibility( true );
			} else {
				document.getElementById(elemButton.id).value = "Show";
				layer.setVisibility( false );
			}
		}
		/**
		* on click function 
		*/
		$('#'+elemButton.id).click(function () {
			//console.log("button show route clicked") 
			SingletonAirlineRoutes.getInstance().showHideWayPoints( this );
		});
		
	}
	
	configureSidStarLink( oneAirlineRoute ) {
		// correct the SID Id on the fly
		if ( oneAirlineRoute["SID"] && (oneAirlineRoute["SID"].length > 0 )) {
			let elemTdSid = document.getElementById( 'tdSidId-' + oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"] );
		
			elemTdSid.id = "tdSidId-" + oneAirlineRoute["SID"];
			let idSidName = this.LayerSidPrefix +  oneAirlineRoute["SID"];
			let idSidId = idSidName.replaceAll("/","-");
			elemTdSid.innerHTML = '<span> <a name="' + idSidName + '" id="' +  idSidId + '" href="#" >' + oneAirlineRoute["SID"] + '</a> </span>'  
			elemTdSid.title = "click me";
			// onclick
			$('#'+idSidId).click(function () {
				//console.log("link SID clicked") 
				showHideSidStarRoute( this );
			});
		}
		// correct the STAR Id on the fly
		if ( oneAirlineRoute["STAR"] && (oneAirlineRoute["STAR"].length > 0 )) {
			let elemTdStar = document.getElementById( 'tdStarId-' + oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"] );
		
			elemTdStar.id = "tdStarId-" + oneAirlineRoute["STAR"];
			let idStarName = this.LayerStarPrefix +  oneAirlineRoute["STAR"];
			let idStarId = idStarName.replaceAll("/","-");
			elemTdStar.innerHTML = '<span> <a name="' + idStarName + '" id="' +  idStarId + '" href="#"  >' + oneAirlineRoute["STAR"] + '</a> </span>'  
			elemTdStar.title = "click me";
			// onclick
			$('#'+idStarId).click(function () {
				//console.log("link STAR clicked") 
				showHideSidStarRoute( this );
			});
		}
		// onclick
		
		
		
	}
	

	// April 2023 - add best runway
	// 11th June 2023 add SID and STAR
	addOneAirlineRoute( oneAirlineRoute ) {
		
		let sidId = oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"] ;
		let starId = oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"] ;
		
		$("#airlineRoutesTableId").find('tbody')
		.append($('<tr>')
			.append($('<td>')
				.append( oneAirlineRoute["Airline"] )
			)
			.append($('<td>')
				.append( oneAirlineRoute["DepartureAirport"] )
			)
			.append($('<td>')
				.append( oneAirlineRoute["DepartureAirportICAOCode"] )
			)
			.append($('<td id="tdSidId-' + sidId + '" >')
				.append( oneAirlineRoute["SID"] )
			)
			.append($('<td id="tdAdepRwyId" >')
				.append( oneAirlineRoute["BestDepartureRunway"] )
			)
			.append($('<td>')
				.append( oneAirlineRoute["ArrivalAirport"] )
			)
			.append($('<td>')
				.append( oneAirlineRoute["ArrivalAirportICAOCode"] )
			)
			.append($('<td id="tdStarId-' + starId + '" >')
				.append( oneAirlineRoute["STAR"] )
			)
			.append($('<td id="tdAdesRwyId" >')
				.append( oneAirlineRoute["BestArrivalRunway"] )
			)
			.append($('<td id="tdButtonId" >')
				.append ( " <input type='button' id='buttonRouteId' style='width:100%; height:100%;' value='Show'  /> " )
			)
		);
		
		SingletonAirlineRoutes.getInstance().configureRoutesWayPointsButton( oneAirlineRoute );
		SingletonAirlineRoutes.getInstance().configureSidStarLink( oneAirlineRoute );
	}

	/**
	* display only the names of the departure and arrival airports
	*/
	addAirlineRoutes( airlineRoutesArray ) {
	
		$('#airlineRoutesTableId tbody').empty();
		for (var airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
			// insert one waypoint
			SingletonAirlineRoutes.getInstance().addOneAirlineRoute( airlineRoutesArray[airlineRouteId] );
		}
	}

	removeOneAirlineRoute ( oneAirlineRoute ) {
	
		let globus = this.globus;
		
		let Adep = oneAirlineRoute["DepartureAirportICAOCode"];
		let Ades = oneAirlineRoute["ArrivalAirportICAOCode"];
		let layerName = this.LayerNamePrefix + Adep + "-" + Ades;
		let layer = globus.planet.getLayerByName( layerName );
		if (layer) {
			if (layer.getVisibility() == false) {
				document.getElementById(elemButton.id).value = "Hide";
				layer.setVisibility( true );
			} else {
				document.getElementById(elemButton.id).value = "Show";
				layer.setVisibility( false );
			}
		}
	}

	removeGlobusRoutesWayPointsLayers( airlineRoutesArray ) {
	
		for (var airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
			SingletonAirlineRoutes.getInstance().removeOneAirlineRoute( airlineRoutesArray[airlineRouteId] );
		}
	}

	hideAirlineRoutesDiv() {
	
		if ( $('#airlineRoutesDivId').is(":visible") ) {
			$("#airlineRoutesDivId").hide();
		}
	}

	initAirlineRoutes(globus) {
	
		this.globus = globus;
		$("#airlineRoutesDivId").hide();

		if ( ! document.getElementById("btnAirlineRoutes") ) {
			return;
		}
		// listen to button
		document.getElementById("btnAirlineRoutes").onclick = function () {
			
			if ( ! $('#airlineRoutesDivId').is(":visible") ) {
								
				$("#airlineRoutesDivId").show();
				
				// disable the button 
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
				
				/**
				 * @todo - encapsulate in the MainSingleton class
				 * get the name of the airline
				 **/ 
				let airlineName = $("#airlineSelectId option:selected").val();
				airlineName = encodeURIComponent(airlineName);

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "airline/airlineRoutes/" + airlineName,
						async : true,
						success: function(data) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);		
							if ( dataJson.hasOwnProperty("airlineRoutes") ) {
								
								let airlineRoutesArray = dataJson["airlineRoutes"];
								SingletonAirlineRoutes.getInstance().addAirlineRoutes(  airlineRoutesArray );
							} else {
								if ( dataJson.hasOwnProperty("errors") ) {
									
									showMessage("Error - Airline Routes" , data);
								}
							}
						},
						error: function(data, status) {
							console.log("Error - show Airline Routes : " + status + " Please contact your admin");
							showMessage("Error - Airline Routes" , data);
						},
						complete : function() {
							stopBusyAnimation();
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);						},
				});

			} else {
				
				$("#airlineRoutesDivId").hide();
			}
		}
	}
}