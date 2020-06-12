"use strict";

const ip = window.location.hostname;
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
//#endregion

//#region *** DOM references ***
let html_games, html_modal, html_closeModal;
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
const showGames = function (jsonObject) {
  console.log(jsonObject);
  let htmlString = "";
  for (const game of jsonObject.games) {
    htmlString += `
    <li class="c-list-games o-layout__item u-1-of-2-bp3">
      ${game.Name}
      <button data-gameID=${game.ID} class="o-button-reset c-delete-game js-delete"><svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="trash-alt" class="svg-inline--fa fa-trash-alt fa-w-14 c-delete-game__svg" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M32 464a48 48 0 0 0 48 48h288a48 48 0 0 0 48-48V128H32zm272-256a16 16 0 0 1 32 0v224a16 16 0 0 1-32 0zm-96 0a16 16 0 0 1 32 0v224a16 16 0 0 1-32 0zm-96 0a16 16 0 0 1 32 0v224a16 16 0 0 1-32 0zM432 32H312l-9.4-18.7A24 24 0 0 0 281.1 0H166.8a23.72 23.72 0 0 0-21.4 13.3L136 32H16A16 16 0 0 0 0 48v32a16 16 0 0 0 16 16h416a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16z"></path></svg></button>
      <button data-gameID=${game.ID} class="o-button-reset c-edit-game js-edit"><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="edit" class="svg-inline--fa fa-edit fa-w-18 c-edit-game__svg" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path fill="currentColor" d="M402.3 344.9l32-32c5-5 13.7-1.5 13.7 5.7V464c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V112c0-26.5 21.5-48 48-48h273.5c7.1 0 10.7 8.6 5.7 13.7l-32 32c-1.5 1.5-3.5 2.3-5.7 2.3H48v352h352V350.5c0-2.1.8-4.1 2.3-5.6zm156.6-201.8L296.3 405.7l-90.4 10c-26.2 2.9-48.5-19.2-45.6-45.6l10-90.4L432.9 17.1c22.9-22.9 59.9-22.9 82.7 0l43.2 43.2c22.9 22.9 22.9 60 .1 82.8zM460.1 174L402 115.9 216.2 301.8l-7.3 65.3 65.3-7.3L460.1 174zm64.8-79.7l-43.2-43.2c-4.1-4.1-10.8-4.1-14.8 0L436 82l58.1 58.1 30.9-30.9c4-4.2 4-10.8-.1-14.9z"></path></svg></button>
    </li>`;
  }
  html_games.innerHTML = htmlString;
  listenToClickEdit();
  listenToClickDelete();
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
const listenToClickEdit = function () {
  let editButtons = document.querySelectorAll(".js-edit");

  for (const edit of editButtons) {
    edit.addEventListener("click", function () {
      let gameID = edit.getAttribute("data-gameID");
      // console.log(gameID);
      window.location = `http://${ip}/changeGame.html?gameID=${gameID}`;
    });
  }
};

const listenToClickDelete = function () {
  let deleteButtons = document.querySelectorAll(".js-delete");

  for (const deleteButton of deleteButtons) {
    deleteButton.addEventListener("click", function () {
      let gameID = deleteButton.getAttribute("data-gameID");
      const data = {
        ID: gameID,
      };
      socket.emit("F2B_delete_game", data);
    });
  }
};
//#endregion

//#region *** modal ***
// window.onclick = function (event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }
//#endregion

//#region *** SocketIO ***
const listenToSocket = function () {
  socket.on("B2F_game_deleted", function () {
    console.log('Game deleted')
    getGames();
  });
};
//#endregion

const init = function () {
  console.log("DOM loaded");
  html_games = document.querySelector(".js-games");
  html_modal = document.querySelector(".js-modal");
  // html_closeModal = document.querySelector('.js-close-modal').addEventListener('click', function () {
  //   html_modal.style.display = "none";
  // });
  getGames();
  toggleNav();
  listenToSocket();
};

document.addEventListener("DOMContentLoaded", init);
