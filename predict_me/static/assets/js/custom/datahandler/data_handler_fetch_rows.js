"use strict";
var isAjaxRequestDone = { // this object will be in the success(), method of ajax requests, to set true mean all done, false not done
  isDone: "",
  functionName: "",
};


// this function will fetch the rows of the saved file
function fetchDataFileRows(recordsCount) {
  const parameters = window.location.pathname;
  if (typeof recordsCount === 'undefined') {
    recordsCount = 50;
  }
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/rows",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      "recordsCount": parseInt(recordsCount),
      'parameters': parameters,
    },
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    complete: function(jqXHR, textStatus) {
      /*  console.log(textStatus);
        console.log(jqXHR.status);
        console.log(jqXHR);*/
      // check if the request complete successfully
      /* if(textStatus === 'success' && jqXHR.status === 200){

       }*/

    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

// this function will fetch rows with not validate data
function fetchNotValidateRows(colName) {
  const parameters = window.location.pathname;
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/filter-rows",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      "column_name": colName,
      'records_number': clickedRecordsCount,
      'parameters': parameters,
    },
    dataSrc: '',
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

// function will sort the rows based on the errors...
function sortHeader(colObj) {
  // check if there is no search query, to run the validate
  if ($("#searchQuery").val() === "") {
    $("#resetSortTableBtn").removeClass("disabled");
    $("#resetSortTableBtn").removeAttr("disabled style");
    isClickedFilterCol = true;
    const colJqObj = $(colObj);
    const colName = colJqObj.data("col-name");
    clickedFilteredColName = colName;
    //console.log(colJqObj[0].attributes);
    // check if the clicked column has error in validation of his cell(s)
    if (colJqObj.data('is-error') === 1) {
      //data_handler_table
      const dataTable = $("#data_handler_table");
      $("#loadingDataSpinner").fadeIn();
      // $("#data_handler_table tbody tr").detach();
      document.getElementById("data_handler_body").innerHTML = "";

      let fetchNotValidateRowsResponse = fetchNotValidateRows(colName);
      $.when(fetchNotValidateRowsResponse).done(function(rowData, rowTextStatus, rowJqXHR) {
        /* console.log(rowData);
        console.log(rowTextStatus);
        console.log(rowJqXHR); */
        // console.log(rowData);
        drawDataTableRows(rowData, true);
      });
    }
  } else {
    return false;
  }
}


// function will call when user change the select menu of how many records will dispaly
function fetchRecordsByCount(recordsCount) {
  const recCount = parseInt(recordsCount);
  $("#data_handler_table > tbody tr").empty();
  $("#loadingDataSpinner").fadeIn('fast');
  // let tableBody = document.getElementById("data_handler_body");
  // tableBody.innerHTML = "";
  let resetFetchRecoredsResponse = fetchDataFileRows(recCount);
  $.when(resetFetchRecoredsResponse).done(function(data, textStatus, jqXHR) {
    if (textStatus == "success") {
      drawDataTableRows(data, false);
    } else {
      swAlert("Error", data, 'error');
    }
  });
}


// this function will fetch the rows which contain search query
function fetchDataFileRowsBySearchQuery(searchQuery) {
  const parameters = window.location.pathname;
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/search-query-records",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      "searchQuery": searchQuery,
      'parameters': parameters,
    },
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

// function will call when user change the select menu of how many records will dispaly
function fetchRecordsBySearchQuery(searchQuery) {
  $("#data_handler_table > tbody tr").empty();
  $("#loadingDataSpinner").fadeIn();
  $("#resetSortTableBtn").removeClass("disabled");
  $("#resetSortTableBtn").removeAttr("disabled style");
  // let tableBody = document.getElementById("data_handler_body");
  // tableBody.innerHTML = "";
  let searchQureyResponse = fetchDataFileRowsBySearchQuery(searchQuery);
  $.when(searchQureyResponse).done(function(data, textStatus, jqXHR) {
    if ((textStatus == "success") && (jqXHR.status === 200)) {
      // console.log(data);
      drawDataTableRows(data, false);
    } else {
      swAlert("Error", data, 'error');
    }
  });
}


// function will save if the member accept and download upload template
function saveMemberAccepts(acceptData) {
  const parameters = window.location.pathname;
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/accepts-download",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      "accept_data": JSON.stringify(acceptData),
      'parameters': parameters,
    },
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}


// function will send request for the server to check if member upload data file, this will use in setTheCookie function
function checkIfMemberUploadDataFile() {
  const parameters = window.location.pathname;

  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/check-upload-member",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      'parameters': parameters
    },
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}


