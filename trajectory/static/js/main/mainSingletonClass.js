
const SingletonMainClass = (function () {
	
	let instance;
    function createInstance() {
        var object = new MainClass();
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


class MainClass {
	
	constructor( ) {
	}
	
	init ( globus ) {
		this.globus = globus;
	}
	
	setExtent( waypointsArray ) {
		
		if ( Array.isArray ( waypointsArray ) == false ) {
			return;
		}
		
		let longitudeArr = [];
		let latitudeArr = [];
		for (let wayPointId = 0; wayPointId < waypointsArray.length; wayPointId++ ) {
			
			let waypoint = waypointsArray[wayPointId];
			let longitude = 0.0;
			if ( waypoint.hasOwnProperty("Longitude")) {
				longitude = parseFloat(waypoint.Longitude);
				longitudeArr.push(longitude);
			}
			let latitude = 0.0;
			if ( waypoint.hasOwnProperty("Latitude")) {
				latitude = parseFloat(waypoint.Latitude);
				latitudeArr.push(latitude);
			}
		}
		let MinLongitude = Math.min.apply(Math, longitudeArr);
		// take some margin to see airports
		MinLongitude = Math.min(MinLongitude - 2, MinLongitude);
		
		let MaxLongitude = Math.max.apply(Math, longitudeArr);
		MaxLongitude = Math.max(MaxLongitude + 2, MaxLongitude);

		let MinLatitude = Math.min.apply(Math, latitudeArr);
		MinLatitude = Math.min(MinLatitude - 2, MinLatitude);
		
		let MaxLatitude = Math.max.apply(Math, latitudeArr);
		MaxLatitude = Math.max(MaxLatitude + 2, MaxLatitude);
		
		let SouthWest = new og.LonLat( parseFloat(MinLongitude) , parseFloat(MinLatitude) , parseFloat("0.0") );
		let NorthEast = new og.LonLat( parseFloat(MaxLongitude) , parseFloat(MaxLatitude) , parseFloat("0.0") );
		let viewExtent = new og.Extent( SouthWest , NorthEast );
		this.globus.planet.viewExtent(viewExtent);
		
	}
	
	// 30th July 2023 
	getSelectedAirline() {
		// encode URI component as this airline name will be used as a argument of an URL
		return encodeURIComponent($("#airlineSelectId option:selected").val());
	}
	
	// 10th September 2023 - get standard label
	getStandardOgLabel(name) {
		return {text: name,
				outline: 0.58,
				outlineColor: "rgba(255,255,255,.4)",
				size: 10,
				color: "black",
				offset: [0, -2]};
	}
	
	// retrieve a standardized marker
	getStandardOgBillBoard() {
		return {src: "/static/images/marker.png",
				width: 16,
				height: 16,
				offset: [0,-2]};
	}
	
	enableDisableMainMenuButtons(enable) {
		const buttonNames = ["btnAirlineFleet","btnAirwaysId", "btnAirports",
							"btnLaunchFlightProfile","btnLaunchAirlineCosts","btnOptimizationsId","btnLaunchCostsOptimization", "btnLaunchCASM",
							"btnLaunchCasmOptimization","btnLaunchSeatMilesMaximization","btnLaunchFuelPlanner","btnMetar",
							"btnComputeFlightProfileId","btnComputeCostsId","btnDownLoadVerticalProfileId","btnDownLoadKMLfileId"];
		if ( enable ) {
			for (const button of buttonNames) { 
				document.getElementById(button).disabled = false;
			}
		} else {
			for (const button of buttonNames) { 
				document.getElementById(button).disabled = true;
			}
		}
	}
}