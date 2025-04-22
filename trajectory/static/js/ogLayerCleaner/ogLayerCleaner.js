import { removeLayer } from "../main/main.js";

export const SingletonOgLayerCleaner = (function () {
	
	let instance;

    function createInstance() {
        let object = new OgLayerCleaner();
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

function deleteLayer( element ) {
		// should return an element id
		let globus = SingletonOgLayerCleaner.getInstance().getGlobus();
		//console.log ( element.id );
		let layerName = element.id;
		//console.log( layerName );
		let ogLayer = globus.planet.getLayerByName( layerName );
		if ( ogLayer ) {
			//console.log( "layer with name = " + layerName + " is existing in OG");
			/**
			 * @TODO remain -> following global function defined in main.js
			 **/ 
			removeLayer( globus , layerName );
			//console.log( "layer is now removed");
			SingletonOgLayerCleaner.getInstance().cleanTableRow( element );
			// if there are no more rows 
			let mainTableId = SingletonOgLayerCleaner.getInstance().getOgCleanerControl().getMainTableId();
			let rowCount = $('#'+mainTableId+' tr').length;
			// table row has not been deleted yet -> hence row count is 1
			if ( rowCount == 1 ) {
				let mainDivId = SingletonOgLayerCleaner.getInstance().getOgCleanerControl().getMainDivId();
				document.getElementById(mainDivId).style.visibility = 'hidden';
				
			}
		}
}


class OgLayerCleaner {
	
	constructor() {
		//console.log("og Layer Cleaner constructor") 
	}
	
	cleanTableRow( element ) {
		$("#"+element.id).closest('tr').remove();
	}
	
	getGlobus() {
		return this.globus;
	}
	
	getOgCleanerControl() {
		return this.ogLayerCleanerControl;
	}
	
	init(globus, ogLayerCleanerControl) {
		this.globus = globus;
		this.ogLayerCleanerControl = ogLayerCleanerControl;
	}
	
	addLayer( layerName, airlineName , Adep, Ades ){
		
		let mainDiv = this.ogLayerCleanerControl.getMainDivId();
		document.getElementById(mainDiv).style.visibility = 'visible';
		
		let mainTableId = this.ogLayerCleanerControl.getMainTableId();
		$("#"+mainTableId).find('tbody')
			.append($('<tr>')
				.append($('<td>')
						.append( airlineName )
				)
				.append($('<td>')
						.append( Adep )
				)
				.append($('<td>')
						.append( Ades )
				)
				.append($('<td>')
						.append( layerName )
				)
				.append($('<td id="tdButtonId" >')
					.append ( " <input type='button' title='click to temove the layer' id='buttonLayerId' style='width:100%; height:100%;' value='Delete'  /> " )
				)
			)
			
		// on the fly correct button id
		let elemButton = document.getElementById('buttonLayerId');
		// id of the button equals name of the layer
		elemButton.id = layerName;
		/**
		* on click function 
		*/
		$('#'+elemButton.id).click(function () {
			//console.log("button show route clicked") 
			// this represents the id of the html button element
			deleteLayer( this );
		});
	}	
}