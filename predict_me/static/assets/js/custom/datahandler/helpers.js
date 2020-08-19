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

function swConfrim(title, msg) {

    bootbox.confirm("This is the default confirm!", function (result) {
        console.log('This was logged in the callback: ' + result);
    });

    // return ;

}

// sweetalert2 confirm custom dialogbox only show when the memeber change the data type of the column
function swConfirmDtype(elem, msg, tmpSpan, dataIX) {

    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: msg,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        backdrop: true,
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        showLoaderOnConfirm: true,
        reverseButtons: true,
        stopKeydownPropagation: false,
        focusCancel: true,

    }).then((result) => {
        if (result.value) {

            tmpSpan.show();
            elem.attr("title", `Default data format: TEXT\nCurrent data format: ${elem.val().split(" ")[0].toUpperCase()}`);

        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            elem.val("");
            tmpSpan.hide();
            delete optionsSelected[dataIX];
            setCriterias();  // to fix criterias

        }
    });


}

// this will get the function name
function getFunctionName(fun) {
    let funName = fun.toString();
    funName = funName.substr('function '.length);
    funName = funName.substr(0, funName.indexOf('('));
    return funName;
}


// count duplicated items in array
function coutItems(arrayVar, value) {
    let count = 0;
    arrayVar.forEach((v) => (v === value && count++));
    return count;
}

// count duplicated values in json object
function countJsonItems(jsonObj, value) {
    let count = 0;
    for (let i in jsonObj) {
        if (jsonObj[i] === value) {
            count++;
        }
    }
    return count;
}

// check if value exists in json object
function checkValueExists(json, value) {
    for (let key in json) {
        if (typeof (json[key]) === "object") {
            return checkForValue(json[key], value);
        } else if (json[key] === value) {
            return true;
        }
    }
    return false;
}


// this ajax function which will upload the donor data file
function uploadDonorDataFile(uploadForm) {
    const webSiteUrl = window.location.origin;
    const parameters = window.location.pathname;
    // const webSiteMemberUrl = window.location;
    const donerFileInput = $("#donerFile");
    if (donerFileInput.val()) {
        // $form = uploadForm;
        var formData = new FormData($("#uploadDataFileForm")[0]);
        const fileName = donerFileInput.val().split(/(\\|\/)/g).pop(); // get the file name to parse it in url
        formData.append('parameters', parameters);
        formData.append('session-label', $("#session-name").val());
        formData.append('file_name', fileName);
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
                let swalUploadProgressDialog = swal.fire({
                    title: "Uploading...",
                    text: "Uploading you data file, Please wait...",
                    showConfirmButton: false,
                    allowOutsideClick: false,
                    allowEscapeKey: false,
                    allowEnterKey: false,
                    // stopKeydownPropagation: false,
                    // keydownListenerCapture: true,
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
            Swal.close();
            setSessionLastName("upload");

        }).fail(function (e) {
            console.error("upload failed");
            console.log(e);
        });

    } else {
        swal.fire("Error", "You have to select a file!", "error");
    }
}


