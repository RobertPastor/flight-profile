

const SingletonAirlineRoutes = (function () {
	
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


function showSidStarRoute( elem ) {
	
	let globus = SingletonAirlineRoutes.getInstance().getGlobus();
	
	let layerName = elem.id ;
	let layer = globus.planet.getLayerByName( layerName );
	if (layer) {
		
		/**
		 * @todo remove Layer is defined in main.js
		 *  */ 
		removeLayer( globus , layerName );
			
	} else {
		// load a Sid Star route
		try {
			// load a SID STAR from backend
			SingletonSidStar.getInstance().queryServer ( elem.id );
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
	}
	
	getGlobus() {
		return this.globus;
	}
	
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
		layerRouteWayPoints.add(new og.Entity({
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

	loadRouteWayPoints(  airlineRoutesWaypointsArray , layerName ) {
		
		let globus = this.globus;
	
		//console.log("start loading route WayPoints");
		let layerRouteWayPoints = new og.layer.Vector( layerName , {
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
		
		let globus = this.globus;
	
		let id = domElement.id ;
		//console.log( id );
		let arr = id.split("-");
		let Adep = arr[1];
		//console.log(Adep)
		let Ades = arr[2];
		//console.log(Ades)
			
		let layerName =  this.LayerNamePrefix + Adep + "-" + Ades;
		let layer = globus.planet.getLayerByName( layerName );
		if (layer) {
			
			document.getElementById(id).value = "Show";
			try {
				/**
				 * @todo remove Layer is defined in main.js
				 *  */ 
				removeLayer( globus , layerName );
			
			} catch (err) {
				console.log(JSON.stringify(err));
			}
			
		} else {
			//console.log( " layer " + layerName + " is NOT existing");
			document.getElementById(id).value = "Hide";
			
			//console.log(id)
			SingletonAirlineRoutes.getInstance().loadOneAirlineRoute( id );
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
			// layer is existing -> hide -> show button as hidden
			document.getElementById(elemButton.id).value = "Hide";
			try {
				/**
				 * @todo remove Layer as it is defined in main.js
				 *  */ 
				removeLayer( globus , layerName );
			
			} catch (err) {
				console.error(JSON.stringify(err));
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
			let id = this.LayerSidPrefix +  oneAirlineRoute["SID"];
			elemTdSid.innerHTML = '<span> <a id="' +  id + '" href="#" onclick="showSidStarRoute(this);" >' + oneAirlineRoute["SID"] + '</a> </span>'  
			elemTdSid.title = "click me";
		}
		// correct the STAR Id on the fly
		if ( oneAirlineRoute["STAR"] && (oneAirlineRoute["STAR"].length > 0 )) {
			let elemTdStar = document.getElementById( 'tdStarId-' + oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"] );
		
			elemTdStar.id = "tdStarId-" + oneAirlineRoute["STAR"];
			let id = this.LayerStarPrefix +  oneAirlineRoute["STAR"];
			elemTdStar.innerHTML = '<span> <a id="' +  id + '" href="#" onclick="showSidStarRoute(this);" >' + oneAirlineRoute["STAR"] + '</a> </span>'  
			elemTdStar.title = "click me";
		}
	}
	
	getSidStarLayerNamePrefix() {
		// openglobus global layer name prefix
		return "SidStar-";
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
		try {
			let layerName = this.LayerNamePrefix + Adep + "-" + Ades;
			/**
			 * @todo remove layer is defined in main.js
			 * */ 
			removeLayer( globus , layerName );
			
		} catch (err) {
			console.log(JSON.stringify(err));
		}
	}

	removeGlobusRoutesWayPointsLayers( airlineRoutesArray ) {
	
		for (var airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
			// insert one waypoint
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
				document.getElementById("btnAirlineRoutes").disabled = true;
				
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
							}
							
						},
						error: function(data, status) {
							console.log("Error - show Airline Routes : " + status + " Please contact your admin");
							showMessage("Error - Airline Routes" , data);
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirlineRoutes").disabled = false;
						},
				});

			} else {
				
				// get the name of the airline
				let airlineName = $("#airlineSelectId option:selected").val();
				airlineName = encodeURIComponent(airlineName);

				// only to retrieve the list of Adep Ades
				// use ajax to get the data 
				$.ajax( {
							method: 'get',
							url :  "airline/airlineRoutes/" + airlineName,
							async : true,
							success: function(data, status) {
											
								//alert("Data: " + data + "\nStatus: " + status);
								var dataJson = eval(data);		
								var airlineRoutesArray = dataJson["airlineRoutes"]
								//removeGlobusRoutesWayPointsLayers (  globus, airlineRoutesArray );
								//showRoutesWayPointsLayers ( globus, airlineRoutesArray );
								
							},
							error: function(data, status) {
								console.log("Error - show Airline Routes : " + status + " Please contact your admin");
								showMessage("Error - Airline Routes" , data);
							},
							complete : function() {
								stopBusyAnimation();
								document.getElementById("btnAirlineRoutes").disabled = false;
							},
				});
				
				$("#airlineRoutesDivId").hide();
			}
		}
	}
}