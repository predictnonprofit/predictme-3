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
        if(actionLabel === "upgrade"){
            if (upgradePlanBtn === "" || upgradePlanBtn === undefined) {
            swal.fire("Error", "You have to select plan!", "error");
        } else {
            swal.fire("Good", `You select ${upgradePlanBtn}`, "success");
            $(this).attr("disabled", "disabled");
            $(this).html("<div class='kt-spinner kt-spinner--lg kt-spinner--dark' style='width: 2rem; height: 1.3rem; left: 32px;'></div>");

        }

        }else if(actionLabel === "pay"){
            swal.fire("👍", `Purchased done`, "success");
        }

    });

});  // end of $(function)