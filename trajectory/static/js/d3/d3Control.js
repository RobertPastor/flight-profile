
import { Control } from "../og/og.es.js";
    
//Define custom control class
export class D3Control extends Control {
            constructor(options) {
                super(options);
            }
            onadd() {
				//console.log("D3 Control - onadd");
				
				let d3Div = document.createElement('div');
				d3Div.id = "d3vizId";
				d3Div.style="display: none;";
				d3Div.classList.add('d3Div');

				this.renderer.div.appendChild(d3Div);
            }
            oninit() {
                //console.log("D3 Control - oninit");
            }
        };