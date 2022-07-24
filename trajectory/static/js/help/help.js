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

	this.init = function() {

		var htmlContent = "This help is displayed each time the user clicks on the question mark ";
		htmlContent += '<img src="/static/images/question-mark.png" style="width:24px;height:24px;border:0">';
		htmlContent += "available in the upper right corner of the page.<br>";
		this.helpArray.push(htmlContent);

		this.helpArray.push("<h3>Goals</h3>");
		this.helpArray.push("The solution allows to manage an airline, its fleet, the airways , the routes, the wayPoints , etc...<br>");
		
		this.helpArray.push("<h3>Airline Fleet</h3>");
		this.helpArray.push("The fleet is composed of types of aircrafts, number of available aircrafts, number of seats, and operational costs per flight hour.<br>");
		this.helpArray.push("Using a flight leg duration, it allows to compute costs based upon flight duration Added to fuel costs.<br>");


		this.helpArray.push("<h3>Airline Airports</h3>");
		this.helpArray.push("The airline has a set of departure and arrival airports.<br>");
		this.helpArray.push("These airports are the starting or ending points of the flight legs.<br>");

		this.helpArray.push("<h3>Airline Routes</h3>");
		this.helpArray.push("The airline routes are defined by a set of WayPoints to link a departure to an arrival airport.<br>");
		this.helpArray.push("Warning : for the time being, these routes are not dependent upon the departure and arrival runways.<br>");


		this.helpArray.push("<h3>Flight Profile</h3>");
		this.helpArray.push("A vertical profile is drawn on top of the horizontal route.<br>");
		this.helpArray.push("If you move the cursor above the screen, you will follow the vertical profile.<br>");
		this.helpArray.push("On its X axis, the vertical profile shows a time line expressed in seconds.<br>");
		this.helpArray.push("On its Y axis, the vertical profile shows a flight level expressed as a Mean Sea Level in meters.<br>");
		this.helpArray.push("To escape the vertical profile view, double click on the screen. <br>");

		this.helpArray.push("<h3>Airline Costs</h3>");
		this.helpArray.push("Costs are based upon :<br>");
		this.helpArray.push("   1) flight duration TIMES operational costs per flight hours.<br>");
		this.helpArray.push("   2) fuel costs based upon aircraft mass loss - translated into liters of fuel TIMES cost of one liter of fuel.<br>");

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
				dialogClass : 'small',
				resizable	: true,
				modal		: true,
				title		: title,
				width 		: 'auto',
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