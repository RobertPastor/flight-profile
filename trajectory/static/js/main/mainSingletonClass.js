
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
	
}