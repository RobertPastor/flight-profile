

document.addEventListener('DOMContentLoaded', (event) => {
    //the event occurred
		  
	let MinLongitude = -130.
	let MinLatitude = 25.
	let MaxLongitude = -70.
	let MaxLatitude = 50.
	let viewExtent = [MinLongitude , MinLatitude, MaxLongitude, MaxLatitude]
	setTimeout( function() {
		initMain(viewExtent);
		} , 500 );
	
})

function initMain(viewExtent) {
	console.log("init Main ");
	let osm = new og.layer.XYZ("OpenStreetMap", {
            isBaseLayer: true,
            url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            visibility: true,
            attribution: 'Data @ OpenStreetMap contributors, ODbL'
    });
	    
    // a HTMLDivElement which its id is `globus`
    let globus = new og.Globe({
            "target": "globus", 
            "name": "Earth",
            "terrain": new og.terrain.GlobusTerrain(),
            "layers": [osm],
            "autoActivated": true,
            "viewExtent": viewExtent
    });
	
	// load the airline airports
	airports(globus);
	
	// load the airline routes waypoints
	wayPoints(globus, viewExtent)
	
	// load a flight profile
	showFlightProfile(globus);
	
	// compute Flight Profile
	computeFlightProfile(globus);
	
	globus.planet.events.on("layeradd", function (e) {
		
		console.log("layeradd event");
		if (e.pickingObject instanceof og.Layer) {
            console.log(e.pickingObject.name);
        }
    });
	
}




