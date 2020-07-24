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
    enableOtherOrgType("#gen-filter-users-org-type", '#gen-filter-other-org-type');

    // reset function btn
    const resetReportsFilterBtn = $("#resetReportsFilterBtn");
    resetReportsFilterBtn.on('click', resetFilters);

});

