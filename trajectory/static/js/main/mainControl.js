
function listenSubMenuMeteoEntry( btnSubMenuMeteoId, mainSubMenuMeteoDivId ) {
	
	document.getElementById(btnSubMenuMeteoId).onclick = function () {
		
			let position =  $("#"+ btnSubMenuMeteoId).offset();
				
    		// show the submenu defined in SubMenuAirways.js
    		if ( document.getElementById(mainSubMenuMeteoDivId) ) {
				
				$("#" + mainSubMenuMeteoDivId).css({
					'position': 'absolute',
					'top': position.top + 5, // Leave some margin
					'left': position.left + 5 , // Leave some margin
					'display': 'block'
				});
				
				$("#"+ mainSubMenuMeteoDivId).show();
				
				document.getElementById(mainSubMenuMeteoDivId).addEventListener("mouseleave", function (e) {
					$("#"+ mainSubMenuMeteoDivId).hide();
				});
			}
    		return false;
		};
	
}


function listenSubMenuFuelEntry( btnSubMenuFuelId , mainSubMenuFuelDivId) {
	
	document.getElementById(btnSubMenuFuelId).onclick = function () {
		
			let position =  $("#"+ btnSubMenuFuelId).offset();
				
    		// show the submenu defined in SubMenuAirways.js
    		if ( document.getElementById(mainSubMenuFuelDivId) ) {
				
				$("#" + mainSubMenuFuelDivId).css({
					'position': 'absolute',
					'top': position.top + 5, // Leave some margin
					'left': position.left + 5 , // Leave some margin
					'display': 'block'
				});
				
				$("#"+ mainSubMenuFuelDivId).show();
				
				document.getElementById(mainSubMenuFuelDivId).addEventListener("mouseleave", function (e) {
					$("#"+ mainSubMenuFuelDivId).hide();
				});
			}
    		return false;
		};
}

function listenSubMenuOptimizationsEntry( btnOptimizationsId , mainSubMenuOptimizationsDivId) {
		
		document.getElementById(btnOptimizationsId).onclick = function () {
			
			//console.log("button Optimizations was clicked")
			let position =  $("#"+ btnOptimizationsId).offset();
				
    		// show the submenu defined in SubMenuOptimizations.js
    		if ( document.getElementById(mainSubMenuOptimizationsDivId) ) {
				
				$("#" + mainSubMenuOptimizationsDivId).css({
					'position': 'absolute',
					'top': position.top + 5, // Leave some margin
					'left': position.left + 5 , // Leave some margin
					'display': 'block'
				});
				
				$("#"+ mainSubMenuOptimizationsDivId).show();
				
				document.getElementById(mainSubMenuOptimizationsDivId).addEventListener("mouseleave", function (e) {
					$("#"+ mainSubMenuOptimizationsDivId).hide();
				});
			}
    		return false;
		};
}


function listenSubMenuAirwaysEntry( btnAirwaysId , mainSubMenuAirwaysDivId) {
		
		document.getElementById(btnAirwaysId).onclick = function () {
			
			//console.log("button airways was clicked")
			let position =  $("#"+ btnAirwaysId).offset();
				
    		// show the submenu defined in SubMenuAirways.js
    		if ( document.getElementById(mainSubMenuAirwaysDivId) ) {
				
				$("#" + mainSubMenuAirwaysDivId).css({
					'position': 'absolute',
					'top': position.top + 5, // Leave some margin
					'left': position.left + 5 , // Leave some margin
					'display': 'block'
				});
				
				$("#"+ mainSubMenuAirwaysDivId).show();
				
				document.getElementById(mainSubMenuAirwaysDivId).addEventListener("mouseleave", function () {
					$("#"+ mainSubMenuAirwaysDivId).hide();
				});
			}
    		return false;
		};
}


//Define custom control class
class MainControl extends og.Control {
	
	constructor(options) {
		super(options);
	}
	
	oninit() {
	}

