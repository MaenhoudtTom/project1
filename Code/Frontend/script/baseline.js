"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
//#endregion

//#region *** DOM references ***
//#endregion

//#region *** Callback-Visualisation - show___ ***
//#endregion
  
//#region  *** Callback-No Visualisation - callback___ ***
//#endregion
  
//#region *** Data Access - get___ ***
//#endregion
  
//#region *** Event Listeners - listenTo___ ***
//#endregion
  
//#region *** SocketIO ***
const listenToSocket = function () {  
  socket.on("", function () {
    
  });
};
//#endregion
  
const init = function () {
  console.log("DOM loaded");
  
};

document.addEventListener("DOMContentLoaded", init);