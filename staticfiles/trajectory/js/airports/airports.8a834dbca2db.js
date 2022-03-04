document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("airports js is loaded");
}); 

function stopBusyAnimation(){
	console.log("stop busy anymation");
}

function loadOneAirport( layerVector, airport ) {
	
	let longitude = airport.Longitude;
	var latitude = parseFloat(airport.Latitude);
	var name = parseFloat(airport.AirportName);
	
	layerVector.add(new og.Entity({
		    lonlat: [longitude, latitude],
			label: {
					text: name,
					outline: 0.77,
					outlineColor: "rgba(255,255,255,.4)",
					size: 27,
					color: "black",
					offset: [10, -2]
				    },
			billboard: {
					src: "/static/trajectory/images/marker.png",
					width: 32,
					height: 32,
					offset: [0, 32]
				    }
	}));
				
}

function loadAirports(layerVector, dataJson) {
	
	// get all airports
	var airports = eval(dataJson['airports']);

	// add the reservations
	for (var airportId = 0; airportId < airports.length; airportId++ ) {
		// insert one reservation
		loadOneAirport( layerVector, airports[airportId] );
	}
	
}

function airports(globus) {
	
	console.log("start airports");
	let layerVector = new og.layer.Vector("Airports", {
                clampToGround: true
            });
	layerVector.addTo(globus.planet);
	    
	let show = true;
    	
    document.getElementById("btnAirports").onclick = function () {
            
        if (show) {
			show = false;
			document.getElementById("btnAirports").innerText = "Hide Airports";
			
			// use ajax to get the data 
			$.ajax( {
				method: 'get',
				url :  "trajectory/airports",
				async : true,
				success: function(data, status) {
								
					//alert("Data: " + data + "\nStatus: " + status);
					var dataJson = eval(data);
					loadAirports( layerVector, dataJson );	
				},
				error: function(data, status) {
					console.log("Error - delete old bookings: " + status + " SVP veuillez contactez votre administrateur");
				},
				complete : stopBusyAnimation,
			} );
			
			
			
		} else {
			show = true;
			document.getElementById("btnAirports").innerText = "Show Airports";
			let entities = layerVector.getEntities();
			layerVector.removeEntities(entities);
		}
    };
}
