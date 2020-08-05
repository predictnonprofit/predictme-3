const dataTypeArray = ["", "object", "int64", "float64", 'bool', 'datetime64', 'category', 'timedelta'];
const dataTypesOptions = ["", "Unique Identifier (ID)", "Text Field", "Numeric Field", "Donation Field"];
const leftClickedColumnClass = 'columnItem';
const rightClickedColumnClass = 'pickedItem';
let clickedLeftColumnItem = "";
let clickedRightColumnItem = "";
let checkMark = "&#10004;";
let timesMark = "&#10060;";
let selectedOptionsArray = [];
let selectedValidateColumns = {};
let optionsSelected = {};
let isUniqueIDSelected = false;  // if true the member select the unique id column, false not selected


function setColumnsTotal() {
    // this function will set the total of items in the left and right columns title
    let avaTotal = $("#availableColumnsList li").length;
    let pickTotal = $("#pickedColumnsList li").length;
    //console.log(avaTotal, '---', pickTotal);
    $("#avaliableColumnsTotal h5 > b").text(avaTotal);
    $("#pickedColumnsTotal h5 > b").text(pickTotal);
}


function createNewItemRightColumn(colIdx, colName, colDataType, optionsList) {
    // console.log(colIdx, colName, colDataType, optionsList);
    // console.log(colIdx, colName, colDataType);
    //pickedColumnsList
    // console.log(colDataType);
    const liMarkup = `
            <li data-idx="${colIdx}"
                class='pickedItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action'>
                ${colName}
                <span class="nav-label mx-10">
                    <select data-value='${colDataType}' class="form-control form-control-sm column-option-dtype w-130px">
                            ${optionsList}
                    </select>
                </span>
                <span class="label position-absolute" style='background-color: unset; right: 12px; display: none;'>
                      <i class="icon-lg la la-info-circle text-warning font-weight-bolder"></i>
                </span>
                <span class="label position-absolute" style='background-color: unset; right: 12px; display: none;' id="resetIDColumnBtn" title="Reset ID column">
                      <i class="icon-lg la la-minus-circle text-danger font-weight-bolder"></i>
                </span>
                
            </li>
        `;
    // let tLi = $($.parseHTML(liMarkup)).filter('li');
    // console.log(tLi.find('select'));
    $("#pickedColumnsList").append(liMarkup);
    //$("#pickedColumnsList").after(liMarkup);


}

function enableLeftColumnItem(colIdx) {
    const leftItem = fetchColumnByDataIdx(true, colIdx);
    leftItem.removeClass("disabled bg-gray-200");
}

function fetchColumnByDataIdx(isLeftCol, colIdx) {
    if (isLeftCol === true) {
        const leftColItem = $(`.${leftClickedColumnClass}[data-idx="${colIdx}"]`);
        //console.log(leftColItem.text());
        return leftColItem;
    } else {
        const rightColItem = $(`.${rightClickedColumnClass}[data-idx="${colIdx}"]`);
        //console.log(rightColItem.html());
        return rightColItem;
    }
}

function extractLeftColData(colItem) {
    //let colItem = fetchColumnByDataIdx(colIdx);
    const selectedColumnName = colItem.clone().children().remove().end().text().trim();
    const selectedColumnNameWithoutIdxNumber = selectedColumnName.split(". ")[1];  // whitout number before the column name
    const selectedColumnDataType = colItem.children().text().trim().toLowerCase();
    const selectedColumnIdx = colItem.data('idx');
    // console.log(selectedColumnIdx, selectedColumnName, selectedColumnDataType);
    // console.log(selectedColumnIdx, selectedColumnNameWithoutIdxNumber, selectedColumnDataType);
    return [selectedColumnIdx, selectedColumnNameWithoutIdxNumber, selectedColumnDataType];
    // return [selectedColumnIdx, selectedColumnName, selectedColumnDataType];
}

function extractRightColData(colItem) {
    //console.log(colItem.children().find("select").val());
    const colClone = colItem.clone();
    const tt = colClone.children().find("select").data('value');
    //console.log(tt);
    //let colItem = fetchColumnByDataIdx(colIdx);
    let name = colClone.children().remove().end().text().trim();
    let dType = colClone.children().find("select").data('value');
    let colIdx = colClone.data('idx');
    //console.log(colIdx, name, tt);
    return [colIdx, name, tt];
}


