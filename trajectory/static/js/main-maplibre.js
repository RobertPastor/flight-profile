var worker = undefined;

document.addEventListener('DOMContentLoaded', (event) => {
	
	console.log("document is loaded");
	var mapLibre = new maplibregl.Map({
			container: 'map', // container id
			//style: 'https://demotiles.maplibre.org/style.json', // style URL
			style: 'https://api.maptiler.com/maps/basic/style.json?key=clQgrZvyCGsbZgyRzmPo',
			center: [-96.0, 38.0], // starting position [lng, lat]
			zoom: 4 // starting zoom
	});
		
	init(mapLibre);
	
});

function init(map) {
	
	if (map) {
		map.on('load', function () {
			console.log("map is loaded")
		});
	}
	
}

function stopBusyAnimation(){
	console.log("stop busy anymation");
	stopWorker();
	initProgressBar();
}


function initProgressBar() {
    // Gets the number of image elements
    var numberOfSteps = 100;
    var progressBar = document.getElementById('workerId');
    if (progressBar) {
        progressBar.style.width = "0" + '%';
    }
}

function stopWorker() {
	if (worker) {
		worker.terminate();
	}
    worker = undefined;
    console.log("worker is stopped !!!");
    // hide the progress bars
}


function initWorker() {
	
	if (typeof (Worker) !== "undefined") {
        console.log("Yes! Web worker is supported !");
        // Some code.....
        if (typeof (worker) == "undefined") {
            worker = new Worker("/static/js/worker/worker.js");
            worker.onmessage = function (event) {
				
				//console.log(`message received - ${event.data}`);

                var progressBar = document.getElementById('workerId');
				if (progressBar) {
					progressBar.style.width = event.data + '%';
					progressBar.innerText = event.data + '%';
				}
            };
        }
    } else {
        // Sorry! No Web Worker support..
		console.log("Sorry! no web worker support ...");
    }
}