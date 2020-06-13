/*
    this file contain custom js functions for ajax,...etc
*/
"use strict"
var selectedPickedColumns = Array();  // global array will include the picked and validated column names
var webSiteUrl = window.location.origin;
const tooltipInfo = {
    "object": "Text or mixed numeric and non-numeric values",
    "int64": "Integer numbers",
    "float64": "Floating point numbers",
    "bool": "True/False values",
    "datetime64": "Date and time values",
    "category": "Finite list of text values",
    "timedelta": "Differences between two datetimes",
};

function swAlert(alertTitle, alertMsg, alertType) {
    swal.fire(`${alertTitle}`, `${alertMsg}`, `${alertType}`);
}

// here the columns dual box
// Class definition
var pickedColumns = []; // this will hold all columns that user selected
// Class definition
var KTDualListbox = function () {
    // Private functions
    var initDualListbox = function () {
        // Dual Listbox
        var listBoxes = $(".dual-listbox");

        listBoxes.each(function () {
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
            $this.children("option").each(function () {
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
                addEvent: function (value) {
                    pickedColumns.push(value);
                    // console.log(value);
                },
                removeEvent: function (value) {
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
        init: function () {
            initDualListbox();
        },
    };
}();




// this ajax function which will upload the donor data file
function uploadDonorDataFile(uploadForm) {
    const webSiteUrl = window.location.origin;
    // const webSiteMemberUrl = window.location;
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
            timeout: 300000, // 5 minutes
            // timeout: 5000,
            url: `${webSiteUrl}/dashboard/data/upload/${fileName}`,
            // url: `${webSiteUrl}/dashboard/data/upload`,
            data: formData,
            beforeSend: function (xhr, settings) {
                let timerInterval;
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                var swalUploadProgressDialog = swal.fire({
                    title: "Uploading...",
                    text: "Uploading you data file, Please wait...",
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
            // console.log("done");
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
    // let selectedColumns = JSON.stringify(pickedColumns);
    // let selectedColumns = JSON.parse(pickedColumns);
    
    let selectedColumns = {
        "columns": selectedPickedColumns
    };
    console.log(selectedColumns);
    const webSiteMemberUrl = window.location;

    // ajax request to data handler init
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/save-columns",
        // dataType: "json",
        data: selectedColumns,
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



// this function will fetch the columns of the saved file
function fetchDataFileColumns(fetchedColumns) {

    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/get-columns",
        // dataType: "json",
        data: fetchedColumns,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        /*  success: function (data) {
             for(let c of data){
                 columnsList.push(c);
             }
            
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


function setColumnNamesHeader(columnsList) {
    // console.log(columnsList);

    var tableHeaderElement = $("#data_handler_table > thead > tr:last");
    for (let col of columnsList) {
        var row = `
            <td data-col-name='${col}'>${col} <i class="icon-lg d-none text-danger la la-info-circle"></i></td>
        `;
        tableHeaderElement.append(row);
    }
}

// this function return markup oject of every table cell will append to every row in the datatable
function drawDataTableRows(rowsData) {
    var tableBodyElement = $("#data_handler_table > tbody tr:last");
    // console.log(rowsData.data);
    let currentRowData = rowsData.data;
    for (let colIdx = 0; colIdx < currentRowData.length; colIdx++) {
        let currentDataObj = currentRowData[colIdx];
        let allCells = "";
        let tableRow = "<tr class='datatable-row'> ";
        // console.log(Object.entries(currentDataObj));
        // loop through key and value in the json object of the row
        for (let [key, value] of Object.entries(currentDataObj)) {
            
            
            if (key !== "ID") {
                if (value.is_error == false) {
                    var cellMarkup = `

                <td>
                    <input class='form-control form-control-solid w-auto data-table-col ' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                </td>

            `;
                } else if (value.is_error == true) {
                    const tableColHeader = $(`#data_handler_table > thead tr > td[data-col-name='${key}']`);
                    const colText = tableColHeader.text().trim();
                    // check if the current table td value has error, highlighted the column name header
                    if (key.trim() === colText) {
                        //console.log("error", colText);
                        tableColHeader.find("i").removeClass("d-none");
                       // tableColHeader.addClass("bg-light-danger")
                        tableColHeader.addClass("text-danger");
                    }
                    var cellMarkup = `

                <td>
                    <input class='form-control bg-light-danger is-invalid data-table-col w-auto form-control-solid form-control-sm' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                </td>

            `;
                }
                allCells += cellMarkup;
            }
        }
        tableRow += allCells + "</tr>";
        tableBodyElement.after(tableRow);
    }



}



// this when the user enter the amount of rows which will purchased
function culcalteExtraRows() {
    let totlaAmountDue = $("#totlaAmountDue");
    let extraRowsPurchased = $("#extraRowsPurchased");
    totlaAmountDue.val(parseFloat(extraRowsPurchased.val() * 0.5));
}

var allRowsUpdated = {
    "rows": [] // array of new updated rows
};
// this function will run on change the input of the data file
function getChangedValue() {
    $(".data-table-col").on("change", function () {
        let currentTableCellVal = $(this).val().trim();
        let currentColumnName = $(this).attr("name");
        let currentRowIdx = $(this).data('rowId');
        // console.log(currentColumnName, currentRowIdx);
        let allNewUpdateValues = {
            "rowIdx": currentRowIdx,
            "colName": currentColumnName,
            "newCellVal": currentTableCellVal,
        };
        allRowsUpdated['rows'].push(allNewUpdateValues);

        console.log(allRowsUpdated);

    });

}


// this function when user want to save changes to data file
function updateMemberDataFile() {
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/save-rows",
        // dataType: "json",
        data: allRowsUpdated,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        /*  success: function (data) {
             for(let c of data){
                 columnsList.push(c);
             }
            
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

// delete data file function
function deleteDataFile() {
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/delete-file",
        // dataType: "json",
        data: {
            "rows[]": allRowsUpdated
        },
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        /*  success: function (data) {
             for(let c of data){
                 columnsList.push(c);
             }
            
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


// this function when user upload the file, and show the progress modal,
// this will hide or show as needed
function uploadProgressModal(isOk, data) {
    //var optionsList = [];
    var optionsList = '';
    var dataFileColumnsSelect = $("#availableColumnsList");
    // is Ok mean if the row counts dont cross the records limit of the member supscription plan

    let rowCount = parseInt(data['row_count']);
    // console.log(rowCount);
    var rowCountProgressDialog = $("#recordsCountModal");
    var recordsCounterProgressBar = $("#recordsCounterProgressBar");
    let currentRowCounter = $("#currentRowCounter > b");
    let progressWarnText = $("#progressWarnText");
    var nextProgressBtnModal = $("#nextProgressBtnModal");
    let allowdedRowsCount = $("#progressRecords > b:first");
    rowCountProgressDialog.modal('handleUpdate');
    rowCountProgressDialog.modal('show');
    recordsCounterProgressBar.attr("aria-valuemax", '100');
    let progVal = 0;
    // the interval
    var progressInterval = setInterval(progressIntervalFunc, 35);
    function progressIntervalFunc() {
        
        let recordNowValue = parseInt(recordsCounterProgressBar.attr("aria-valuenow"));
        recordsCounterProgressBar.attr("aria-valuenow", recordNowValue + 1);
        var progressPercentage = ((recordNowValue/rowCount) * 100);
        // var progressPercentage = Math.round((recordNowValue/rowCount) * 100);
        // var progressPercentage = Math.trunc((recordNowValue/rowCount) * 100);
        // var progressPercentage = Math.ceil((recordNowValue/rowCount) * 100);

        //set the labels and width to progressbar
        recordsCounterProgressBar.css('width', progressPercentage + '%');
        recordsCounterProgressBar.children().text(progressPercentage.toFixed() + " %");
        currentRowCounter.text(recordNowValue);
        
        if(isOk === true){
            if(progVal <= rowCount){
                progVal++;
               // console.log(progVal);
            }else{
                clearInterval(progressInterval);
                let i = 0;
                for(let [name, dType] of Object.entries(data['columns'])){
                    i++;
                    
                    let tmpMarkupLi = `
                    <li data-idx='${i}' class="columnItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action">
                                ${name}
                               <span>
                                    <span class="label label-inline label-light-primary font-weight-bold">${dType}</span>
                                    <span class="label pulse pulse-info" style="top: 6px;" data-toggle="tooltip" title='${tooltipInfo[dType]}'>
                                        <span class="position-relative"><i class="icon-xl la la-info-circle"></i></span>
                                        <span class="pulse-ring"></span>
                                    </span>
                               </span>
                            </li>
                        \n
                    `;
                    optionsList += tmpMarkupLi;
                }
               
                dataFileColumnsSelect.html(optionsList);
                // console.log(dataFileColumnsSelect);
                //KTDualListbox.init();
                rowCountProgressDialog.modal('hide');
                $('#columnsDualBoxModal').modal('handleUpdate');
                $('#columnsDualBoxModal').modal('show');
                
            }
           
            

        }else{
            // here in this elese block, when records count more than the allowed 
            if(progVal <= parseInt(allowdedRowsCount.text())){
                progVal++;
                // console.log(progVal);
            }else{
                // clearInterval(progressInterval);
                currentRowCounter.addClass("text-danger bg-danger-o-50 p-1");
                recordsCounterProgressBar.removeClass("bg-success");
                recordsCounterProgressBar.addClass("bg-danger-o-50");
                nextProgressBtnModal.fadeIn();
                $("#useSubPlanBtn").fadeIn();
                progressWarnText.fadeIn();
                
                
            }
            // console.log("Here get to else block if isOk is false");
            
            
            
        }
        
    }
    /* nextProgressBtnModal.click(function (ev){
        clearInterval(progressInterval);
        rowCountProgressDialog.modal('hide');
       $("#extraRecordsModel").modal("handleUpdate");
       $("#extraRecordsModel").modal("show");
    }); */
}


// this function will fetch all columns in the data file to make the member reselect the columns
function fetchDataFileAllColumns() {

    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/get-all-columns",
        // dataType: "json",
        //data: fetchedColumns,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        /*  success: function (data) {
             for(let c of data){
                 columnsList.push(c);
             }
            
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

// when user click on reselect columns btn
function reselectColumnsFunc(){
    var optionsList = '';
    var dataFileColumnsSelect = $("#availableColumnsList");
    const columnsDualBoxModal = $("#columnsDualBoxModal");
    $("#closeColumnsDualBoxBtn").show();
    
    const allColumnsResponse = fetchDataFileAllColumns();
    $.when(allColumnsResponse).done(function (data, textStatus, jqXHR){
        let i = 0;
        for(let [name, dType] of Object.entries(data)){
            i++;  
             let tmpMarkupLi = `
                    <li data-idx='${i}' class="columnItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action">
                                ${name}
                               <span>
                                    <span class="label label-inline label-light-primary font-weight-bold">${dType}</span>
                                    <span class="label pulse pulse-info" style="top: 6px;" data-toggle='tooltip' title="${tooltipInfo[dType]}">
                                        <span class="position-relative"><i class="icon-xl la la-info-circle"></i></span>
                                        <span class="pulse-ring"></span>
                                    </span>
                               </span>
                            </li>
                        \n
                    `;
            optionsList += tmpMarkupLi;
        }

        dataFileColumnsSelect.html(optionsList);
        columnsDualBoxModal.modal("handleUpdate");
        columnsDualBoxModal.modal("show");

    });
    
}

