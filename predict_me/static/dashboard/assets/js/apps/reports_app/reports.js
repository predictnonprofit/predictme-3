'use strict';
$(document).ready(function () {
    // this to set the filter select option
    setFilterOptions();
    // this when filter button clicked
    let reportsFilterBtn = $("#reportsFilterBtn");
    reportsFilterBtn.on('click', function (evt) {
        let filterTypeSelect = $("#filterTypeSelect");
        setURLQuery(filterTypeSelect);
    });

    // enable other org type input
    enableOtherOrgType("#reports-users-org-type", '#reports-other-org-type');

});

