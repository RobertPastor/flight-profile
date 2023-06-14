/**
 * this class is dedicated to manage the help information
 * this help is displayed in a modal dialog box
 * 8 May 2016 - Robert Pastor
 */
 
 class baseHelpConfiguration {
	 
	constructor() {
		this.helpArray = [];
	}
	
	getSize() {
		return this.helpArray.length;
	}
	
	pushSection (title , contents , id) {
		this.helpArray.push("<div>");
		this.helpArray.push('<input type="checkbox" id="toggle-' + id + '" class="unfolder-' + id + '"/>');
		
		this.helpArray.push('<label for="toggle-' + id + '" class="toggle-label-' + id + '"><span class="unfold-icon">&#9654;</span><span class="fold-icon">&#9660;</span>');
		this.helpArray.push(title);
		this.helpArray.push('</label>');
		
		this.helpArray.push('<div class="fold-' + id + '">');
		for (let i = 0; i < contents.length ; i++) {
			this.helpArray.push( contents[i] );
		} 
		this.helpArray.push("</div>");
		this.helpArray.push("</div>");
	}
	 
 }
 
 class Configuration extends baseHelpConfiguration {
	 
	init() {
		
		let htmlContent = "This help is displayed each time the user clicks on the exclamation mark ";
		htmlContent += '<img src="/static/images/exclamation-mark.png" style="width:16px;height:16px;border:0">';
		htmlContent += " available in the upper right corner of the navigation bar.<br>";
		this.helpArray.push(htmlContent);
		
		let contents = [];
		
		contents.push("Airline fleet configuration defines the aircraft types, the typical number of seats, operational hourly costs rates, and the crew costs rates.<br>");
		contents.push("These values are specific to each aircraft and each airline.<br>");
		contents.push("Turn-around times are added to compute the number of rotations an aircraft can perform on a flight leg.<br>");
		contents.push("Turn-around times are defined for each aircraft type of an airline.<br>");
		contents.push("Turn-around times are corrected by a coefficient depending upon the size of the airport.<br>");
		contents.push("For an airport, the more runways it has the higher is the average turn-around time (on top of the part depending upon the aircraft).<br>");
		
		this.pushSection("Fleet Configuration" , contents , "1");
		
		contents = [];
		contents.push("Airline Routes are defined first by a pair of departure and arrival airports.<br>");
		contents.push("For the airports, the ICAO code with 4 letters is used to identify in a unique way any airport on all continents.<br>");
		contents.push('Between two airports, routes are obtained from <a href="http://rfinder.asalink.net/free/" target="_blank">route finder</a> <br>');
		
		this.pushSection("Airports & Routes Configuration" , contents , "2");
		
		contents = [];
		contents.push("Waypoints are provided for each oriented route from departure to arrival airport.<br>");
		contents.push("Waypoints are defined by a unique name, a longitude and a latitude.<br>");
		
		contents.push("Waypoints names are unique for all routes whatever configured airline is available in the database.<br>");
		contents.push("Best Runways are runways having minimal distance from the runway end to the first route waypoint.<br>");
		
		contents.push("a SID, independent from any airline route, defines a set of waypoints connecting a departure runway to the first waypoint of the route.<br>");
		contents.push("a STAR, independent from any airline route, defines a set of waypoints connecting the last waypoint of the route to the runway.<br>");

		this.pushSection("WayPoints Configuration" , contents , "3");
		
		contents = [];
		contents.push("Note: all costs are computed in the same currency unit : the US dollars.<br>");
		contents.push("Total flight costs are summed up from hourly operational costs and hourly crew costs based upon the computed flight duration.<br>");
		contents.push("Fuel costs are added to the previous total.<br>");
		contents.push("In order to compute fuel costs, the aircraft mass loss is computed first.<br>");
		contents.push("The lost fuel mass is converted into liters and a coefficient is applied to convert liters to costs (US$).<br>");
		
		this.pushSection("Costs" , contents , "4");

		contents = [];
		contents.push("There is a unique airport configuration for all airports.<br>");
		contents.push('Data is obtained from <a href="https://www.openflights.org" target="_blank">openflights.org</a> <br>');
		
		contents.push("Only airports defined as departure or arrival airports - for all airlines - are extracted from this dataset and loaded into the database.<br>");
		contents.push("There is one unique database of airports locations and of runways for these airports.<br>");
		contents.push("Only runways related to these above airports are loaded into the database.<br>");

		this.pushSection("Airports & Runways Configuration" , contents , "5");
		
		contents = [];
		contents.push("There is one unique aircraft performance database.<br>");
		contents.push("The key is based upon the ICAO code of the aircraft.<br>");
		contents.push("Aircraft configuration defines the minimum and the maximum takeoff weight.<br>");
		contents.push("It defines the operational cruise level and the operation mach at this level.<br>");
		contents.push("For each flight configuration, speeds ae defined to transition from one flight configuration to the next.<br>");
		contents.push("The main flight configurations are ground-run, initial climb slope, climb, cruise, descent, glide-slope and ground-run until taxi speed is reached.<br>");
		
		this.pushSection("Aircraft Configuration" , contents , "6");
		
		contents = [];
		contents.push("There are three implemented optimizations : <br>");
		contents.push("1) Costs Minimization<br>");
		contents.push("2) Costs per Available Seat Miles (CASM) minimization.<br>");
		contents.push("3) Seats Miles maximization.<br>");
		contents.push("<br>");
		contents.push("For the first two, the minimum of the sum of a set of costs is computed.<br>");
		contents.push("In order to find this minimum, a squared table of aircraft instances versus flight legs is built.<br>");
		contents.push("For each aircraft type, flight legs are run to compute costs for each pair of aircraft type versus flight leg.<br>");
		contents.push("For CASM, on top of the costs based upon flight leg duration, the aircraft number of seats and the flown distance are used.<br>");
		contents.push("<br>");
		contents.push("For Seat Miles, a number of rotations is computed based upon each flight leg duration and a turn-around time specific for each aircraft type.<br>");
		contents.push("The number of rotations is topped by a maximum of 20 Hours flight plus turn-around time.<br>");
		contents.push("Using this number of rotations, the total Seat Miles is computed based upon the distance flown in each leg.<br>");
		contents.push("For Seat Miles, a squared table of aircraft instances versus Seat Miles for each flight leg is built.<br>");
		contents.push("<br>");
		contents.push("Future improvement: flight legs departing and arriving in the symetrical airports must be related as they will be flown by the same aircraft.<br>");
		contents.push("Note: A turn-around time correction is computed based upon the airport number of runways.<br>");
		
		this.pushSection("Optimizations" , contents , "7");
	}
	 
 }


