/* 
    this file contain custom js functions for ajax,...etc 
*/
"use strict"


// here the columns dual box
// Class definition
var pickedColumns = []; // this will hold all columns that user selected
// Class definition
var KTDualListbox = function() {
    // Private functions
    var initDualListbox = function() {
        // Dual Listbox
        var listBoxes = $(".dual-listbox");

        listBoxes.each(function() {
            var $this = $(this);
            // get titles
            var availableTitle = ($this.attr("data-available-title") != null) ? $this.attr("data-available-title") : "Available Columns";
            var selectedTitle = ($this.attr("data-selected-title") != null) ? $this.attr("data-selected-title") : "Selected Columns";

            // get button labels
            var addLabel = ($this.attr("data-add") != null) ? $this.attr("data-add") : "Add";
            var removeLabel = ($this.attr("data-remove") != null) ? $this.attr("data-remove") : "Remove";
            var addAllLabel = ($this.attr("data-add-all") != null) ? $this.attr("data-add-all") : "Add All";
            var removeAllLabel = ($this.attr("data-remove-all") != null) ? $this.attr("data-remove-all") : "Remove All";

            // get options
            var options = [];
            $this.children("option").each(function() {
                var value = $(this).val();
                var label = $(this).text();
                options.push({
                    text: label,
                    value: value
                });
            });

            // get search option
            var search = ($this.attr("data-search") != null) ? $this.attr("data-search") : "";

            // init dual listbox
            var dualListBox = new DualListbox($this.get(0), {
                addEvent: function(value) {
                    pickedColumns.push(value);
                    // console.log(value);
                },
                removeEvent: function(value) {
                    let arrayIdx = pickedColumns.indexOf(value);
                    if (arrayIdx > -1) {
                        pickedColumns.splice(arrayIdx, 1);
                    }
                    // console.log(value);
                },
                availableTitle: availableTitle,
                selectedTitle: selectedTitle,
                addButtonText: addLabel,
                removeButtonText: removeLabel,
                addAllButtonText: addAllLabel,
                removeAllButtonText: removeAllLabel,
                // options: options,  // commented to avoid duplicated options
            });

            if (search == "false") {
                dualListBox.search.classList.add("dual-listbox__search--hidden");
            }
        });
    };

    return {
        // public functions
        init: function() {
            initDualListbox();
        },
    };
}();




// this ajax function which will upload the donor data file
function uploadDonorDataFile(uploadForm) {
    const webSiteUrl = window.location.origin;
    const webSiteMemberUrl = window.location;
    const donerFileInput = $("#donerFile");
    if (donerFileInput.val()) {
        // $form = uploadForm;
        var formData = new FormData($("#uploadDataFileForm")[0]);
        const fileName = donerFileInput.val().split(/(\\|\/)/g).pop(); // get the file name to parse it in url
        // ajax request to data handler init
        return $.ajax({
            method: "POST",
            cache: false,
            // async: false,
            processData: false,
            contentType: false,
            timeout: 300000,  // 5 minutes
            // timeout: 5000,  
            url: `${webSiteUrl}/dashboard/data/upload/${fileName}`,
            // url: `${webSiteUrl}/dashboard/data/upload`,
            data: formData,
            beforeSend: function (xhr, settings) {
                let timerInterval;
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                var swalUploadProgressDialog = swal.fire({
                    title: "Uploading...",
                    text: "Uploading and Extract the columns from your file, Please wait...",
                    showConfirmButton: false,
                    allowOutsideClick: false,
                    // timer: 3000,
                    onBeforeOpen: () => {
                        Swal.showLoading()
                        timerInterval = setInterval(() => {
                            const content = Swal.getContent()
                            if (content) {
                                const b = content.querySelector('b')
                                if (b) {
                                    b.textContent = Swal.getTimerLeft()
                                }
                            }
                        }, 100)
                    },
                    onClose: () => {
                        clearInterval(timerInterval);
                    }
                });
            },
            
            error: function (error) {
                //called when there is an error
                // console.log(error);
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

            },
            xhr: function () {
                var xhr = $.ajaxSettings.xhr();
                xhr.onprogress = function (e) {
                    // For downloads
                    
                    if (e.lengthComputable) {
                        console.log(e.loaded / e.total);
                    }
                };
                xhr.upload.onprogress = function (e) {
                    // For uploads
                    console.log(e);
                    if (e.lengthComputable) {
                        console.log(e.loaded / e.total);
                    }
                };
                return xhr;
            }
        }).done(function (e) {
            console.log("done");
            // console.log(e);
            // swalUploadProgressDialog.close();
            Swal.close();
        }).fail(function (e) {
            console.log("failed");
            console.log(e);
        });

    } else {
        swal.fire("Error", "You have to select a file!", "error");
    }
}


// this function which will take the picked columns and send them to make the datatable view
function sendPickedColumns(params) {
        let selectedColumns = JSON.stringify(pickedColumns);

        const webSiteUrl = window.location.origin;
        const webSiteMemberUrl = window.location;

        // ajax request to data handler init
        return $.ajax({  // should return to can access from $.when()
            method: "POST",
            cache: false,
            // processData: false,
            // contentType: false,
            timeout: 300000,  // 5 minutes
            url: webSiteUrl + "/dashboard/data/records",
            // dataType: "json",
            data: {
                "columns": selectedColumns
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            /* success: function (data) {
                alert(data);
                // if (data == "OK") {
                //     alert("Your Data has been updated");
                //     location.reload();
                // }
            }, */
            error: function (error) {
                //called when there is an error
                swAlert("Error", error.message, "error");
                //console.log(e.message);
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