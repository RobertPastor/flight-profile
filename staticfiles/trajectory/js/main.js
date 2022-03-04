document.addEventListener('DOMContentLoaded', (event) => {
    //the event occurred
		  
	init();
})

function init() {
	
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
            autoActivated: true,
            viewExtent: [-130. , 25. , -70. , 50. ]
    });
	// load the airports
	airports(globus);
	
}




