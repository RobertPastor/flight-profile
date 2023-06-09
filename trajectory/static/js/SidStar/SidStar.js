
const SingletonSidStar = (function () {
	
	let instance;

    function createInstance() {
        let object = new SidStar();
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


class SidStar {
	
	constructor() {
		//console.log("SID STAR constructor");
	}
	
	getButtonId() {
		return "btnSidStar";
	}
	
	getGlobus() {
		return this.globus;
	}
	
	showSidStar( dataJson, showHide ) {
		
		
	}
	
	showHideAllSidStar( showHide ) {
		
		// init progress bar.
		initProgressBar();
		initWorker();
		
		// get the name of the airline
		let airlineName = $("#airlineSelectId option:selected").val();
		airlineName = encodeURIComponent(airlineName);

		// use ajax to get the data 
		// only show Sid Star for the airports of the current airline
		$.ajax( {
				method: 'get',
				url :  "trajectory/showSidStar/" + airlineName,
				async : true,
				success: function(data, status) {
					
					stopBusyAnimation();
					//alert("Data: " + data + "\nStatus: " + status);
					let dataJson = eval(data);
					
					SingletonSidStar.getInstance().showSidStar( dataJson , showHide );	
				},
				error: function(data, status) {
					stopBusyAnimation();
					console.log("Error - show SID STAR : " + status + " Please contact your admin");
					showMessage ( "Error - show SID STAR" , data );
				},
				complete : function() {
					stopBusyAnimation();
					document.getElementById(SingletonSidStar.getInstance().getButtonId()).disabled = false
				}
		} );
		
	}
	
	initSidStar( globus ) {
		
		// 9th May 2023 - class attributes
		this.globus = globus;
		
		if ( !document.getElementById(SingletonSidStar.getInstance().getButtonId()) ) {
			console.error("button Sid Star is not declared");
			return;
		}
		let show = true;
		
		document.getElementById(SingletonSidStar.getInstance().getButtonId()).onclick = function () {
			console.log("button SID STAR clicked");
			
			if (show) {
				
				show = false;					
				SingletonSidStar.getInstance().showHideAllSidStar( true );
				
			} else {
				
				show = true;
				SingletonSidStar.getInstance().showHideAllSidStar( false );
				
			}
		}
	}
}