import { Entity , Vector , LonLat , Ellipsoid , math  } from "../og/og.es.js";
import { removeLayer } from "../main/main.js";

const POINTS_NUMBER = 30;

export class PolyLine {
	
	constructor( sidStarPattern ) {
		//console.log("Polyline constructor");
		this.sidStarPattern = sidStarPattern.replaceAll ( "/" , "-" );
	}
	
	getLayerName() {
		let sidStarPattern = this.sidStarPattern ;
		return "Sid-Star-Polyline-" + sidStarPattern;
	}
	
	removeLayer () {
		
		let globus = this.globus;
		let layerName = this.getLayerName();
		/**
		 * @todo defined in main.js
		 */
		removeLayer(globus, layerName);
		
	}
	
	init( globus, wayPointsArr ) {
		
		this.globus = globus;
		
		this.paths = [];
        this.colors = [];
        this.animIndex = [];
		
		if ( Array.isArray(wayPointsArr)) {
		
			for ( let wayPointId  = 0; wayPointId < wayPointsArr.length; wayPointId++ ) {
			
				let srcWayPoint = wayPointsArr[wayPointId]["src"];
				let dstWayPoint = wayPointsArr[wayPointId]["dst"];
				
				if ( srcWayPoint.hasOwnProperty("Longitude") && srcWayPoint.hasOwnProperty("Latitude") && 
					dstWayPoint.hasOwnProperty("Longitude") && dstWayPoint.hasOwnProperty("Latitude") )  {
										
					let src = new LonLat( Number(srcWayPoint["Longitude"] ), Number( srcWayPoint["Latitude"] ) );
					let dst = new LonLat( Number(dstWayPoint["Longitude"] ), Number( dstWayPoint["Latitude"] ) );
					
					let path = this.getPath( globus.planet.ellipsoid, src, dst );
					
					this.paths.push(path.path);
	        		this.colors.push(path.colors);
	            
	        		this.animIndex.push(math.randomi(0, POINTS_NUMBER));
				}
			}
		}
	}
	
	draw() {
		
		let globus = this.globus ;
       	let entity = new Entity({
                    'polyline': {
	                    'path3v': this.paths,
	                    'pathColors': this.colors,
	                    'thickness': 10.0,
                        'color': "blue",
                        'isClosed': false
                    }
        });
        let layerName = this.getLayerName();
        let collection = new Vector(layerName, {
	            	'entities': []
	    });
	    collection.add( entity );
	    collection.addTo( globus.planet );
	    // show some animation along the line between each SID or STAR waypoint
	    globus.planet.renderer.handler.defaultClock.setInterval(30, () => {
			try {
                    let e = collection.getEntities()[0].polyline;
                    let cArr = e.getPathColors();
                    for (let i = 0; i < cArr.length; i++) {
                        this.animIndex[i]++;
                        let ind = this.animIndex[i];
                        if (ind > POINTS_NUMBER + 4) {
                            this.animIndex[i] = 0;
                            ind = 0;
                        }
                        let r = this.colors[i][0][0],
                            g = this.colors[i][0][1],
                            b = this.colors[i][0][2];
                        e.setPointColor([r, g, b, 0.8], ind, i);
                        e.setPointColor([r, g, b, 0.6], ind - 1, i);
                        e.setPointColor([r, g, b, 0.3], ind - 2, i);
                        e.setPointColor([r, g, b, 0.1], ind - 3, i);
                        e.setPointColor(this.colors[i][ind] || this.colors[i][POINTS_NUMBER - 1], ind - 4, i);
                    }
          	} catch (err) {
				//console.error(JSON.stringify(err));
				//globus.planet.renderer.handler.defaultClock.clearInterval();
			}
        });
        return layerName;
	}
	
	getPath(ell, start, end) {
		 
         let num = POINTS_NUMBER;
		// getInitialBearing no more in Ellipsoid for og 0.25.0
         let brng = Ellipsoid.getBearing(start, end);
         let dist = ell.getGreatCircleDistance(start, end);

         let p25 = ell.getGreatCircleDestination(start, brng, dist * 0.25);
         let p75 = ell.getGreatCircleDestination(start, brng, dist * 0.75);

         start.height = 50;
         end.height = 50;
         
         let h = dist / 4;
         p25.height = h;
         p75.height = h;

         let startCart = ell.lonLatToCartesian(start),
                endCart = ell.lonLatToCartesian(end),
                p25Cart = ell.lonLatToCartesian(p25),
                p75Cart = ell.lonLatToCartesian(p75);

         let path = [];
         let colors = [];
         
         let color = [math.random(0, 2), Math.random(0, 2), Math.random(0, 2)];
         for (let i = 0; i <= num; i++) {
             let cn = math.bezier3v(i / num, startCart, p25Cart, p75Cart, endCart);
             path.push(cn);
             colors.push([color[0], color[1], color[2], 0.1]);
         }
         return {
                path: path,
                colors: colors
         };
     }
}