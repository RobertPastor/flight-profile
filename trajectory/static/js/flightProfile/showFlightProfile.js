

document.addEventListener('DOMContentLoaded', (event) => { 
       
	//console.log("show KML flight profile js is loaded");
}); 


function loadOneRay( rayLayer, placeMark ) {
	
	let ellipsoid = new og.Ellipsoid(6378137.0, 6356752.3142);
	
	let latitude = parseFloat(placeMark["latitude"])
	let longitude = parseFloat(placeMark["longitude"])
	let height = parseFloat(placeMark["height"])
	
	let lonlat = new og.LonLat(longitude, latitude , 0.);
	//coordinate above Bochum to allow a upwards direction of ray
	let lonlatAir = new og.LonLat(longitude, latitude , height);
	
	//coordinates of Bochum in Cartesian
	let cart = ellipsoid.lonLatToCartesian(lonlat);
	let cartAir = ellipsoid.lonLatToCartesian(lonlatAir);
	
	if ( placeMark["name"].length > 0 ) {
		let offset = [10, 10]
		if ( placeMark["name"].startsWith("turn") || placeMark["name"].startsWith("groundRun") 
			|| placeMark["name"].startsWith("climbRamp") ) {
			offset = [10, -20]
		} 
		
		rayLayer.add(new og.Entity({
			cartesian : cartAir,
			label: {
					text: placeMark["name"],
					outline: 0.77,
					outlineColor: "rgba(255,255,255,.4)",
					size: 12,
					color: "black",
					offset: offset
				    }
		}));
	}
	
	rayLayer.add ( new og.Entity({
			ray: {
				startPosition: cart,
				endPosition: cartAir,
				length: height,
				startColor: "blue",
				endColor: "green",
				thickness: 5
			}
		})
	);
}

function addRays ( rayLayer , placeMarks ) {
	
	// add the waypoints
	for (var placeMarkId = 0; placeMarkId < placeMarks.length; placeMarkId++ ) {
		// insert one waypoint
		loadOneRay( rayLayer, placeMarks[placeMarkId] );
	}
}

function showFlightProfile(globus) {
	
	//console.log("start show flight profile");
	
	let layerKML = new og.layer.KML( "FlightProfile" , {
		billboard: { 
			src: '/static/images/move_down_icon.png', 
			color: '#6689db' ,
			width : 4,
			height : 4
			},
		color: '#6689db'
	} ) ;
	layerKML.addTo(globus.planet);
	
	//polygonOffsetUnits is needed to hide rays behind globe
	let rayLayer = new og.layer.Vector("rays", { polygonOffsetUnits: 0 });
	rayLayer.addTo(globus.planet);
	
	rayLayer.events.on("postdraw", function (e) {
		console.log("event is post draw")
		if (e.pickingObject instanceof og.Layer) {
			console.log("picking object is instance of layer")
		}
	});
	
	let first = true;
	let show = true;
	if ( ! document.getElementById("btnComputeFlightProfile") ) {
		return;
	}
	document.getElementById("btnComputeFlightProfile").onclick = function () {
		
		if (show) {
			show = false;
			document.getElementById("btnComputeFlightProfile").innerText = "Hide Flight Profile";
			if (first) {
				first = false
				document.getElementById("btnComputeFlightProfile").disabled = true

				// init progress bar.
				initProgressBar();
				initWorker();
				
				// use ajax to get the data 
				$.ajax( {
					method: 'get',
					url :  "trajectory/showFlightProfile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						console.log( dataJson["kmlURL"] );
						layerKML.addKmlFromUrl( url = dataJson["kmlURL"] );
						addRays( rayLayer , dataJson["placeMarks"] );
						setTimeout(
							function(){ 
								stopWorker(); 
							}
						, 10000);
						
					},
					error: function(data, status) {
						console.log("Error - show Flight Profile : " + status + " Please contact your admin");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnComputeFlightProfile").disabled = false
					},
				} );
				
			} else {
				layerKML.setVisibility(true);
				rayLayer.setVisibility(true);
			}
		} else {
			show = true;
			document.getElementById("btnComputeFlightProfile").innerText = "Show Flight Profile";
			layerKML.setVisibility(false);
			rayLayer.setVisibility(false);
		}
	};
}