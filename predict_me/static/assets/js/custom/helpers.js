/*
    this file contain custom js functions for ajax,...etc
*/
"use strict"
var selectedPickedColumns = Array(); // global array will include the picked and validated column names
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

// this variable will save all new update for the every row that change its data
var allRowsUpdated = {};  // object of new updated rows
var clickedRecordsCount = 50;   // the current records number that appear to the member
var clickedFilteredColName = "";   // the clicked column to filter, "" -> means no column has been clicked
var isClickedFilterCol = false;   // true means the member clicked on the column header to sort the columns


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
    
    // console.log(selectedPickedColumns);
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
            <th style="cursor: default !important; width:50%" data-col-name='${col}' onclick='sortHeader(this);' class='dataTableHeader text-center'>${col} <i class="icon-lg d-none text-danger la la-info-circle"></i></th>
        `;
        tableHeaderElement.append(row);
    }
}

// this function return markup oject of every table cell will append to every row in the datatable
function drawDataTableRows(rowsData, isValidate) {
    let currentRowData = rowsData.data;
    console.log(currentRowData.length, "records");
    
    // check if this data not validate
    if (isValidate === false) {
        let tableBodyElement = $("#data_handler_table > tbody tr:last");
        // console.log(rowsData.data);

        for (let colIdx = 0; colIdx < currentRowData.length; colIdx++) {
            let currentDataObj = currentRowData[colIdx];
            let allCells = "";
            let tableRow = "<tr class='datatable-row'> ";
            // console.log(Object.entries(currentDataObj));
            // loop through key and value in the json object of the row
            for (let [key, value] of Object.entries(currentDataObj)) {
                //console.log(key, value);

                if (key !== "ID") {
                    if (value.is_error == false) {
                        var cellMarkup = `

                <td class='text-center'>
                    <input class='form-control form-control-solid w-auto data-table-col data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                </td>

            `;
                    } else if (value.is_error == true) {
                        const tableColHeader = $(`#data_handler_table > thead tr > th[data-col-name='${key}']`);
                        // the below to mark the column header it has error
                        tableColHeader.attr("data-is-error", '1');
                        tableColHeader.css('cursor', "pointer");
                        const colText = tableColHeader.text().trim();
                        // check if the current table td value has error, highlighted the column name header
                        if (key.trim() === colText) {
                            //console.log("error", colText);
                            tableColHeader.find("i").removeClass("d-none");
                            // tableColHeader.addClass("bg-light-danger")
                            tableColHeader.addClass("text-danger");
                        }
                        var cellMarkup = `

                <td class='text-center'>
                    <input class='form-control bg-light-danger is-invalid data-table-col w-auto form-control-solid form-control-sm data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                </td>

            `;
                    }
                    allCells += cellMarkup;
                }
            }
            tableRow += allCells + "</tr>";
            tableBodyElement.after(tableRow);
        }
        // to run the function of save the new updates of data table cells
        saveNewUpdatedData();
    } else {
        // console.log(currentRowData);
        // this else if the data are not valid
        $("#loadingDataSpinner").fadeOut();
        let tableBody = document.getElementById("data_handler_body");
        tableBody.innerHTML = "";
        //$("#data_handler_table tbody tr").fadeIn();
        for (let colIdx = 0; colIdx < currentRowData.length; colIdx++) {
            let currentDataObj = currentRowData[colIdx];
            let allCells = "";
            let tableRow = "<tr> ";
            // console.log(currentDataObj);
            for (let [key, value] of Object.entries(currentDataObj)) {

                if (key !== "ID") {
                    // console.log(currentDataObj["ID"], "|", key, "|", value.value);
                    //console.log(key, '---', value);


                    if (value.is_error == false) {
                        var cellMarkup = `

                        <td>
                            <input class='form-control form-control-solid w-auto data-table-col data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                        </td>
        
                    `;


                    } else if (value.is_error == true) {
                        var cellMarkup = `

                <td>
                    <input class='form-control bg-light-danger is-invalid data-table-col w-auto form-control-solid form-control-sm data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                </td>

            `;

                    }
                    allCells += cellMarkup;
                }

                // console.log(allCells);
                // throw new Error("Something went badly wrong!");

            }
            tableRow += allCells + "</tr>";
            tableBody.innerHTML += tableRow;


        }

        // to run the function of save the new updates of data table cells
        saveNewUpdatedData();


    }



}



// this when the user enter the amount of rows which will purchased
function culcalteExtraRows() {
    let totlaAmountDue = $("#totlaAmountDue");
    let extraRowsPurchased = $("#extraRowsPurchased");
    totlaAmountDue.val(parseFloat(extraRowsPurchased.val() * 0.5));
}