function saveClickedColumn(isLeftCol, colIdx) {
    // isLeftCol means if the memeber click on right column
    if (isLeftCol === true) {
        return fetchColumnByDataIdx(true, colIdx);
    } else {
        return fetchColumnByDataIdx(false, colIdx);
    }
}

function selectAvaliableColumns() {
    // single click on the avaliable column
    //let allColumnsSelection = $('.columnItem');
    $("ul#availableColumnsList").on("click", 'li', function (ev) {
        try {
            ev.preventDefault();
            $("#availableColumnsList li.active").removeClass("active");
            $(this).addClass('active');
            //extractLeftColData($(this));
            const selectedColumnIdx = $(this).data('idx');
            //console.log(selectedColumnIdx, selectedColumnName, selectedColumnDataType.toLowerCase());
            clickedLeftColumnItem = saveClickedColumn(true, selectedColumnIdx);
            //console.log(clickedLeftColumnItem);
        } catch (err) {
            throw err;
            clickedLeftColumnItem = '';
        }

    });

    $("ul#availableColumnsList").on("dblclick", 'li', function (ev) {
        ev.preventDefault();
        try {

            const [idx, colName, colDataType] = extractLeftColData(clickedLeftColumnItem);
            // console.log(idx, colName, colDataType);
            const optionsMarkup = dataTypeOptions(colDataType);
            createNewItemRightColumn(idx, colName, colDataType, optionsMarkup);
            clickedLeftColumnItem.removeClass('active').addClass("disabled bg-gray-200");
            // $(".column-option-dtype").trigger('change', "reselect");

        } catch (error) {
            //throw error;
            if (error instanceof TypeError) {
                swAlert("error", "Please select column from left!", 'error');
            }
        } finally {
            clickedLeftColumnItem = ""; // to avoid duplicat items

        }

    });
}

function selectPickedRightColumns() {

    let pickedColumnsSeList = $(".colPickedItem");
    $('ul#pickedColumnsList').on('click', 'li', function (ev) {
        ev.preventDefault();
        $("#pickedColumnsList li.active").removeClass("active");
        $(this).addClass('active');
        const selectedColumnIdx = $(this).data('idx');
        //console.log(selectedColumnIdx, $(this).html());
        clickedRightColumnItem = saveClickedColumn(false, selectedColumnIdx);


    });

    $("ul#pickedColumnsList").on("dblclick", 'li', function (ev) {
        ev.preventDefault();
        const [idx, colName, colDataType] = extractRightColData(clickedRightColumnItem);
        enableLeftColumnItem(idx);
        clickedRightColumnItem.remove();
        clickedRightColumnItem = "";
    });


}

function addItemRightColumn() {
    // add item to from left column to right column
    if (clickedLeftColumnItem !== "") {
        try {

            const [idx, colName, colDataType] = extractLeftColData(clickedLeftColumnItem);
            //console.log(idx, colName, colDataType);
            const optionsMarkup = dataTypeOptions(colDataType);
            createNewItemRightColumn(idx, colName, colDataType, optionsMarkup);
            clickedLeftColumnItem.removeClass('active').addClass("disabled bg-gray-200");

        } catch (error) {
            //throw error;
            if (error instanceof TypeError) {
                swAlert("error", "Please select column from left!", 'error');
            }
        } finally {
            clickedLeftColumnItem = ""; // to avoid duplicat items
        }
    } else {
        swAlert("error", "Please select column from left!", 'error');
    }
}

function addItemLeftColumn() {
    // add item to from right column to left column
    if (clickedRightColumnItem !== "") {
        const [idx, colName, colDataType] = extractRightColData(clickedRightColumnItem);
        enableLeftColumnItem(idx);
        clickedRightColumnItem.remove();
        // to set the notes in the bottom of modal
        let tmpRemovedItem = $(clickedRightColumnItem.find('select'));

        clickedRightColumnItem = "";
    } else {
        swAlert("error", "Please select column from right!", 'error');
    }
}

