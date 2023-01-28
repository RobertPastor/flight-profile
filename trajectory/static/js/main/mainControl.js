

//Define custom control class
		class MainControl extends og.Control {
            constructor(options) {
                super(options);
            }

            onadd() {
				//console.log("main Control - onadd");
				
				let mainDiv = document.createElement('div');
				mainDiv.id = "mainTableId";
				mainDiv.classList.add('mainTable');
				
				let draggableMainDiv = document.createElement('div');
				draggableMainDiv.id = mainDiv.id  + "Header";
				draggableMainDiv.innerHTML = "Click here to move";
				draggableMainDiv.classList.add("draggableDivHeader");
				mainDiv.appendChild(draggableMainDiv);
								
				let table = document.createElement('table');
				let tbody = document.createElement('tbody');
				
				let row_1 = document.createElement('tr');
				
				let row_1_data_1 = document.createElement('td');
				row_1_data_1.colSpan = "1";
				
				let div_1 = document.createElement('div');
				
				let select = document.createElement("select");
				select.id = "airlineSelectId";
				select.classList.add('airlineSelect');
				
                //select.id = "airlineSelectId";
				//select.name = "airlineSelectName";                             

                //let option_1 = document.createElement("option");
                //option_1.text = "AmericanWings";
				//select.add(option_1);

                //let option_2 = document.createElement("option");  
				//option_2.text = "EuropeanWings";
				//select.add(option_2);

                div_1.appendChild(select);
				row_1_data_1.appendChild(div_1);
				row_1.appendChild(row_1_data_1);
				
				let row_1_data_2 = document.createElement('td');
				row_1_data_2.colSpan = "6";
				row_1_data_2.innerHTML = '<div id="workerId" class="w3-container w3-green" style="width:100%"></div>';
				row_1.appendChild(row_1_data_2);
				
				tbody.appendChild(row_1);
				
				let row_2 = document.createElement('tr');
				
				let row_2_data_1 = document.createElement('td');
				row_2_data_1.innerHTML = '<div ><span>Welcome to the Airline Fleet Management tool</span></div>';
				row_2.appendChild(row_2_data_1);
				
				let row_2_data_2 = document.createElement('td');
				row_2_data_2.innerHTML = '<div><button id="btnAirlineFleet" >Show Airline Fleet</button></div>';
				row_2.appendChild(row_2_data_2);
				
				let row_2_data_3 = document.createElement('td');
				row_2_data_3.innerHTML = '<div><button id="btnAirports" >Show Airline Airports</button></div>';
				row_2.appendChild(row_2_data_3);
				
				let row_2_data_4 = document.createElement('td');
				row_2_data_4.innerHTML = '<div><button id="btnAirlineRoutes" >Show Airline Routes</button></div>';
				row_2.appendChild(row_2_data_4);
				
				/**
				// 18th September 2022 - airline way points is useless as we can show them for any route
				let row_2_data_5 = document.createElement('td');
				row_2_data_5.innerHTML = '<div><button id="btnWayPoints" >Show Airline WayPoints</button></div>';
				row_2.appendChild(row_2_data_5);
				**/
				
				let row_2_data_6 = document.createElement('td');
				row_2_data_6.innerHTML = '<div><button id="btnLaunchFlightProfile" >Show Profile / Costs</button></div>';
				row_2.appendChild(row_2_data_6);
				
				// 3rd November 2022 - flight profile and costs merged 
				//let row_2_data_7 = document.createElement('td');
				//row_2_data_7.innerHTML = '<div><button id="btnLaunchCosts" >Show Compute Costs</button></div>';
				//row_2.appendChild(row_2_data_7);
				
				// 27th January 2023 - Fleet Assignment based upon costs controls
				let row_2_data_7 = document.createElement('td');
				row_2_data_7.innerHTML = '<div><button id="btnLaunchCostsOptimization" >Show Costs Optimization</button></div>';
				row_2.appendChild(row_2_data_7);
				
				
				let row_2_data_8 = document.createElement('td');
				row_2_data_8.classList.add('question_mark_bg')
				row_2_data_8.innerHTML = '<div class="question_mark" onclick="showHelp()" title="click to obtain some help"></div>';
				row_2.appendChild(row_2_data_8);
				
				tbody.appendChild(row_2);
				
				table.appendChild(tbody);
				mainDiv.appendChild(table);
                
                this.renderer.div.appendChild(mainDiv);
				
				// Make the Main Div element draggable:
				dragElement(document.getElementById("mainTableId"));

            }

            oninit() {
                //console.log("main Control - oninit");
            }
        };