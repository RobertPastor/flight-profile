const SingletonMetars = (function () {
	
	let instance;
    function createInstance() {
        let object = new Metars();
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


class Metars {
	
	constructor() {
	}
	
	getGlobus() {
		return this.globus;
	}
	
	hideMetarsDiv() {
		let metarMainDivId = this.metarsOgControl.getMainDivId();
		$('#' + metarMainDivId).hide();
	}
	
	showOneMetarResult( oneMetarJson ) {
		
		$("#airportsMetarsTableId")
			.find('tbody')
			.append($('<tr>')

				.append('<td>'+ oneMetarJson["AirportICAOcode"] +'</td>')
				.append('<td>'+ oneMetarJson["AirportName"] +'</td>')
				.append('<td>'+ oneMetarJson["DateTimeUTC"] +'</td>')
				
				.append('<td>'+ oneMetarJson["MetarType"] +'</td>')
				
				.append('<td>'+ oneMetarJson["TemperatureCelsius"] +'</td>')
				.append('<td>'+ oneMetarJson["DewPointCelsius"] +'</td>')
				
				.append('<td>'+ oneMetarJson["WindSpeedKt"] +'</td>')
				.append('<td>'+ oneMetarJson["WindDirectionCompass"] +'</td>')
				.append('<td>'+ oneMetarJson["WindDirectionDegrees"] +'</td>')
				
				.append('<td>'+ oneMetarJson["WindGustKt"] +'</td>')
				.append('<td>'+ oneMetarJson["SeaLevelPressureHpa"] +'</td>')

			);
		
	}
	
	populateMetars( metarsArray ) {
		
		$('#airportsMetarsTableId tbody').empty();
		
		for (let metarId = 0; metarId < metarsArray.length; metarId++ ) {
			
			let oneMetarJson = metarsArray[metarId];
			SingletonMetars.getInstance().showOneMetarResult(oneMetarJson);
		}
	}
	
	initMetars( globus , metarsOgControl ) {
		
		this.globus = globus;
		this.metarsOgControl = metarsOgControl;
		
		// listen to the button define in MainControl.js
		document.getElementById("btnMetar").onclick = function () {
			
			if ( ! $('#airportsMetarsMainDivId').is(":visible") ) {
			
				// get the name of the airline
				let airlineName = SingletonMainClass.getInstance().getSelectedAirline();
				
				SingletonMainClass.getInstance().enableDisableMainMenuButtons(false);
				// init progress bar.
				initProgressBar();
				initWorker();

				// use ajax to get the data 
				$.ajax( {
						method: 'get',
						url :  "trajectory/metar/" + airlineName,
						async : true,
						success: function(data) {
										
							//alert("Data: " + data + "\nStatus: " + status);
							let dataJson = eval(data);
							// metars
							SingletonMetars.getInstance().populateMetars( dataJson["metars"] );
							
							$('#airportsMetarsMainDivId').show();
						},
						error: function(data, status) {
							console.log("Error - Metars : " + status + " Please contact your admin");
							showMessage("Error - Metars ", eval(data) );
						},
						complete : function() {
							stopBusyAnimation();
							SingletonMainClass.getInstance().enableDisableMainMenuButtons(true);
						},
				});
				
			} else {
				SingletonMetars.getInstance().hideMetarsDiv();
			}
		}
	}
	
}
	