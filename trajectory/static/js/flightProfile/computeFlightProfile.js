
document.addEventListener('DOMContentLoaded', (event) => { 
       
	console.log("compute flight profile js is loaded");
	 
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	$("#launchComputeId").hide();

}); 

// What happens when the mouse move -> show the annotations at the right positions.
function mouseover() {
		focus.style("opacity", 1)
		focusText.style("opacity",1)
}

function mousemove(domElement) {
		// recover coordinate we need
		var x0 = x.invert(d3.pointer(domElement)[0]);
		var i = bisect(data, x0, 1);
		try {
			selectedData = data[i]
			focus
				.attr("cx", x(selectedData.x))
					  .attr("cy", y(selectedData.y))
			focusText
				.html("x:" + selectedData.x + "  -  " + "y:" + selectedData.y)
				.attr("x", x(selectedData.x) + 15)
				.attr("y", y(selectedData.y))
		} catch (err) {
			console.log(JSON.stringify(err))
		}
}
				
function mouseout() {
		focus.style("opacity", 0)
		focusText.style("opacity", 0)
}

function populateAircraftSelector( airlineAircraftsArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeFlightProfileId").show();
	// aircraftSelectionId
	$("#aircraftSelectionId").show();

	for (var index = 0; index < airlineAircraftsArray.length; index++) {
      $('#airlineAircraftId').append('<option value="' + airlineAircraftsArray[index]["airlineAircraftICAOcode"] + '">' + airlineAircraftsArray[index]["airlineAircraftFullName"] + '</option>');
	}
}

function populateAirlineRoutesSelector( airlineRoutesArray ) {
	
	// trComputeFlightProfileId
	$("#trComputeFlightProfileId").show();
	// routesSelectionId
	$("#routesSelectionId").show();

	for (var index = 0; index < airlineRoutesArray.length; index++) {
		var airlineRouteName = airlineRoutesArray[index]["DepartureAirport"] + " -> " + airlineRoutesArray[index]["ArrivalAirport"];
		var airlineRouteKey = airlineRoutesArray[index]["DepartureAirportICAOCode"] + "-" + airlineRoutesArray[index]["ArrivalAirportICAOCode"];
		$('#airlineRouteId').append('<option value="' + airlineRouteKey + '">' + airlineRouteName + '</option>');
	}
}

function loadOneFlightProfileWayPoint( layerWayPoints, waypoint ) {
	
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
					src: "/static/images/marker.png",
					width: 16,
					height: 16,
					offset: [0, -2]
				    }
	}));
				
}

function loadFlightProfileWayPoints( layerWayPoints, dataJson) {
	
	// get all waypoints
	var waypoints = eval(dataJson['waypoints']);

	// add the waypoints
	for (var wayPointId = 0; wayPointId < waypoints.length; wayPointId++ ) {
		// insert one waypoint
		loadOneFlightProfileWayPoint( layerWayPoints, waypoints[wayPointId] );
	}
}

