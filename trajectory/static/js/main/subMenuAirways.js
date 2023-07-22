

class AirlineRoutesAirwaysSubMenu extends og.Control {
	
	constructor(options) {
		super(options);
	}
	
	oninit() {
		//console.log("main Control - oninit");
	}
	
	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "mainSubMenuAirwaysDivId";
		mainDiv.classList.add('mainControlSubMenu');
		
		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		let row_0 = document.createElement('tr');
				
		let row_0_data_3 = document.createElement('td');
		row_0_data_3.innerHTML = '<div><button id="btnAirports" >Airports</button></div>';
		row_0_data_3.title = "click to see the airline airports and the waypoints";
		row_0.appendChild(row_0_data_3);
		
		let row_0_data_4 = document.createElement('td');
		row_0_data_4.innerHTML = '<div><button id="btnAirlineRoutes" >Airways</button></div>';
		row_0_data_4.title = "click to see the routes, way-points, best runway";
		row_0.appendChild(row_0_data_4);
		
		// ---------------
		tbody.appendChild(row_0);
		
		table.appendChild(tbody);
		mainDiv.appendChild(table);
		
		this.renderer.div.appendChild(mainDiv);
		
		// start hiding this table
		$("#mainSubMenuAirwaysDivId").hide();
		
	}
}



