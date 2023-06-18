
const SingletonSidStar = (function () {
	
	let instance;

    function createInstance() {
        let object = new SidStar();
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


class SidStar {
	
	constructor() {
		//console.log("SID STAR constructor");
	}
	
	getButtonId() {
		return "btnSidStar";
	}
	
	getGlobus() {
		return this.globus;
	}
	
	removeLayer ( sidStarPattern ) {
		
		if ( sidStarPattern == undefined ) {
			return;
		}
		// sidStar Pattern -> SID-KLAX/24R/SLI
		//console.log( sidStarPattern );
		
		let globus = this.globus;
			
		let layerName =  sidStarPattern.replaceAll("/", "-");
		//console.log( "layer name with underscores only = " + layerName );
		
		// function defined in main.js
		removeLayer( globus , layerName );
		
		// remove layer related to the SID Star animation
		try {
			let polyLine = this.polyLine;
			if ( polyLine ) {
				polyLine.removeLayer();
			}
		} catch (err) {
			console.error(JSON.stringify(err));
		}
		
		try {
			let polyLine = this.polyLine;
			if ( polyLine ) {
				let polyLineLayerName = polyLine.getLayerName();

				//console.log ( " remove layer with name = " + polyLineLayerName );
				if ( polyLineLayerName ){
					removeLayer ( globus, polyLineLayerName );
				}
			}
		} catch (err) {
			console.error(JSON.stringify(err));
		}
		
	}
	
	loadSidStarOneRouteWayPoint( layerSidStarGlobusLayer , wayPoint) {
		
		let name      = wayPoint["wayPointName"];
		let latitude  = parseFloat(wayPoint["latitudeDegrees"]);
		let longitude = parseFloat(wayPoint["longitudeDegrees"]);
		
		layerSidStarGlobusLayer.add(new og.Entity({
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
	
	// zoom on the sID or STAR area
	setViewPort ( sidStarRoutesWaypointsArray ) {
		
		// compute viewPort
		let globus = this.globus;
		
		let MinLatitude = 90.0;
		let MaxLatitude = -90.0;
		let MinLongitude = 180.0;
		let MaxLongitude = -180.0;
		for (let wayPointId = 0; wayPointId < sidStarRoutesWaypointsArray.length; wayPointId++ ) {
			// insert one waypoint
			let wayPoint = sidStarRoutesWaypointsArray[wayPointId];
			if ( parseFloat(wayPoint["latitudeDegrees"]) > MaxLatitude ) {
				MaxLatitude = parseFloat(wayPoint["latitudeDegrees"]);
			}
			if ( parseFloat(wayPoint["latitudeDegrees"]) < MinLatitude ) {
				MinLatitude = parseFloat(wayPoint["latitudeDegrees"]);
			}
			if ( parseFloat(wayPoint["longitudeDegrees"]) > MaxLongitude ) {
				MaxLongitude = parseFloat(wayPoint["longitudeDegrees"]);
			}
			if ( parseFloat(wayPoint["longitudeDegrees"]) < MinLongitude ) {
				MinLongitude = parseFloat(wayPoint["longitudeDegrees"]);
			}	
		}
		// margin
		let margin = 0.5;
		MinLatitude = MinLatitude - margin;
		MaxLatitude = MaxLatitude + margin;
		MinLongitude = MinLongitude - margin;
		MaxLongitude = MaxLongitude + margin;
		let SouthWest = new og.LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
		let NorthEast = new og.LonLat( parseFloat(MaxLongitude), parseFloat(MaxLatitude) , parseFloat("0.0") );
		let viewExtent = new og.Extent( SouthWest , NorthEast );
					
		globus.planet.viewExtent( viewExtent );
		
	}
	
	drawPolyline( sidStarPattern , sidStarRoutesWaypointsArray ) {
	
		let globus = this.globus;
		
		let wayPointsArr = [];
		for (let wayPointId = 0; wayPointId < sidStarRoutesWaypointsArray.length; wayPointId++ ) {
			
			if ( wayPointId >= 1) {
				let srcWayPoint = sidStarRoutesWaypointsArray[wayPointId-1];
				let dstWayPoint = sidStarRoutesWaypointsArray[wayPointId];
				wayPointsArr.push( {"src": srcWayPoint , "dst": dstWayPoint }  );
			}
		}
		// defined in the polyline.js file
		let polyLine = new PolyLine (sidStarPattern);
		polyLine.init( globus, wayPointsArr );
		polyLine.draw(); 
		
		this.polyLine = polyLine;
		
		// store polyline layer name
		this.polylineLayerName = polyLine.getLayerName();
		//console.log( "polyline layer name = " + this.polylineLayerName );
	}
	
	hideShowSidStar( sidStarPattern , sidStarRoutesWaypointsArray ) {
		
		if ( sidStarRoutesWaypointsArray.length > 0 ) {
		
			SingletonSidStar.getInstance().removeLayer(sidStarPattern);
			
			let layerName = sidStarPattern.replaceAll("/", "-");
			//console.log( "layer Name with underscores only = " + layerName );
			
			let sidStarGlobusLayer = new og.layer.Vector( layerName , {
					billboard: { 
						src: '/static/trajectory/images/marker.png', 
						color: '#6689db' ,
						width : 4,
						height : 4
						},
					clampToGround: true,
					});
					
			let globus = SingletonSidStar.getInstance().getGlobus();
			sidStarGlobusLayer.addTo(globus.planet);
			
			// add the waypoints
			for (let wayPointId = 0; wayPointId < sidStarRoutesWaypointsArray.length; wayPointId++ ) {
				// insert one waypoint
				SingletonSidStar.getInstance().loadSidStarOneRouteWayPoint( sidStarGlobusLayer, sidStarRoutesWaypointsArray[wayPointId] );
			}
			
			// set the viewport
			SingletonSidStar.getInstance().setViewPort( sidStarRoutesWaypointsArray );
			
			// draw polyline wetween waypoints
			SingletonSidStar.getInstance().drawPolyline( sidStarPattern , sidStarRoutesWaypointsArray );
			
		} else {
			SingletonSidStar.getInstance().removeLayer(sidStarPattern);
		}
	}
	
	queryServer( sidStarPattern ) {
		
		// SidStar Pattern -> Sid-KLAX/24R/SIL
		// SidStar Pattern -> Star-KATL/26L/MEM
		this.sidStarPattern = sidStarPattern;
		//console.log(sidStarPattern);
		
		let globus = this.globus;
		let layerName = sidStarPattern.replaceAll("/","-");
		//console.log ( "SID STAR layer with underscores only = "+ layerName);
		
		let layer = globus.planet.getLayerByName( layerName );
		if (layer) {
			//console.log( "layer with name = "+ layerName + " already existing ");
			
			// loca layer removal
			this.removeLayer ( sidStarPattern );
			return ;
		}
		
		sidStarPattern = sidStarPattern.replaceAll("-","/");
		//console.log(" SID Star with SLASH only = " + sidStarPattern);
		
		// init progress bar.
		initProgressBar();
		initWorker();
		
		// get the name of the airline
		let airlineName = $("#airlineSelectId option:selected").val();
		airlineName = encodeURIComponent(airlineName);

		// use ajax to get the data 
		// only show Sid Star for the airports of the current airline
		$.ajax( {
				method: 'get',
				url :  "trajectory/showSidStar/" + sidStarPattern,
				async : true,
				success: function(data, status) {
					
					stopBusyAnimation();
					//alert("Data: " + data + "\nStatus: " + status);
					let dataJson = eval(data);
					if ( dataJson.hasOwnProperty( "SidStar" )) {
						let sidStarJson = dataJson["SidStar"];
						if ( sidStarJson.hasOwnProperty( "SidStarWayPoints" ) && sidStarJson.hasOwnProperty( "DepartureArrivalRunWay" ) ) {
							
							let sidStarRoutesWaypointsArray = sidStarJson["SidStarWayPoints"];
							//let runWayJson = sidStarJson["DepartureArrivalRunWay"]
							SingletonSidStar.getInstance().hideShowSidStar( sidStarPattern, sidStarRoutesWaypointsArray );
						} else {
							console.error("Error - show SID STAR : Property SidStarWayPoints is missing  - Please contact your admin");
						}
					} else {
						console.error("Error - show SID STAR : Property SidStar is missing  - Please contact your admin");
					}
				},
				error: function(data, status) {
					stopBusyAnimation();
					console.error("Error - show SID STAR : " + status + " Please contact your admin");
					showMessage ( "Error - show SID STAR" , data );
				},
				complete : function() {
					stopBusyAnimation();
					//document.getElementById(SingletonSidStar.getInstance().getButtonId()).disabled = false
				}
		} );
		
	}
	
	initSidStar( globus ) {
		
		
		// 9th May 2023 - class attributes
		this.globus = globus;
		
		if ( !document.getElementById(SingletonSidStar.getInstance().getButtonId()) ) {
			//console.error("button Sid Star is not declared");
			return;
		}
		
		document.getElementById(SingletonSidStar.getInstance().getButtonId()).onclick = function () {
			
			//console.log("button SID STAR clicked");
			
			SingletonSidStar.getInstance().queryServer();
				
		}
	}
}