// function will check if the member set his process steps to done
function checkIfMemberProcessStatus(choice) {
  const parameters = window.location.pathname;
  let data = "";
  if (typeof choice !== "undefined") data = {
    "choice": choice,
    'parameters': parameters
  }
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/check-process-status",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: data,
    global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}


// fetch the last session name of the member
function fetchLastSessionName() {
  const parameters = window.location.pathname;
  const data = {
    'parameters': parameters
  };

  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/fetch-last-session-name",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: data,
    global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}


// set the last session name or the last step on datahandler
function setSessionLastName(sessionName) {
  const parameters = window.location.pathname;
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/set-last-session-name",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      "session_name": sessionName,
      'parameters': parameters
    },
    global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

function checkSessionLabelRequest() {
  const parameters = window.location.pathname;
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/set-session-label",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      'get_session_label': true,
      'parameters': parameters
    },
    // global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

function setSessionLabelRequest(sessionLabel, sessionTask) {
  const parameters = window.location.pathname;
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/set-session-label",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: {
      'session_task': sessionTask,
      "session_label": sessionLabel,
      'parameters': parameters
    },
    // global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

// delete single or all sessions for the user
function deleteDataSessionsRequest(singleOrAll) {
  const parameters = window.location.pathname;
  let data = {
    'parameters': parameters,
    "method": singleOrAll
  };
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/delete-data-session",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: data,
    global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

function renameSessionRequest(sessionName) {
  const parameters = window.location.pathname;
  let data = {
    'parameters': parameters,
    "session_name": sessionName
  };
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/rename-data-session",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: data,
    global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}

// this is the function will run the Model
function runModel() {
  const parameters = window.location.pathname;
  let data = {};
  return $.ajax({
    url: webSiteUrl + "/dashboard/data/api/run-model",
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    method: "POST",
    data: data,
    global: false,
    error: function(error) {
      //called when there is an error
      swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
    },
    success: function(results) {
      console.log("results", results)
    },
    statusCode: {
      404: function() {
        swAlert("Error", "Page not Found!!", "error");
      },
      400: function() {
        swAlert("Error", "Bad Request!!!", "error");
      },
      401: function() {
        swAlert("Error", "Unauthorized!!", "error");
      },
      403: function() {
        swAlert("Error", "Forbidden!!", "error");
      },
      500: function() {
        swAlert("Error", "Internal Server Error!!", "error");
      },
      502: function() {
        swAlert("Error", "Bad Gateway!!", "error");
      },
      503: function() {
        swAlert("Error", "Service Unavailable!!", "error");
      },

    }

  });
}


// this function will connect using webSocket
function runSocket() {
  try {
    $("#runModelModal").modal("show");
    $('#runModelModal').modal('handleUpdate');
    const url = webSiteUrl.replace("http", "ws") + "/dashboard/data/ws/run-model";
    if (!window.WebSocket) alert("WebSocket not supported by this browser");
    // const url = webSiteUrl + "/dashboard/data/api/socket";
    const socket = new WebSocket(url);
    // if (socket.readyState == WebSocket.OPEN) {
    //   console.log("oelsadfi")
    // }
    socket.onopen = function open() {
      console.log('WebSockets connection established.');
      socket.send('RUN_THE_MODEL');
    };


    // when get message from the server
    socket.onmessage = function(event) {
      // alert(`[message] Data received from server: ${event.data}`);
      const content = document.querySelector("#runModalResults").innerHTML;
      document.querySelector("#runModalResults").innerHTML = content + "<br />" + event.data;
      if(event.data === "Complete Successfully!"){
        // console.log("the model complete running");
        // $("#runModalResults").addClass("text-success");
        setTimeout(function() {
          window.location.href = webSiteUrl + "/profile";
        }, 1000);
      }
    };

    // onclose connection
    socket.onclose = function(event) {
      if (event.wasClean) {
        console.log(event)
        // alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
        // console.log(event);
        // swAlert("Info", `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`, "info");
        // $("#runModelModal").modal("hide");
      } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        alert('[close] Connection died');
        // $("#runModelModal").modal("hide");
      }

    };

    // onerror
    socket.onerror = function(error) {
      // alert(`[error] ${error.message}`);
      swAlert("Error", `[error] ${error.message}`, "error");
    };

    // close
    //socket.close();
  } catch (error) {
    // console.error(error);
    console.error(error);
  }

}
