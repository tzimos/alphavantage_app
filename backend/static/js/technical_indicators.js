$(document).ready(function () {
  var intervals = [
    "1min",
    "5min",
    "15min",
    "30min",
    "60min",
  ]
  var colors = {
    0: "red",
    1: "green",
    2: "yellow",
    3: "black",
  }
  var timePeriods = [
    "20",
    "50",
    "200",
  ]
  var supportedFunctions = [
    "SMA", "EMA", "WMA", "DEMA", "TEMA", "TRIMA", "KAMA",
    "MAMA", "VWAP", "T3", "MACD", "MACDEXT",
    "STOCH", "STOCHF", "RSI", "STOCHRSI", "WILLR",
    "ADX", "ADXR", "APO", "PPO", "MOM", "BOP", "CCI", "CMO",
    "ROC", "ROCR", "AROON", "AROONOSC", "MFI", "TRIX", "ULTOSC", "DX",
    "MINUS_DI", "PLUS_DI", "MINUS_DM", "PLUS_DM", "BBANDS", "MIDPOINT",
    "MIDPRICE", "SAR", "TRANGE", "ATR", "NATR", "AD", "ADOSC",
    "OBV", "HT_TRENDLINE", "HT_SINE", "HT_TRENDMODE", "HT_DCPERIOD",
    "HT_DCPHASE", "HT_PHASOR"
  ]
  var seriesTypes = [
    "close",
    "open",
    "high",
    "low",
  ]
  var selectedFunction = "SMA"
  var selectedInterval = "1min";
  var selectedTimePeriod = "20";
  var selectedSeriesType = "close";

  function initialisePage() {
    var mapping = {
      "#function-options": {
        options: supportedFunctions,
        createdElements: "",
      },
      "#interval-options": {
        options: intervals,
        createdElements: "",
      },
      "#time-period-options": {
        options: timePeriods,
        createdElements: "",
      },
      "#series-type-options": {
        options: seriesTypes,
        createdElements: "",
      },
    }
    $.each(mapping, function (elementId, value) {
      $.each(value.options, function (idx, elem) {
        value.createdElements += `<a class="dropdown-item" href="#">${elem}</a>`;
      })
      $(elementId).append(value.createdElements);
    })
  }

  function createChart(data) {
    var intradayChart = $("#technical-indicators-chart");
    intradayChart.remove();
    $('.chart-wrapper').append('<canvas id="technical-indicators-chart"></canvas>');
    var datasets = [];
    $.each(data.data_keys, function (index, name) {
      yAxisValues = $.map(data.data, function (element) {
        if (element.name === name) {
          return element.price
        }
      });
      console.log(index, colors[index])
      datasets.push({
        label: name,
        data: yAxisValues,
        backgroundColor: colors[index],
        borderColor: colors[index],
        borderWidth: 1,
        fill: false
      })
    })
    return new Chart($("#technical-indicators-chart"), {
      type: "line",
      data: {
        labels: data.labels,
        datasets: datasets
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


  function getHistoricalData(selectedFunction, selectedInterval, selectedTimePeriod, selectedSeriesType) {
    var payload = {
      "interval": selectedInterval,
      "function": selectedFunction,
      "symbol": window.symbol,
      "time_period": selectedTimePeriod,
      "series_type": selectedSeriesType,
    }
    $.ajax(
      {
        type: "POST",
        url: window.technical_indicators_url,
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

  function registerListeners() {

    $(".refresh-icon").click(function () {
      getHistoricalData();
    })
    $(".dropdown-menu a").click(function () {
      var selectedText = $(this).text();
      if (intervals.includes(selectedText)) {
        selectedInterval = selectedText;
      }
      if (supportedFunctions.includes(selectedText)) {
        selectedFunction = selectedText
      }
      if (timePeriods.includes(selectedText)) {
        selectedTimePeriod = selectedText;
      }
      if (seriesTypes.includes(selectedText)) {
        selectedSeriesType = selectedText
      }
      $(this).parents(".dropdown").find(".dropdown-toggle").text(selectedText);
      getHistoricalData(selectedFunction, selectedInterval, selectedTimePeriod, selectedSeriesType)
    });
  }

  initialisePage()
  registerListeners()
  getHistoricalData(selectedFunction, selectedInterval, selectedTimePeriod, selectedSeriesType)
});