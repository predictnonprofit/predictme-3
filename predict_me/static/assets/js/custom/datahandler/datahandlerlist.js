let undoValue = "";  // the undo value
let undoValue2 = '';  // the undo value which will save when save button clicked
let undoElement = null;  // the undo input element
let isDownloaded = false;  // if true mean the member download the data template
$(function () {

    // this to delay the donner files but show the spinner first
    var donerFilesSpinner = $('#donerFilesSpinner');
    var donerFilesTree = $('#donerFilesTree');

    // This event is fired when the modal has been made visible to the user
    $('#donerFilesModal').on('shown.bs.modal', function (e) {
        //$('#donerFilesModal').modal('handleUpdate'); // to make Dynamic heights
        setTimeout(function () {
            // this will be ajax request to grab users files

            // hide the spinner & show the tree view
            //donnerFilesSpinner.addClass("d-none");
            donerFilesSpinner.fadeOut(1000, function () {
                donerFilesTree.fadeIn();
            });


        }, 3000);
    });


    // enable upload btn by check agree terms and conditions
    const agreeDataHandlerCheckBox = $("#agreeDataHandlerCheckBox");
    const dataUploadBtn = $("#dataUploadBtn");
    agreeDataHandlerCheckBox.on("change", function () {
        if (this.checked) {
            dataUploadBtn.removeAttr("disabled");
            dataUploadBtn.removeClass("my-disabled-btn");
            $("#semitransparent").addClass("d-none");

            $("#donerFile").removeAttr("disabled");
        } else {
            dataUploadBtn.attr("disabled", "disabled");
            $("#semitransparent").removeClass("d-none");
            $("#donerFile").attr("disabled", "disabled");

        }
    });


    // enable the check button on the instruction modal
    let validateObj = {
        "agree": false,
        "download": false,
    };
    const instructionsCheckButtons = $(".instruction-check-btn");
    instructionsCheckButtons.on("change", function (evt) {
        let checkedDataVal = $(this).data('action');

        if ($(this).is(":checked")) {
            validateObj[checkedDataVal] = true;
        } else {
            validateObj[checkedDataVal] = false;
        }
        // if two checked enable download button
        if ((validateObj['agree'] === true) && (validateObj['download'] === true)) {
            $("#downloadTemplateLink").removeClass('disabled not-allowed-cursor');
            $("#downloadTemplateLink").attr('href', "/profile/download");
        } else {
            $("#downloadTemplateLink").addClass('disabled not-allowed-cursor');
            $("#downloadTemplateLink").removeAttr('href');
        }

    });

    // this for disable the upload button when user not accept the terms from the modal dialog
    let closeUploadInstBtn = $('#closeUploadInstBtn');
    let acceptUploadInstBtn = $("#acceptUploadInstBtn");
    let downloadTemplateLink = $("#downloadTemplateLink");
    var acceptDownloadObj = {};
    downloadTemplateLink.on('click', function (evt) {
        isDownloaded = true;
        // check if the two options checked enable the check button in the modal
        $("#acceptUploadInstBtn").removeClass("disabled notAllowedCur").removeAttr("disabled");
        $("#uploadDataFileBtn").removeClass("disabled notAllowedCur").removeAttr("disabled");
        $("#acceptsCheckMark").replaceWith('<i class="icon-lg text-success la la-check-double" id="acceptsCheckMark"></i>');
        /*dataUploadBtn.attr("disabled", "disabled");
        $("#semitransparent").removeClass("d-none");
        $("#donerFile").attr("disabled", "disabled");
        $("#acceptUploadInstBtn").addClass("disabled notAllowedCur").attr("disabled", "disabled");
        $("#acceptsCheckMark").replaceWith('<i class="icon-lg text-danger la la-times" id="acceptsCheckMark"></i>');*/

    });

    // this here when member close the upload modal with instructions
    $('#uploadFileModal').on('hidden.bs.modal', function (e) {
        $("#acceptUploadInstBtn").addClass("disabled notAllowedCur").attr("disabled", 'disabled');
        $("#uploadDataFileBtn").addClass("disabled notAllowedCur").attr("disabled", 'disabled');
        $("#acceptsCheckMark").replaceWith('<i class="icon-lg text-danger la la-times" id="acceptsCheckMark"></i>');
        $("#donerFile").attr("disabled", "disabled");
    })
    // accept upload instruction terms button
    acceptUploadInstBtn.click(function (e) {
        $("#semitransparent").toggleClass("d-none");
        $("#donerFile").removeAttr("disabled");
        dataUploadBtn.removeAttr("disabled");
        agreeDataHandlerCheckBox.prop("checked", true);
        $(".instruction-check-btn").each(function (index, item) {
            const elem = $(item);
            // elem.is(":checked")
            if (elem.data('action') === "agree") {
                acceptDownloadObj['is_accept_terms'] = true;
            }
            if (elem.data('action') === "download") {
                acceptDownloadObj['is_accept_download_template'] = true;
            }
        });
        acceptDownloadObj['is_download_template'] = isDownloaded;
        const acceptDownloadResponse = saveMemberAccepts(acceptDownloadObj);
        $.when(acceptDownloadResponse).done(function (data, textStatus, jqXHR) {
            if ((textStatus === "success") && (jqXHR.status === 200)) {
                // console.log(data);

            } else {
                swAlert("Error", data, 'error');
            }
        });
    });

    // not accept upload instruction terms button
    closeUploadInstBtn.click(function (e) {
        // check if agree upload terms checkbox checked or not
        if ((agreeDataHandlerCheckBox.prop("checked") === false) || (agreeDataHandlerCheckBox.prop("checked") === true)) {
            agreeDataHandlerCheckBox.prop("checked", false);
            dataUploadBtn.prop("disabled", true);

        }
        $("#downloadTemplateLink").addClass('disabled not-allowed-cursor');
        $("#downloadTemplateLink").removeAttr('href');

    });


    // this for the next button when user click next in pay or upgrade subscription dialog
    // all forms sections vars
    const askPayUpgradeSection = $("#askPayUpgradeSection");
    const payExtraRecordsSection = $("#payExtraRecordsSection");
    const upgradeSubscriptionSection = $("#upgradeSubscriptionSection");
    const closeUpgradeModalBtn = $("#closeUpgradeModalBtn");
    let purchaseUpgradeExtraBtn = $(".purchaseUpgradeExtraBtn");
    let currentShownSection = "";
    // the next btn
    const nextBtn = $('#nextBtn');
    // the back bth
    const backBtn = $("#backModalBtn");

    // const payUpgradeRadioBtn = $("#askPayUpgradeForm:radio");
    // next button click action
    nextBtn.on("click", function (e) {
        // radio btn which member will checks
        const actionRadioBtn = $('input[name=action]:checked').val();

        if (actionRadioBtn === "pay") {
            $(".purchaseUpgradeExtraBtn").filter("[data-action='pay']").fadeIn();
            currentShownSection = payExtraRecordsSection;
            askPayUpgradeSection.fadeOut(300, function () {
                payExtraRecordsSection.fadeIn();
            });
            backBtn.removeAttr("disabled");
            $(this).attr("disabled", "disabled");
            $(this).addClass("disabled my-disabled-btn");


        } else if (actionRadioBtn === "upgrade") {
            $(".purchaseUpgradeExtraBtn").filter("[data-action='upgrade']").fadeIn();
            currentShownSection = upgradeSubscriptionSection;
            askPayUpgradeSection.fadeOut(300, function () {
                upgradeSubscriptionSection.fadeIn();
            });
            backBtn.removeAttr("disabled");
            $(this).attr("disabled", "disabled");
            $(this).addClass("disabled my-disabled-btn");

        } else if (actionRadioBtn === "cancel") {
            Swal.fire({
                title: 'Are you sure?',
                text: "You want to abort this operation,\n and re-upload the file?",
                icon: 'warning',
                showCancelButton: true,
                allowOutsideClick: false,
                cancelButtonText: "No",
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes'
            }).then((result) => {
                if (result.value) {
                    let deleteDataFileResponse = deleteDataFile();
                    $.when(deleteDataFileResponse).done(function (data, textStatus, jqXHR) {
                        // console.log(textStatus);
                        // console.log(jqXHR);
                        // console.log(data);

                        if ((textStatus === "success") && (jqXHR.status === 200)) {
                            // swAlert("Success", "Your data file has been deleted successfully!", "success");
                            window.location.reload();
                        } else {
                            swAlert("Error", "Error when delete the data file!", "error");
                        }

                    });

                    $("#extraRecordsModel").modal("hide");
                }
            });
        } else {

            swal.fire("Oops...", "You have to select one of the two options!", "error");

        }

    });

    // this for the back button when user click back in pay or upgrade subscription dialog
    backBtn.on('click', function (e) {
        $(".purchaseUpgradeExtraBtn").fadeOut();
        // alert($('body').hasClass('modal-open'));
        currentShownSection.fadeOut(300, function () {
            askPayUpgradeSection.fadeIn();
        });
        $(this).attr("disabled", "disabled");
        nextBtn.removeAttr("disabled");
        nextBtn.toggleClass("disabled my-disabled-btn");
    });

    // when member want to close the dialog
    closeUpgradeModalBtn.on('click', function () {
        Swal.fire({
            title: 'Are you sure?',
            text: "You want to abort this operation?",
            icon: 'warning',
            showCancelButton: true,
            allowOutsideClick: false,
            cancelButtonText: "No",
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes'
        }).then((result) => {
            if (result.value) {

                $("#extraRecordsModel").modal("hide");
            }
        });
    });


    // upgrade plan button
    // this to get the selected plan to upgrade
    purchaseUpgradeExtraBtn.on('click', function (e) {
        let actionLabel = $(this).data("action");
        const upgradePlanBtn = $('input[name=upgrade_plane]:checked').val();
        if (actionLabel === "upgrade") {
            if (upgradePlanBtn === "" || upgradePlanBtn === undefined) {
                swal.fire("Error", "You have to select plan!", "error");
            } else {
                swal.fire("Good", `You select ${upgradePlanBtn}`, "success");
                $(this).text("Upgrading...");
                $(this).addClass('spinner spinner-darker-success spinner-left');
                $(this).attr("disabled", "disabled");

            }

        } else if (actionLabel === "pay") {
            swal.fire("👍", `Purchased done`, "success");
        }

    });


    // upload data file functionality
    const uploadDataFileBtn = $("#uploadDataFileBtn");
    const uploadDataFileForm = $("#uploadDataFileForm");

    uploadDataFileForm.submit(function (e) {
        e.preventDefault();
        let donorFileuploadFormRequest = uploadDonorDataFile($(this));
        // console.log($("#session-name").val());
        $.when(donorFileuploadFormRequest).done(function (data, textStatus, jqXHR) {

            if ((textStatus === "success") && (jqXHR.status === 200)) {
                // var optionsList = [];
                if (typeof data === "object") {
                    //console.log(data);
                    if (data['is_allowed'] === true) {
                        // this mean the records total more than the allowed in subscription plan
                        $("#uploadFileModal").modal('hide');
                        uploadProgressModal(true, data);

                        nextProgressBtnModal.on('click', function (event) {

                            rowCountProgressDialog.modal('hide');
                            $("#extraRecordsModel").modal("handleUpdate");
                            $("#extraRecordsModel").modal("show");

                        });


                    } else if (data['is_allowed'] === false) {
                        if (data['row_count'] === 0) {
                            // this mean no row count, which means the donor id column not exists
                            swAlert("attention!!".toUpperCase(), `${data['msg']}`, 'error');

                        } else {
                            uploadProgressModal(false, data);
                        }


                    } else if ((data['is_allowed'] === false) && (data['is_empty'] === true)) {
                        // this mean no row count, which means the donor id column not exists
                        swAlert("attention!!".toUpperCase(), `${data['msg']}`, 'error');
                    }

                }

            } else {
                swAlert("Error!", "There is error, no success", "error");
            }


        });


    });


    // process button, which will send ajax request with the selected columns
    const processPickedColumnsBtn = $("#processPickedColumnsBtn");
    processPickedColumnsBtn.on('click', function (e) {
        selectedPickedColumns = _.uniq(selectedPickedColumns);  // to avoid duplicate columns name
        // console.log(selectedPickedColumns);
        // throw new Error("Something went badly wrong!");
        let selectedColumnsRequest = sendPickedColumns();
        $.when(selectedColumnsRequest).done(function (data, textStatus, jqXHR) {
            // console.log(jqXHR.statusCode);
            // console.log(jqXHR.responseText);
            //data, textStatus, jqXHR
            // console.log(data);
            // console.log(textStatus);
            // console.log(jqXHR);
            if ((textStatus === "success") && (jqXHR.status === 200)) { // change the condition
                setSessionLastName("data_process");
                window.location.reload();
            } else {
                swAlert("Error", data, "error");
            }

        });
    });


}); // end of $(function)