function addAllRightColumnItems() {
    // this when member clicked on the left column to add new item to right column 
    $("#pickedColumnsList").empty(); // to avoid duplicate items in the list
    let availableColumnsList = $("#availableColumnsList li");
    availableColumnsList.each(function (cIdx, column) {
        //console.log(idx, '-> ', li);
        const columnIndex = cIdx;
        const columnItem = $(column);
        clickedLeftColumnItem = columnItem;
        const [idx, colName, colDataType] = extractLeftColData(clickedLeftColumnItem);
        const optionsMarkup = dataTypeOptions(colDataType);
        createNewItemRightColumn(idx, colName, colDataType, optionsMarkup);
        clickedLeftColumnItem.removeClass('active').addClass("disabled bg-gray-200");
        clickedLeftColumnItem = "";

    });
    // this to reset and fix the criteria when add all columns btn clicked
    $(".column-option-dtype").trigger('change', "reselect");
    resetAllCriteria();
}

function addAllLeftColumnItems() {
    // this when member clicked on the right column to get back old item to left column 
    const pickedColumnsList = $("#pickedColumnsList li");
    pickedColumnsList.each(function (cIdx, column) {
        //console.log(idx, '-> ', li);
        const columnIndex = parseInt(cIdx);
        const columnItem = $(column);
        clickedRightColumnItem = columnItem;
        //console.log(columnItem.find('select').data('value').toLowerCase());
        const [idx, colName, colDataType] = extractRightColData(clickedRightColumnItem);
        //console.log(idx, colName, colDataType);
        //console.log(clickedRightColumnItem.html());
        enableLeftColumnItem(idx);

        clickedRightColumnItem.remove();
        clickedRightColumnItem = "";
        selectedOptionsArray = [];
        resetAllColumnsToDefault();


    });
}

function validatePickedColumns(evt) {
    evt.preventDefault();
    let isAllOK = true; // if this true means all columns data type have been selected


    let validatePickedColumnsList = $("#pickedColumnsList").children('li');


    // console.log(validatePickedColumnsList);
    if (validatePickedColumnsList.length >= 3) {
        for (let tmpPic of validatePickedColumnsList) {
            const val = $(tmpPic).children().find("select option:selected").text().trim().toLowerCase();
            selectedOptionsArray.push(val);
        }
        //console.log(validatePickedColumnsList);
        for (let col of validatePickedColumnsList) {
            const selectedDtypeOption = $(col).children().find("select option:selected").text().trim().toLowerCase();
            // console.log(selectedDtypeOption);
            const tmpCol = $(col);
            const [idx, colName, colDataType] = extractRightColData(tmpCol);
            //console.log(idx, colName, colDataType);
            if (selectedDtypeOption === "") {
                //console.log('not selected', typeof selectedColumnDataType);
                // if the member did not selecte the data type of columns
                // $("#isValidateData").html(timesMark).removeClass('text-success').addClass("text-danger");
                $(col).children().find("select").addClass('is-invalid');
                isAllOK = false;
            } else {
                // $("#isValidateData").html(checkMark).removeClass('text-danger').addClass("text-success");
                $(col).children().find('select').removeClass('is-invalid');
                selectedValidateColumns[colName] = selectedDtypeOption;
            }

        }

    } else {
        swAlert("Error", "Please select at least 3 columns with the data type!", 'error');
    }

    // if all columns options selected validate the columns types
    if (isAllOK === true) {

        if (selectedOptionsArray.includes("Donation Field".toLowerCase()) === false) {
            Swal.fire({
                title: 'Are you sure?',
                text: "Do you want to select donation field?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, select it',
                cancelButtonText: "No, process without it",
                allowOutsideClick: false,
                reverseButtons: true,
                allowEscapeKey: false,
                allowEnterKey: false,
            }).then((result) => {
                if (!result.value) {  // means the member does not select donation field
                    sendRequestValidate();
                } else {
                    $("#donationFieldLi").removeClass("d-none");
                }
            })
        } else {
            sendRequestValidate();
        }
    }
}


