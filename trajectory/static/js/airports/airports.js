document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("airports js is loaded");
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
					offset: [0, 32]
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

function airports(globus) {
	
	console.log("start airports");
	let layerAirports = new og.layer.Vector("Airports", {
            clampToGround: true,
    });
	layerAirports.addTo(globus.planet);
	    
	let show = true;
	let first = true;
    	
    document.getElementById("btnAirports").onclick = function () {
            
        if (show) {
			show = false;
			document.getElementById("btnAirports").innerText = "Hide Airline Airports";
			
			if (first) {
				document.getElementById("btnAirports").disabled = true;
				
				// init progress bar.
				initProgressBar();
				initWorker();
				
				first = false;
				// use ajax to get the data 
				$.ajax( {
					method: 'get',
					url :  "trajectory/airports",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						loadAirports( layerAirports, dataJson );	
					},
					error: function(data, status) {
						console.log("Error - show Airports : " + status + " Please contact your admin");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnAirports").disabled = false
					}
				} );
			} else {
				layerAirports.setVisibility(true);
			}
			
		} else {
			show = true;
			document.getElementById("btnAirports").innerText = "Show Airline Airports";
			layerAirports.setVisibility(false);
		}
    };
}
