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
                }
            })
        }
    }

}