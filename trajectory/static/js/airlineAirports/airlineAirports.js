document.addEventListener('DOMContentLoaded', (event) => { 
       
	// console.log("airline airports js is loaded");
}); 

function loadOneAirport( layerAirports, airport ) {
	
	let longitude = parseFloat(airport.Longitude);
	var latitude = parseFloat(airport.Latitude);
	var name = airport.AirportName;
	
	layerAirports.add(new og.Entity({
		    lonlat: [longitude, latitude],
			label: {
					text: name,
					outline: 0.77,
					outlineColor: "rgba(255,255,255,.4)",
					size: 12,
					color: "black",
					offset: [10, -2]
				    },
			billboard: {
					src: "/static/images/plane.png",
					width: 16,
					height: 16,
					offset: [0, -2]
				    }
	}));
				
}

function loadAirports(layerAirports, dataJson) {
	
	// get all airports
	var airports = eval(dataJson['airports']);

	// add the reservations
	for (var airportId = 0; airportId < airports.length; airportId++ ) {
		// insert one reservation
		loadOneAirport( layerAirports, airports[airportId] );
	}
}

function initAirports(globus) {
	
	let show = true;
    	
	if ( !document.getElementById("btnAirports") ) {
		return;
	}
    document.getElementById("btnAirports").onclick = function () {
            
        if (show) {
			show = false;
			document.getElementById("btnAirports").innerText = "Hide Airline Airports";
			document.getElementById("btnAirports").style.backgroundColor = "green";

			document.getElementById("btnAirports").disabled = true;
				
			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);
			
			let layerName = airlineName + "-" + "AirlineAirports";
			let layerAirports = globus.planet.getLayerByName( layerName );
			if (! layerAirports ) {
				// layer is not existing
				console.log("layer = " + layerName + " is not existing");
				layerAirports = new og.layer.Vector(layerName , { clampToGround: true, 	});
				layerAirports.addTo(globus.planet);
				
				// init progress bar.
				initProgressBar();
				initWorker();
					
				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "trajectory/airports/" + airlineName,
						async : true,
						success: function(data, status) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							var dataJson = eval(data);
							loadAirports( layerAirports, dataJson );	
						},
						error: function(data, status) {
							console.log("Error - show Airports : " + status + " Please contact your admin");
							showMessage ( "Error - show Airports" , data );
						},
						complete : function() {
							stopBusyAnimation();
							document.getElementById("btnAirports").disabled = false
						}
				} );
				
			} else {
				console.log("layer = " + layerName + " is existing");
				layerAirports.setVisibility(true);
				document.getElementById("btnAirports").disabled = false
			}
			
		} else {
			show = true;
			document.getElementById("btnAirports").innerText = "Show Airline Airports";
			document.getElementById("btnAirports").style.backgroundColor = "yellow";

			// get the name of the airline
			let airlineName = $("#airlineSelectId option:selected").val();
			airlineName = encodeURIComponent(airlineName);

			// hide the airports
			let layerName = airlineName + "-" + "AirlineAirports";
			let layerAirports = globus.planet.getLayerByName( layerName );
			if (layerAirports) {
				// layer is existing
				console.log("layer = " + layerName + " is existing");
				layerAirports.setVisibility(false);
				//removeLayer(globus, layerAirports);
			} else {
				console.log("layer = " + layerName + " is not existing");
			}
		}
    };
}