function validateColumnsAjaxRequest(columnsObj) {
    const parameters = window.location.pathname;
    // this function when memeber want to validate the data type in dual dialog box
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/validate-columns",
        // dataType: "json",
        data: {
            "columns": JSON.stringify(columnsObj),
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

function resetAllColumnsToDefault() {
    $("#pickedColumnsList").empty();
    let availableColumnsList = $("#availableColumnsList li");
    availableColumnsList.each(function (cIdx, column) {
        //console.log(idx, '-> ', li);
        const colIt = $(column);
        colIt.removeClass("disabled bg-gray-200");
        clickedLeftColumnItem = "";
        clickedRightColumnItem = "";
        selectedOptionsArray = [];
        optionsSelected = {};
        isUniqueIDSelected = false;
    });
    resetAllCriteria();
}

function sendRequestValidate() {
    let validateResponseObj = validateColumnsAjaxRequest(selectedValidateColumns);
    $.when(validateResponseObj).done(function (data, textStatus, jqXHR) {
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);

        if ((textStatus === 'success') && (jqXHR.status === 200)) {
            // setSessionLastName("pick_columns"); // to save the current session name
            setSessionLastName("data_process");
            $("#processPickedColumnsBtn").removeClass("disabled").removeAttr("disabled style");
            for (let key in selectedValidateColumns) {
                // let colKey = key.split(". ")[1].trim(); // to split the column name from the index number
                // selectedPickedColumns.push(colKey);
                selectedPickedColumns.push(key);
            }
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success',
                    cancelButton: 'btn btn-primary'
                },
                buttonsStyling: false
            })

            swalWithBootstrapButtons.fire({
                title: 'Success',
                text: "Validation done, all data are valid you can process or click on back to edit the picked columns",
                icon: 'success',
                showCancelButton: true,
                confirmButtonText: 'Process',
                cancelButtonText: 'Back',
                reverseButtons: true,
                allowOutsideClick: false,
                allowEscapeKey: false,
            }).then((result) => {
                if (result.value) {
                    $("#validateColumnsBtn").attr("disabled", 'disabled').toggleClass('disabled');
                    $("#processPickedColumnsBtn").attr("disabled", 'disabled').toggleClass('disabled');
                    $("#processPickedColumnsBtn").trigger('click');
                } else if (
                    /* Read more about handling dismissals below */
                    result.dismiss === Swal.DismissReason.cancel
                ) {
                    Swal.close();
                }
            })
        }


    });
}


