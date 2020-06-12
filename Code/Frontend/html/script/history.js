"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region *** Global variables ***
//#endregion

//#region *** DOM references ***
let html_historyTable, html_logValues, html_selectSensors;
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
    trigger.addEventListener('touchstart', function () {
      document.querySelector('html').classList.toggle('has-mobile-nav');
    })
  }
};
//#endregion

//#region *** Chart***
const drawChart = function (data, sensorName, timestamps) {
  let ctx = document.querySelector("#myChart").getContext("2d");

  let config = {
    type: "line", //type of chart
    data: {
      labels: timestamps, //all of the labels that are going to be shown along the bottom of the chart
      datasets: [
        {
          label: sensorName, //labe that we added at the top
          backgroundColor: "white", //styling
          borderColor: "red",
          data: data, //this is basically just the data that we would like to bind to the chart
          fill: false,
        },
      ],
    },
    options: {
      //options to change style and behaviour of the chart
      responsive: true,
      title: {
        display: true,
        text: "Line chart with sensor values",
      },
      tooltips: {
        mode: "index",
        intersect: true,
      },
      hover: {
        mode: "nearest",
        intersect: true,
      },
      scales: {
        xAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: "Timestamp",
            },
          },
        ],
        yAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: "Value",
            },
          },
        ],
      },
    },
  };
  let myChart = new Chart(ctx, config);
};
//#endregion

//#region *** Callback-Visualisation - show___ ***
const showHistory = function (jsonObject) {
  console.log(jsonObject);

  let sensorName;
  let converted_labels = [];
  let converted_data = [];

  let htmlString = `<tr class="odd">
        <th>d</th>
        <th>Type</th>
        <th>Description</th>
        <th>Value</th>
        <th>Unit</th>
        <th>Date</th>
        </tr>`;

  for (const historyRow of jsonObject.sensordata) {
    converted_labels.push(historyRow.Date);
    converted_data.push(historyRow.Value);
    htmlString += `<tr><td>${historyRow.Name}</td><td>${historyRow.Type}</td><td>${historyRow.Description}</td><td>${historyRow.Value}</td><td>${historyRow.Unit}</td><td>${historyRow.Date}</td>`;
    sensorName = historyRow.Name;
    console.log(`Sensor name chart: ${sensorName}`);
  }

  drawChart(converted_data, jsonObject.sensordata.Name, converted_labels);
  html_historyTable.innerHTML = htmlString;
};

const showSensors = function (jsonObject) {
  console.log(jsonObject);
  let htmlString;
  for (const sensor of jsonObject.sensors) {
    htmlString += `<option class="js-sensor-option" value="${sensor.ID}">${sensor.Name}</option>`;
  }
  html_selectSensors.innerHTML = htmlString;
  listenToSelectSensor();
};
//#endregion

//#region  *** Callback-No Visualisation - callback___ ***
//#endregion

//#region *** Data Access - get___ ***
const getHistory = function (sensorID) {
  handleData(`http://${lanIP}/api/v1/sensordata/${sensorID}`, showHistory);
};

const getSensors = function () {
  handleData(`http://${lanIP}/api/v1/sensors`, showSensors);
};
//#endregion

//#region *** Event Listeners - listenTo___ ***
const listenToClickLogData = function (btn) {
  console.log("Logging new sensor data");
  socket.emit("F2B_log_sensor_data");
};

const listenToSelectSensor = function () {
  html_selectSensors = document.querySelector(".js-select-sensor");
  html_selectSensors.addEventListener("change", function () {
    console.log("You selected a sensor");
    const selectedSensorID = document.getElementById("select-sensor").value;
    console.log(selectedSensorID);
    getHistory(selectedSensorID);
  });
};
//#endregion

//#region *** SocketIO ***
const listenToSocket = function () {
  socket.on("B2F_logged_data", function () {
    document.querySelector(".js-error-message").innerHTML = "New data succesfully added.";
    getHistory();
  });

  socket.on("B2F_error_logging_data", function (errors) {
    let errorMessage;
    for (const error of errors) {
      errorMessage += `${error}\n`;
    }
    document.querySelector(".js-error-message").innerHTML = errorMessage;
  });
};
//#endregion

const init = function () {
  console.log("DOM loaded");
  html_historyTable = document.querySelector(".js-history-table");
  html_logValues = document.querySelector(".js-log-values").addEventListener("click", listenToClickLogData);
  html_selectSensors = document.querySelector(".js-select-sensor");
  getHistory(101);
  getSensors();
  listenToSocket();
  toggleNav();
};

document.addEventListener("DOMContentLoaded", init);
