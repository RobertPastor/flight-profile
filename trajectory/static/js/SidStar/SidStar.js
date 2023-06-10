
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
	
	getLayerName() {
		// only one layer displayed at a given time
		return "SidStar";
	}
	
	getGlobus() {
		return this.globus;
	}
	
	removeLayer() {
		
		let globus = this.globus;
			
		let layerName =  SingletonSidStar.getInstance().getLayerName();
		// function defined in main.js
		removeLayer( globus , layerName );
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
	
	hideShowSidStar( sidStarRoutesWaypointsArray , runWayJson ) {
		
		SingletonSidStar.getInstance().removeLayer();
		let layerName = SingletonSidStar.getInstance().getLayerName();
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
		
		// compute viewPort
		
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
	
	queryServer() {
		
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
				url :  "trajectory/showSidStar/" + airlineName,
				async : true,
				success: function(data, status) {
					
					stopBusyAnimation();
					//alert("Data: " + data + "\nStatus: " + status);
					let dataJson = eval(data);
					if ( dataJson.hasOwnProperty( "SidStar" )) {
						let sidStarJson = dataJson["SidStar"];
						if ( sidStarJson.hasOwnProperty( "SidStarWayPoints" ) && sidStarJson.hasOwnProperty( "DepartureArrivalRunWay" ) ) {
							
							let sidStarRoutesWaypointsArray = sidStarJson["SidStarWayPoints"];
							let runWayJson = sidStarJson["DepartureArrivalRunWay"]
							SingletonSidStar.getInstance().hideShowSidStar( sidStarRoutesWaypointsArray , runWayJson);
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
					document.getElementById(SingletonSidStar.getInstance().getButtonId()).disabled = false
				}
		} );
		
	}
	
	initSidStar( globus ) {
		
		this.LayerName = SingletonSidStar.getInstance().getLayerName();
		
		// 9th May 2023 - class attributes
		this.globus = globus;
		
		if ( !document.getElementById(SingletonSidStar.getInstance().getButtonId()) ) {
			console.error("button Sid Star is not declared");
			return;
		}
		
		document.getElementById(SingletonSidStar.getInstance().getButtonId()).onclick = function () {
			
			//console.log("button SID STAR clicked");
			
			SingletonSidStar.getInstance().queryServer();
				
		}
	}
}