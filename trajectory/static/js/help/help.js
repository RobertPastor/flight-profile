/**
 * this class is dedicated to manage the help information
 * this help is displayed in a modal dialog box
 * 8 May 2016 - Robert Pastor
 */


function Help () {

	this.helpArray = [];

	this.getSize = function() {
		return this.helpArray.length;
	};
	
	this.pushSection = function(title , contents , id) {
		this.helpArray.push("<div>");
		this.helpArray.push('<input type="checkbox" id="toggle-' + id + '" class="unfolder-' + id + '"/>');
		
		this.helpArray.push('<label for="toggle-' + id + '" class="toggle-label-' + id + '"><span class="unfold-icon">&#9654;</span><span class="fold-icon">&#9660;</span>');
		this.helpArray.push(title);
		this.helpArray.push('</label>');
		
		this.helpArray.push('<div class="fold-' + id + '">');
		for (i = 0; i < contents.length ; i++) {
			this.helpArray.push( contents[i] );
		} 
		this.helpArray.push("</div>");
		this.helpArray.push("</div>");
	}

	this.init = function() {

		var htmlContent = "This help is displayed each time the user clicks on the question mark ";
		htmlContent += '<img src="/static/images/question.png" style="width:16px;height:16px;border:0">';
		htmlContent += " available in the upper right corner of the navigation bar.<br>";
		this.helpArray.push(htmlContent);

		let contents = [];
		contents.push("This highly configurable tool allows to build a fleet of aircrafts with departure and arrival airports and their routes.<br>");
		contents.push("For each flight leg, the tool computes a detailed 4 dimensions lateral and vertical profile. <br>");
		contents.push("For each leg, it is possible to select a departure and an arrival runway.<br>");
		contents.push("It is possible also to select a takekoff mass and a cruise level.<br>");
		contents.push("<br>");
		contents.push("For each aircraft, configuration includes hourly operational costs, crew costs.<br>");
		contents.push("Fuel costs are based upon aircraft mass losses as computed at the end of each simulation.<br>");
		contents.push("The flight profile provides duration, distance flown and with mass loss, it is allowing to compute overall costs.<br>");
		contents.push("Current optimizations are focused upon minimizing costs or Cost per Available Seat Mile.<br>");
		contents.push("Optimizations allow the selection of the best aircraft for each flight leg in order to minimize for instance Costs per Available Seat Miles.<br>");
		contents.push("<br>");
		contents.push("Note: Due to the size of some results table, usability of this tool is optimal on a desktop, laptop computer or a tablet.<br>");

		this.pushSection("Goals" , contents , "1");
		
		contents = [];
		contents.push("There are 3 defined airlines, each with its fleet, airports, routes, and unitary costs.<br>");
		contents.push("All these informations are some kind of parameters, they are configurable.<br>");
		contents.push("An airline is also defined by a South-West and a North-East geograpical points to display an earth map.<br>");
		
		this.pushSection("Airlines" , contents , "2");

		contents = [];
		contents.push("The fleet is composed of types of aircrafts, number of available aircrafts, number of seats, and operational costs per flight hour.<br>");
		contents.push("Using a flight leg duration, it allows to compute costs based upon flight duration added to fuel costs.<br>");

		this.pushSection("Airline Fleet" , contents , "3");

		contents = [];
		contents.push("Each airline has a set of departure and arrival airports.<br>");
		contents.push("These airports are the starting or ending points of the flight legs.<br>");
		contents.push("<u><b>Note:</b></u> When the cursor mouves over an airport, the pointer changes its shape meaning that the mouse buttons are active.<br>");
		contents.push("<u><b>Warning:</b></u> you will have to dezoom in order to see an airport in Alaska or in France.<br>");
		contents.push("<br>");
		contents.push("<u><b>Note:</b></u> Right click on an airport to see the routes starting from this airport.<br>");
		
		this.pushSection("Airline Airports" , contents , "4");
		
		contents = [];
		contents.push("The airline routes are defined by a set of WayPoints that are linking a departure to an arrival airport.<br>");
		contents.push("When the route wayPoints are displayed on the map, the best departure and arrival runways are computed and inserted in the routes table.<br>");
		contents.push("<u><b>Warning:</b></u> for the time being, these routes are not dependent upon the departure and arrival runways.<br>");
		contents.push("Future improvements : SID and STAR have to be implemented.<br>");
		
		this.pushSection("Airline Routes" , contents , "5");

		contents = [];
		contents.push("A vertical profile is drawn on top of the horizontal route.<br>");
		contents.push("If you move the cursor above the screen, you will follow the vertical profile.<br>");
		contents.push("On its X axis, the vertical profile shows a time line expressed in seconds.<br>");
		contents.push("On its Y axis, the vertical profile shows a flight level expressed as a Mean Sea Level in meters.<br>");
		contents.push("To escape the vertical profile view, double click on the screen. <br>");
		contents.push("Warning: case where a A330 takes off from Atlanta 08L after 2915 meters of ground run (more than the length of the runway). <br>");

		this.pushSection("Flight Profile" , contents , "6");

		contents = [];
		contents.push("Costs are split into :<br>");
		contents.push("   1) operational costs based upon flight duration TIMES hourly flight costs.<br>");
		contents.push("   2) fuel costs based upon aircraft mass loss - translated into liters of fuel TIMES cost of one liter of fuel.<br>");
		contents.push("   3) crew costs based upon flight duration TIMES hourly crew costs.<br>");
		
		this.pushSection("Airline Costs" , contents , "7");
		
		contents = [];
		contents.push("This tab allows to minimize the sum of the costs for all flight legs ");
		contents.push("while finding the best aircraft for each flight leg.");
		
		this.pushSection("Costs Optimization" , contents , "8");
		
		contents = [];
		contents.push("Fuel costs are based upon aircraft mass difference between initial mass and final mass.<br>");
		contents.push("This Mass difference expressed in Kilograms is converted into US gallons -> Mass Kg * 0.33 <br>");
		contents.push("Finally the value in US gallons is timed by a US Gallon to US Dollar constant -> US gallons *  3.25.<br>");

		this.pushSection("Fuel Costs" , contents , "9");

		contents = [];
		contents.push("For each flight leg, compute number of available seats TIMES flight leg length in miles.<br>");
		contents.push("Compute CASM as the total costs divided by (nb Seats * flight leg length miles).<br>");
		contents.push("The lower is this cost (in tenth of US dollars), the better efficiency of the aircraft on this flight leg.<br>");
		
		this.pushSection("Cost per Available Seat Miles" , contents , "10");

		//this.helpArray.push("<h4>About Trajectory Prediction</h4>");
		//this.helpArray.push('<a href="https://trajectoire-predict.monsite-orange.fr/page-557223c123784.html" target="_blank">Aircraft Trajectory Prediction</a>');
		//this.helpArray.push("<br>");
		//this.helpArray.push('<a href="https://trajectoire-predict.monsite-orange.fr/index.html" target="_blank">Prédiction de Trajectoire des Avions de Ligne</a>');

	};
}

function show(help) {
	
	var divHelp = document.getElementById('helpDiv');
	if (divHelp == undefined) {
		console.log (' cannot display help - div not found!!! ');
		return;
	}
	var title = 'help';
	$("#helpDiv").dialog (
			{
				dialogClass : 'helpDiv',
				resizable	: true,
				modal		: true,
				title		: title,
				width 		: 'auto',
				overflow    : 'scroll',
				position	: 'top',
				open: function() {
					var htmlContent = "";
					for (i = 0; i < help.getSize() ; i++) {
						htmlContent += help.helpArray[i];
					} 
					$(this).html(htmlContent);
				},
			}
	);
}
	

function showHelp() {
	//console.log ( ' show help !!! ');
	var help = new Help();
	help.init();
	show(help);
	
};