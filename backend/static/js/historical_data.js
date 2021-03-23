$(document).ready(function () {
  var intervals = [
    "1min",
    "5min",
    "15min",
    "30min",
    "60min",
  ]
  var _functions = [
    "Intraday",
    "Daily",
    "Weekly",
    "Monthly",
  ]
  var functionsMapping = {
    "Intraday": "TIME_SERIES_INTRADAY",
    "Daily": "TIME_SERIES_DAILY",
    "Weekly": "TIME_SERIES_WEEKLY",
    "Monthly": "TIME_SERIES_MONTHLY",
  }
  var selectedFunction = "Intraday"
  var selectedInterval = "1min";

  $(".dropdown-menu a").click(function () {
    var selectedText = $(this).text();
    if (intervals.includes(selectedText)) {
      selectedInterval = selectedText;
    }
    if (_functions.includes(selectedText)) {
      selectedFunction = selectedText
    }
    var intervalDropDown = $(".interval-dropdown");
    if (selectedFunction === "Intraday") {
      intervalDropDown.show();
    } else {
      intervalDropDown.hide();
    }
    $(this).parents(".dropdown").find(".dropdown-toggle").text(selectedText);
    getHistoricalData(selectedInterval, functionsMapping[selectedFunction]);
  });

  $(".refresh-icon").click(function () {
    getHistoricalData();
  })

  function createChart(data) {
    var intradayChart = $("#intradayChart");
    intradayChart.remove();
    $('.chart-wrapper').append('<canvas id="intradayChart"></canvas>');
    return new Chart($("#intradayChart"), {
      type: "line",
      data: {
        labels: data.labels,
        datasets: [
          {
            label: "Open",
            data: $.map(data.open, function (val) {
              return val
            }),
            backgroundColor: "blue",
            borderColor: "blue",
            borderWidth: 1,
            fill: false
          },
          {
            label: "Close",
            data: $.map(data.close, function (val) {
              return val
            }),
            backgroundColor: "yellow",
            borderColor: "yellow",
            borderWidth: 1,
            fill: false
          },
          {
            label: "High",
            data: $.map(data.high, function (val) {
              return val
            }),
            backgroundColor: "green",
            borderColor: "green",
            borderWidth: 1,
            fill: false
          },
          {
            label: "Low",
            data: $.map(data.low, function (val) {
              return val
            }),
            backgroundColor: "red",
            borderColor: "red",
            borderWidth: 1,
            fill: false
          },
        ]
      },
      options: {
        title: {
          display: true,
          text: data.meta.symbol + " | " + data.meta.information
        },
        scales: {
          xAxes: [{
            ticks: {
              autoSkip: true,
              maxTicksLimit: 10
            }
          }]
        }
      }
    });
  }

  function getHistoricalData(interval = null, _function = null) {
    if (!_function) {
      _function = functionsMapping[selectedFunction]
    }
    if (!interval) {
      interval = selectedInterval
    }
    var payload = {
      "symbol": window.symbol,
      "function": _function,
    }
    if (_function === "TIME_SERIES_INTRADAY") {
      payload["interval"] = interval
    }
    $.ajax(
      {
        type: "POST",
        url: window.historical_data_url,
        data: payload,
        success: function (data) {
          createChart(data);
        },
        error: function (data) {
          window.location.href = data.responseJSON.redirect;
        },
        options: {"contentType": "application/json"}
      }
    )
  }


  getHistoricalData();


});
