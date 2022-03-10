
document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("waypoints.js is loaded");
}); 


function stopBusyAnimation(){
	console.log("stop busy anymation");
}

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
					src: "/static/trajectory/images/marker.png",
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

function wayPoints(globus, viewExtent) {
	
	console.log("start WayPoints");
	let layerWayPoints = new og.layer.Vector("WayPoints", {
			billboard: { 
				src: '/static/trajectory/images/marker.png', 
				color: '#6689db' ,
				width : 4,
				height : 4
				},
            clampToGround: true,
            });
	layerWayPoints.addTo(globus.planet);
	
	layerWayPoints.events.on("postdraw", function (e) {
		console.log("event is postdraw")
		if (e.pickingObject instanceof og.Layer) {
			console.log("picking object is instance of layer")
		}
	});
	    
	let show = true;
    	
	document.getElementById("btnWayPoints").onclick = function () {
		
		console.log( globus.planet.getViewExtent() )
		
		if (show) {
			show = false;
			document.getElementById("btnWayPoints").innerText = "Hide Airline WayPoints";
			
			// use ajax to get the data 
			data = 'minlatitude=' + viewExtent[1].toString() + "&"
			data += 'maxlatitude=' + viewExtent[3].toString() + "&"
			data += 'minlongitude=' + viewExtent[0].toString() + "&"
			data += 'maxlongitude=' + viewExtent[2].toString()
			$.ajax( {
				method: 'get',
				url :  "trajectory/waypoints",
				data:  data,
				async : true,
				success: function(data, status) {
								
					//alert("Data: " + data + "\nStatus: " + status);
					var dataJson = eval(data);
					loadWayPoints ( layerWayPoints , dataJson );	
				},
				error: function(data, status) {
					console.log("Error - delete old bookings: " + status + " SVP veuillez contactez votre administrateur");
				},
				complete : stopBusyAnimation,
			} );
			
		} else {
			show = true;
			document.getElementById("btnWayPoints").innerText = "Show Airline WayPoints";
			let entities = layerWayPoints.getEntities();
			layerWayPoints.removeEntities(entities);
		}
    };
			
}