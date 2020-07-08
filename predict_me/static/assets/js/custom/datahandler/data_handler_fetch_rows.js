"use strict";



// this function will fetch the rows of the saved file
function fetchDataFileRows(recordsCount){
    if(typeof recordsCount === "undefined"){
        recordsCount = 50;
    }
    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/rows",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
        data: {
            "recordsCount": parseInt(recordsCount)
        },
        error: function (error) {
            //called when there is an error
            swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
        },
        statusCode: {
            404: function () {
                swAlert("Error", "Page not Found!!", "error");
            },
            400: function () {
                swAlert("Error", "Bad Request!!!", "error");
            },
            401: function () {
                swAlert("Error", "Unauthorized!!", "error");
            },
            403: function () {
                swAlert("Error", "Forbidden!!", "error");
            },
            500: function () {
                swAlert("Error", "Internal Server Error!!", "error");
            },
            502: function () {
                swAlert("Error", "Bad Gateway!!", "error");
            },
            503: function () {
                swAlert("Error", "Service Unavailable!!", "error");
            },

        }
        
    }); 
}

// this function will fetch rows with not validate data
function fetchNotValidateRows(colName){
    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/filter-rows",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
        data: {
            "column_name": colName,
            'records_number': clickedRecordsCount,
        },
        dataSrc: '',
        error: function (error) {
            //called when there is an error
            swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
        },
        statusCode: {
            404: function () {
                swAlert("Error", "Page not Found!!", "error");
            },
            400: function () {
                swAlert("Error", "Bad Request!!!", "error");
            },
            401: function () {
                swAlert("Error", "Unauthorized!!", "error");
            },
            403: function () {
                swAlert("Error", "Forbidden!!", "error");
            },
            500: function () {
                swAlert("Error", "Internal Server Error!!", "error");
            },
            502: function () {
                swAlert("Error", "Bad Gateway!!", "error");
            },
            503: function () {
                swAlert("Error", "Service Unavailable!!", "error");
            },

        }
        
    }); 
}

// function will sort the rows based on the errors...
function sortHeader(colObj){
    $("#resetSortTableBtn").removeClass("disabled");
    $("#resetSortTableBtn").removeAttr("disabled style");
    isClickedFilterCol = true;
    const colJqObj = $(colObj);
    const colName = colJqObj.data("col-name");
    clickedFilteredColName = colName;
    //console.log(colJqObj[0].attributes);
    // check if the clicked column has error in validation of his cell(s)
    if(colJqObj.data('is-error') === 1){
        //data_handler_table
        const dataTable = $("#data_handler_table");
        $("#loadingDataSpinner").fadeIn();
        // $("#data_handler_table tbody tr").detach();
        document.getElementById("data_handler_body").innerHTML = "";

        let fetchNotValidateRowsResponse = fetchNotValidateRows(colName);
        $.when(fetchNotValidateRowsResponse).done(function (rowData, rowTextStatus, rowJqXHR) {
            /* console.log(rowData);
            console.log(rowTextStatus);
            console.log(rowJqXHR); */
            // console.log(rowData);
            drawDataTableRows(rowData, true);
        });
    }
}


// function will call when user change the select menu of how many records will dispaly
function fetchRecordsByCount(recordsCount){
    const recCount = parseInt(recordsCount);
    $("#data_handler_table > tbody tr").empty();
    $("#loadingDataSpinner").fadeIn('fast');
    // let tableBody = document.getElementById("data_handler_body");
    // tableBody.innerHTML = "";
    let resetFetchRecoredsResponse = fetchDataFileRows(recCount);
    $.when(resetFetchRecoredsResponse).done(function (data, textStatus, jqXHR){
        if(textStatus == "success"){
            drawDataTableRows(data, false);
        }else{
            swAlert("Error", data, 'error');
        }
    });
}


// this function will fetch the rows which contain search query
function fetchDataFileRowsBySearchQuery(searchQuery){
    
    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/search-query-records",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
        data: {
            "searchQuery": searchQuery
        },
        error: function (error) {
            //called when there is an error
            swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
        },
        statusCode: {
            404: function () {
                swAlert("Error", "Page not Found!!", "error");
            },
            400: function () {
                swAlert("Error", "Bad Request!!!", "error");
            },
            401: function () {
                swAlert("Error", "Unauthorized!!", "error");
            },
            403: function () {
                swAlert("Error", "Forbidden!!", "error");
            },
            500: function () {
                swAlert("Error", "Internal Server Error!!", "error");
            },
            502: function () {
                swAlert("Error", "Bad Gateway!!", "error");
            },
            503: function () {
                swAlert("Error", "Service Unavailable!!", "error");
            },

        }
        
    }); 
}

// function will call when user change the select menu of how many records will dispaly
function fetchRecordsBySearchQuery(searchQuery){
    $("#data_handler_table > tbody tr").empty();
    $("#loadingDataSpinner").fadeIn();
    $("#resetSortTableBtn").removeClass("disabled");
    $("#resetSortTableBtn").removeAttr("disabled style");
    // let tableBody = document.getElementById("data_handler_body");
    // tableBody.innerHTML = "";
    let searchQureyResponse = fetchDataFileRowsBySearchQuery(searchQuery);
    $.when(searchQureyResponse).done(function (data, textStatus, jqXHR){
        if(textStatus == "success"){
            console.log(data.length)
            drawDataTableRows(data, false);
        }else{
            swAlert("Error", data, 'error');
        }
    });
}


// function will save if the member accept and download upload template
function saveMemberAccepts(acceptData) {
    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/accepts-download",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
        data: {
            "accept_data": JSON.stringify(acceptData)
        },
        error: function (error) {
            //called when there is an error
            swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
        },
        statusCode: {
            404: function () {
                swAlert("Error", "Page not Found!!", "error");
            },
            400: function () {
                swAlert("Error", "Bad Request!!!", "error");
            },
            401: function () {
                swAlert("Error", "Unauthorized!!", "error");
            },
            403: function () {
                swAlert("Error", "Forbidden!!", "error");
            },
            500: function () {
                swAlert("Error", "Internal Server Error!!", "error");
            },
            502: function () {
                swAlert("Error", "Bad Gateway!!", "error");
            },
            503: function () {
                swAlert("Error", "Service Unavailable!!", "error");
            },

        }

    });
}


// function will send request for the server to check if member upload data file, this will use in setTheCookie function
function checkIfMemberUploadDataFile() {
    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/check-upload-member",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
        error: function (error) {
            //called when there is an error
            swAlert("Error", `${error.statusText}:-> ${error.message}`, "error");
        },
        statusCode: {
            404: function () {
                swAlert("Error", "Page not Found!!", "error");
            },
            400: function () {
                swAlert("Error", "Bad Request!!!", "error");
            },
            401: function () {
                swAlert("Error", "Unauthorized!!", "error");
            },
            403: function () {
                swAlert("Error", "Forbidden!!", "error");
            },
            500: function () {
                swAlert("Error", "Internal Server Error!!", "error");
            },
            502: function () {
                swAlert("Error", "Bad Gateway!!", "error");
            },
            503: function () {
                swAlert("Error", "Service Unavailable!!", "error");
            },

        }

    });
}