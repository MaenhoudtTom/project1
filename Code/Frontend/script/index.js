"use strict";

const ip = window.location.hostname;
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
//#endregion

//#region *** DOM references ***
let html_games, html_addButton, html_poweroffButton;
//#endregion

//#region *** Navigation ***
const toggleNav = function () {
  let toggleTrigger = document.querySelectorAll(".js-toggle-nav");

  for (let trigger of toggleTrigger) {
    trigger.addEventListener("touchstart", function () {
      document.querySelector("html").classList.toggle("has-mobile-nav");
    });
  }
};
//#endregion

//#region *** Callback-Visualisation - show___ ***
const showGames = function (jsonObject) {
  console.log(jsonObject);
  let htmlString = "";
  for (const game of jsonObject.games) {
    // htmlString += `<a class="c-game-button" href="http://${ip}/playerinfo.html?gameID=${game.ID}">${game.Name}</a>`;
    htmlString += `<div class="o-layout__item u-1-of-2-bp3"><a class="c-game-button" href="http://${ip}/playerinfo.html?gameID=${game.ID}">${game.Name}</a></div>`;
  }
  html_games.innerHTML = htmlString;
};

const showAddGameButton = function () {
  html_addButton.innerHTML = `<a href="http://${ip}/newGame.html"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="74" height="74" viewBox="0 0 74 74">
  <defs>
    <filter id="teal_circle" x="0" y="0" width="74" height="74" filterUnits="userSpaceOnUse">
      <feOffset dy="6" input="SourceAlpha"/>
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feFlood flood-opacity="0.239"/>
      <feComposite operator="in" in2="blur"/>
      <feComposite in="SourceGraphic"/>
    </filter>
    <linearGradient id="linear-gradient" x1="0.5" y1="1" x2="0.5" gradientUnits="objectBoundingBox">
      <stop offset="0"/>
      <stop offset="0.14" stop-opacity="0.631"/>
      <stop offset="1" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="linear-gradient-2" x1="0.5" y1="1" x2="0.5" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.23" stop-color="#fff" stop-opacity="0.012"/>
      <stop offset="0.36" stop-color="#fff" stop-opacity="0.039"/>
      <stop offset="0.47" stop-color="#fff" stop-opacity="0.102"/>
      <stop offset="0.57" stop-color="#fff" stop-opacity="0.18"/>
      <stop offset="0.67" stop-color="#fff" stop-opacity="0.278"/>
      <stop offset="0.75" stop-color="#fff" stop-opacity="0.412"/>
      <stop offset="0.83" stop-color="#fff" stop-opacity="0.561"/>
      <stop offset="0.91" stop-color="#fff" stop-opacity="0.741"/>
      <stop offset="0.98" stop-color="#fff" stop-opacity="0.929"/>
      <stop offset="1" stop-color="#fff"/>
    </linearGradient>
  </defs>
  <g id="Round_Btn_Default_Dark" data-name="Round Btn Default Dark" transform="translate(9 3)">
    <g transform="matrix(1, 0, 0, 1, -9, -3)" filter="url(#teal_circle)">
      <path id="teal_circle-2" data-name="teal circle" d="M28,0A28,28,0,1,1,0,28,28,28,0,0,1,28,0Z" transform="translate(9 3)" fill="#2d7b8e"/>
    </g>
    <g id="ic_add_white" transform="translate(-120 -51)">
      <path id="ic_add_white-2" data-name="ic_add_white" d="M3438,988h-6v6h-2v-6h-6v-2h6v-6h2v6h6Z" transform="translate(-3283 -908)" fill="#fafafa"/>
    </g>
    <g id="Group_332" data-name="Group 332" transform="translate(-2970 398)" opacity="0.12">
      <path id="gradient_border_2" data-name="gradient border 2" d="M3431,959.5a27.5,27.5,0,1,1-27.5,27.5,27.5,27.5,0,0,1,27.5-27.5m0-.5a28,28,0,1,0,28,28,28,28,0,0,0-28-28Z" transform="translate(-433 -1357)" fill="url(#linear-gradient)"/>
      <path id="gradient_border_1" data-name="gradient border 1" d="M3431,959.5a27.5,27.5,0,1,1-27.5,27.5,27.5,27.5,0,0,1,27.5-27.5m0-.5a28,28,0,1,0,28,28,28,28,0,0,0-28-28Z" transform="translate(-433 -1357)" fill="url(#linear-gradient-2)"/>
    </g>
  </g>
</svg></a>`;
};
//#endregion

//#region  *** Callback-No Visualisation - callback___ ***
//#endregion

//#region *** Data Access - get___ ***
const getGames = function () {
  handleData(`http://${lanIP}/api/v1/games`, showGames);
};
//#endregion

//#region *** Event Listeners - listenTo___ ***
const listenToClickPoweroff = function () {
  for (const powerButton of html_poweroffButton) {
    powerButton.addEventListener("click", function () {
      console.log('poweroff');
      socket.emit("F2B_shutdown");
    });
  }
};
//#endregion

const init = function () {
  console.log("DOM loaded");
  html_games = document.querySelector(".js-games");
  html_addButton = document.querySelector(".js-add-button");
  html_poweroffButton = document.querySelectorAll(".js-poweroff");
  getGames();
  toggleNav();
  showAddGameButton();
  listenToClickPoweroff();
};

document.addEventListener("DOMContentLoaded", init);
