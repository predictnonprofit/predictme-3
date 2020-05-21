$(function () {
    // this to delay the donner files but show the spinner first
    var donerFilesSpinner = $('#donerFilesSpinner');
    var donerFilesTree = $('#donerFilesTree');

    // This event is fired when the modal has been made visible to the user
    $('#donerFilesModal').on('shown.bs.modal', function (e) {
        //$('#donerFilesModal').modal('handleUpdate'); // to make Dynamic heights
        setTimeout(function () {
            // this will be ajax request to grab users files

            // hide the spinner
            //donnerFilesSpinner.addClass("d-none");
            donerFilesSpinner.fadeOut(1000, function () {
                donerFilesTree.fadeIn();
            });

            // show the tree view
            //donerFilesTree.removeClass("d-none");
            //donerFilesTree.delay(5000).fadeIn().removeClass("d-none");


        }, 3000);
    });


    // enable upload btn by check agree terms and conditions
    const agreeDataHandlerCheckBox = $("#agreeDataHandlerCheckBox");
    const dataUploadBtn = $("#dataUploadBtn");
    agreeDataHandlerCheckBox.change(function () {

        if (this.checked) {
            dataUploadBtn.removeAttr("disabled");
            dataUploadBtn.removeClass("my-disabled-btn");
        } else {
            dataUploadBtn.attr("disabled", "disabled");
        }
    });

    // this for disable the upload button when user not accept the terms from the modal dialog
    let closeUploadInstBtn = $('#closeUploadInstBtn');
    let acceptUploadInstBtn = $("#acceptUploadInstBtn");

    // accept upload instruction terms button
    acceptUploadInstBtn.click(function (e) {
        dataUploadBtn.removeAttr("disabled");
        agreeDataHandlerCheckBox.prop("checked", true);
    });

    // not accept upload instruction terms button
    closeUploadInstBtn.click(function (e) {
        // check if agree upload terms checkbox checked or not
        if (agreeDataHandlerCheckBox.prop("checked") === false || agreeDataHandlerCheckBox.prop("checked") === true) {
            agreeDataHandlerCheckBox.prop("checked", false);
            dataUploadBtn.prop("disabled", true);
        }

    });


    // this for the next button when user click next in pay or upgrade subscription dialog
    // all forms sections vars
    const askPayUpgradeSection = $("#askPayUpgradeSection");
    const payExtraRecordsSection = $("#payExtraRecordsSection");
    const upgradeSubscriptionSection = $("#upgradeSubscriptionSection");
    const closeUpgradeModalBtn = $("#closeUpgradeModalBtn");
    var purchaseUpgradeExtraBtn = $(".purchaseUpgradeExtraBtn");
    var currentShownSection = "";
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
            currentShownSection = payExtraRecordsSection;
            askPayUpgradeSection.fadeOut(300, function () {
                payExtraRecordsSection.fadeIn();
            });
            backBtn.removeAttr("disabled");
            $(this).attr("disabled", "disabled");
            $(this).addClass("disabled my-disabled-btn");


        } else if (actionRadioBtn === "upgrade") {
            currentShownSection = upgradeSubscriptionSection;
            askPayUpgradeSection.fadeOut(300, function () {
                upgradeSubscriptionSection.fadeIn();
            });
            backBtn.removeAttr("disabled");
            $(this).attr("disabled", "disabled");
            $(this).addClass("disabled my-disabled-btn");

        } else {

            swal.fire("Oops...", "You have to select one of the two options!", "error");

        }

    });

    // this for the back button when user click back in pay or upgrade subscription dialog
    backBtn.click(function (e) {
        // alert($('body').hasClass('modal-open'));
        currentShownSection.fadeOut(300, function () {
            askPayUpgradeSection.fadeIn();
        });
        $(this).attr("disabled", "disabled");
        nextBtn.removeAttr("disabled");
        nextBtn.toggleClass("disabled my-disabled-btn");
    });

    // when member want to close the dialog
    closeUpgradeModalBtn.click(function () {
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
                /*Swal.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )*/
                $("#extraRecordsModel").modal("hide");
            }
        });
    });


    // upgrade plan button
    // this to get the selected plan to upgrade
    purchaseUpgradeExtraBtn.click(function (e) {
        let actionLabel = $(this).data("action");
        const upgradePlanBtn = $('input[name=upgrade_plane]:checked').val();
        if (actionLabel === "upgrade") {
            if (upgradePlanBtn === "" || upgradePlanBtn === undefined) {
                swal.fire("Error", "You have to select plan!", "error");
            } else {
                swal.fire("Good", `You select ${upgradePlanBtn}`, "success");
                $(this).attr("disabled", "disabled");
                $(this).html("<div class='kt-spinner kt-spinner--lg kt-spinner--dark' style='width: 2rem; height: 1.3rem; left: 32px;'></div>");

            }

        } else if (actionLabel === "pay") {
            swal.fire("👍", `Purchased done`, "success");
        }

    });


    // upload data file functionality
    const uploadDataFileBtn = $("#uploadDataFileBtn");
    const uploadDataFileForm = $("#uploadDataFileForm");
    const donerFileInput = $("#donerFile");
    uploadDataFileForm.submit(function (e) {
        e.preventDefault();
        const webSiteUrl = window.location.origin;
        const webSiteMemberUrl = window.location;
        if (donerFileInput.val()) {
            var timerInterval;
            $form = $(this);
            var formData = new FormData($("#uploadDataFileForm")[0]);
            const fileName = donerFileInput.val().split(/(\\|\/)/g).pop();  // get the file name to parse it in url
            // ajax request to data handler init
            $.ajax({
                method: "POST",
                cache: false,
                processData: false,
                contentType: false,
                timeout: 3000,
                url: `${webSiteUrl}/dashboard/data/upload/${fileName}`,
                // url: `${webSiteUrl}/dashboard/data/upload`,
                data: formData,
                beforeSend: function (xhr, settings) {
                    let timerInterval;
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    swal.fire({
                        title: "Uploading...",
                        text: "Checking your file, Please wait...",
                        showConfirmButton: false,
                        allowOutsideClick: false,
                        timer: 2000,
                        timerProgressBar: true,
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
                            $('#columnsDualBoxModal').modal('handleUpdate');
                            $('#columnsDualBoxModal').modal('show');
                        }
                    });
                },
                success: function (data, textStatus, jqXHR) {
                    let timerInterval;
                    swal.fire({
                        title: "Extracting...",
                        text: "Extract the columns from your data file, Please wait...",
                        showConfirmButton: false,
                        allowOutsideClick: false,
                        timer: 3000,
                        timerProgressBar: true,
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
                            // $('#columnsDualBoxModal').modal('handleUpdate');
                            // $('#columnsDualBoxModal').modal('show');
                            // get the columns select element
                            const dataFileColumnsSelect = $("#data_file_available_columns");
                            if (textStatus == "success") {
                                // alert(jqXHR.status);
                                // alert(jqXHR.responseText);
                                alert(data);
                                $('#columnsDualBoxModal').modal('handleUpdate');
                                $('#columnsDualBoxModal').modal('show');
                                // swAlert("Success", `${jqXHR.responseText}`, "success");

                            } else if (textStatus == "error") {
                                swAlert("Error", "There is error while extracting!!", "error");
                            } else {
                                swAlert("Error", "Unknown error while extracting!!", "error");
                            }
                        }
                    });


                },
                error: function (error) {
                    //called when there is an error
                    swAlert("Error", error.message, "error");
                    //console.log(e.message);
                },
                /*complete: function (jqXHR, textStatus) {

                    if(textStatus == "success"){
                        $('#columnsDualBoxModal').modal('handleUpdate');
                        $('#columnsDualBoxModal').modal('show');
                        // swAlert("Success", `${jqXHR.responseText}`, "success");

                    }else if(textStatus == "error"){
                        swAlert("Error", "There is error while extracting!!", "error");
                    }else{
                        swAlert("Error", "Unknown error while extracting!!", "error");
                    }
                },*/
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

        } else {
            swal.fire("Error", "You have to select a file!", "error");
        }
    });
    /*uploadDataFileBtn.click(function () {

    });
*/

    // here the columns dual box
    // Class definition
    var pickedColumns = [];  // this will hold all columns that user selected
    var KTDualListbox = function () {
        // Private functions
        var initDualListbox = function () {
            // Dual Listbox
            var listBoxes = $(".dual-listbox");

            listBoxes.each(function () {
                var $this = $(this);
                // get titles
                var availableTitle = ($this.attr("data-available-title") != null) ? $this.attr("data-available-title") : "Available columns";
                var selectedTitle = ($this.attr("data-selected-title") != null) ? $this.attr("data-selected-title") : "Picked columns";

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
                        //console.log(pickedColumns);
                    },
                    removeEvent: function (value) {
                        let arrayIdx = pickedColumns.indexOf(value);
                        if (arrayIdx > -1) {
                            pickedColumns.splice(arrayIdx, 1);
                        }
                        //console.log(pickedColumns);
                    },
                    availableTitle: availableTitle,
                    selectedTitle: selectedTitle,
                    addButtonText: addLabel,
                    removeButtonText: removeLabel,
                    addAllButtonText: addAllLabel,
                    removeAllButtonText: removeAllLabel,
                    options: options,
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
    KTDualListbox.init();

    // process button, which will send ajax request with the selected columns
    const processPickedColumnsBtn = $("#processPickedColumnsBtn");
    processPickedColumnsBtn.click(function (e) {
        let selectedColumns = JSON.stringify(pickedColumns);
        // let selectedColumns = pickedColumns;
        // let selectedColumns = pickedColumns;
        const webSiteUrl = window.location.origin;
        const webSiteMemberUrl = window.location;

        // ajax request to data handler init
        $.ajax({
            method: "POST",
            cache: false,
            url: webSiteUrl + "/dashboard/data/init",
            dataType: "json",
            data: {"columns": selectedColumns},
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            },
            success: function (data) {
                alert(data);
                // if (data == "OK") {
                //     alert("Your Data has been updated");
                //     location.reload();
                // }
            },
            error: function (error) {
                //called when there is an error
                swAlert("Error", error.message, "error");
                //console.log(e.message);
            }
        });
    });

});  // end of $(function)


function swAlert(alertTitle, alertMsg, alertType) {
    swal.fire(`${alertTitle}`, `${alertMsg}`, `${alertType}`);
}