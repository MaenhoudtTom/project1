"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
let gameID;
//#endregion

//#region *** DOM references ***
let html_header, html_description, html_gameRules, html_play, html_poweroffButton, html_error;
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
    let htmlString = `
        <tr class="u-mb-lg">
            <td>Minimum age:</td>
            <td>${game.MinimumAge}</td>
        </tr>
        <tr class="u-mb-lg">
            <td>Minimum players:</td>
            <td class="js-minPlayers">${game.MinimumPlayers}</td>
        </tr>
        <tr class="u-mb-lg">
            <td>Maximum players:</td>
            <td class="js-maxPlayers">${game.MaximumPlayers}</td>
        </tr>
        <tr class="u-mb-lg">
            <td>Cards per player:</td>
            <td class="js-cardsPerPlayer">${game.CardsPerPlayer}</td>
        </tr>
        <tr class="u-mb-lg">
          <td>Card decks:</td>
          <td class="js-card-decks">${game.CardDecks}</td>
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
    html_error.innerHTML = ``;
    let playerAmount = document.querySelector(".js-player-amount").value;
    let cardsPerPlayer = document.querySelector(".js-cardsPerPlayer").innerHTML;
    let minPlayers = document.querySelector(".js-minPlayers").innerHTML;
    let maxPlayers = document.querySelector(".js-maxPlayers").innerHTML;
    let cardDecks = document.querySelector(".js-card-decks").innerHTML;
    console.log(`${playerAmount} players`);
    console.log(minPlayers);
    console.log(maxPlayers);
    console.log(typeof minPlayers);
    console.log(typeof maxPlayers);
    if (playerAmount) {
      if (playerAmount <= parseInt(maxPlayers) && playerAmount >= parseInt(minPlayers)) {
        html_error.innerHTML = `<input type="text" class="o-layout__item o-button-reset c-message js-error" value="Checking if everything is alright......" />`;
        const data = {
          Players: playerAmount,
          CardsPerPlayer: cardsPerPlayer,
          CardDecks: cardDecks,
        };
        socket.emit("F2B_distribute_cards", data);
      } else {
        console.log(playerAmount);
        html_error.innerHTML = `<input type="text" class="o-layout__item o-button-reset c-error js-error" value="You can play with minimum ${minPlayers} players and maximum ${maxPlayers} players" />`;
      }
    } else {
      html_error.innerHTML = `<input type="text" class="o-layout__item o-button-reset c-error js-error" value="Please fill in the amount of players" />`;
    }
  });
};
//#endregion

//#region *** SocketIO ***
const listenToSocket = function () {
  socket.on("B2F_distributing", function () {
    console.log("enjoy");
    html_error.innerHTML = `<input type="text" class="o-layout__item o-button-reset c-message js-error" value="Have fun!!" />`;
  });

  socket.on("B2F_error_according_to_sensors", function () {
    html_error.innerHTML += `<input type="text" class="o-layout__item o-button-reset c-error js-error" value="Make sure the device stands still and the case is closed!" />`;
  });

  socket.on("B2F_no_cards_placed", function () {
    html_error.innerHTML += `<input type="text" class="o-layout__item o-button-reset c-error js-error" value="No cards placed!" />`;
  });

  socket.on("B2F_error_sensors", function (sensorErrors) {
    let htmlString = "";
    for (const sensor of sensorErrors) {
      htmlString = +`${sensor} <br>`;
    }
    html_error.innerHTML += `<input type="text" class="o-layout__item o-button-reset c-error js-error" value="There is something wrong with these sensors:<br> ${htmlString}" />`;
  });

  socket.on("B2F_error_saving_data", function (sensorErrorsSavingData) {
    let htmlString = "";
    for (const error of sensorErrorsSavingData) {
      htmlString += `${error} <br>`;
    }
    html_error.innerHTML += `<input type="text" class="o-layout__item o-button-reset c-error js-error" value="There went something wrong while logging data from these sensors:<br> ${htmlString}" />`;
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

const init = function () {
  console.log("DOM loaded");
  const querystring = new URLSearchParams(window.location.search);
  gameID = querystring.get("gameID");
  html_header = document.querySelector(".js-header");
  html_description = document.querySelector(".js-description");
  html_gameRules = document.querySelector(".js-game-rules");
  html_play = document.querySelector(".js-play");
  html_poweroffButton = document.querySelectorAll(".js-poweroff");
  html_error = document.querySelector(".js-action-button");
  console.log(`play: ${html_play}`);
  getGame();
  listenToSocket();
  toggleNav();
  listenToClickPoweroff();
};

document.addEventListener("DOMContentLoaded", init);
