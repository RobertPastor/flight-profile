
import { initProgressBar , initWorker , removeLayer , stopBusyAnimation } from "../main/main.js";
import { SingletonMainClass } from "../main/mainSingletonClass.js";
import { Entity , Vector } from "../og/og.es.js";
import { PolyLine  } from "./polyline.js";

export const SingletonSidStar = (function () {
	
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


export class SidStar {
	
	constructor() {
		//console.log("SID STAR constructor");
		// store polylines
		this.polyLineObjects = {};
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
		
		let globus = this.globus;
		let layerName =  sidStarPattern.replaceAll("/", "-");
		//console.log( "layer name with underscores only = " + layerName );
		let layer = globus.planet.getLayerByName( layerName );
		if (layer) {
			if ( layer.getVisibility() ==  true ){
				layer.setVisibility( false );
			} 
		}
		sidStarPattern = sidStarPattern.replaceAll("/", "-");
		let polyLine = this.polyLineObjects[sidStarPattern];
		if ( polyLine ) {
			try {
				polyLine.removeLayer();
			} catch (err) {
				console.error("Error during polyline layer remove - err = "+ JSON.stringify(err));
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
		layerSidStarGlobusLayer.add(new Entity({
				lonlat: [longitude, latitude],
				label: {
						text: name,
						outline: 0.77,
						outlineColor: "rgba(255,255,255,.4)",
						size: 12,
						color: "black",
						offset: [0, -10]
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
		sidStarPattern = sidStarPattern.replaceAll("/", "-");
		let polyLine = new PolyLine (sidStarPattern);
		polyLine.init( globus, wayPointsArr );
		polyLine.draw(); 
		
		// store multiple polylines
		this.polyLineObjects[sidStarPattern] = polyLine;
		
	}
	
	hideShowSidStar( sidStarPattern , sidStarRoutesWaypointsArray ) {
		
		if ( Array.isArray(sidStarRoutesWaypointsArray) && ( sidStarRoutesWaypointsArray.length > 0 ) ) {
					
			// because the runway is part of the SidStar waypoint and the runway is written like ADEP/RWY or ADES/RWY
			let layerName = sidStarPattern.replaceAll("/", "-");
			//console.log( "layer Name with underscores only = " + layerName );
			
			let sidStarGlobusLayer = new Vector( layerName , {
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
			
			// draw polyline between waypoints
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

		this.sidStarPattern = sidStarPattern.replaceAll("/","-");;
		
		let globus = this.globus;
		//console.log ( "SID STAR layer with underscores only = "+ layerName);
		
		let layerName = sidStarPattern.replaceAll("/","-");
		let layer = globus.planet.getLayerByName( layerName );
		if (layer) {
			/**
			 * @todo using remove layer from main.js
			 */
			removeLayer ( globus , layerName )
			let polyLine = this.polyLineObjects[sidStarPattern];
			if ( polyLine ) {
				polyLine.removeLayer();
			}
		} 
			
		sidStarPattern = sidStarPattern.replaceAll("-","/");
		//console.log(" SID Star with SLASH only = " + sidStarPattern);
			
		// init progress bar.
		initProgressBar();
		initWorker();
			
		// only show Sid Star for the airports of the current airline
		/**
		* @warning SID STAR pattern to send to the back end needs to be using SLASH separator
		*/
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
								console.error("Error - show SID STAR : Property SidStarWayPoints is missing - Please contact your admin");
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
		
	}
}