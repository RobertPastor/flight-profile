document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("KML flight profile js is loaded");
}); 

function stopBusyAnimation(){
	console.log("stop busy anymation");
}

function flightprofile(globus) {
	
	console.log("start flight profile");
	let layerKML = new og.layer.KML("FlightProfile");
	layerKML.addTo(globus.planet);
	    
	let first = true;
	let show = true;
	document.getElementById("btnFlightProfile").onclick = function () {
		
		if (show) {
			show = false;
			document.getElementById("btnFlightProfile").innerText = "Hide Flight Profile";

			if (first) {
				first = false
				// use ajax to get the data 
				$.ajax( {
					method: 'get',
					url :  "trajectory/flightprofile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						console.log( dataJson["kmlURL"] );
						let billBoard = new og.entity.Billboard({
								src: "/static/trajectory/images/plane.png",
								width: 32,
								height: 32,
								offset: [0, 32]
							})
						layerKML.addKmlFromUrl( url = dataJson["kmlURL"] , color = '#194a8d' );	
					},
					error: function(data, status) {
						console.log("Error - delete old bookings: " + status + " SVP veuillez contactez votre administrateur");
					},
					complete : stopBusyAnimation,
				} );
				
			} else {
				layerKML.setVisibility(true);
				
			}
			
		} else {
			show = true;
			document.getElementById("btnFlightProfile").innerText = "Show Flight Profile";
			
			layerKML.setVisibility(false);
		}
		
		
	};
}