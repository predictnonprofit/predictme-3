"use strict";
//webSiteUrl + "/dashboard/data/api/rows"
//'X-CSRFToken': getCookie('csrftoken')


// this function will fetch the rows of the saved file
function fetchDataFileRows(){
    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/rows",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
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