function loadFlightProfileOneAirport( layerAirports, airport ) {
	
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
		if ( placeMark["name"].includes("turn") || placeMark["name"].includes("ground") 
			|| placeMark["name"].includes("climb") || placeMark["name"].includes("touch") ) {
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
	for (let placeMarkId = 0; placeMarkId < placeMarks.length; placeMarkId++ ) {
		// insert one waypoint
		loadOneRay( rayLayer, placeMarks[placeMarkId] );
	}
}

function removeAllChilds (parent) {
    while (parent.lastChild) {
        parent.removeChild(parent.lastChild);
    }
};

function showErrors ( jsonErrors ) {
	
	const dialog = document.getElementById("dialogId");
	removeAllChilds(dialog)
	$("#dialogId")
			.dialog({
               autoOpen: false,
			   title: "Compute Flight Profile Error",
			   modal: true,
               hide: "puff",
               show : "slide",
               height: 200      
            })
			.html(JSON.stringify(jsonErrors))
			.dialog('open'); 
}

function createKMLLayer(globus , layerName ) {
	
	let finalLayerName = "FlightProfile-" + layerName 
	removeLayer( globus , finalLayerName )
	
	let layerKML = new og.layer.KML( finalLayerName , {
		billboard: { 
			src: '/static/images/move_down_icon.png', 
			color: '#6689db' ,
			width : 4,
			height : 4
			},
		color: '#6689db'
	} ) ;
	layerKML.addTo(globus.planet);
	return layerKML;
}

function createRayLayer(globus , layerName ) {
	
	let finalLayerName = "Rays-" + layerName
	removeLayer( globus , finalLayerName )

	//polygonOffsetUnits is needed to hide rays behind globe
	let rayLayer = new og.layer.Vector( finalLayerName , { polygonOffsetUnits: 0 });
	rayLayer.addTo(globus.planet);
	return rayLayer;
}


function displayD3LineChart( arrayAltitudeMSLtime ) {
	
	// set the dimensions and margins of the graph
	var margin = {top: 10, right: 30, bottom: 10, left: 50}
    var width = 700 - margin.left - margin.right;
    var height = 700 - margin.top - margin.bottom;
	
	var data =  arrayAltitudeMSLtime["groundTrack"] 
	
	var parentDiv = document.getElementById("globusDivId");
	
	width = parentDiv.clientWidth - margin.left - margin.right; 
	height = parentDiv.clientHeight - margin.top - margin.bottom;
	
	var topTable = document.getElementById("mainTableId")
	height = height - topTable.clientHeight

	// append the svg object to the body of the page
	removeAllChilds (document.getElementById("dialogId"))
	
	// Creating a div element at the end
    $("#dialogId").append('<div id="d3vizId" style="width: 100%; height: 100%;"></div>');   
	
	var svg = d3.select("#d3vizId")
		.data(data)
		.append("svg")
		.attr("width", width)
		.attr("height", height)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
			  
	let maxX = arrayAltitudeMSLtime["maxElapsedTimeSeconds"]
		
	// Add X axis --> it is a integer format
	var x = d3.scaleLinear()
		.domain([1,maxX ])
		.range([ 0, width ]);
	
	// .attr("transform", "translate(0," + height + ")")
	// the axis will appear on the top
	svg.append("g")
		.call(d3.axisBottom(x));
		
	// x Axis label
	svg.append("text")
		.attr("class", "x label")
		.attr("text-anchor", "end")
		.attr("x", width - 60)
		.attr("y", 30)
		.text("duration time (seconds)");
			
	let maxY = arrayAltitudeMSLtime["MaxAltitudeMSLmeters"]
	
	// create Y axis
	var y = d3.scaleLinear()
			.domain([0, maxY + 1000])
			.range([ height, 0 ]);
	// add Y axis
	svg.append("g")
			.call(d3.axisLeft(y));
			
	// add Y axis label
	svg.append("text")
		.attr("class", "y label")
		.attr("text-anchor", "end")
		.attr("y", 6)
		.attr("dy", ".75em")
		.attr("transform", "rotate(-90)")
		.text("Altitude Mean Sea Level (meters)");
			
	// This allows to find the closest X index of the mouse:
	var bisect = d3.bisector(function(d) { return d.x; }).left;

	// Create the circle that travels along the curve of chart
	var focus = svg.append('g')
			.append('circle')
			.style("fill", "yellow")
			.attr("stroke", "black")
			.attr('r', 8.5)
			.style("opacity", 0)
			
	function getBB(selection) {
		selection.each(function(d){
			d.bbox = this.getBBox();
		})
	}

	// Create the text that travels along the curve of chart
	var focusText = svg.append('g')
			.append('text')
			.style("opacity", 1)
			.attr("text-anchor", "left")
			.attr("alignment-baseline", "middle")
			.call(getBB);   
			
	focusText.insert("rect","text")
		.attr("width", function(d){return d.bbox.width})
		.attr("height", function(d){return d.bbox.height})
		.style("fill", "yellow");

	// Add the line
	svg.append("path")
		.attr("class", "line")
		.attr("stroke", "#32CD32")
		.attr("stroke-width", 1.2)
		.attr("fill", "#FFFFFF")
		.attr("d", d3.line()
		  .x(function(d) {
				// assumption that data has x element
				return x(d.x) 
			})
		  .y(function(d) { 
				return y(d.y) 
			})
		  )
		  
	var path = svg.selectAll("dot")
		 .data(data)
		 .enter().append("circle")
		 .attr("r", 0.5)
		 .attr("cx", function (d) {
			   return x(d.x);
		 })
		 .attr("cy", function (d) {
			  return y(d.y);
		 })
		 .attr("stroke", "#32CD32")
		 .attr("stroke-width", 0.5)
		 .attr("fill", "#FFFFFF");

	// Create a rect on top of the svg area: this rectangle recovers mouse position
	svg.append('rect')
		.style("fill", "none")
		.style("pointer-events", "all")
		.attr('width', width)
		.attr('height', height)
		.on('mouseover', mouseover)
		.on('mousemove', mousemove)
		.on('mouseout', mouseout)
		.on('dblclick',function(node) { 
			//console.log("node was double clicked");
			$("#d3vizId").hide();
			//$("#globusDivId").show()
	})

	// show the vertical profile
	$("#dialogId")
			.dialog({
               autoOpen: false,
			   title: "Compute Flight Profile",
			   modal: true,
               hide: "puff",
               show : "slide",
               height: "auto",
			   width: "auto",
			   maxHeight: true,
			   maxWidth: true
            })
			.html(document.getElementById('d3vizId').innerHTML)
			.dialog('open'); 

	// show the svg
	//$("#d3vizId").show();
	//$("#globusDivId").hide()
}

function launchFlightProfile(globus) {
	
	globus.planet.events.on("layeradd", function (e) {
		
		console.log("layeradd event");
		if (e.pickingObject instanceof og.Layer) {
            console.log(e.pickingObject.name);
			
        }
		stopBusyAnimation();
    });
	
	console.log( "compute flight profile ");
	
	/**
	let layerFlightProfileWayPoints = new og.layer.Vector("FlightProfileWayPoints", {
			billboard: { 
				src: '/static/trajectory/images/marker.png', 
				color: '#6689db' ,
				width : 4,
				height : 4
				},
            clampToGround: true,
            });
	layerFlightProfileWayPoints.addTo(globus.planet);
	*/
	    
	$("#trComputeFlightProfileId").hide();
	$("#aircraftSelectionId").hide();
	$("#routesSelectionId").hide();
	
	let show = true;
	
	/**
	* monitor the button used to show the table with the inputs
	* it allows only to choose the aircraft, the route before clicking to launch the profile computation
	**/
	document.getElementById("btnLaunchFlightProfile").onclick = function () {

		if (show) {
			show = false;
			//document.getElementById("btnLaunchFlightProfile").disabled = true
			
			$('#tableFlightProfileId').show();
			
			// change name on the button
			document.getElementById("btnLaunchFlightProfile").innerText = "Hide Flight Profile";

			// use ajax to get the data 
			$.ajax( {
					method: 'get',
					url :  "trajectory/launchFlightProfile",
					async : true,
					success: function(data, status) {
									
						//alert("Data: " + data + "\nStatus: " + status);
						var dataJson = eval(data);
						// airlineAircrafts
						populateAircraftSelector( dataJson["airlineAircrafts"] );
						populateAirlineRoutesSelector( dataJson["airlineRoutes"] );
						
						$("#launchComputeId").show();
						
					},
					error: function(data, status) {
						console.log("Error - launch Flight Profile: " + status + " Please contact your admin");
					},
					complete : function() {
						stopBusyAnimation();
						document.getElementById("btnLaunchFlightProfile").disabled = false
					},
			});
		} else {
			show = true;
			//document.getElementById("btnLaunchFlightProfile").disabled = true
			document.getElementById("btnLaunchFlightProfile").innerText = "Show Flight Profile";
			$('#tableFlightProfileId').hide();
		}
	} 
	 
	/**
	* monitor the button used to launch the profile computation
	**/
	let once = false;
	//document.getElementById("btnComputeFlightProfile").disabled = true
	document.getElementById("btnComputeFlightProfile").onclick = function () {
	
		console.log ("button compte flight profile pressed");
	
		document.getElementById("btnComputeFlightProfile").disabled = true
		
		let aircraft = $("#airlineAircraftId option:selected").val()
		let route =  $("#airlineRouteId option:selected").val()
		
		// init progress bar.
		initProgressBar();
		initWorker();
		
		$.ajax( {
					method: 'get',
					url :  "trajectory/computeFlightProfile",
					async : true,
					data: 'aircraft=' + aircraft + '&route=' + route ,
					success: function(data, status) {
						
						var dataJson = eval(data);
						if ( dataJson.hasOwnProperty("errors") ) {
							stopBusyAnimation();
							showErrors( dataJson["errors"] );
							
						} else {
							// create layers does also a delete layer if name found
							let layerKML = createKMLLayer(globus , route);
							let rayLayer = createRayLayer(globus , route)
							
							// convert JSON to XML
							var x2js = new X2JS();
							var xml = x2js.js2xml(dataJson["kmlXMLjson"]);
							
							let parser = new DOMParser();
							let xmlDoc = parser.parseFromString(xml, "text/xml");
							
							layerKML.addKmlFromXml( kmlAsXml = xmlDoc , color = null , billboard = null );
							
							// add rays to Rays layer
							addRays( rayLayer , dataJson["placeMarks"] );
							
							let arrayAltitudeMSLtime = dataJson["csvAltitudeMSLtime"]
							displayD3LineChart(arrayAltitudeMSLtime);
							
						}
					},
					error: function(data, status) {
						alert("Error - compute Flight Profile: " + status + " Please contact your admin");
						showErrors( eval(data) );
					},
					complete : function() {
						//stopBusyAnimation();
						document.getElementById("btnComputeFlightProfile").disabled = false
					},
			});
	}
}