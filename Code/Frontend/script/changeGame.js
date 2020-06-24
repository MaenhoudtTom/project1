"use strict";

const ip = window.location.hostname;
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
let gameID,
  gameSettings,
  html_saveButton,
  html_cancelButton,
  html_name,
  html_desc,
  html_cardDecks,
  html_cards,
  html_minAge,
  html_minPlayers,
  html_maxPlayers,
  html_rulesetID,
  html_playerInfoID,
  html_poweroffButton;
//#endregion

//#region *** DOM references ***
let html_header;
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
    trigger.addEventListener("click", function () {
      document.querySelector("html").classList.toggle("has-mobile-nav");
    });
  }
};
//#endregion

//#region *** Callback-Visualisation - show___ ***
const showGameData = function (jsonObject) {
  console.log(jsonObject);
  let htmlString = "";
  for (const game of jsonObject.game) {
    html_header.innerHTML = game.Name;
    htmlString = `<fieldset class="c-form-settings__row">
      <label class="c-form-label o-layout__item u-1-of-2-bp3" for="name">Name:</label>
      <input type="text" class="o-layout__item u-1-of-2-bp3 c-form-settings__input js-name" data-ruleset=${game.RulesetID} data-playerinfo=${game.PlayerInfoID} name="name" id="name" placeholder="Name" value="${game.Name}" required/>
    </fieldset>
    <fieldset class="c-form-settings__row">
      <label class="c-form-label o-layout__item u-1-of-2-bp3" for="description">Description:</label>
      <input type="text" class="o-layout__item u-1-of-2-bp3 c-form-settings__input js-desc" name="description" id="description" value="${game.Description}" placeholder="Description" required/>
      <!-- <textarea class="c-form-settings__input js-desc" name="description" id="description" cols="30" rows="10">${game.Description}</textarea> -->
    </fieldset>
    <fieldset class="c-form-settings__row">
      <label class="c-form-label o-layout__item u-1-of-2-bp3" for="card-decks">Card decks:</label>
      <input type="text" class="o-layout__item u-1-of-2-bp3 c-form-settings__input js-decks" name="card-decks" id="card-decks" placeholder="Card decks" value="${game.CardDecks}" required/>
    </fieldset>
    <fieldset class="c-form-settings__row">
      <label class="c-form-label o-layout__item u-1-of-2-bp3" for="cards-player">Cards per player:</label>
      <input type="text" class="o-layout__item u-1-of-2-bp3 c-form-settings__input js-cards" name="cards-player" id="cards-player" placeholder="Cards per player" value="${game.CardsPerPlayer}" required/>
    </fieldset>
    <fieldset class="c-form-settings__row">
      <label class="c-form-label o-layout__item u-1-of-2-bp3" for="age">Minimum age:</label>
      <input type="text" class="o-layout__item u-1-of-2-bp3 c-form-settings__input js-age" name="age" id="age" placeholder="Minimum age" value="${game.MinimumAge}" required/>
    </fieldset>
    <fieldset class="c-form-settings__row">
      <label class="c-form-label o-layout__item u-1-of-2-bp3" for="min-players">Minimum players:</label>
      <input type="text" class="o-layout__item u-1-of-2-bp3 c-form-settings__input js-min-players" name="min-players" id="min-players" placeholder="Minimum players" value="${game.MinimumPlayers}" required/>
    </fieldset>
    <fieldset class="c-form-settings__row">
      <label class="c-form-label o-layout__item u-1-of-2-bp3" for="max-players">Maximum players:</label>
      <input type="text" class="o-layout__item u-1-of-2-bp3 c-form-settings__input js-max-players" name="max-players" id="max-players" placeholder="Maximum players" value="${game.MaximumPlayers}"/>
    </fieldset>
    <fieldset class="c-form-settings__row">
      <input type="button" id="save" class="o-button-reset c-save-button js-save" value="Save" />
      <input type="button" class="o-button-reset c-cancel-button u-mr-lg js-cancel" id="cancel" value="Cancel" />
    </fieldset>`;
  }

  gameSettings.innerHTML = htmlString;
  listenToClickSave();
  listenToClickCancel();
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
const listenToClickSave = function () {
  console.log("functie listentoclicksave");
  document.querySelector('#save').addEventListener("click", function () {
    console.log("save geklikt");
    html_name = document.querySelector(".js-name").value;
    html_desc = document.querySelector(".js-desc").value;
    html_cardDecks = document.querySelector(".js-decks").value;
    html_rulesetID = document.querySelector('.js-name').getAttribute("data-ruleset");
    html_cards = document.querySelector(".js-cards").value;
    html_playerInfoID = document.querySelector('.js-name').getAttribute("data-playerinfo");
    html_minAge = document.querySelector(".js-age").value;
    html_maxPlayers = document.querySelector(".js-min-players").value;
    html_minPlayers = document.querySelector(".js-max-players").value;

    const updatedGameData = {
      ID: gameID,
      Name: html_name,
      Description: html_desc,
      CardDecks: html_cardDecks,
      RulesetID: html_rulesetID,
      CardsPerPlayer: html_cards,
      PlayerInfoID: html_playerInfoID,
      MinimumAge: html_minAge,
      MinimumPlayers: html_minPlayers,
      MaximumPlayers: html_maxPlayers,
    };
    console.log("change game bericht");
    socket.emit("F2B_change_game", updatedGameData);
  });
};

const listenToClickCancel = function () {
  console.log("functie listentoclickcancel");
  // console.log(html_cancelButton);
  // console.log(document.querySelector('#cancel'));
  document.querySelector('#cancel').addEventListener("click", function () {
    console.log("cancel geklikt");
    window.location = `http://${ip}/settings.html`;
  });
};

const listenToClickPoweroff = function () {
  for (const powerButton of html_poweroffButton) {
    powerButton.addEventListener("click", function () {
      console.log('poweroff');
      socket.emit("F2B_shutdown");
    });
  }
};
//#endregion

//#region *** SocketIO ***
const listenToSocket = function () {
  socket.on("B2F_changed_game", function () {
    window.location = `http://${ip}/settings.html`;
  });
};
//#endregion

const init = function () {
  console.log("DOM loaded");
  gameID = new URLSearchParams(window.location.search).get("gameID");
  console.log(`Game id: ${gameID}`);
  html_header = document.querySelector(".js-header");
  gameSettings = document.querySelector(".js-game-settings");
  html_saveButton = document.querySelector(".js-save");
  // html_cancelButton = document.querySelector(".js-cancel");
  html_poweroffButton = document.querySelectorAll(".js-poweroff");
  console.log(html_saveButton);
  // console.log(html_cancelButton);
  getGame();
  toggleNav();
  listenToClickPoweroff();
};

document.addEventListener("DOMContentLoaded", init);
