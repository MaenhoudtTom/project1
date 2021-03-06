"use strict";

const ip = window.location.hostname;
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
//#endregion

//#region *** DOM references ***
let html_name,
  html_desc,
  html_cardDecks,
  html_cards,
  html_minAge,
  html_minPlayers,
  html_maxPlayers,
  html_saveButton,
  html_cancelButton;
//#endregion

//#region *** Callback-Visualisation - show___ ***
//#endregion

//#region  *** Callback-No Visualisation - callback___ ***
//#endregion

//#region *** Data Access - get___ ***
//#endregion

//#region *** Event Listeners - listenTo___ ***
const listenToClickSave = function () {
  html_saveButton.addEventListener("click", function () {
    html_name = document.querySelector(".js-name").value;
    html_desc = document.querySelector(".js-desc").value;
    html_cardDecks = document.querySelector(".js-decks").value;
    html_cards = document.querySelector(".js-cards").value;
    html_minAge = document.querySelector(".js-age").value;
    html_minPlayers = document.querySelector(".js-min-players").value;
    html_maxPlayers = document.querySelector(".js-max-players").value;

    const data = {
      Name: html_name,
      Description: html_desc,
      CardDecks: html_cardDecks,
      CardsPerPlayer: html_cards,
      MinimumAge: html_minAge,
      MinimumPlayers: html_minPlayers,
      MaximumPlayers: html_maxPlayers,
    };
    socket.emit("F2B_create_game", data);
  });
};

const listenToClickCancel = function () {
  html_cancelButton.addEventListener("click", function () {
    window.location = `http://${ip}/index.html`;
  });
};
//#endregion

//#region *** SocketIO ***
const listenToSocket = function () {
  socket.on("B2F_game_created", function () {
    window.location(`http://${ip}/index.html`);
  });
};
//#endregion

const init = function () {
  console.log("DOM loaded");
  html_saveButton = document.querySelector(".js-save");
  html_cancelButton = document.querySelector(".js-cancel");
  listenToClickCancel();
  listenToClickSave();
};

document.addEventListener("DOMContentLoaded", init);
