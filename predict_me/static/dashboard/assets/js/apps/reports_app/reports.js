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



});