class Help extends baseHelpConfiguration {


	init() {

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
		contents.push("While using a Right click on an airport, it is possible to see / hide waypoints for all routes starting from this airport.<br>");
		contents.push("When the waypoints are displayed on the map, in each airport the Best Runway is also displayed.<br>");
		
		this.pushSection("Airline Airports" , contents , "4");
		
		contents = [];
		contents.push("The airline routes are defined by a set of WayPoints that are linking a departure to an arrival airport.<br>");
		contents.push("When the route wayPoints are displayed on the map, the best departure and arrival runways are computed and inserted in the routes table.<br>");
		contents.push("<u><b>Warning:</b></u> for the time being, these routes are not dependent upon the departure and arrival runways.<br>");
		contents.push("<br>");
		contents.push("a SID, independent from any airline route, defines a set of waypoints connecting a departure runway to the first waypoint of the route.<br>");
		contents.push("a STAR, independent from any airline route, defines a set of waypoints connecting the last waypoint of the route to the runway.<br>");
		
		
		this.pushSection("Airline Routes" , contents , "5");

		contents = [];
		contents.push("A vertical profile is drawn on top of the horizontal route.<br>");
		contents.push("If you move the cursor above the screen, you will follow the vertical profile.<br>");
		contents.push("On its X axis, the vertical profile shows a time line expressed in seconds.<br>");
		contents.push("On its Y axis, the vertical profile shows a flight level expressed as an altitude above Mean Sea Level in meters.<br>");
		contents.push("To escape the vertical profile view, double click on the screen. <br>");
		contents.push("Warning: case where a A330 takes off from Atlanta 08L after 2915 meters of ground run (more than the length of the runway). <br>");

		this.pushSection("Flight Profile" , contents , "6");

		contents = [];
		contents.push("Costs are split into :<br>");
		contents.push("   1) operational costs based upon flight duration TIMES hourly flight costs.<br>");
		contents.push("   2) fuel costs based upon aircraft mass loss - translated into liters of fuel TIMES cost of one liter of fuel.<br>");
		contents.push("   3) crew costs based upon flight duration TIMES hourly crew costs.<br>");
		contents.push("<br>");
		contents.push("Fuel costs are based upon aircraft mass difference between initial mass and final mass.<br>");
		contents.push("This Mass difference expressed in Kilograms is converted into US gallons -> Mass Kg * 0.33 <br>");
		contents.push("Finally the value in US gallons is timed by a US Gallon to US Dollar constant -> US gallons *  3.25.<br>");
		contents.push("<br>");
		contents.push("Future improvement : show the runways used for the costs computations.<br>");
		contents.push('Use the fuel planner to compare fuel costs : <a href="http://fuelplanner.com/index.php" target="_blank">Fuel Planner</a>');

		this.pushSection("Airline Costs" , contents , "7");
		
		contents = [];
		contents.push("The Costs Minimization allows to find the minimum of the sum of the costs for all flight legs ");
		contents.push("A solver is used to find the best set of aircrafts for each flight leg.");
		
		this.pushSection("Optimizations" , contents , "8");

		contents = [];
		contents.push("For each flight leg, compute number of available seats TIMES flight leg length in miles.<br>");
		contents.push("Compute CASM as the total costs divided by (nb Seats * flight leg length miles).<br>");
		contents.push("The lower is this cost (in tenth of US dollars), the better efficiency of the aircraft on this flight leg.<br>");
		
		this.pushSection("Cost per Available Seat Miles" , contents , "9");
		
		contents = [];
		contents.push("It is possible to query programmatically the service and retrieve a result in Json format.<br>");
		contents.push('Use the following URL : <a href="https://airlineservices.eu.pythonanywhere.com/airline/airlineFleet/AmericanWings" target="_blank">Fleet Definition</a> to retrieve the fleet definition.<br>');
		contents.push('Use the following URL : <a href="https://airlineservices.eu.pythonanywhere.com/airline/airlineRoutes/AmericanWings" target="_blank">Routes Definition</a> to retrieve the routes.<br>');
		contents.push('Use the following URL : <a href="https://airlineservices.eu.pythonanywhere.com/airline/airlineCosts/AmericanWings" target="_blank">Costs</a> to retrieve the costs.<br>');
		contents.push('Use the following URL : <a href="http://airlineservices.eu.pythonanywhere.com/airline/wayPointsRoute/KATL/KLAX" target="_blank">WayPoints</a> to retrieve the wayPoints.<br>');
		contents.push('Use the following URL : <a href="http://airlineservices.eu.pythonanywhere.com/trajectory/airports/AmericanWings" target="_blank">Airports</a> to retrieve the airports of the airline.<br>');
		contents.push('Use the following URL : <a href="http://airlineservices.eu.pythonanywhere.com/trajectory/computeRunwayOvershoot/A332/KATL/08L/230" target="_blank">Runway overshoot</a> to retrieve the ground run length.<br>');

		this.pushSection("API - Application Programming Interface" , contents , "10");

		//this.helpArray.push("<h4>About Trajectory Prediction</h4>");
		//this.helpArray.push('<a href="https://trajectoire-predict.monsite-orange.fr/page-557223c123784.html" target="_blank">Aircraft Trajectory Prediction</a>');
		//this.helpArray.push("<br>");
		//this.helpArray.push('<a href="https://trajectoire-predict.monsite-orange.fr/index.html" target="_blank">Prédiction de Trajectoire des Avions de Ligne</a>');

	};
}

function show(help, title) {
	
	var divHelp = document.getElementById('helpDiv');
	if (divHelp == undefined) {
		console.error (' cannot display help - div not found!!! ');
		return;
	}
	// remove child elements
	$("#helpDiv").empty();
	
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
	show(help, "Help");
};

function showConfiguration() {
	let configuration = new Configuration();
	configuration.init();
	show(configuration, "Configuration");
}



