
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
	
	hideLayer ( sidStarPattern ) {
		
		if ( sidStarPattern == undefined ) {
			return;
		}
		// sidStar Pattern -> SID-KLAX/24R/SLI
		//console.log( sidStarPattern );
		
		let globus = this.globus;
			
		let layerName =  sidStarPattern.replaceAll("/", "-");
		//console.log( "layer name with underscores only = " + layerName );
		let layer = globus.planet.getLayerByName( layerName );
		if (layer && (layer.getVisibility() ==  true)) {
			
			layer.setVisibility( false );
		
			let polyLine = this.polyLine;
			if ( polyLine ) {
				let polyLineLayerName = polyLine.getLayerName();
				let layer = globus.planet.getLayerByName( polyLineLayerName );
				if (layer && (layer.getVisibility() ==  true)) {

					layer.setVisibility( false );
				}
			}
		}
	}
	
	loadSidStarOneRouteWayPoint( layerSidStarGlobusLayer , wayPoint) {
		
		let name = "";
		if (wayPoint.hasOwnProperty("name")) {
			name = wayPoint["name"];
		}
		let latitude  = 0.0;
		if (wayPoint.hasOwnProperty("Latitude")) {
			latitude  = parseFloat(wayPoint["Latitude"]);
		}
		let longitude = 0.0;
		if (wayPoint.hasOwnProperty("Longitude")) {
			longitude  = parseFloat(wayPoint["Longitude"]);
		}
		
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
	}
	
	hideShowSidStar( sidStarPattern , sidStarRoutesWaypointsArray ) {
		
		if ( Array.isArray(sidStarRoutesWaypointsArray) && ( sidStarRoutesWaypointsArray.length > 0 ) ) {
					
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
			
			// draw polyline wetween waypoints
			SingletonSidStar.getInstance().drawPolyline( sidStarPattern , sidStarRoutesWaypointsArray );
			
			// set the viewport
			SingletonMainClass.getInstance().setExtent( sidStarRoutesWaypointsArray );
			
		} else {
			SingletonSidStar.getInstance().hideLayer(sidStarPattern);
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
		if (layer && (layer.getVisibility() ==  true)) {
			
			// hide layer 
			layer.setVisibility( false );
			
		} else {
			
			sidStarPattern = sidStarPattern.replaceAll("-","/");
			//console.log(" SID Star with SLASH only = " + sidStarPattern);
			
			// init progress bar.
			initProgressBar();
			initWorker();
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);
	
			// only show Sid Star for the airports of the current airline
			$.ajax( {
					method: 'get',
					url :  "trajectory/sidStar/" + sidStarPattern,
					async : true,
					success: function(data) {
						
						stopBusyAnimation();

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