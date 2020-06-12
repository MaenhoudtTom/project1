"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
let gameID;
//#endregion

//#region *** DOM references ***
let html_header, html_description, html_gameRules, html_play;
//#endregion

//#region *** Navigation ***
const toggleNav = function () {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
  // for (let i = 0; i < toggleTrigger.length; i++) {
  //   toggleTrigger[i].addEventListener("touchstart", function () {
  //     document.querySelector("html").classList.toggle("has-mobile-nav");
  //   });
  // }

  for (let trigger of toggleTrigger) {
    trigger.addEventListener("touchstart", function () {
      document.querySelector("html").classList.toggle("has-mobile-nav");
    });
  }
};
//#endregion

//#region *** Callback-Visualisation - show___ ***
const showGameData = function (jsonObject) {
  console.log(jsonObject);
  for (const game of jsonObject.game) {
    let htmlString = `<tr class="u-mb-lg">
            <td>Minimum players:</td>
            <td>${game.MinimumPlayers}</td>
        </tr>
        <tr class="u-mb-lg">
            <td>Minimum age:</td>
            <td>${game.MinimumAge}</td>
        </tr>
        <tr class="u-mb-lg">
            <td>Maximum players:</td>
            <td>${game.MaximumPlayers}</td>
        </tr>`;

    html_header.innerHTML = game.Name;
    html_description.innerHTML = game.Description;
    html_gameRules.innerHTML = htmlString;
  }
  listenToClickPlay();
};
//#endregion

//#region  *** Callback-No Visualisation - callback___ ***
//#endregion

//#region *** Data Access - get___ ***
const getGame = function () {
  handleData(`http://${lanIP}/api/v1/gamesWithRules/${gameID}`, showGameData);
};
//#endregion

//#region *** Event Listeners - listenTo___ ***
const listenToClickPlay = function () {
  html_play.addEventListener("click", function () {
    console.log("Clicked on play button.");
    let playerAmount = document.querySelector(".js-player-amount").value;
    console.log(`${playerAmount} players`);
    const data = {
      Players: playerAmount,
    };
    socket.emit("F2B_distribute_cards", data);
  });
};
//#endregion

//#region *** SocketIO ***
const listenToSocket = function () {
  socket.on("B2F_error_logging_data", function (sensorErrors) {
    // let sensErrors = "";
    // for (const error of sensorErrors) {
    //   sensErrors += error;
    // }

    html_play.innerHTML = "Make sure the device is closed, stands up and stands still.";
    html_play.classList.add("c-error");
  });
};
//#endregion

const init = function () {
  console.log("DOM loaded");
  const querystring = new URLSearchParams(window.location.search);
  gameID = querystring.get("gameID");
  html_header = document.querySelector(".js-header");
  html_description = document.querySelector(".js-description");
  html_gameRules = document.querySelector(".js-game-rules");
  html_play = document.querySelector(".js-play");
  console.log(`play: ${html_play}`);
  getGame();
  listenToSocket();
  toggleNav();
};

document.addEventListener("DOMContentLoaded", init);
