'use strict';

let currentFilterOptionSelected = '';  // this will change dynamically when user change filter option


// this function to build or set the query in url
function setURLQuery(reportFilterOption) {
    let wholeURL = window.location.href;  // this to use with query parameters
    let originURL = new URL(window.location.origin.concat("/dashboard/reports/"));
    let urlObj = new URL(wholeURL);
    let tmpChangedURL = '';
    // this to check if the member select option from the select menu
    if (reportFilterOption.val() !== null) {

        const reportFilterValue = reportFilterOption.val();
        let filterParam = originURL.searchParams;
        // check if there is any previous reports query params
        if (filterParam !== "") {
            filterParam.append('reports', reportFilterValue);
            originURL.search = filterParam.toString();
            // location.replace(originURL);  // this without save in the history
            currentFilterOptionSelected = reportFilterOption.val();
            location.assign(originURL);
        }
    }


}


// function will set the select option value based on the url query parameter
function setFilterOptions() {
    let filterTypeSelect = $("#filterTypeSelect");
    //<option selected disabled value="choose">Choose report section</option>
    let wholeURL = new URL(window.location.href);  // this to use with query parameters
    let wholeSearchParam = wholeURL.searchParams;
    // check if there is value in the url
    if (wholeSearchParam.get("reports") !== null) {
        filterTypeSelect.val(wholeSearchParam.get("reports")).trigger('change');
        // $("#filterTypeSelect").select2(wholeSearchParam.get("reports")).trigger('change');
    }else{
        filterTypeSelect.find("optgroup:first").before('<option selected disabled value="choose">Choose report section</option>');
    }
}

// this function will enable other organization type input if member select other from select menu
function enableOtherOrgType(selectID, otherInputID) {
    let selectIDJq = $(selectID);
    let otherIDJq = $(otherInputID);
    selectIDJq.on("change", function (evt) {
        const selectedValue  = $(this).val();
        if(selectedValue === "Other"){
            // selectIDJq.toggleClass('disabled').attr("disabled", "disabled");
            otherIDJq.toggleClass('disabled not-allowed-cursor').removeAttr('disabled');
        }else{
            otherIDJq.toggleClass('disabled not-allowed-cursor').attr("disabled", "disabled");
        }
    })

}