let webSiteUrl = window.location.origin;

function setSessionLabelRequest(sessionLabel, sessionTask){

    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/set-session-label",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
        data: {'session_task': sessionTask, "session_label": sessionLabel},
        // global: false,
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



function checkSessionLabelRequest(){
    return $.ajax({
        url: webSiteUrl + "/dashboard/data/api/set-session-label",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        method: "POST",
        data: {'get_session_label': true},
        // global: false,
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