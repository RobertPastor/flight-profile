

document.addEventListener('DOMContentLoaded', (event) => {
    //the event occurred
	
	
		  
	let MinLongitude = -130.
	let MinLatitude = 25.
	let MaxLongitude = -70.
	let MaxLatitude = 50.
	let viewExtent = [MinLongitude , MinLatitude, MaxLongitude, MaxLatitude]
	initMain(viewExtent);
})

function initMain(viewExtent) {
	
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
	// load the airports
	airports(globus);
	// load a flight profile
	flightprofile(globus);
	
}