// this function which will take the picked columns and send them to make the datatable view
function sendPickedColumns(params) {
    const parameters = window.location.pathname;
    // let selectedColumns = JSON.stringify(pickedColumns);
    // let selectedColumns = JSON.parse(pickedColumns);
    // console.log(typeof JSON.stringify(selectedValidateColumns));
    let selectedColumns = {
        "columns": selectedPickedColumns,
        "columns_with_datatype": JSON.stringify(selectedValidateColumns),
        'parameters': parameters
    };
    // console.log(selectedColumns);
    // throw new Error("Wait");
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
    const parameters = window.location.pathname;

    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/get-columns",
        // dataType: "json",
        data: {'parameters': parameters},
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

// this function will sort the columns for data handler table
function setColumnNamesHeader(columnsList) {
    let tableHeaderElement = $("#data_handler_table > thead > tr:last");
    for (let col of columnsList) {

        let row = "";
        if (col['isUnique'] === true) {
            row = `
            <th style="cursor: default !important;" data-col-name='${col["headerName"]}' data-is-unique-col="1" onclick='sortHeader(this);' class='dataTableHeader'>${col["headerName"]}<i style="top: 2px" class="icon-md d-none position-relative text-danger la la-sort"></i></th>
        `;
        } else {
            row = `
            <th style="cursor: default !important;" data-col-name='${col["headerName"]}' data-is-unique-col="0" onclick='sortHeader(this);' class='dataTableHeader'>${col["headerName"]} <i style="top: 2px" class="icon-md d-none position-relative text-danger la la-sort"></i></th>
        `;
        }
        tableHeaderElement.append(row);
    }
}

// this function return markup oject of every table cell will append to every row in the datatable
function drawDataTableRows(rowsData, isValidate) {
    let currentRowData = rowsData.data;
    // console.log(rowsData);
    // console.log(rowsData.total_rows);
    // console.log(currentRowData.length, "records");
    // check the length of total rows came from excel file, in case one row, or less than 50 rows
    if(rowsData.total_rows < 50){
        $(".data-table-nav-btns").addClass('disabled').attr('disabled', 'disabled');
    }

     if ((typeof currentRowData.length === undefined) || (typeof currentRowData.length === 'undefined')) {
        // here when no rows, 0
        console.error("No records to display!!");
        $("[data-action='next']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
        $("#no-data-watermark").show();
    } else {
        // check if the (clickedRecordsCount) = 50 this mean the user in the first page, then disable the previous (<) indicator of pagination
        if (clickedRecordsCount === 50) {
            $("[data-action='previous']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
            $("[data-action='first']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
        } else {
            $("[data-action='previous']").removeAttr("disabled").removeClass("disabled").tooltip('update');
            $("[data-action='first']").removeAttr("disabled").removeClass("disabled").tooltip('update');
        }

        // check if the no data watermark exists remove it before display if there is new data
        if ($("#no-data-watermark").is(":visible") === true) {
            $("#no-data-watermark").hide();
        }

        // check if this data not validate
        if (isValidate === false) {
            let tableBodyElement = $("#data_handler_table > tbody tr:last");
            // console.log(rowsData.data);

            for (let colIdx = 0; colIdx < currentRowData.length; colIdx++) {
                let currentDataObj = currentRowData[colIdx];
                if (currentDataObj["ID"] === 4) {
                    // console.log(currentDataObj);
                }
                // console.log(currentDataObj);
                let allCells = "";
                let tableRow = "<tr class='datatable-row'> ";
                // console.log(Object.entries(currentDataObj));
                // loop through key and value in the json object of the row
                for (let [key, value] of Object.entries(currentDataObj)) {
                    // console.log(key, value);

                    if (key !== "ID") {
                        if (value.is_error === false) {
                            // check if the data type is numeric or donation will restric the member from enter numeric data
                            if (value.data_type === "donation field" || value.data_type === "numeric field" || value.data_type === "unique identifier (id)") {
                                var cellMarkup = `
    
                    <td class=''>
                        <input class='form-control-sm form-control w-auto data-table-col data-table-input' data-row-id='${currentDataObj["ID"]}' onkeypress="return isNumber(event)" type='text' name='${key}' value='${value.value}' />
                    </td>
    
                `;
                            } else {
                                var cellMarkup = `
    
                    <td class=''>
                        <input class='form-control-sm form-control w-auto data-table-col data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                    </td>
    
                `;
                            }
                        } else if (value.is_error === true) {

                            const tableColHeader = $(`#data_handler_table > thead tr > th[data-col-name='${key}']`);
                            // the below to mark the column header it has error
                            tableColHeader.attr("data-is-error", '1');
                            tableColHeader.css('cursor', "pointer");
                            tableColHeader.addClass('protip');
                            // tableColHeader.attr('data-toggle', 'tooltip');
                            // tableColHeader.attr('title', 'Error data not match the required data type!');
                            tableColHeader.attr('data-pt-title', `Default data format: ${value['original_dtype'].toUpperCase()} <br /> Current data format: ${value['data_type'].split(" ")[0].toUpperCase()}`);
                            tableColHeader.attr('data-pt-gravity', 'top');
                            tableColHeader.attr('data-pt-classes', 'bg-danger text-white');
                            tableColHeader.attr('data-pt-animate', 'animate__animated animate__tada');
                            tableColHeader.attr('data-pt-delay-in', '500');
                            const colText = tableColHeader.text().trim();
                            // check if the current table td value has error, highlighted the column name header
                            if (key.trim() === colText) {
                                //console.log("error", colText);
                                tableColHeader.find("i").removeClass("d-none");
                                // tableColHeader.addClass("bg-light-danger")
                                tableColHeader.addClass("text-danger");
                            }

                            if (value.data_type === "donation field" || value.data_type === "numeric field" || value.data_type === "unique identifier (id)") {
                                var cellMarkup = `
    
                    <td class='text-center'>
                        <input class='form-control bg-light-danger data-table-col w-auto form-control-sm data-table-input' onkeypress="return isNumber(event)" data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                    </td>
    
                `;
                            } else {
                                var cellMarkup = `
    
                    <td class='text-center'>
                        <input class='form-control bg-light-danger data-table-col w-auto form-control-sm data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                    </td>
    
                `;
                            }

                        }
                        allCells += cellMarkup;
                    }
                }
                tableRow += allCells + "</tr>";
                tableBodyElement.after(tableRow);
            }
            $("#dataListTable").css("opacity", "1");

            // to run the function of save the new updates of data table cells
            saveNewUpdatedData();
        } else {
            // console.log(currentRowData);
            // this else if the data are not valid

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


                        if (value.is_error === false) {
                            if (value.data_type === "donation field" || value.data_type === "numeric field" || value.data_type === "unique identifier (id)") {
                                var cellMarkup = `
    
                            <td>
                                <input class='form-control form-control-solid w-auto data-table-col data-table-input' onkeypress="return isNumber(event)" data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                            </td>
            
                        `;
                            } else {
                                var cellMarkup = `
    
                            <td>
                                <input class='form-control form-control-solid w-auto data-table-col data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                            </td>
            
                        `;
                            }


                        } else if (value.is_error === true) {

                            if (value.data_type === "donation field" || value.data_type === "numeric field" || value.data_type === "unique identifier (id)") {
                                var cellMarkup = `
    
                    <td>
                        <input class='form-control bg-light-danger is-invalid data-table-col w-auto form-control-solid form-control-sm data-table-input' onkeypress="return isNumber(event)" data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                    </td>
    
                `;
                            } else {
                                var cellMarkup = `
    
                    <td>
                        <input class='form-control bg-light-danger is-invalid data-table-col w-auto form-control-solid form-control-sm data-table-input' data-row-id='${currentDataObj["ID"]}' type='text' name='${key}' value='${value.value}' />
                    </td>
    
                `;
                            }

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


    $("#dataListTable").css("opacity", "1");
    $("#loadingDataSpinner").fadeOut('fast');

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
            "rows": JSON.stringify(updatedRowsObj),
            "parameters": window.location.pathname,
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
    const parameters = window.location.pathname;
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/delete-file",
        // dataType: "json",
        data: {
            "rows[]": allRowsUpdated,
            'parameters': parameters
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
    var rowCountProgressDialog = $("#recordsCountModal");
    var recordsCounterProgressBar = $("#recordsCounterProgressBar");
    let currentRowCounter = $("#currentRowCounter > b");
    let progressWarnText = $("#progressWarnText");
    let nextProgressBtnModal = $("#nextProgressBtnModal");
    let allowdedRowsCount = $("#progressRecords > b:first");
    rowCountProgressDialog.modal('show');
    rowCountProgressDialog.modal('handleUpdate');
    recordsCounterProgressBar.attr("aria-valuemax", '100');
    let progVal = 0;
    // the interval
    var progressInterval = setInterval(progressIntervalFunc, 35);

    function progressIntervalFunc() {

        let recordNowValue = parseInt(recordsCounterProgressBar.attr("aria-valuenow"));

        let progressPercentage = ((recordNowValue / rowCount) * 100);
        // console.log(progressPercentage);
        //set the labels and width to progressbar

        if (progressPercentage <= 100) {
            recordsCounterProgressBar.children().text(progressPercentage.toFixed() + " %");
            recordsCounterProgressBar.css('width', progressPercentage + '%');
            recordsCounterProgressBar.attr("aria-valuenow", recordNowValue + 1);
        }
        currentRowCounter.text(recordNowValue);

        if (isOk === true) {
            if (progVal <= rowCount) {
                progVal++;
                // console.log(progVal, ' of ', rowCount);

            } else {
                clearInterval(progressInterval);
                let i = 0;

                for (let [name, dType] of Object.entries(data['columns'])) {
                    i++;

                    let tmpMarkupLi = `
                    <li data-idx='${i}' class="columnItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action noselect">
                                ${i}. ${name.trim()}
                                <span class="noselect">
                                <span class="noselect label label-inline label-light-primary font-weight-bold w-60px">${getDataType(dType)}</span>
                               
                                
                           </span>
                            </li>
                        \n
                    `;
                    tmpMarkupLi.replace(/ /g, "");
                    optionsList += tmpMarkupLi;
                }

                dataFileColumnsSelect.html(optionsList);
                rowCountProgressDialog.modal('hide');
                $("#uploadFileModal").modal('hide');
                $('#columnsDualBoxModal').modal('show');
                $('#columnsDualBoxModal').modal('handleUpdate');
                /*if(rowCountProgressDialog.hasClass('show') === true){
                    console.error('modal is shown');
                }else{
                    console.log('modal is hidden')
                }*/

            }


        } else {
            // here in this elese block, when records count more than the allowed
            if (progVal <= parseInt(allowdedRowsCount.text())) {
                progVal++;
                // console.log(progVal);
            } else {
                // clearInterval(progressInterval);
                $("#uploadFileModal").modal('hide');
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

    nextProgressBtnModal.on('click', function (ev) {
        clearInterval(progressInterval);
        rowCountProgressDialog.modal('hide');

        $("#extraRecordsModel").modal("handleUpdate");
        $("#extraRecordsModel").modal("show");
    });
}


// this function will fetch all columns in the data file to make the member reselect the columns
function fetchDataFileAllColumns(withDtypes) {
    const parameters = window.location.pathname;
    let data = '';
    if (typeof withDtypes !== undefined) {
        data = {"with_dtype": true, 'parameters': parameters};
    } else {
        data = {'parameters': parameters};
    }
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        data: data,
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
function getDataType(dt) {
    // const dataTypeArray = ["", "object", "int64", "float64", 'bool', 'datetime64', 'category', 'timedelta'];
    if (dt === "int64" || dt === "float64") {
        return "Numeric";
    } else if ((dt === "object") || (dt === "category") || (dt === "bool")) {
        return "Text";
    } else {
        return "Alphanumeric";
    }
}

// this function will set the options list of the select to every column (item) in the right side
function dataTypeOptions(dataType, setSelected, uniqueColumn, colName) {
    let optionsMarkup = "";
    // this to set the selected option selected
    if ((typeof setSelected !== 'undefined' || setSelected === true) && (typeof uniqueColumn !== 'undefined') && (typeof colName !== 'undefined')) {
        // console.log(dataType, setSelected, uniqueColumn, colName);
        for (let dType of dataTypesOptions) {

            // check if isUniqueIDSelected is true make it selected by default, to avoid unique id enabled in the new items come from left side after selecte it
            if ((colName === uniqueColumn) && (dType.includes('Unique Identifier') === true)) {
                isUniqueIDSelected = true;
                optionsMarkup += `<option selected="selected" data-unique-id-col="1" value='${dType}'>${dType}</option>\n`;


            } else {
                // check to set selected if the column match the data type, so in this case make the option selected with the dtype
                if (dataType.toLowerCase() === dType.toLowerCase()) {
                    // console.log(colName, '--> ', dataType.toLowerCase(), '==>  ', dType);
                    optionsMarkup += `<option value='${dType}' selected="selected">${dType}</option>\n`;
                } else {
                    optionsMarkup += `<option value='${dType}'>${dType}</option>\n`;
                }

            }

        }
        // return optionsMarkup;
    } else {
        for (let dType of dataTypesOptions) {

            // check if isUniqueIDSelected is true make it selected by default, to avoid unique id enabled in the new items come from left side after selecte it
            optionsMarkup += `<option value='${dType}'>${dType}</option>\n`;

        }
        // return optionsMarkup;
    }

    return optionsMarkup;

}

// when user click on reselect columns btn
function reselectColumnsFunc(openDialog) {

    $("#closeReselectColsModal").removeClass("d-none");
    let optionsList = '';
    let rightOptionsList = '';
    let dataFileColumnsSelect = $("#availableColumnsList");
    let rightPickedColumnsList = $("#pickedColumnsList");
    const columnsDualBoxModal = $("#columnsDualBoxModal");
    $("#closeColumnsDualBoxBtn").show();

    const allColumnsResponse = fetchDataFileAllColumns(true);


    $.when(allColumnsResponse).done(function (data, textStatus, jqXHR) {
        /*console.log(textStatus);
        console.log(jqXHR);
        console.log(data);*/


        const tmpSelectedColsArr = Object.keys(data['selected_columns']);  // member selected columns
        let i = 0;
        for (let [name, dType] of Object.entries(data['all_columns'])) {
            i++;
            // console.log([name, dType]);
            let tmpMarkupLi = "";

            // console.log(getDataType(dType), dType);
            // check if the column name in the picked columns, so will disable it
            if (tmpSelectedColsArr.includes(name) === true) {
                tmpMarkupLi = `
                    <li data-idx = '${i}' class="disabled noselect bg-gray-200 columnItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action" >
                               ${i}. ${name.trim()}
                               <span>
                                    <span class="noselect label label-inline label-light-primary font-weight-bold w-60px">${getDataType(dType)}</span>
                                   
                               </span>
                            </li>
                        \n
                    `;
            } else {
                tmpMarkupLi = `
                    <li data-idx = '${i}' class="noselect columnItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action" >
                               ${i}. ${name.trim()}
                               <span>
                                    <span class="noselect label label-inline label-light-primary font-weight-bold w-60px">${getDataType(dType)}</span>
                                    
                               </span>
                            </li>
                        \n
                    `;
            }

            tmpMarkupLi.replace(/ /g, "");
            optionsList += tmpMarkupLi;

            // here set the columns options for the right side, which mean the previously selected columns
            let tmpRightColOpMarkup = "";
            if (tmpSelectedColsArr.includes(name) === true) {
                // this to set isUniqueIDSelected = true
                // console.log(getDataType(dType), true, data['unique_column'], name);  // Numeric true Donor_Id Donor_Id
                // console.log(data['selected_columns'][name]);
                tmpRightColOpMarkup = `
                    <li data-idx="${i}"
                        class='pickedItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action'>
                        ${name}
                        <span class="nav-label mx-10" >
                            <select data-value='${getDataType(dType)}' class="form-control form-control-sm column-option-dtype w-110px">
                                    ${dataTypeOptions(data['selected_columns'][name], true, data['unique_column'], name)}
                            </select>
                        </span>
                        <span class="label position-absolute" style='background-color: unset; right: 12px; display: none;'>
                              <i class="icon-lg la la-info-circle text-warning font-weight-bolder"></i>
                        </span>
                        <span class="label position-absolute" style='background-color: unset; right: 12px; display: none;' id="resetIDColumnBtn" title="Reset ID column">
                              <i class="icon-lg la la-minus-circle text-danger font-weight-bolder"></i>
                        </span>
                        
                    </li>
                    \n
                `;

                rightOptionsList += tmpRightColOpMarkup;
            }

        }

        dataFileColumnsSelect.html(optionsList);
        rightPickedColumnsList.html(rightOptionsList);
        fixSelectedColumnsItems(rightPickedColumnsList);
        if (openDialog === true) {
            columnsDualBoxModal.modal("handleUpdate");
            columnsDualBoxModal.modal("show");
        }


    });

}

// this function will take the current item from right side to set the options of unique id column
function fixSelectedColumnsItems(allRightColsParent) {
    const allRightJQElement = $(allRightColsParent);
    allRightJQElement.children('li').each(function (index, element) {
        const liElem = $(element);
        const liSelectMenu = liElem.find('select.column-option-dtype');
        let opSelectUniqueIDCol = $(liSelectMenu.children('option[data-unique-id-col="1"]'));
        // liSelectMenu.attr('disabled', 'disabled');
        // console.log(liSelectMenu.val());
        liSelectMenu.trigger('change', 'reselect');
    })


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
        if (textStatus === "success") {
            $("#loadingDataSpinner").fadeOut(200);
            drawDataTableRows(data, false);
        } else {
            swAlert("Error", data, 'error');
        }
    });

}

// this function well return the array without duplicate
function removeDuplicates(originalArray, prop) {

    let newArray = [];
    let lookupObject = {};

    for (let i in originalArray) {
        lookupObject[originalArray[i][prop]] = originalArray[i];
    }

    for (let i in lookupObject) {
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

    $('.data-table-col').each(function (key, value) {

        let elem = $(this);
        // allNewRowsUpdates["ROW_"+elem.data('row-id')] = Array();
        // console.log(allNewRowsUpdates);
        // throw new Error("Something went badly wrong!");
        // Save current value of element
        elem.data('oldVal', elem.val());
        // console.log(elem.data(), elem.val());
        // console.log(elem.val());

        // Look for changes in the value
        // elem.bind("propertychange change click keyup input paste", function(event){  // with click event
        elem.bind("propertychange keyup input paste", function (event) {
            // console.log("propertychange event fire");
            // If value has changed...
            if (elem.data('oldVal') !== elem.val()) {

                // Updated stored value
                elem.data('oldVal', elem.val());
                // console.log(elem.data())
                clearTimeout(typingTimer);
                typingTimer = setTimeout(function () {
                    runSaveFunc(elem);
                }, doneTypingInterval);


            }

        });

        elem.bind("keypress", function () {
            // console.log('keydown run')

            clearTimeout(typingTimer);
        })
    });


}

// this function to save the old data to undo action
function saveUndo() {

    $(document).on('focusin', '.data-table-col', function () {
        // console.log("Saving value " + $(this).val());
        // undoValue = $(this).val();
        // console.log($(this).data());
        undoValue = undoValue2 = $(this).data('undo-val');
        undoElement = $(this);
        $(this).data('undo-val', $(this).val());
    }).on('change', '.data-table-col', function () {
        let prev = $(this).data('undo-val');
        let current = $(this).val();
        /*console.log("this is change event");
        console.log("Prev value " + prev);
        console.log("New value " + current);*/
    });
    // 

}

// this function will fire when timer run
function runSaveFunc(elem) {
    $("#undoBtn").removeClass("disabled");
    $("#undoBtn").removeAttr("disabled style");
    let rowNumTmp = "ROW_" + elem.data('row-id');
    allNewRowsUpdates[rowNumTmp] = Array();
    let currentRowIdx = elem.data('row-id');
    let currentColumnName = elem.attr("name");
    let currentTableCellVal = elem.val().trim();
    // check if the column exists or not

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
    console.log(allNewRowsUpdates);
    saveTheUpdates(allNewRowsUpdates, elem);


}

// this function will run every 1s in set time out when member update his data
function saveTheUpdates(allUpdatedRows, elem) {
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

        if ((textStatus === "success") && (jqXHR.status === 200)) {
            // console.log(undoElement);
            // console.log(undoValue2);
            // window.location.reload();
            undoValue = "";
            undoValue2 = "";
            // console.log(currInput.data());
            // console.log(data);
            if (data['is_error'] === true || data['msg'].includes("could not")) {
                currInput.addClass("is-invalid bg-light-danger", {duration: 1000});
                showToastrNotification("Error while saving the data, check the data type or try later!", "danger");

            } else {
                // currInput.removeClass("is-invalid bg-light-danger").delay(1000).addClass("bg-light-success").delay(1000).removeClass("bg-light-success");
                currInput.removeClass("is-invalid bg-light-danger", {duration: 1000}).addClass("bg-success-o-40", {duration: 1000});
                setTimeout(function () {
                    currInput.removeClass("bg-success-o-40", {duration: 1500});
                }, 1500);
                showToastrNotification(data['msg'][1]);

            }
            allNewRowsUpdates = {};
            // console.log(currInput.data());
            $("#dataListTable").css("opacity", "1");
            $(".data-table-col").removeAttr("disabled");
            $("#save-row-loader").fadeOut();

            // currInput.focus();


            // $(".data-table-input").on("change");

        } else {
            swAlert("Error", "Error when save the data!", "error");
            showToastrNotification("Error when save the data!", "danger");

        }

    });
}


// function to display Toastr Notifications
function showToastrNotification(msg, msgType = "success") {
    let icon = "";
    if (msgType === "danger") {
        icon = "icon la la-times";
    } else {
        icon = "icon la la-check";
    }
    $.notify({
        // options
        message: msg,
        icon: icon,
    }, {
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

// function well set cookie if the member does not upload any data file yet, this cookie if it set, it will prevent the user from reload the page and disable f5 key
function setTheCookie() {
    let setTheCookieResponse = checkIfMemberUploadDataFile()
    $.when(setTheCookieResponse).done(function (data, textStatus, jqXHR) {
        // console.log(textStatus);
        // console.log(jqXHR.status);
        // console.log(data);

        if (data !== "None" && jqXHR.status === 200) {
            $(document).on("keydown", disableF5);
            window.onbeforeunload = function (e) {
                e = e || window.event;

                // For IE and Firefox prior to version 4
                if (e) {
                    e.returnValue = 'Sure?';
                }

                // For Safari
                return 'Sure?';
            };
        } else {
            window.onbeforeunload = null;
        }
    });
}


// Restricts input for the given textbox to the given inputFilter function.
function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    let charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}

// this function will run after all page load and all ajax requests have complete, to check if the user has previous seesions or not
function checkMemberSessionStatus() {
    const checkMemberProcessStatusResponse = checkIfMemberProcessStatus();
    $.when(checkMemberProcessStatusResponse).done(function (data, textStatus, jqXHR) {
        // console.log(textStatus);
        // console.log(jqXHR);
        // console.log(data);
        if ((textStatus === 'success') && (jqXHR.status === 200) && (data === false)) {
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success',
                    cancelButton: 'btn btn-danger'
                },
                buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
                title: 'Attention!',
                text: "There is previously session, do you want to restore it?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, restore it!',
                cancelButtonText: 'No, start fresh!',
                // reverseButtons: true,
                backdrop: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false,
                showLoaderOnConfirm: true,
            }).then((result) => {
                if (result.value) {
                    const newResponse = checkIfMemberProcessStatus("Restore");
                } else if (
                    /* Read more about handling dismissals below */
                    result.dismiss === Swal.DismissReason.cancel
                ) {
                    const newResponse = checkIfMemberProcessStatus("Fresh");
                }
            })
        }
    });
}

// disable F5 Key
function disableF5(e) {
    if ((e.which || e.keyCode) === 116) e.preventDefault();
}

// run modal function
function confirmRunModal() {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: 'Are you sure?',
        text: "Do you want to run the modal!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, run it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true
    }).then((result) => {
        if (result.value) {
            let timerInterval
            Swal.fire({
                title: 'Please wait!',
                html: 'Running the modal...<br /> please be patient.',
                timer: 2000,
                timerProgressBar: true,
                onBeforeOpen: () => {
                    Swal.showLoading()
                    timerInterval = setInterval(() => {
                        const content = Swal.getContent()

                    }, 100)
                },
                onClose: () => {
                    clearInterval(timerInterval);

                }
            }).then((result) => {
                /* Read more about handling dismissals below */
                if (result.dismiss === Swal.DismissReason.timer) {
                    console.log('I was closed by the timer');

                }
            })
        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {

        }
    })
}


// this function will handle the data handler wrapper tabs
function dataHandlerWrapperTabs() {
    //tabindex="-1", aria-disabled="true"

    let fetchLastSessionNameResponse = fetchLastSessionName();
    $.when(fetchLastSessionNameResponse).done(function (data, textStatus, jqXHR) {
        //  console.log(textStatus);
        // console.log(jqXHR);
        // console.log(data);
        if ((textStatus === 'success') && (jqXHR.status === 200)) {
            $("#data-handler-wrapper-spinner").fadeOut();
            $("#wrapper-ul").fadeIn();
            $("#wrapper-content").fadeIn();
            // This event fires on tab show, but before the new tab has been shown
            $('#wrapper-ul').on('show.bs.tab', function (event) {
                // do something...
                const ulElement = $(this);
                // ulElement.find('a[data-section-name="data_process"]').addClass('disabled');
                const previousActiveTab = $(event.relatedTarget);
                const previousSectionName = previousActiveTab.data('section-name');
                const activeTab = $(event.target);
                const activeSectionName = activeTab.data('section-name');

            });
        }
    })


}

// this function will set the label of the data handler session
async function setSessionLabel() {
    let checkStatus = '';  // if the check label is false means no session in the db
    // first check if the current session has label or not


    if (!checkStatus) {
        const {value: sessionLabel} = await Swal.fire({
            title: 'Enter Label for current session',
            input: 'text',
            allowOutsideClick: false,
            allowEscapeKey: false,
            // inputValue: inputValue,
            showLoaderOnConfirm: true,
            showCancelButton: false,
            confirmButtonText: "Submit",
            inputValidator: (value) => {
                if (!value) {
                    return 'You need to write something!'
                }
            }
        })

        if (sessionLabel) {
            let sessionLabelRespone = setSessionLabelRequest(sessionLabel, 'set');
            $.when(sessionLabelRespone).done(function (data, textStatus, jqXHR) {
                if ((jqXHR.status === 200) && (textStatus === 'success')) {
                    document.title = sessionLabel;
                    $("#data-handler-dashboard-label").text(sessionLabel);
                    Swal.fire(data);
                    window.location.href = webSiteUrl.concat("/profile/dashboard");
                }
            })
        }
    }

}


// delete single session from table
function deleteSingleSession() {
    $(".delete-data-session, #deleteAllSessionsBtn").on('click', function (evt) {
        const elem = $(this);
        const sessionID = elem.data('session-id');
        let deleteMsg = ""
        if (typeof sessionID === 'number') {
            deleteMsg = "Do you want to delete your session with its file, You won't be able to revert this!";
        } else {
            deleteMsg = "Do you want to delete all your sessions and files!, You won't be able to revert this!";
        }
        Swal.fire({
            title: 'Are you sure?',
            text: deleteMsg,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete!',
            allowEnterKey: false,
        }).then((result) => {
            if (result.value) {
                const deleteSessionResponse = deleteDataSessionsRequest(sessionID);
                $.when(deleteSessionResponse).done(function (data, textStatus, jqXHR) {
                    //  console.log(textStatus);
                    // console.log(jqXHR);
                    // console.log(data);
                    if ((textStatus === 'success') && (jqXHR.status === 200)) {
                        Swal.fire(
                            'Deleted!',
                            'Delete Successfully!.',
                            'success'
                        );
                        setTimeout(function () {
                            window.location.reload();
                        }, 1000);
                    }
                });

            }
        })


    })
}


// rename session function
function renameSessionFunc() {
    $("#rename-session-btn").on('click', function (evt) {
        const newSessionNameJq = $("#rename-session-input");
        if (newSessionNameJq.val() !== "") {
            const renameSessionResponse = renameSessionRequest(newSessionNameJq.val());
            $.when(renameSessionResponse).done(function (data, textStatus, jqXHR) {
                /* console.log(textStatus);
                console.log(jqXHR);
                console.log(data);*/
                if ((textStatus === 'success') && (jqXHR.status === 200)) {
                    Swal.fire(
                        'Updated!',
                        'Rename Successfully!.',
                        'success'
                    );
                    setTimeout(function () {
                        window.location.reload();
                    }, 1000);
                }
            });
        }


    });
}


