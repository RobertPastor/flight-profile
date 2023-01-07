document.addEventListener('DOMContentLoaded', (event) => { 
       
	// console.log("airline airports js is loaded");
}); 

const SingletonAirlineAirports = (function () {
	
	let instance;

    function createInstance() {
        let object = new AirlineAirports();
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

class AirlineAirports {
	
	constructor() {
		//console.log("Airline Airports constructor") 
	}
	
	writeRoutesFromStartingAirport( globus , departureAirportICAOcode , airlineRoutesArray , position ) {
		
		// modify the div position
		// Update the position of `#div` dynamically
		$('#airlineAirportsRoutesMainDivId').css({
			'position': 'absolute',
			'top': position["y"] + 5, // Leave some margin
			'left': position["x"] + 5, // Leave some margin
			'display': 'block'
		});
		
		$('#airlineAirportsRoutesMainDivId tbody').empty();
		for (let airlineRouteId = 0; airlineRouteId < airlineRoutesArray.length; airlineRouteId++ ) {
			// insert one route
			
			let oneAirlineRoute = airlineRoutesArray[airlineRouteId];
			if ( oneAirlineRoute["DepartureAirportICAOCode"] == departureAirportICAOcode ) {
			
				$("#airlineAirportsRoutesMainDivId").find('tbody')
				.append($('<tr>')
					.append($('<td>')
						.append( oneAirlineRoute["Airline"] )
					)
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

				);
			}
		}
	}
	
	loadRoutesStartingFromAirport ( globus, departureAirportICAOcode , position ) {
		
		// get the name of the airline
		let airlineName = $("#airlineSelectId option:selected").val();
		airlineName = encodeURIComponent(airlineName);
		
		// use ajax to get the data 
		$.ajax( {
				method: 'get',
				url :  "airline/airlineRoutes/" + airlineName,
				async : true,
				success: function(data, status) {
								
					//alert("Data: " + data + "\nStatus: " + status);
					let dataJson = eval(data);		
					let airlineRoutesArray = dataJson["airlineRoutes"]
					SingletonAirlineAirports.getInstance().writeRoutesFromStartingAirport(  globus, departureAirportICAOcode, airlineRoutesArray , position );
					
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
	}

	loadOneAirport( globus, airport , showHide ) {
	
		// get the name of the airline
		let airlineName = $("#airlineSelectId option:selected").val();
		airlineName = encodeURIComponent(airlineName);

		// need to prefix an airport ICAO code with the airline name 
		// as the same airport might be used by several airlines
		let layerName = airlineName + "-" + airport.AirportICAOcode;
		//console.log( layerName ) ;
		
		let layer = globus.planet.getLayerByName( layerName );
		if (! layer) {
			// layer is not existing
			
			let layerAirport = new og.layer.Vector(layerName , { clampToGround: true, 	});
			layerAirport.addTo(globus.planet);
			
			let longitude = parseFloat(airport.Longitude);
			let latitude = parseFloat(airport.Latitude);
			let name = airport.AirportName;
			
			layerAirport.add(new og.Entity({
					lonlat: [longitude, latitude],
					label: {
							text: name,
							outline: 0.77,
							outlineColor: "rgba(255,255,255,.4)",
							size: 11,
							color: "black",
							offset: [10, -2],
							align: "center"
							},
					billboard: {
							src: "/static/images/plane.png",
							width: 16,
							height: 16,
							offset: [0, -10]
							}
			}));
			
			layerAirport.events.on("rclick", function (e) {
				console.log("right click - layer name = " + this.name);
				console.log("right click - airport name = " + e.pickingObject.label._text);
				
				let position = {}
				position["x"] = e.clientX;
				position["y"] = e.clientY
				
				// show table with routes starting in this airport
				$("#airlineAirportsRoutesMainDivId").show();
				
				let airportICAOcode = this.name.split("-")[1];
				SingletonAirlineAirports.getInstance().loadRoutesStartingFromAirport(globus, airportICAOcode, position);

			});
			
			layerAirport.events.on("mouseenter", function (e) {
				e.renderer.handler.canvas.style.cursor = "pointer";
				// show ICAO code of the airport
				e.renderer.handler.canvas.title = this.name.split("-")[1];
			});

			layerAirport.events.on("mouseleave", function (e) {
				e.renderer.handler.canvas.style.cursor = "default";
				e.renderer.handler.canvas.title = "";
				
				// hide table with routes starting in this airport
				$("#airlineAirportsRoutesMainDivId").hide();

			});
			
		} else {
			// no need to create the layer
			layer.setVisibility(showHide)
		}
	}

	loadAirports( globus, dataJson , showHide ) {
	
		// get all airports
		let airports = eval(dataJson['airports']);

		// add the reservations
		for (let airportId = 0; airportId < airports.length; airportId++ ) {
			// insert one airport
			SingletonAirlineAirports.getInstance().loadOneAirport(  globus, airports[airportId] , showHide );
		}
	}

	showHideAllAirports( globus, showHide ) {
		
		//console.log("show hide all airports = " + showHide.toString() );
	
		// init progress bar.
		initProgressBar();
		initWorker();
		
		// get the name of the airline
		let airlineName = $("#airlineSelectId option:selected").val();
		airlineName = encodeURIComponent(airlineName);

		//if ( showHide == true ) {

			// use ajax to get the data 
			$.ajax( {
				method: 'get',
				url :  "trajectory/airports/" + airlineName,
				async : true,
				success: function(data, status) {
					stopBusyAnimation();
					//alert("Data: " + data + "\nStatus: " + status);
					let dataJson = eval(data);
					SingletonAirlineAirports.getInstance().loadAirports( globus, dataJson , showHide );	
				},
				error: function(data, status) {
					stopBusyAnimation();
					console.log("Error - show Airports : " + status + " Please contact your admin");
					showMessage ( "Error - show Airports" , data );
				},
				complete : function() {
					stopBusyAnimation();
					document.getElementById("btnAirports").disabled = false
				}
			} );
		//}
	
	}

	initAirports(globus) {
	
		let show = true;
			
		if ( !document.getElementById("btnAirports") ) {
			return;
		}
		document.getElementById("btnAirports").onclick = function () {
				
			if (show) {
				
				show = false;
				document.getElementById("btnAirports").innerText = "Hide Airline Airports";
				document.getElementById("btnAirports").style.backgroundColor = "green";
					
				SingletonAirlineAirports.getInstance().showHideAllAirports( globus, true );
				
			} else {
				
				show = true;
				document.getElementById("btnAirports").innerText = "Show Airline Airports";
				document.getElementById("btnAirports").style.backgroundColor = "yellow";

				SingletonAirlineAirports.getInstance().showHideAllAirports( globus, false );
				
			}
		};
	}
}
