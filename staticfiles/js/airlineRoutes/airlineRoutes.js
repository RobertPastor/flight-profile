let LayerNamePrefix = "Route-WayPoints-"

document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("Airline Routes.js is loaded");
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


function loadRouteWayPoints( globus, airlineRoutesWaypointsArray , layerName) {
	
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
	layerRouteWayPoints.addTo(globus.planet);
	
	layerRouteWayPoints.events.on("add", function (e) {
		//console.log("event is add")
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
	//console.log(Adep)
	let Ades = arr[2]
	//console.log(Ades)
	// use ajax to get the data 
	$.ajax( {
			method: 'get',
			url :  "airline/wayPointsRoute/" + Adep +"/" + Ades,
			async : true,
			success: function(data, status) {
										
					//alert("Data: " + data + "\nStatus: " + status);
					var dataJson = eval(data);		
					var airlineRoutesWaypointsArray = dataJson["airlineRouteWayPoints"]
					var layerName =  LayerNamePrefix + Adep + "-" + Ades;
					loadRouteWayPoints(globus, airlineRoutesWaypointsArray , layerName )
							
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

function showHideWayPoints(globus, domElement) {
	
	let id = domElement.id ;
	let value = document.getElementById(id).value ;
	
	if (value == "Show") {
		
		document.getElementById(id).value = "Hide"
		//console.log(id)
		loadOneAirlineRoute(globus, id);
		domElement.style.backgroundColor = "green";
		
	} else {
		
		document.getElementById(id).value = "Show"
		let arr = id.split("-")
		let Adep = arr[1]
		//console.log(Adep)
		let Ades = arr[2]
		//console.log(Ades)
		
		let layerName =  LayerNamePrefix + Adep + "-" + Ades;
		// function defined in main.js
		removeLayer( globus , layerName )
		domElement.style.backgroundColor = "yellow";

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
	
	let layerName = LayerNamePrefix + oneAirlineRoute["DepartureAirportICAOCode"] + "-" + oneAirlineRoute["ArrivalAirportICAOCode"] 
	let layer = globus.planet.getLayerByName( layerName );
	if (layer) {
		// layer is existing -> hide it
		document.getElementById(elemButton.id).value = "Hide"
		document.getElementById(elemButton.id).style.backgroundColor = "green";
	}
	
	/**
	* on click function forwarding the globus argument
	*/
	$('#'+elemButton.id).click(function () {
		//console.log("button clicked") 
		showHideWayPoints(globus, this);
	});

}

/**
* display only the names of the departure and arrival airports
*/
function addAirlineRoutes(globus, airlineRoutesArray) {
	
	$('#tableAirlineRoutesId tbody').empty();
	for (var airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
		// insert one waypoint
		addOneAirlineRoute( globus, airlineRoutesArray[airlineRouteId] );
	}
}

function removeOneAirlineRoute ( globus, oneAirlineRoute ) {
	
	let Adep = oneAirlineRoute["DepartureAirportICAOCode"];
	let Ades = oneAirlineRoute["ArrivalAirportICAOCode"];
	try {
		
		let layerName = LayerNamePrefix + Adep + "-" + Ades;
		removeLayer( globus , layerName )
		
	} catch (err) {
		console.log(JSON.stringify(err));
	}
	
}

function removeGlobusRoutesWayPointsLayers( globus , airlineRoutesArray) {
	
	for (var airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
		// insert one waypoint
		removeOneAirlineRoute( globus, airlineRoutesArray[airlineRouteId] );
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
			document.getElementById("btnAirlineRoutes").style.backgroundColor = "green";
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
							addAirlineRoutes(  globus, airlineRoutesArray )
							
						},
						error: function(data, status) {
							console.log("Error - show Airline Routes : " + status + " Please contact your admin");
							showMessage("Error - Airline Routes" , data)
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirlineRoutes").disabled = false
						},
			});

		} else {

			show = true;
			document.getElementById("btnAirlineRoutes").innerText = "Show Airline Routes";
			document.getElementById("btnAirlineRoutes").style.backgroundColor = "yellow";

			// only to retrieve the list of Adep Ades
			// use ajax to get the data 
			$.ajax( {
						method: 'get',
						url :  "airline/airlineRoutes",
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
							showMessage("Error - Airline Routes" , data)
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirlineRoutes").disabled = false
						},
			});
			
			$("#trAirlineRoutesId").hide();
			$('#tableAirlineRoutesId').hide();
		}
	}
}