function columnOptionsChangeSaved(ele, option) {
    const element = $(ele);
    if (element.hasClass('border border-danger')) element.removeClass('border border-danger');
    element.attr("data-toggle", 'tooltip');
    element.attr('title', `Default data format ${element.data('value').toUpperCase()}\nCurrent data format ${element.val().split(" ")[0].toUpperCase()}`);
    // element.removeAttr('title');  // to remove current tooltip if exists, avoid tooltip bug
    const elementLiParent = $(element.parent().parent());
    const dataIX = elementLiParent.data("idx");

    // console.log(optionsSelected);
    // console.log(dataIX, element.val());
    // console.log(element.data(), element.text());
    // console.log(element.val());
    // check if the value not empty to add
    try {
        // const tmpValue = element.val().trim().toLowerCase();
        // optionsSelected.push(tmpValue);
        // if (element.val() !== "" || element.val() !== '0') optionsSelected[dataIX] = element.val().trim().toLowerCase();
        if (element.val() === "") {
            // here if the member select blank or empty option
            element.attr('title', 'Data format is empty!');

            element.addClass('border border-danger');
            // setCriterias();
            // return;

        }
        optionsSelected[dataIX] = element.val().trim().toLowerCase();
        // console.log(countJsonItems(optionsSelected, "Text Field".toLowerCase()));
        // console.log(optionsSelected);


    } catch (e) {
        if (e instanceof TypeError) {
            // statements to handle TypeError exceptions
            console.error(e);
            // console.error(tmpValue);
        } else {
            // statements to handle any unspecified exceptions
            console.error(e)
        }
    } finally {
        setCriterias();
    }
    // console.log(optionsSelected, Object.keys(optionsSelected).length);
    const selectOpVal = element.find("option:selected");
    // get the span of tooltip
    const tmpSpan = $(element.parent().parent().find("span")[1]);
    const tmpIDSpan = $(element.parent().parent().find("span")[2]);
    // check the data type if convert from number to text and otherwise
    if ((element.data("value").toLowerCase().includes("text".toLowerCase()) === true && selectOpVal.text().toLowerCase().includes('numeric') === true) || (element.data("value").toLowerCase().includes('text') === true && selectOpVal.text().toLowerCase().includes("Donation Field".toLowerCase()) === true)) {
        let confirmMsg = `Warning. You are converting a default '${element.data("value").toUpperCase()}' data type to a '${selectOpVal.text().replace(" Field", "")}' data type!`;

        // check if this call from reselect columns function to ignore show the dialog of change data type warning
        // check if member click no set the select option to null, else select the option
        // console.log(elementLiParent.text());
        if ((typeof option === undefined) || (typeof option === 'undefined')) {
            swConfirmDtype(element, confirmMsg, tmpSpan);
        } else if (option === 'reselect') {
            tmpSpan.show();
            element.addClass('border border-danger');
            element.attr("data-toggle", 'tooltip');
            element.attr('title', `Default data format TEXT\nCurrent data format ${element.val().split(" ")[0].toUpperCase()}`);
            // check if the donation field selected to make it visible with check mark
            if (element.val().toLowerCase().includes('donation') === true) {
                $("#donationFieldLi").removeClass("d-none");
                $("#donationField").html(checkMark).removeClass('text-danger').addClass("text-success");
            }
        }


    } else {
        tmpSpan.hide();
    }
    // check if the member select the id so disabled on the others select
    // console.log(element.data())
    if ((element.val().toLowerCase() === "Unique Identifier (ID)".toLowerCase())) {
        element.data('is-uid', '1');
        if (element.data("value") !== "") {
            $(".column-option-dtype  option:contains('Unique Identifier (ID)')").attr("disabled", "disabled");
            isUniqueIDSelected = true;
            tmpIDSpan.show();
            element.attr("disabled", "disabled");
            element.addClass("disabled");
            // when member click on the reset unique button
            tmpIDSpan.on("click", function (e) {
                let clickedResetID = $(this);
                let clickedResetIDParent = $(this).parent().find("select");
                $(".column-option-dtype  option:contains('Unique Identifier (ID)')").removeAttr("disabled");
                // let ix = optionsSelected.indexOf("Unique Identifier (ID)".toLowerCase());
                // optionsSelected.splice(ix, 1);  // delete the id from the array
                delete optionsSelected[dataIX];  // delete the id from the json object
                clickedResetID.hide();
                isUniqueIDSelected = false;
                clickedResetIDParent.val("");
                $("#selectUniqueID").html(timesMark).removeClass('text-success').addClass("text-danger");
                // $("#isValidateData").html(timesMark).removeClass("text-success").addClass("text-danger");
                element.addClass('border border-danger');
                clickedResetIDParent.removeAttr("disabled");
                clickedResetIDParent.removeClass("disabled");
                setCriterias();
                // disable the validate & process buttons
                /*$("#validateColumnsBtn").addClass("btn-light-primary disabled");
                $("#validateColumnsBtn").attr("disabled", "disabled");
                $("#validateColumnsBtn").attr("style", "cursor: not-allowed;");
                $("#processPickedColumnsBtn").addClass("disabled");
                $("#processPickedColumnsBtn").attr("disabled", "disabled");
                $("#processPickedColumnsBtn").attr("style", "cursor: not-allowed;");*/


            });

        } else {
            swAlert("Error", "Unique ID must be not NULL!", 'error');
            delete optionsSelected[dataIX];  // delete the id from the json object
            element.val("");
        }
    }


    // check if the member select unique id option, check mark criteria of it
    setCriterias();


}