// this function when user want to save changes to data file
function updateMemberDataFile(updatedRowsObj) {
    // console.log(updatedRowsObj);
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/update-rows",
        // dataType: "json",
        data: {
            "rows": JSON.stringify(updatedRowsObj)
        },
        // dataType: "json",
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
        var progressPercentage = ((recordNowValue / rowCount) * 100);
        // var progressPercentage = Math.round((recordNowValue/rowCount) * 100);
        // var progressPercentage = Math.trunc((recordNowValue/rowCount) * 100);
        // var progressPercentage = Math.ceil((recordNowValue/rowCount) * 100);

        //set the labels and width to progressbar
        recordsCounterProgressBar.css('width', progressPercentage + '%');
        recordsCounterProgressBar.children().text(progressPercentage.toFixed() + " %");
        currentRowCounter.text(recordNowValue);

        if (isOk === true) {
            if (progVal <= rowCount) {
                progVal++;
                // console.log(progVal);
            } else {
                clearInterval(progressInterval);
                let i = 0;
                
                for (let [name, dType] of Object.entries(data['columns'])) {
                    i++;

                    let tmpMarkupLi = `
                    <li data-idx='${i}' class="columnItem font-weight-bolder list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action">
                                ${i}. ${name.trim()}
                                <span>
                                <span class="label label-inline label-light-primary font-weight-bold">${getDataType(dType)}</span>
                                <span class="position-relative tooltip-test" style='top: 4px;' title="${tooltipInfo[dType]}">
                                    <i class="icon-lg la la-info-circle text-dark"></i>
                                </span>
                                
                           </span>
                            </li>
                        \n
                    `;
                    tmpMarkupLi.replace(/ /g, "");
                    optionsList += tmpMarkupLi;
                }

                dataFileColumnsSelect.html(optionsList);
                // console.log(dataFileColumnsSelect);
                //KTDualListbox.init();
                rowCountProgressDialog.modal('hide');
                $('#columnsDualBoxModal').modal('handleUpdate');
                $('#columnsDualBoxModal').modal('show');

            }



        } else {
            // here in this elese block, when records count more than the allowed 
            if (progVal <= parseInt(allowdedRowsCount.text())) {
                progVal++;
                // console.log(progVal);
            } else {
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


// this function will return Numerice or String for the data type
function getDataType(dt){
    // const dataTypeArray = ["", "object", "int64", "float64", 'bool', 'datetime64', 'category', 'timedelta'];
    if(dt == "int64" || dt == "float64"){
        return "Numeric";
    }else if(dt == "object" || dt == "category"){
        return "Textual";
    }else{
        return "Alphanumeric";
    }
}

// when user click on reselect columns btn
function reselectColumnsFunc() {
    var optionsList = '';
    var dataFileColumnsSelect = $("#availableColumnsList");
    const columnsDualBoxModal = $("#columnsDualBoxModal");
    $("#closeColumnsDualBoxBtn").show();

    const allColumnsResponse = fetchDataFileAllColumns();
    $.when(allColumnsResponse).done(function (data, textStatus, jqXHR) {
        let i = 0;
        for (let [name, dType] of Object.entries(data)) {
            i++;
            let tmpMarkupLi = `
                    <li data-idx = '${i}' class="columnItem font-weight-bolder list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action" >
                               ${i}. ${name.trim()}
                               <span>
                                    <span class="label label-inline label-light-primary font-weight-bold">${getDataType(dType)}</span>
                                    <span class="position-relative tooltip-test" style='top: 4px;' title="${tooltipInfo[dType]}">
                                        <i class="icon-lg la la-info-circle text-dark"></i>
                                    </span>
                                    
                               </span>
                            </li>
                        \n
                    `;
            tmpMarkupLi.replace(/ /g, "");
            optionsList += tmpMarkupLi;
        }

        dataFileColumnsSelect.html(optionsList);
        columnsDualBoxModal.modal("handleUpdate");
        columnsDualBoxModal.modal("show");

    });

}

// quick function to check if undefind
function checkUndefind(value) {
    console.log(typeof value === 'undefined');
}


// function will reset the data table to default sorting
function resetSorting() {
    $("#loadingDataSpinner").fadeIn();
    // let tableBody = document.getElementById("data_handler_body");
    // tableBody.innerHTML = "";
    let resetFetchRecoredsResponse = fetchDataFileRows();
    $.when(resetFetchRecoredsResponse).done(function (data, textStatus, jqXHR) {
        if (textStatus == "success") {
            $("#loadingDataSpinner").fadeOut(200);
            drawDataTableRows(data, false);
        } else {
            swAlert("Error", data, 'error');
        }
    });

}
// this function well return the array without duplicate
function removeDuplicates(originalArray, prop) {
    
    var newArray = [];
    var lookupObject  = {};

    for(var i in originalArray) {
       lookupObject[originalArray[i][prop]] = originalArray[i];
    }

    for(i in lookupObject) {
        newArray.push(lookupObject[i]);
    }
     return newArray;
}


var allNewRowsUpdates = {};
// var allNewRowsUpdates = [];
//setup before functions
var typingTimer;                //timer identifier
var doneTypingInterval = 2000;  //time in ms, 2 second for example
// this function will run on change the input of the data file
function saveNewUpdatedData() {

    $('.data-table-col').each(function(key, value) {
        
        var elem = $(this);
        // allNewRowsUpdates["ROW_"+elem.data('row-id')] = Array();
        
        // console.log(allNewRowsUpdates);
        // throw new Error("Something went badly wrong!");
        // Save current value of element
        elem.data('oldVal', elem.val());
        //focusin
       

        // Look for changes in the value
        // elem.bind("propertychange change click keyup input paste", function(event){  // with click event
        elem.bind("propertychange change keyup input paste", function(event){
            
             // If value has changed...
            if (elem.data('oldVal') != elem.val()) {
                
                // Updated stored value
                elem.data('oldVal', elem.val());
                clearTimeout(typingTimer);
                typingTimer = setTimeout(function (){runSaveFunc(elem);}, doneTypingInterval);

                
            }
           
        });

        elem.bind("keypress", function (){
            // console.log('keydown run')
            
            clearTimeout(typingTimer);
        })
      });

      
      
}

// this function to save the old data to undo action
function saveUndo(){
    /* $('.data-table-col').on("focus", function (evt){
        undoValue = $(this).data('oldVal');
        undoElement = $(this);
    }); */

    $(document).on('focusin', '.data-table-col', function(){
        // console.log("Saving value " + $(this).val());
        // undoValue = $(this).val();
        undoValue = $(this).data('val');
        undoElement = $(this);
        $(this).data('val', $(this).val());
    }).on('change','.data-table-col', function(){
        var prev = $(this).data('val');
        var current = $(this).val();
        // console.log("Prev value " + prev);
        // console.log("New value " + current);
    });
    // 
   
}

// this function will fire when timer run
function runSaveFunc(elem){
    $("#undoBtn").removeClass("disabled");
    $("#undoBtn").removeAttr("disabled style");
    let rowNumTmp = "ROW_"+elem.data('row-id');
    allNewRowsUpdates[rowNumTmp] = Array();
    let currentRowIdx = elem.data('row-id');
    let currentColumnName = elem.attr("name");
    let currentTableCellVal = elem.val().trim();
   
    // console.log(allNewRowsUpdates[tmpRowIdx].length);
    // check if the column exists or not
    // console.log(allNewRowsUpdates[tmpRowIdx]);
    let tmpData = {
        "colName": currentColumnName,
        "colValue": currentTableCellVal
    };
    allNewRowsUpdates[rowNumTmp].push(tmpData);
    // to remove duplicate column name
    let nonDuplicateValues = removeDuplicates(allNewRowsUpdates[rowNumTmp], 'colName');
    // console.log(nonDuplicateValues);
    allNewRowsUpdates[rowNumTmp] = nonDuplicateValues;
    // allNewRowsUpdates[rowNumTmp].push(nonDuplicateValues);
    // console.log(allNewRowsUpdates[rowNumTmp]);
    saveTheUpdates(allNewRowsUpdates, elem);
    //   console.log(allNewRowsUpdates);

  

//   console.log(allNewRowsUpdates);
}
// this function will run every 1s in set time out when member update his data
function saveTheUpdates(allUpdatedRows, elem){
    let currInput = $(elem);
    
    // console.log(currInput);
    $("#dataListTable").css("opacity", "0.3");
    $(".data-table-col").attr("disabled", "disabled");
    $("#save-row-loader").fadeIn();
    let saveDataRespone = updateMemberDataFile(allUpdatedRows);
    $.when(saveDataRespone).done(function (data, textStatus, jqXHR) {
      // console.log(textStatus);
      // console.log(jqXHR);
      // console.log(data);

      if (textStatus === "success") {
        
        // window.location.reload();
        console.log(data);
        if(data['is_error'] == true){
            currInput.addClass("is-invalid bg-light-danger");
        }else{
            currInput.removeClass("is-invalid bg-light-danger").delay(1000).addClass("bg-light-success").delay(1000).removeClass("bg-light-success");
        }
        $("#dataListTable").css("opacity", "1");
        $(".data-table-col").removeAttr("disabled");
        $("#save-row-loader").fadeOut();
        showToastrNotification(data['msg']);
        currInput.focus();

      } else {
        swAlert("Error", "Error when save the data!", "error");
        showToastrNotification("Error when save the data!", "danger");
    }

    });
}


// function to display Toastr Notifications
function showToastrNotification(msg, msgType="success"){
    $.notify({
        // options
        message: msg,
        icon: 'icon la la-check',
    },{
        // settings
        type: msgType,
        animate: {
            enter: 'animate__animated animate__ animate__faster animate__slideInRight',
            exit: 'animate__animated animate__ animate__faster animate__slideOutRight'
        },
        z_index: 1031,
        timer: 1000,
    });
   
}