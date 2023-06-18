
//Define custom control class
class DialogControl extends og.Control {
      
      constructor(options) {
                super(options);
      }

      onadd() {
				//console.log("dialog Control - onadd");
				
				let dialogDiv = document.createElement('div');
				dialogDiv.id = "dialogId";
				dialogDiv.style="display: none;";
                
                this.renderer.div.appendChild(dialogDiv);
      }

      oninit() {
                //console.log("dialog Control - oninit");
      }
}