// this function will set the criterias if the user delete, ...etc
function setCriterias() {
    let cirStatus = false;
    let cirMsg = "";
    // check if the member select unique id option, check mark criteria of it
    if (checkValueExists(optionsSelected, "Unique Identifier (ID)".toLowerCase()) === true) {
        $("#selectUniqueID").html(checkMark).removeClass('text-danger').addClass("text-success");
        isUniqueIDSelected = true;
    } else {
        $("#selectUniqueID").html(timesMark).removeClass('text-success').addClass("text-danger");
        isUniqueIDSelected = false;
        cirStatus = true;
        cirMsg = 'error in uid';
    }
    // console.log(checkValueExists(optionsSelected, "Donation Field".toLowerCase()));
    // check if donation field selected
    if (checkValueExists(optionsSelected, "Donation Field".toLowerCase()) === true) {
        $("#donationFieldLi").removeClass("d-none");
        $("#donationField").html(checkMark).removeClass('text-danger').addClass("text-success");
    } else {
        if ($("#donationFieldLi").is(":hidden") === true) {
            $("#donationField").html(timesMark).removeClass('text-success').addClass("text-danger");

        } else {
            $("#donationField").html(timesMark).removeClass('text-success').addClass("text-danger");
            $("#donationFieldLi").addClass("d-none");
        }

    }

    // check if the length more than 3 options mean select 3 columns, check its criteria
    if (Object.keys(optionsSelected).length <= 2) {
        // console.log(Object.keys(optionsSelected).length, 'in if');
        $("#isValidateData").html(timesMark).removeClass("text-success").addClass("text-danger");
        cirStatus = true;
        cirMsg = 'error in minimum selected'

    } else {
        // console.log(Object.keys(optionsSelected).length, 'in else');
        $("#isValidateData").html(checkMark).removeClass("text-danger").addClass("text-success");
    }

    // check if text fields more than 2
    if (countJsonItems(optionsSelected, "Text Field".toLowerCase()) > 2) {
        $("#isSelect3Col").html(checkMark).removeClass("text-danger").addClass("text-success");
    } else {
        $("#isSelect3Col").html(timesMark).removeClass('text-success').addClass("text-danger");
        cirStatus = true;
        cirMsg = 'error text fields less than 3';

    }
    // console.log(checkValueExists(optionsSelected, ""));
    // check if there is any empty select menu
    /*if (checkValueExists(optionsSelected, "") === true) {
        cirStatus = true;
    }*/


     $(".column-option-dtype").each(function (idx, val) {
         let currTmpEle = $(val);
        // console.log(currTmpEle.val() === '', currTmpEle);
        //  console.log(typeof currTmpEle.val(), currTmpEle.val());

         if ((currTmpEle.val() !== '') && (currTmpEle.val() !== null)) {
             // here if the element is not uid
             // console.log(currTmpEle.data());
             // console.log('value not uid and not empty');
             currTmpEle.removeClass("border border-danger");

         } else if((currTmpEle.data('is-uid') === '1') && (currTmpEle.val() === null)){
             // here if the element is uid
            // console.log('this is the uid select')
         }else {
             // here if the element is empty
            // console.error('empty', currTmpEle.val())
             currTmpEle.addClass("border border-danger");
             $("#isValidateData").html(timesMark).removeClass("text-success").addClass("text-danger");
             cirStatus = true;
             cirMsg = 'emtpy select';
         }
     });
    if(cirStatus === true){
        console.error('there errors!!!');
        console.error(cirMsg);
        enableValidateProcBtn('disable');

    }else {
        // here no errors or all criterias are good to go
        enableValidateProcBtn('enable');
    }
}

// reset all criteria after reset button clicked
function resetAllCriteria() {
    $("#isValidateData").html(timesMark).removeClass('text-success').addClass("text-danger");
    $("#isSelect3Col").html(timesMark).removeClass('text-success').addClass("text-danger");
    $("#selectUniqueID").html(timesMark).removeClass('text-success').addClass("text-danger");
    $("#donationField").html(timesMark).removeClass('text-success').addClass("text-danger");
    $("#donationFieldLi").addClass("d-none");
    $("#validateColumnsBtn").addClass("btn-light-primary disabled");
    $("#validateColumnsBtn").attr("disabled", "disabled");
    $("#validateColumnsBtn").attr("style", "cursor: not-allowed;");
}

// this function will disable or enable validate or process buttons as needed
function enableValidateProcBtn(action) {
    if (action === 'enable') {
        $("#validateColumnsBtn").removeClass("disabled btn-light-primary");
        $("#validateColumnsBtn").removeAttr("disabled style");
        $("#validateColumnsBtn").addClass("btn-primary");
    } else {
        $("#validateColumnsBtn").addClass("btn-light-primary disabled");
        $("#validateColumnsBtn").attr("disabled", "disabled");
        $("#validateColumnsBtn").attr("style", "cursor: not-allowed;");
    }
}


