

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
				
				let table = document.createElement('table');
				let tbody = document.createElement('tbody');
				
				let row_1 = document.createElement('tr');
				
				let row_1_data_1 = document.createElement('td');
				row_1_data_1.colSpan = "1";
				
				let div_1 = document.createElement('div');
				
				let select = document.createElement("select");
				select.id = "airlineSelectId";
				
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
				row_1_data_2.colSpan = "7";
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
				
				let row_2_data_5 = document.createElement('td');
				row_2_data_5.innerHTML = '<div><button id="btnWayPoints" >Show Airline WayPoints</button></div>';
				row_2.appendChild(row_2_data_5);
				
				let row_2_data_6 = document.createElement('td');
				row_2_data_6.innerHTML = '<div><button id="btnLaunchFlightProfile" >Compute Flight Profile</button></div>';
				row_2.appendChild(row_2_data_6);
				
				let row_2_data_7 = document.createElement('td');
				row_2_data_7.innerHTML = '<div><button id="btnLaunchCosts" >Show Compute Costs</button></div>';
				row_2.appendChild(row_2_data_7);
				
				let row_2_data_8 = document.createElement('td');
				row_2_data_8.classList.add('question_mark_bg')
				row_2_data_8.innerHTML = '<div class="question_mark" onclick="showHelp()" title="click to obtain some help"></div>';
				row_2.appendChild(row_2_data_8);
				
				tbody.appendChild(row_2);
				
				table.appendChild(tbody);
				mainDiv.appendChild(table);
                
                this.renderer.div.appendChild(mainDiv);
            }

            oninit() {
                //console.log("main Control - oninit");
            }
        };