$(document).ready(function () {
    setTimeout(function () {
        let sessionLabelCheckRespone = checkSessionLabelRequest();
        $.when(sessionLabelCheckRespone).done(function (data, textStatus, jqXHR) {
            if ((jqXHR.status === 200) && (textStatus === 'success')) {

                if(data === false){
                    setSessionLabel();
                }

            }
        });
    }, 2000);
})