let targetNodes = $("#pickedColumnsList");
let MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
let myObserver = new MutationObserver(mutationHandler);
let obsConfig = {childList: true, characterData: true, attributes: true, subtree: true};
//--- Add a target node to the observer. Can only add one node at a time.
targetNodes.each(function () {
    myObserver.observe(this, obsConfig);
});

function mutationHandler(mutationRecords) {

    // console.info("mutationHandler:");
    mutationRecords.forEach(function (mutation) {
        // this condition if one the childes is delete or remove from the dom
        if (typeof mutation.removedNodes === 'object') {

            try {
                const textContent = mutation.removedNodes[0].textContent.trim() ? (typeof mutation.removedNodes !== undefined) : "";
                if (textContent !== "") {
                    let pickedRightCol = $(mutation.removedNodes);
                    const pickedRightSelect = pickedRightCol.find('select');
                    const rightSelectParentLi = pickedRightSelect.parents('li');
                    // console.log(rightSelectParentLi.data());
                    // console.log(pickedRightSelect.val());
                    // check if the removed item is the unique id
                    if (pickedRightSelect.is(":disabled") === true) {
                        //unique identifier (id)
                        // console.log(optionsSelected);
                        for (key in optionsSelected) {
                            if (optionsSelected.hasOwnProperty(key) && optionsSelected[key] === 'unique identifier (id)') {
                                delete optionsSelected[key];
                                $(".column-option-dtype  option:contains('Unique Identifier (ID)')").removeAttr("disabled");
                                isUniqueIDSelected = false;
                            }
                        }
                    } else {
                        const idx = rightSelectParentLi.data('idx');
                        // console.log(idx, optionsSelected[idx])
                        delete optionsSelected[idx];

                    }
                    setCriterias();


                }

            } catch (e) {
                if (e instanceof TypeError) {

                }
                if (!(e instanceof TypeError)) {
                    console.error(e);
                }
            }


            // console.log(pickedRightSelect.val());
        }

        if (typeof mutation.addedNodes === 'object') {

            // console.log(isUniqueIDSelected);
            let pickedRightCol = $(mutation.addedNodes);
            const pickedRightSelect = pickedRightCol.find('select');
            if (pickedRightSelect.length > 0) {
                if (isUniqueIDSelected === true) {
                    $(".column-option-dtype  option:contains('Unique Identifier (ID)')").attr("disabled", "disabled");
                } else {
                    $(".column-option-dtype  option:contains('Unique Identifier (ID)')").removeAttr("disabled");
                }
                setCriterias();

                // here for set criteria to false because no data type selected for new column

            }
        }


    });
}


jQuery(document).ready(function () {
    //mutationObservFunc();
    selectAvaliableColumns();
    selectPickedRightColumns();
    let addColumnBtn = $("#addColumnBtn");
    addColumnBtn.on("click", addItemRightColumn);
    let removeColumnBtn = $("#removeColumnBtn");
    removeColumnBtn.on('click', addItemLeftColumn);
    let addAllColumnsBtn = $("#addAllColumnsBtn");
    addAllColumnsBtn.on('click', addAllRightColumnItems);
    let removeAllColumnsBtn = $("#removeAllColumnsBtn");
    removeAllColumnsBtn.on('click', addAllLeftColumnItems);
    let validateColumnsBtn = $("#validateColumnsBtn");
    validateColumnsBtn.on("click", validatePickedColumns);
    let columnsDataTypeOptions = $(".column-option-dtype");
    $("#pickedColumnsList").on("change", ".column-option-dtype", function (evt, option) {
        columnOptionsChangeSaved(this, option);
        // console.log("change event fired!!");
    });
    /*$("#pickedColumnsList").on("hover", ".column-option-dtype", function (evt, option) {
        console.log($(this));
        // console.log("change event fired!!");
    });*/


    let totalInterval = setInterval(function () {
        setColumnsTotal();
    }, 200);


    //removePickedColumn();
    let resetColumnBoxBtn = $("#resetColumnBoxBtn");
    resetColumnBoxBtn.on("click", resetAllColumnsToDefault);

    //let dataTableHeaders = $('#data_handler_table thead tr th');
    // $('.dataTableHeader').on('click', function(){
    //   alert("kdifr.d");
    // });


});


