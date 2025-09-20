import { removeAllChilds } from "../main/main.js"
//import { d3 } from "../d"

export class VerticalProfile {
	
	constructor() {
		//console.log("Vertical Profile constructor") 
	}
	
	displayVerticalProfile (arrayAltitudeMSLtime) {
		console.log("displayVerticalProfile");
		// set the dimensions and margins of the graph
		let margin = {top: 10, right: 100, bottom: 10, left: 50}
		let width = 700 - margin.left - margin.right;
		let height = 700 - margin.top - margin.bottom;
		
		let data =  arrayAltitudeMSLtime["groundTrack"];
		
		let parentDiv = document.getElementById("globusDivId");
		//let parentDiv = document.getElementById("d3vizId");
		
		width = parentDiv.clientWidth - margin.left - margin.right; 
		height = parentDiv.clientHeight - margin.top - margin.bottom;
		
		width = parentDiv.getBoundingClientRect().width;
		height = parentDiv.getBoundingClientRect().height;
		// path width 
		width = width - margin.left - margin.right;
		height = height - margin.top - margin.bottom;
		
		let topTable = document.getElementById("mainTableId");
		height = height - topTable.clientHeight;

		// append the svg object to the body of the page
		//removeAllChilds (document.getElementById("dialogId"))
		// d3vizId is define in MainControl.js
		removeAllChilds (document.getElementById("d3vizId"));
		document.getElementById("d3vizId").classList.add("d3Div");
		
		// Creating a div element at the end
		//$("#dialogId").append('<div id="d3vizId" style="width: 100%; height: 100%;"></div>');
		
		let svg = d3.select("#d3vizId")
			.data(data)
			.append("svg")
			.attr("width", width)
			.attr("height", height)
			.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
				  
		let maxX = arrayAltitudeMSLtime["maxElapsedTimeSeconds"]
			
		// Add X axis --> it is a integer format
		let x = d3.scaleLinear()
			.domain([1,maxX ])
			.range([ 0, width ]);
		
		// .attr("transform", "translate(0," + height + ")")
		// the axis will appear on the top
		svg.append("g")
			.call(d3.axisBottom(x));
		
		// x Axis label
		svg.append("text")
			.attr("class", "x label")
			.attr("text-anchor", "end")
			.attr("x", width - 60)
			.attr("y", 30)
			.text("duration time (seconds)");
				
		// max on the Y axis
		let maxY = arrayAltitudeMSLtime["MaxAltitudeMSLmeters"];
		
		// create Y axis
		let y = d3.scaleLinear()
				.domain([0, maxY + 1000])
				.range([ height, 0 ]);
				
		// add Y axis to the svg
		svg.append("g").call(d3.axisLeft(y));
				
		// add Y axis label
		svg.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "end")
			.attr("y", 6)
			.attr("dy", ".75em")
			.attr("transform", "rotate(-90)")
			.text("Altitude Mean Sea Level (meters)");
		
		// This allows to find the closest X index of the mouse:
		let bisect = d3.bisector(function(d) { return d.x; }).left;

		// Create the circle that travels along the curve of chart
		let focus = svg.append('g')
				.append('circle')
				.style("fill", "yellow")
				.attr("stroke", "black")
				.attr('r', 12.5)
				.style("opacity", 0)
				
		// bounding box
		function getBB(selection) {
			selection.each(function(d){
				d.bbox = this.getBBox();
			})
		}

		// Create the text that travels along the curve of chart
		let focusText = svg
				.append('g')
				.append('text')
				.style("opacity", 1)
				.attr("text-anchor", "left")
				.attr("alignment-baseline", "middle")
				.call(getBB);   
		
		
		focusText.insert("rect","text")
			.attr("width", function(d){
				return d.bbox.width
				})
			.attr("height", function(d){
				return d.bbox.height
				})
			.style("fill", "yellow");
		

		// Add the line
		svg.append("path")
			.attr("class", "line")
			.attr("stroke", "#000000")
			.attr("stroke-width", 3.5)
			.attr("fill", "#FFFFFF")
			.attr("d", d3.line()
			  .x(function(d) {
					// assumption that data has x key element
					return x(d.x) 
				})
			  .y(function(d) { 
					// assumption that the data has a y key element
					return y(d.y) 
				})
			  )
		
		let path = svg.selectAll("dot")
			 .data(data)
			 .enter()
			 .append("circle")
			 .attr("r", 1.5)
			 .attr("cx", function (d) {
				   return x(d.x);
			 })
			 .attr("cy", function (d) {
				  return y(d.y);
			 })
			 .attr("stroke", "#32CD32")
			 .attr("stroke-width", 0.5)
			 .attr("fill", "#FFFFFF");
		
		// What happens when the mouse move -> show the annotations at the right positions.
		function mouseover() {
			//console.log("mouse over")
			focus.style("opacity", 1);
			focusText.style("opacity",1);
		}

		function mousemove(domElement) {
			//console.log("mouse move")
			// recover coordinate we need
			let x0 = x.invert(d3.pointer(domElement)[0]);
			let i = bisect(data, x0, 1);
			try {
				let selectedData = data[i];
				let deltaPosX = ((selectedData.x) > ( maxX / 2 )) ? -115 : +15;
				let deltaPosY = ((selectedData.y) < ( maxY / 2 )) ? -30 : +30;
				focus
					.attr("cx", x(selectedData.x))
					.attr("cy", y(selectedData.y));
				focusText
					.html(selectedData.x + " sec " + " - " + selectedData.y + " m")
					.attr("x", x(selectedData.x) + deltaPosX)
					.attr("y", y(selectedData.y) + deltaPosY);
			} catch (err) {
				console.log(JSON.stringify(err))
			}
		}
						
		function mouseout() {
			focus.style("opacity", 0);
			focusText.style("opacity", 0);
		}

		// Create a rect on top of the svg area: this rectangle recovers mouse position
		svg.append('rect')
			.style("fill", "none")
			.style("pointer-events", "all")
			.attr('width', width)
			.attr('height', height)
			.on('mouseover', mouseover)
			.on('mousemove', mousemove)
			.on('mouseout', mouseout)
			.on('dblclick',function(node) { 
				//console.log("node was double clicked");
				$("#d3vizId").hide();
				$("#globusDivId").show();
		});

		// show the vertical profile
		/*
		$("#dialogId")
				.dialog({
				   autoOpen: false,
				   title: "Compute Flight Profile",
				   modal: true,
				   hide: "puff",
				   show : "slide",
				   height: "auto",
				   width: "auto",
				   maxHeight: true,
				   maxWidth: true
				})
				.html(document.getElementById('d3vizId').innerHTML)
				.dialog('open'); 
		*/
		// show the svg
		$("#d3vizId").show();
		//$("#globusDivId").hide()	
		
	}
}