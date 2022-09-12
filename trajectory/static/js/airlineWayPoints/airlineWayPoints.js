
document.addEventListener('DOMContentLoaded', (event) => { 
       
	// console.log("waypoints.js is loaded");
}); 


function loadOneWayPoint( layerWayPoints, waypoint ) {
	
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

function loadWayPoints(layerWayPoints, dataJson) {
	
	// get all waypoints
	var waypoints = eval(dataJson['waypoints']);

	// add the waypoints
	for (var wayPointId = 0; wayPointId < waypoints.length; wayPointId++ ) {
		// insert one waypoint
		loadOneWayPoint( layerWayPoints, waypoints[wayPointId] );
	}
}

function initWayPoints(globus, viewExtent) {
	    
	let show = true;
    	
	if ( !document.getElementById("btnWayPoints") ) {
		return;
	}
	document.getElementById("btnWayPoints").onclick = function () {
		
		//console.log( globus.planet.getViewExtent() )
		let viewExtent = globus.planet.getViewExtent();
		let northEast = viewExtent["northEast"];
		let southWest = viewExtent["southWest"];
		
		if (show) {
			document.getElementById("btnWayPoints").disabled = true
			
			show = false;
			document.getElementById("btnWayPoints").innerText = "Hide Airline WayPoints";
			document.getElementById("btnWayPoints").style.backgroundColor = "green";

			// use ajax to get the data 
			data = 'minlatitude=' + parseInt(southWest["lat"]).toString() + "&";
			data += 'maxlatitude=' + parseInt(northEast["lat"]).toString() + "&";
			data += 'minlongitude=' + parseInt(southWest["lon"]).toString() + "&";
			data += 'maxlongitude=' + parseInt(northEast["lon"]).toString();
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);
			
			let layerName = airlineName + "-" + "WayPoints";
			let layerWayPoints = globus.planet.getLayerByName( layerName );
			if (! layerWayPoints ) {
				
				// layer is not existing
				console.log("layer = " + layerName + " is not existing");
				
				let layerWayPoints = new og.layer.Vector(layerName, {
					billboard: { 
						src: '/static/trajectory/images/marker.png', 
						color: '#6689db' ,
						width : 4,
						height : 4
						},
					clampToGround: true,
				});
				layerWayPoints.addTo(globus.planet);
	
				$.ajax( {
					method: 'get',
					url :  "trajectory/waypoints/" + airlineName,
					data:  data,
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						loadWayPoints ( layerWayPoints , dataJson );	
					},
					error: function(data, status) {
						console.log("Error - Show Airline WayPoints : " + status + " Please contact your admin");
						showMessage( "Error - Show Airline WayPoints" , data );
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnWayPoints").disabled = false;
					}
				} );
				
			} else {
				console.log("layer = " + layerName + " is existing");
				layerWayPoints.setVisibility(true);
				document.getElementById("btnWayPoints").disabled = false
			}
			
		} else {
			show = true;
			document.getElementById("btnWayPoints").innerText = "Show Airline WayPoints";
			document.getElementById("btnWayPoints").style.backgroundColor = "yellow";
			
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			// hide the airports
			let layerName = airlineName + "-" + "WayPoints";
			let layerWayPoints = globus.planet.getLayerByName( layerName );
			if (layerWayPoints) {
				// layer is existing
				console.log("layer = " + layerName + " is existing");
				layerWayPoints.setVisibility(false);

			} else {
				console.log("layer = " + layerName + " is not existing");
			}
		}
    };
}