	onadd() {
		
		let mainDiv = document.createElement('div');
		mainDiv.id = "mainTableId";
		mainDiv.classList.add('mainTable');
		
		let draggableMainDiv = document.createElement('div');
		draggableMainDiv.id = mainDiv.id  + "Header";
		draggableMainDiv.innerHTML = "Click here to move -> Main navigation bar ---> click to download a User Manual -->";
		draggableMainDiv.classList.add("draggableDivHeader");
		
		let span = document.createElement('span');
		span.id = "PdfPresentationId";
		span.innerHTML = "<a title='download a pdf presentation' id='linkDownloadPdfPresentationId' class='download' href='#' onclick='initDownloadPdfPresentation()' ></a>";
		draggableMainDiv.appendChild(span);
		
		mainDiv.appendChild(draggableMainDiv);

		let table = document.createElement('table');
		let tbody = document.createElement('tbody');
		
		//===================================
		// ------- 1st row --- progress bar
		//===================================
		
		let row_0 = document.createElement('tr');
		
		let row_0_data_1 = document.createElement('td');
		row_0_data_1.colSpan = "11";
		row_0_data_1.innerHTML = '<div id="workerId" class="w3-container progressBar" style="width:100%"></div>';
		row_0.appendChild(row_0_data_1);
						
		tbody.appendChild(row_0);
		
		//===================================================
		// ------- 2nd row --- select the airline -----------
		//===================================================
		
		let row_1 = document.createElement('tr');
		
		let row_1_data_1 = document.createElement('td');
		row_1_data_1.colSpan = "3";
		
		let div_1 = document.createElement('div');
		
		let select = document.createElement("select");
		select.id = "airlineSelectId";
		select.title = "click to select an airline";
		select.classList.add('airlineSelect');

		div_1.appendChild(select);
		row_1_data_1.appendChild(div_1);
		row_1.appendChild(row_1_data_1);
		
		let row_1_data_3 = document.createElement('td');
		row_1_data_3.colSpan = "7";
		
		row_1_data_3.innerHTML = '<div class="alignRight"><span>Fleet Management Tool proposed by </span><a href="https://www.appsintellect.org" target="_blank">appsintellect</a></div>';
		row_1.appendChild(row_1_data_3);
		
		let row_1_data_4 = document.createElement('td');
		row_1_data_4.colSpan = "1";
		
		row_1_data_4.classList.add('question_mark_bg')
		row_1_data_4.innerHTML = '<div id="helpId" class="question_mark" title="click to obtain some help" onclick="showHelp()" ></div>';
		row_1.appendChild(row_1_data_4);
		
		tbody.appendChild(row_1);
		
		//==================================================================
		// --------- 3rd row -----------------------------------------------
		// airfleet ... Airports ... Airways 
		//==================================================================
		
		let row_2 = document.createElement('tr');
		
		// airline fleet
		
		let row_2_data_2 = document.createElement('td');
		row_2_data_2.innerHTML = '<div><button id="btnAirlineFleet" >Fleet</button></div>';
		row_2_data_2.title = "click to see the airline fleet, aircrafts, number of seats, hourly costs ...";
		row_2.appendChild(row_2_data_2);
		
		//=============================================
		// sub menu Airports and Airways
		//=============================================

		let row_2_data_3 = document.createElement('td');
		row_2_data_3.id = "mainSubMenuTdId";
		row_2_data_3.colSpan = "2";
		
		let menuEntryAirwaysDiv = document.createElement('div');
		
		menuEntryAirwaysDiv.innerHTML = '<div><button id="btnAirwaysId" >Airports & Airways</button></div>';
		menuEntryAirwaysDiv.id = "menuEntryAirwaysDivId";
		menuEntryAirwaysDiv.title = "click to open a submenu for Airports & Airways";

		row_2_data_3.appendChild ( menuEntryAirwaysDiv );
		row_2.appendChild(row_2_data_3);
		
		//============
		// profile 
		//============
		let row_2_data_6 = document.createElement('td');
		row_2_data_6.innerHTML = '<div><button id="btnLaunchFlightProfile" >Profile</button></div>';
		row_2_data_6.title = "click to compute a profile, a cost or download an EXCEL profile";
		row_2.appendChild(row_2_data_6);
		
		// 27th January 2023 - Airline costs controls
		let row_2_data_7 = document.createElement('td');
		row_2_data_7.innerHTML = '<div><button id="btnLaunchAirlineCosts" >Costs</button></div>';
		row_2_data_7.title = "click to download an EXCEL costs file";

		row_2.appendChild(row_2_data_7);
		
		//=======================
		// sub menu optimizations
		//=======================
		let row_2_data_8 = document.createElement('td');
		row_2_data_8.id = "mainSubMenuOptimizationsTdId";
		row_2_data_8.colSpan = "3";
		
		let menuEntryOptimizationsDiv = document.createElement('div');
		menuEntryOptimizationsDiv.innerHTML = '<div><button id="btnOptimizationsId" >Optimizations</button></div>';
		menuEntryOptimizationsDiv.id = "menuEntryOptimizationsDivId";
		menuEntryOptimizationsDiv.title = "click to open a submenu for all optimizations";

		row_2_data_8.appendChild ( menuEntryOptimizationsDiv );
		row_2.appendChild(row_2_data_8);
		
		//=============
		// 13th May 2023 - add fuel subMenu
		//=============
		let row_2_data_12 = document.createElement('td');
		row_2_data_12.id = "mainSubMenuFuelTdId";

		let menuEntryFuelDiv = document.createElement('div');
		menuEntryFuelDiv.innerHTML = '<div><button id="btnSubMenuFuelId" >Fuel</button></div>';
		menuEntryFuelDiv.id = "menuEntryFuelDivId";
		menuEntryFuelDiv.title = "click to open a submenu for Fuel Efficiency and Fuel Planner";
		
		row_2_data_12.appendChild ( menuEntryFuelDiv );
		row_2.appendChild(row_2_data_12);
		
		//======
		// 22nd August 2024 -  metar and wind temperature
		//======
		let row_2_data_13 = document.createElement('td');
		row_2_data_13.id = "mainSubMenuMeteoTdId";
		
		let menuEntryMeteoDiv = document.createElement('div');
		menuEntryMeteoDiv.innerHTML = '<div><button id="btnSubMenuMeteoId" >Meteo</button></div>';
		menuEntryMeteoDiv.id = "menuEntryMeteoDivId";
		menuEntryMeteoDiv.title = "click to open a submenu for Metar and Wind Temperature";
		
		row_2_data_13.appendChild ( menuEntryMeteoDiv );
		row_2.appendChild(row_2_data_13);
		
		//===================
		// show configuration
		//===================
		let row_2_data_14 = document.createElement('td');
		row_2_data_14.classList.add('question_mark_bg')
		row_2_data_14.innerHTML = '<div id="helpId" class="exclamation_mark" title="click to obtain some configuration information" onclick="showConfiguration()" ></div>';
		row_2.appendChild(row_2_data_14);
		
		// ---------------
		tbody.appendChild(row_2);
		
		table.appendChild(tbody);
		mainDiv.appendChild(table);
		
		this.renderer.div.appendChild(mainDiv);
		
		// Make the Main Div element draggable:
		dragElement(document.getElementById("mainTableId"));
		
		// listen to the submenu entry Airports Airways
		// buttons are defined in this js, but ids are defined in each js that is creating a sub menu
		listenSubMenuAirwaysEntry( "btnAirwaysId" , "mainSubMenuAirwaysDivId");
		listenSubMenuOptimizationsEntry( "btnOptimizationsId" , "mainSubMenuOptimizationsDivId");
		// 30th December 2023 - add a submenu for fuel efficiency and fuel planning
		listenSubMenuFuelEntry("btnSubMenuFuelId", "mainSubMenuFuelDivId");
		// 22nd August 2024 - listen to sub menu Meteo - metar and wind temperature
		listenSubMenuMeteoEntry("btnSubMenuMeteoId" , "mainSubMenuMeteoDivId");
		
	}
};