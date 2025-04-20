import {
        Control
    } from "../og/og.es.js";

//Define custom control class
export class HelpControl extends Control {
	
	constructor(options) {
		super(options);
	}

	onadd() {
		//console.log("help Control - onadd");
		
		let helpDiv = document.createElement('div');
		helpDiv.id = "helpDiv";
		helpDiv.style="display: none;";
		
		this.renderer.div.appendChild(helpDiv);
	}

	oninit() {
		//console.log("help Control - oninit");
	}
};