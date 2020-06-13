const dataTypeArray = ["", "object", "int64", "float64", 'bool', 'datetime64', 'category', 'timedelta'];
const leftClickedColumnClass = 'columnItem';
const rightClickedColumnClass = 'pickedItem';
var clickedLeftColumnItem = "";
var clickedRightColumnItem = "";
var clickedRemoveSelectedColumn = "";
var allClickedSelectColumns = Array();
var resetAvailableColumnsList = Array();
var resetPickedColumnsList = Array();

function setColumnsTotal() {
    let avaTotal = $("#availableColumnsList li").length;
    let pickTotal = $("#pickedColumnsList li").length;
    //console.log(avaTotal, '---', pickTotal);
    $("#avaliableColumnsTotal h5 > b").text(avaTotal);
    $("#pickedColumnsTotal h5 > b").text(pickTotal);
}

function dataTypeOptions(dataType) {
    let optionsMarkup = "";
    for (let dType of dataTypeArray) {
        if (dType == dataType) {
            optionsMarkup += `<option value='${dType}' selected>${dType}</option>\n`;
        } else {
            optionsMarkup += `<option value='${dType}'>${dType}</option>\n`;
        }
    }
    return optionsMarkup;
}

function createNewItemRightColumn(colIdx, colName, colDataType, optionsList) {
    //console.log(colIdx, colName, colDataType, optionsList);
    //pickedColumnsList
    const liMarkup = `
            <li data-idx="${colIdx}"
                class='pickedItem list-group-item d-flex justify-content-between align-items-center cursor-pointer list-group-item-action'>
                ${colName}
                <span class="nav-label w-100px ">
                    <select data-value='${colDataType}' class="form-control form-control-sm h-40px">
                            ${optionsList}
                    </select>
                </span>
                
            </li>
        `;
    $("#pickedColumnsList").append(liMarkup);
    //$("#pickedColumnsList").after(liMarkup);


}

function enableLeftColumnItem(colIdx) {
    const leftItem = fetchColumnByDataIdx(true, colIdx);
    leftItem.removeClass("disabled");
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
    const selectedColumnDataType = colItem.children().text().trim().toLowerCase();
    const selectedColumnIdx = colItem.data('idx');
    //console.log(selectedColumnIdx, selectedColumnName, selectedColumnDataType);
    return [selectedColumnIdx, selectedColumnName, selectedColumnDataType];
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
            //console.log(idx, colName, colDataType);
            const optionsMarkup = dataTypeOptions(colDataType);
            createNewItemRightColumn(idx, colName, colDataType, optionsMarkup);
            clickedLeftColumnItem.removeClass('active').addClass("disabled");

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
    if (clickedLeftColumnItem != "") {
        try {

            const [idx, colName, colDataType] = extractLeftColData(clickedLeftColumnItem);
            //console.log(idx, colName, colDataType);
            const optionsMarkup = dataTypeOptions(colDataType);
            createNewItemRightColumn(idx, colName, colDataType, optionsMarkup);
            clickedLeftColumnItem.removeClass('active').addClass("disabled");

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
    if (clickedRightColumnItem != "") {

        const [idx, colName, colDataType] = extractRightColData(clickedRightColumnItem);
        enableLeftColumnItem(idx);
        clickedRightColumnItem.remove();
        clickedRightColumnItem = "";
    } else {
        swAlert("error", "Please select column from right!", 'error');
    }
}

function addAllRightColumnItems() {
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
        clickedLeftColumnItem.removeClass('active').addClass("disabled");
        clickedLeftColumnItem = "";
    });
}

function addAllLeftColumnItems() {
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

    });
}


function validatePickedColumns(evt) {
    evt.preventDefault();
    let isAllOK = true; // if this true means all columns data type have been selected
    let selectedValidateColumns = {};
    let validatePickedColumnsList = $("#pickedColumnsList").children('li');
    //console.log(validatePickedColumnsList);
    if (validatePickedColumnsList.length >= 3) {
        //console.log(validatePickedColumnsList);
        for (let col of validatePickedColumnsList) {
            const selectedDtypeOption = $(col).children().find("select option:selected").text().trim().toLowerCase();
            const tmpCol = $(col);
            //                console.log(tmpCol.html());
            const [idx, colName, colDataType] = extractRightColData(tmpCol);
            //                console.log(tmpCol.html());
            //console.log(idx, colName, colDataType);
            if (selectedDtypeOption === "") {
                //console.log('not selected', typeof selectedColumnDataType);
                // if the member did not selecte the data type of columns
                $(col).children().find("select").addClass('is-invalid');
                isAllOK = false;
            } else {
                $(col).children().find('select').removeClass('is-invalid');
                selectedValidateColumns[colName] = selectedDtypeOption;
            }


        }
        if (isAllOK === true) {
            console.log(selectedValidateColumns);
            let validateResponseObj = validateColumnsAjaxRequest(selectedValidateColumns);
            $.when(validateResponseObj).done(function (data, textStatus, jqXHR) {
                console.log(data);
                console.log(textStatus);
                console.log(jqXHR);
                swAlert("Success", "All data looks ok, you can press process button", 'success');
                $("#processPickedColumnsBtn").removeClass("disabled").removeAttr("disabled");
                for (let key in selectedValidateColumns) {
                    selectedPickedColumns.push(key);
                }
            });

        } else {
            swAlert("Error", "Please select data type for the picked column(s)!", 'error');
        }


    } else {
        swAlert("Error", "Please select at least 3 columns with the data type!", 'error');
    }
}


function validateColumnsAjaxRequest(columnsObj) {
    return $.ajax({ // should return to can access from $.when()
        method: "POST",
        cache: false,
        // processData: false,
        // contentType: false,
        timeout: 300000, // 5 minutes
        url: webSiteUrl + "/dashboard/data/api/validate-columns",
        // dataType: "json",
        data: {
            "columns": JSON.stringify(columnsObj)
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
        colIt.removeClass("disabled");
        clickedLeftColumnItem = "";
        clickedRightColumnItem = "";
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
    let totalInterval = setInterval(function () {
        setColumnsTotal();
    }, 300);

    function disableF5(e) {
        if ((e.which || e.keyCode) == 116) e.preventDefault();
    };
    $(document).on("keydown", disableF5);
    //removePickedColumn();
    let resetColumnBoxBtn = $("#resetColumnBoxBtn");
    resetColumnBoxBtn.on("click", resetAllColumnsToDefault);




});