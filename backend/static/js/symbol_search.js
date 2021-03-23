$(document).ready(function () {

  /**
   * Appends to results dom element row by row the symbol and company names data.
   * @param  {String} element: The resutls html element.
   * @param  {Array} arr: An array which contains objects with the symbol and company names as keys.
   */
  function createResultElements(element, arr) {
    element.empty();
    if (arr.length === 0) {
      element.append(
        "<div className='row align-items-center'><div class='col'>No results returned</div></div>"
      )
      return
    }
    elementToAppend = `<div class='row align-items-center grid-header'>
         <div class='col'>Symbol</div>
         <div class='col'>Company name</div>
         </div>`;
    $.each(arr, function (index, val) {
      elementToAppend += `
            <a href="${window.window.symbol_search_url_analytical + val.symbol}" 
                 class='row align-items-center grid-row'>
            <div class='col'>${val.symbol}</div>
            <div class='col'>${val.name}</div>
           </a>`

    });
    element.append(elementToAppend);
  }

  /**
   * Debounces a function for a specified wait period.
   * @param  {function} func: The function to be called
   * @param  {number} wait: The waiting period in milliseconds.
   * @param  {boolean} immediate: Determines if we want to execute the function now.
   * */
  function debounce(func, wait, immediate = false) {
    var timeout;
    return function () {
      var context = this, args = arguments;
      var later = function () {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  }

  $("input[type='search']").keyup(debounce(function (e) {
    e.preventDefault();
    // e.preventDefault();
    var search_term = $('#search-form').val().toLowerCase();
    var resultSelector = $("#result");
    if (search_term.length === 0) {
      resultSelector.empty();
      return;
    }
    $.ajax(
      {
        type: "POST",
        url: window.symbol_search_url,
        data: {"query": search_term},
        success: function (data) {
          createResultElements(resultSelector, data);
        },
        options: {"contentType": "application/json"}
      }
    )
  }, 300));
});
