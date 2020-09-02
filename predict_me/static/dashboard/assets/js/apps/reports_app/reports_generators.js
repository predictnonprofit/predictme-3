'use strict';
const reportsSpinner = $("#reportsLoaderSpinner");
var allCookies = getAllCookies();

// revenue report generator
function revenueGenerator(displayedColumns){
    // first fetch the wrapper of the report section
    const parentWrapper = $("#revenue-reports-wrapper");
    const reportTable = parentWrapper.find('table');
    reportTable.hide()
    reportsSpinner.show();
    setTimeout(function (){
        reportsSpinner.hide();
        reportTable.show();
    }, 2000);
    const fetchReportResponse = fetchReportRequest('revenue', displayedColumns, allCookies);
    $.when(fetchReportResponse).done(function (data, textStatus, jqXHR){
        if((textStatus === 'success') && (jqXHR.status === 200)){
            console.log(data);
        }
    });

}


// data-usage report generator
function dataUsageGenerator(){
    console.log('Data usage report generator function');
}

// extra-records report generator
function extraRecordsGenerator(){
    console.log('Extra Records report generator function');
}

// profit-share report generator
function profitShareGenerator(){
    console.log('Profit Share report generator function');
}