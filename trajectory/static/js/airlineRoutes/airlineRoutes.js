document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("Airline Routes.js is loaded");
	  $('#tableAirlineRoutesId').hide();

}); 

function loadOneRouteWayPoint( layerRouteWayPoints, waypoint ) {
	
	let longitude = parseFloat(waypoint.Longitude);
	let latitude = parseFloat(waypoint.Latitude);
	let name = waypoint.name;
	
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

function removeRouteWayPointsLayer( globus , layerName ) {
	
	let layer = globus.planet.getLayerByName( layerName );
	let entities = layer.getEntities();
	layer.removeEntities(entities);
	
}


function loadRouteWayPoints( globus, airlineRoutesWaypointsArray , layerName) {
	
	console.log("start loading route WayPoints");
	let layerRouteWayPoints = new og.layer.Vector( layerName , {
			billboard: { 
				src: '/static/trajectory/images/marker.png', 
				color: '#6689db' ,
				width : 4,
				height : 4
				},
            clampToGround: true,
            });
	layerRouteWayPoints.addTo(globus.planet);
	
	layerRouteWayPoints.events.on("add", function (e) {
		console.log("event is add")
		if (e.pickingObject instanceof og.Layer) {
			console.log("picking object is instance of layer")
		}
	});

	// add the waypoints
	for (var wayPointId = 0; wayPointId < airlineRoutesWaypointsArray.length; wayPointId++ ) {
		// insert one waypoint
		loadOneRouteWayPoint( layerRouteWayPoints, airlineRoutesWaypointsArray[wayPointId] );
	}
}

function loadOneAirlineRoute(globus, id) {
	let arr = id.split("-")
	let Adep = arr[1]
	console.log(Adep)
	let Ades = arr[2]
	console.log(Ades)
	// use ajax to get the data 
	$.ajax( {
			method: 'get',
			url :  "airline/wayPointsRoute/" + Adep +"/" + Ades,
			async : true,
			success: function(data, status) {
										
					//alert("Data: " + data + "\nStatus: " + status);
					var dataJson = eval(data);		
					var airlineRoutesWaypointsArray = dataJson["airlineRouteWayPoints"]
					var layerName =  "Route-WayPoints-"+ Adep + "-" + Ades
					loadRouteWayPoints(globus, airlineRoutesWaypointsArray , layerName )
							
			},
			error: function(data, status) {
							console.log("Error - show Airline Routes : " + status + " Please contact your admin");
			},
			complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirlineRoutes").disabled = false
			},
	});
	
}

function showHideWayPoints(globus, domElement) {
	
	let id = domElement.id 
	let value = document.getElementById(id).value 
	if (value == "Show") {
		document.getElementById(id).value = "Hide"
		console.log(id)
		loadOneAirlineRoute(globus, id)
	} else {
		document.getElementById(id).value = "Show"
		let arr = id.split("-")
		let Adep = arr[1]
		console.log(Adep)
		let Ades = arr[2]
		console.log(Ades)
		
		let layerName = "Route-WayPoints-"+ Adep + "-" + Ades;
		removeRouteWayPointsLayer( globus , layerName )
	}
}

function addOneAirlineRoute( globus, oneAirlineRoute ) {
	
	$("#tableAirlineRoutesId").find('tbody')
    .append($('<tr>')
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
		//.append($('<td id="tdButtonId" >')
		//	.append ( " <input type='button' id='buttonRouteId' style='width:100%; height:100%;' value='Show' onclick='showHideWayPoints(this)' /> " )
		//)
		.append($('<td id="tdButtonId" >')
			.append ( " <input type='button' id='buttonRouteId' style='width:100%; height:100%;' value='Show'  /> " )
		)
    );
	
	var elemTd = document.getElementById('tdButtonId');
	elemTd.id = "tdButtonId-"+oneAirlineRoute["DepartureAirportICAOCode"]+"-"+oneAirlineRoute["ArrivalAirportICAOCode"];
	
	var elemButton = document.getElementById('buttonRouteId');
	elemButton.id = "buttonRouteId-"+oneAirlineRoute["DepartureAirportICAOCode"]+"-"+oneAirlineRoute["ArrivalAirportICAOCode"];
	
	$('#'+elemButton.id).click(function () {
		console.log("button clicked") 
		showHideWayPoints(globus, this);
	});

}

/**
* only the name of the departure and arrival airports
*/
function addAirlineRoutes(globus, airlineRoutesArray) {
	
	$('#tableAirlineRoutesId tbody').empty();
	for (var airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
		// insert one waypoint
		addOneAirlineRoute( globus, airlineRoutesArray[airlineRouteId] );
	}
}

function loadAirlineRoutes(globus) {
	
	let show = true;
	$("#trAirlineRoutesId").hide();

	document.getElementById("btnAirlineRoutes").onclick = function () {
		
		if (show) {
			$("#trAirlineRoutesId").show();

			show = false;
			// change name on the button
			document.getElementById("btnAirlineRoutes").innerText = "Hide Airline Routes";
			$('#tableAirlineRoutesId').show();
			// disable the button 
			document.getElementById("btnAirlineRoutes").disabled = true

			// use ajax to get the data 
			$.ajax( {
						method: 'get',
						url :  "airline/airlineRoutes",
						async : true,
						success: function(data, status) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							var dataJson = eval(data);		
							var airlineRoutesArray = dataJson["airlineRoutes"]
							addAirlineRoutes(globus, airlineRoutesArray)
							
						},
						error: function(data, status) {
							console.log("Error - show Airline Routes : " + status + " Please contact your admin");
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirlineRoutes").disabled = false
						},
			});

		} else {

			show = true;
			document.getElementById("btnAirlineRoutes").innerText = "Show Airline Routes";
			
			$("#trAirlineRoutesId").hide();
			$('#tableAirlineRoutesId').hide();
		}
	}
}