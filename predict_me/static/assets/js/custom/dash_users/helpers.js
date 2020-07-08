function setMemberData(id){
    // this function will be only for view modal of the user

    // this when click on the view button to display the modal of the clicked user
    $('#viewUserModal').on('shown.bs.modal', function (e) {
        $('#viewUserModal').modal('handleUpdate');   //to readjust the modal’s position in case a scrollbar appears
        // do something...
        console.log("Fetch the data for the member");
        $("#userLoadSpinner").fadeOut(function () {
                $("#user-modal-body").show();
            });
    });
    // this to hide and reset any variable data of the api to default, to prevent any save to previous user when click on new one
    $('#viewUserModal').on('hide.bs.modal', function (e) {
        $('#viewUserModal').modal('handleUpdate');   //to readjust the modal’s position in case a scrollbar appears
        // do something...
        console.log("close the modal and reset the data");
        $("#user-modal-body").fadeOut(function () {
                $("#userLoadSpinner").show();

            });
    });
}