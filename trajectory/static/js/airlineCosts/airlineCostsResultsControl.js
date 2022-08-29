
//Define custom control class
		class AirlineCostsResultsControl extends og.Control {
            constructor(options) {
                super(options);
            }

            onadd() {
				//console.log("airline Costs Results Control - onadd");
				
				let mainDiv = document.createElement('div');
				mainDiv.id = "airlineCostsResultsMainDivId";
				mainDiv.style="display: none;";
				mainDiv.classList.add('airlineCostsResultsMainDiv');
				
				let table = document.createElement('table');
				table.id = "airlineCostsResultsTableId";
				
				let thead = document.createElement('thead');
				let row_1 = document.createElement('tr');

				let th_list = [ 'Aircraft' , 'Seats', 'Adep', 'RunWay', 'Ades', 'RunWay', 'Is Aborted', 'Initial Mass Kg' ,
								'Final Mass Kg', 'Lost Mass Kg', 'Fuel Costs US $', 'Flight Duration Hours', 'Flying Costs US $', 'Total Costs US $' ];
				let th = undefined;
				th_list.forEach ( function ( element ) {
					th = document.createElement('th');
					th.innerHTML = element;
					row_1.appendChild(th);
				});

				thead.appendChild(row_1);
				table.appendChild(thead);

				// --------------------
				let tbody = document.createElement('tbody');
				table.appendChild(tbody);

				
				mainDiv.appendChild(table);
				this.renderer.div.appendChild(mainDiv);
            }

            oninit() {
                //console.log("airline Costs Results Control - oninit");
            }
        };