// show new stripe card input
const newStripeCardBtn = $("#newStripeCardBtn");
const newStripeInput = $("#newStripeInput");
newStripeCardBtn.click(function (e) {
    newStripeInput.fadeIn();
});

$(document).ready(function () {
    // setTheCookie();
    // stripeElementsFormDataHandler();
    let fetchedColumns = fetchDataFileColumns();

    $.when(fetchedColumns).done(function (data, textStatus, jqXHR) {
        // console.log(Object.keys(data));
        /* console.log(data);
         console.log(textStatus);
         console.log(jqXHR);*/
        // console.log(jqXHR.status);

        // check if the data not equal "", this mean no columns

        if ((textStatus === 'success') && (jqXHR.status === 200)) {

            if (data !== "") {
                let sortedColumns = Array();
                let columnsLabels = data;
                for (let cl in data) {
                    //unique identifier (id)
                    if (data[cl] === "unique identifier (id)") {
                        sortedColumns.push({"isUnique": true, "headerName": cl});
                    } else {
                        sortedColumns.push({"isUnique": false, "headerName": cl});
                    }

                }
                // sortedColumns = sortedColumns.sort();
                //initialise columns for the data table
                setColumnNamesHeader(sortedColumns);
                //initialise (fetch) rows, fetch the rows to datatable
                let dataFileRows = fetchDataFileRows();
                $.when(dataFileRows).done(function (rowData, rowTextStatus, rowJqXHR) {

                    //  console.log(rowData);
                    // console.log(rowTextStatus);
                    // console.log(rowJqXHR);

                    // check if there is any returned data
                    if ((rowTextStatus === 'success') && (rowJqXHR.status === 200)) {
                        // first hide the spinner loding div
                        $("#loadingDataSpinner").hide();
                        let rowsObject = rowData;
                        // console.log(rowsObject);
                        drawDataTableRows(rowsObject, false);
                    }


                });
            }
        }

    });

    // save button when member click on save button after click on undo button
    let saveDataFileBtn = $("#saveDataFileBtn");
    saveDataFileBtn.click(function (e) {
        e.preventDefault();
        // this when save button clicked after undo
        $("#dataListTable").css("opacity", "0.3");
        $(".data-table-col").attr("disabled", "disabled");
        $("#save-row-loader").fadeIn();
        // console.log(undoElement.data());
        let clonedNewRowsUpdates = allNewRowsUpdates;
        // console.log(clonedNewRowsUpdates);
        for (let row in clonedNewRowsUpdates) {
            clonedNewRowsUpdates[row]['colValue'] = undoElement.data("undo-val");
            // console.log(undoElement.data());
            // console.log(allNewRowsUpdates[row]);
            // console.log(clonedNewRowsUpdates[row]);
        }

        // throw new Error("Tess");
        let saveDataRespone = updateMemberDataFile(clonedNewRowsUpdates);
        $.when(saveDataRespone).done(function (data, textStatus, jqXHR) {
            // console.log(textStatus);
            // console.log(jqXHR);
            console.log(data);

            if ((textStatus === "success") && (jqXHR.status === 200)) {
                showToastrNotification('Saved successfully');
                $("#save-row-loader").fadeOut();
                $("#dataListTable").css("opacity", "1");
                $(".data-table-col").removeAttr("disabled");
                saveDataFileBtn.addClass("disabled").tooltip('hide');
                saveDataFileBtn.attr("disabled", "disabled");
                saveDataFileBtn.attr("style", "cursor: not-allowed");
                $("#undoBtn").addClass("disabled").tooltip("hide").attr('disabled', 'disabled');


                // window.location.reload();

            } else {
                showToastrNotification('Error while saving the data!', "danger");
            }

        });
    });

    // when I want to delete the data file
    let deleteDataFileBtn = $("#deleteDataFileBtn");
    deleteDataFileBtn.click(function (e) {
        e.preventDefault();
        let conBox = confirm("Do you want to delete the data file!!");
        if (conBox === true) {
            let deleteDataFileResponse = deleteDataFile();
            $.when(deleteDataFileResponse).done(function (data, textStatus, jqXHR) {
                // console.log(textStatus);
                // console.log(jqXHR);
                // console.log(data);

                if (textStatus === "success") {
                    swAlert("Success", "Your data file has been deleted successfully!", "success");
                    // window.location.reload();
                    window.location.href = window.location.origin + "/profile/data/";
                } else {
                    swAlert("Error", "Error when delete the data file!", "error");
                }

            });
        }


    });


    let cancelReuploadBtn = $("#cancelReuploadBtn");
    cancelReuploadBtn.on('click', function (evt) {

        let ask = confirm("Do you want to cancel current uploaded file and re-upload new file!!");
        if (ask === true) {
            const deleteDataFileResponse = deleteDataFile();
            $.when(deleteDataFileResponse).done(function (data, textStatus, jqXHR) {
                // console.log(textStatus);
                // console.log(jqXHR);
                // console.log(data);

                if (textStatus === "success") {
                    swAlert("Success", "Your data file has been deleted successfully!", "success");
                    // window.location.reload();
                    location.reload();
                    $("#columnsDualBoxModal").modal("hide");
                } else {
                    swAlert("Error", "Error when delete the data file!", "error");
                }

            });
        }
    });


    const reselectColumnsBtn = $("#reselectColumnsBtn");
    reselectColumnsBtn.on("click", function (e) {
        e.preventDefault();
        $('[data-toggle="tooltip"]').tooltip('dispose');
        reselectColumnsFunc(true);
    });

    const resetSortTableBtn = $("#resetSortTableBtn");
    resetSortTableBtn.on("click", function () {

        $("#data_handler_table > tbody tr").empty();
        resetSorting();
        $("#searchQuery").val(""); // empty search query
        $(this).addClass("disabled");
        $(this).attr("disabled", 'disabled');
        $(this).attr("style", 'cursor: not-allowed;');
        isClickedFilterCol = false;
        clickedRecordsCount = 50;
        clickedFilteredColName = "";
        $("#no-data-watermark").hide();
        $("[data-action='first']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
        $("[data-action='previous']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
        // check the length of the used rows if less than 50 disable all pagination buttons by default
        if ($('#records-count-alert').find('b').first().text() <= 50) {
            $("[data-action='next']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
            $("[data-action='last']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
        } else {
            $("[data-action='next']").removeAttr("disabled").removeClass("disabled").tooltip('update');
            $("[data-action='last']").removeAttr("disabled").removeClass("disabled").tooltip('update');
        }

        $("#undoBtn").attr("disabled", 'disabled').addClass("disabled").tooltip('hide');
    });


    const showRecordsSumSelect = $("#showRecordsSumSelect");

    const dataTableNavBtns = $(".data-table-nav-btns");
    dataTableNavBtns.on("click", function (evt) {
        // $("#loadingDataSpinner").fadeIn("fast");
        $("#data_handler_table > tbody tr").empty();
        $("#resetSortTableBtn").removeClass("disabled");
        $("#resetSortTableBtn").removeAttr("disabled style");

        const selectedRecCount = $(this).val();
        const theAction = $(this).data('action');
        if (theAction === 'next') {
            clickedRecordsCount += 50;
            let checkLastPageResponse = fetchDataFileRows(clickedRecordsCount + 50);
            $.when(checkLastPageResponse).done(function (data, textStatus, jqXHR) {
                // console.log(data['data'].length);
                if (data['data'].length < 50) {
                    $("[data-action='next']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
                    $("[data-action='last']").attr("disabled", "disabled").addClass("disabled").tooltip('hide');
                    $("[data-action='first']").removeAttr("disabled").removeClass("disabled").tooltip('update');
                }
            });
        } else if (theAction === "previous") {
            if (clickedRecordsCount !== 50) {
                clickedRecordsCount = clickedRecordsCount - 50;
                // check if the next indicator ">" is disabled because the member was in the last page, enable it
                if ($("[data-action='next']").is(":disabled") === true) {
                    $("[data-action='next']").removeAttr("disabled").removeClass("disabled").tooltip('update');
                    $("[data-action='last']").removeAttr("disabled").removeClass("disabled").tooltip('update');
                    $("#no-data-watermark").hide();
                }
            }

        } else if (theAction === 'first') {
            // when member click on first page
            clickedRecordsCount = 50;
            $("[data-action='previous']").attr("disabled", 'disabled').addClass("disabled");
            $(this).tooltip('hide').attr("disabled", 'disabled').addClass("disabled");
            $("[data-action='next']").tooltip('update').removeAttr("disabled").removeClass("disabled");
            $("[data-action='last']").tooltip('update').removeAttr("disabled").removeClass("disabled");

        } else if (theAction === 'last') {
            // when member click on last btn
            const allRecords = $("#records-count-alert b:first");  // get all records from alert in web page
            const tmpDiv = parseInt(parseInt(parseInt(allRecords.text()) / 50) * 50);
            let lastRecordsTotal = parseInt(parseInt(parseInt(allRecords.text()) / 50) * 50);
            clickedRecordsCount = parseInt(lastRecordsTotal);
            $(".data-table-nav-btns[data-action='last']").tooltip('hide').attr("disabled", 'disabled').addClass("disabled");
            $(".data-table-nav-btns[data-action='next']").tooltip('hide').attr("disabled", 'disabled').addClass("disabled");
        }

        if (clickedFilteredColName !== "") {
            let notValidateRowsResponse = fetchNotValidateRows(clickedFilteredColName);
            $.when(notValidateRowsResponse).done(function (data, textStatus, jqXHR) {
                if ((textStatus == "success") && (jqXHR.status == 200)) {
                    $("#loadingDataSpinner").fadeOut();
                    drawDataTableRows(data, false);
                } else {
                    swAlert("Error", data, 'error');
                }
            });
        } else {
            $("#loadingDataSpinner").fadeOut('fast');
            fetchRecordsByCount(clickedRecordsCount);
        }


    });


    const searchDataTableBtn = $("#searchDataTableBtn");
    searchDataTableBtn.on("click", function (evt) {
        const searchQueryValue = $("#searchQuery");
        let searchQuery = searchQueryValue.val().trim();
        if (searchQuery !== "") {
            fetchRecordsBySearchQuery(searchQuery);
            $("#loadingDataSpinner").fadeOut();
            $('.data-table-nav-btns').attr("disabled", 'disabled').addClass('disabled');
            $("#undoBtn").addClass("disabled").tooltip("hide").attr('disabled', 'disabled');
        }
    });


    // the undo button
    const undoBtn = $("#undoBtn");
    undoBtn.on("click", function (evt) {
        // $(".data-table-input").off("change");
        undoElement.focus();
        // console.log(undoValue);
        // console.log(undoValue2);
        // trigger when member clicked on undo to save the old value instead of the new value
        undoElement.val(undoValue).trigger('propertychange');

        $("#saveDataFileBtn").removeClass("disabled");
        $("#saveDataFileBtn").removeAttr("disabled style");
        // undoValue = "";
        $("#undoBtn").addClass("disabled").tooltip('hide');
        $("#undoBtn").attr("disabled", "disabled");
        $("#undoBtn").attr("style", "cursor: not-allowed;");
        // $(".data-table-input").on("change");
        // undoElement = null;
    });
    // save the old value to make undo
    saveUndo();


    // here when member click on run modal btn to run the modal
    $("#run-modal-btn").on("click", function (evt) {
        confirmRunModal();
    });

    // data handler wrapper function
    // dataHandlerWrapperTabs();

    // this to reset upload checkbox when closed
    $('#instructionsModal').on('show.bs.modal', function () {
        let instructionInputs = $(".instruction-check-btn");
        // this to reset the check boxes in upload instruction model if closed and not click on check mark
        for (const input of instructionInputs) {
            const inputJQ = $(input);
            inputJQ.prop("checked", false);
        }

        $(this).find('.modal-body').css({
            'max-height': '100%'
        });
    });
    $('#instructionsModal').on('close.bs.modal', function () {
        let instructionInputs = $(".instruction-check-btn");
        // this to reset the check boxes in upload instruction model if closed and not click on check mark
        for (const input of instructionInputs) {
            const inputJQ = $(input);
            inputJQ.prop("checked", false);
        }
        $("#downloadTemplateLink").addClass('disabled not-allowed-cursor');
        $("#downloadTemplateLink").removeAttr('href');

        $(this).find('.modal-body').css({
            'max-height': '100%'
        });
    });

    // this to make pick column window responsive
    $('#columnsDualBoxModal').on('show.bs.modal', function () {
        $(this).find('.modal-body').css({
            'max-height': '100%',
            'max-width': '100%'
        });
    });

    // this to prevent the sessions table dropdown from close when sort the sessions table
    $(document).on('click', '#sessions-table-dropdown .dropdown-menu', function (e) {
        e.stopPropagation();
    });

    // here when member will delete single session from table
    deleteSingleSession();

    $('#wrapper-ul a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        // console.log(e.target) // newly activated tab
        // console.log(e.relatedTarget) // previous active tab
        const activeTab = $(e.target);
        if (activeTab.data('section-name') === 'pick_columns') {
            reselectColumnsFunc();
        }
    });

    // when member click on rename session button in details page
    renameSessionFunc();
    // to run the function of save the new updates of data table cells
    // saveNewUpdatedData();


});  // end of $(document).ready() event

// handler to be called when all Ajax requests have completed.
/*$(function(){
    setTimeout(checkMemberSessionStatus,10000);
});*/
$(document).ajaxError(function () {
    console.error('Triggered ajaxError handler.');
});



