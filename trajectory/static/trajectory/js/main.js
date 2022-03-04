document.addEventListener('DOMContentLoaded', (event) => {
    //the event occurred
		  
	init()
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
	
	airports(globus);
	
}

function airports(globus) {
	
	
	let layerVector = new og.layer.Vector("Airports", {
                clampToGround: true
            });
	layerVector.addTo(globus.planet);
	    
	let show = true;
    	
    document.getElementById("btnAirports").onclick = function () {
            
        if (show) {
			show = false;
			document.getElementById("btnAirports").innerText = "Hide Airports";
			layerVector.add(new og.Entity({
				    lonlat: [-84.428067, 33.636719],
				    label: {
					text: "Atlanta",
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
		} else {
			show = true;
			document.getElementById("btnAirports").innerText = "Show Airports";
			let entities = layerVector.getEntities();
			layerVector.removeEntities(entities);
		}
    };
}
