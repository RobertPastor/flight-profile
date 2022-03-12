
var worker = undefined;

document.addEventListener('DOMContentLoaded', (event) => { 
       
	  console.log("KML flight profile js is loaded");
}); 

function stopBusyAnimation(){
	console.log("stop busy animation");
}

var imagesIndex = 0;

function updateProgress() {
    var progressBar = document.getElementById('progressId');
    progressBar.value = String(imagesIndex++);
    var progressValue = document.getElementById('progressVal');
    if (progressValue != undefined) {
        progressValue.innerHTML = String(imagesIndex);
    }
}

function initProgressBar() {
    // Gets the number of image elements
    var numberOfSteps = 100;
    var progressBar = document.getElementById('progressId');
    if (progressBar != undefined) {
        progressBar.max = String(numberOfSteps);
    }
}

function stopWorker() {
    worker.terminate();
    worker = undefined;
    console.log("worker is stopped !!!");
    // hide the progress bars
    
    //$("#workerId").hide();
    //$("#progressId").hide();
}

function initWorker() {
	
	if (typeof (Worker) !== "undefined") {
        console.log("Yes! Web worker is supported !");
        // Some code.....
        if (typeof (worker) == "undefined") {
            worker = new Worker("/static/js/worker/worker.js");
            worker.onmessage = function (event) {

                var workerProgressBar = document.getElementById('workerId');
                workerProgressBar.value = event.data;

                var workerProgressValue = document.getElementById('workerVal');
                workerProgressValue.innerHTML = event.data;
            };
        }
    } else {
        // Sorry! No Web Worker support..
		console.log("Sorry! no web worker support ...");
    }
}

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
		if ( placeMark["name"].startsWith("turn") || placeMark["name"].startsWith("ground-run") 
			|| placeMark["name"].startsWith("climb-ramp") ) {
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

function flightprofile(globus) {
	
	console.log("start flight profile");
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
	document.getElementById("btnFlightProfile").onclick = function () {
		
		if (show) {
			show = false;
			document.getElementById("btnFlightProfile").innerText = "Hide Flight Profile";
			if (first) {
				first = false
				document.getElementById("btnFlightProfile").disabled = true

				// init progress bar.
				initProgressBar();
				initWorker();
				
				// use ajax to get the data 
				$.ajax( {
					method: 'get',
					url :  "trajectory/flightprofile",
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
						console.log("Error - delete old bookings: " + status + " SVP veuillez contactez votre administrateur");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnFlightProfile").disabled = false
					},
				} );
				
			} else {
				layerKML.setVisibility(true);
				rayLayer.setVisibility(true);
			}
		} else {
			show = true;
			document.getElementById("btnFlightProfile").innerText = "Show Flight Profile";
			layerKML.setVisibility(false);
			rayLayer.setVisibility(false);
		}
	};
}