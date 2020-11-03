"use strict";

let currentFilterOptionSelected = ""; // this will change dynamically when user change filter option
let typingTimer; //timer identifier
let doneTypingInterval = 100; //time in ms, 5 second for example
let displayedColumnsArray = []; // this array will hold any columns checked by label to display it in the report table
let webSiteUrl = window.location.origin;

function swAlert(alertTitle, alertMsg, alertType) {
  swal.fire(`${alertTitle}`, `${alertMsg}`, `${alertType}`);
}

// this function to build or set the query in url
function setURLQuery(reportFilterOption) {
  let wholeURL = window.location.href; // this to use with query parameters
  let originURL = new URL(window.location.origin.concat("/dashboard/reports/"));

  let urlObj = new URL(wholeURL);
  let tmpChangedURL = "";
  // this to check if the member select option from the select menu
  if (reportFilterOption.val() !== null) {
    location.href = originURL.href.concat(reportFilterOption.val());
  }
}

// function will set the select option value based on the url query parameter
function setFilterOptions() {
  let filterTypeSelect = $("#filterTypeSelect");
  //<option selected disabled value="choose">Choose report section</option>
  let wholeURL = new URL(window.location.href); // this to use with query parameters
  let currentReportsVal = wholeURL.href.split("/").slice(-1)[0]; // to get last part or reports url /users, /plans
  // check if there is value in the url

  if (currentReportsVal !== "") {
    $("#no-filter-option").hide();
    filterTypeSelect.val(currentReportsVal).trigger("change");
    // $("#filterTypeSelect").select2(wholeSearchParam.get("reports")).trigger('change');
  } else {
    $("#no-filter-option").show();
    filterTypeSelect
      .find("optgroup:first")
      .before(
        '<option selected disabled value="choose">Choose report section</option>'
      );
  }
}

// this function will enable other organization type input if member select other from select menu
function enableOtherOrgType(selectID, otherInputID) {
  let selectIDJq = $(selectID);
  let otherIDJq = $(otherInputID);
  selectIDJq.on("change", function (evt) {
    const selectedValue = $(this).val();
    if (selectedValue === "Other") {
      // selectIDJq.toggleClass('disabled').attr("disabled", "disabled");
      otherIDJq
        .toggleClass("disabled")
        .removeAttr("disabled")
        .removeClass("not-allowed-cursor");
    } else {
      otherIDJq
        .toggleClass("disabled not-allowed-cursor")
        .attr("disabled", "disabled")
        .val("");
    }
  });
}

// this function will reset the filters fire when click reset filter button
function resetFilters() {
  location.href = window.location.origin.concat("/dashboard/reports/");
}

function testCookies() {
  console.log(document.cookie);
  document.cookie = "filters=one";
  document.cookie = "filters2=two";
  console.log(document.cookie);
}

// this function will watch any change on the filters to save it in cookies
function watchFilters() {
  $(".reports-filter-input").on(
    "keyup change paste propertychange input",
    function (evt) {
      clearTimeout(typingTimer);
      const filterInputField = () => {
        setCookieFilterFunc(this);
      };
      typingTimer = setTimeout(filterInputField, doneTypingInterval);
    }
  );

  $(".reports-filter-input").on("keydown", function () {
    clearTimeout(typingTimer);
  });
}

// this function will set the cookie when input changed
function setCookieFilterFunc(element) {
  const elem = $(element);
  /*$(elem[0].attributes).each(function () {
        console.log(this.nodeName + ' => ' + this.nodeValue);
    });*/
  setFiltersCookie(elem.attr("id"), elem.val());
}

// function to set cookie with its key and value
function setFiltersCookie(key, value) {
  document.cookie = `${key}=${value}`;
}

// function to delete cookie by name or all cookies
function deleteCookie(name, isAll) {
  if (isAll === true) {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++)
      deleteCookie(cookies[i].split("=")[0]);
  } else {
    document.cookie = `${name}= ; expires = Thu, 01 Jan 1970 00:00:00 GMT`;
  }
}

// function to get cookie value by name
function getCookieValue(name) {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(name))
    .split("=")[1];
}

// function will run after page load to check all filters cookies and set the value if exists
function setFilterInputCookieValue() {
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookieName = cookies[i].split("=")[0].trim();
    const jqSelector = `#${cookieName}`;
    // first check if the cookie not the csrftoken (django cookie)
    if (cookieName !== "csrftoken") {
      // check if the input has select2 class
      if ($(jqSelector).hasClass("select2") === true) {
        $(jqSelector).val(getCookieValue(cookieName)).trigger("change");
      } else {
        // set the value of the input
        $(jqSelector).val(getCookieValue(cookieName));
      }
    }
  }
}

// this method will run when member click on reset button in report
function resetButton() {
  $("#members-table-reset-btn").on("click", function (evt) {
    console.error("delete all cookies...");
    deleteCookie("", true);
    $(".reports-filter-input").val("");
  });
}

// this function will return all cookies {name: value}
function getAllCookies() {
  let allCookies = {};
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookieName = cookies[i].split("=")[0].trim();
    const jqSelector = `#${cookieName}`;
    // first check if the cookie not the csrftoken (django cookie)
    if (cookieName !== "csrftoken") {
      allCookies[cookieName] = getCookieValue(cookieName);
    }
  }

  return allCookies;
}

// this function will set the checked label to display the checked columns in the data table
function setReportTableColumns() {
  $(".lbl-reports-filter-display").on("change", function (evt) {
    const elem = $(this);
    const colName = elem.data("col-name");
    // if checked add to the array, otherwise delete it from the array
    if (this.checked === true) {
      displayedColumnsArray.push(colName);
    } else {
      displayedColumnsArray.splice(displayedColumnsArray.indexOf(colName), 1);
    }
    // console.warn(displayedColumnsArray);
  });
}

// report table draw function
function drawReportTable(reportTableData, reportSectionName) {
  //$("#data_handler_table > tbody tr").empty();
  let tableJQObj = null;
  let tableBodyElement = null;
  let tableHeader = null;
  const tableHeaderColumns = reportTableData["table_header"];
  if (reportSectionName === "users") {
    tableJQObj = $("#all-users-report-table");
    tableHeader = $("#all-users-report-table > thead tr:last");
    // tableBodyElement = $("#all-users-report-table > tbody tr:last");
  }

  // first thing is display the table columns header
  let allColumnsName = new Array();
  for (let col of tableHeaderColumns) {
    let colJQ = $(`.lbl-reports-filter-display[data-col-name="${col}"]`);
    allColumnsName.push(colJQ.data("display-name"));
  }
  let allTh = "";
  tableHeader.empty(); // to avoid and duplicate columns name
  for (let colN of allColumnsName) {
    allTh += `
        <th data-header-name="${colN}">
            ${colN}
        </th>

        `;
  }
  tableHeader.append(allTh);
}

// this function will take head name and return the name with small case and underscore instead space
function fixTableHeadName(name){
  return name.replace(" ", "_").toLocaleLowerCase();
}

// report table draw function
function drawGeneratedReportTable(reportData) {
  // console.log(Object.keys(reportData));
  // const reportObj = JSON.parse(reportData['report_data']);
  // console.log(reportData['report_data'])
  let reportObj = reportData['report_data'];
  // console.log(reportData);
  //$("#data_handler_table > tbody tr").empty();
  let tableTd = "";
  let allTableRow = "";
  let tmpTableTd = "";
  let tmpTableTr = "";
  let tableJQObj = null;
  let tableBodyElement = null;
  let tableHeader = null;
  // const tableHeaderColumns = reportTableData['table_header'];
  if (reportData["report_section_name"] === "users") {
    tableJQObj = $("#all-users-report-table");
    tableHeader = $("#all-users-report-table > thead tr:last");
    tableBodyElement = $("#all-users-report-table > tbody");
  }else if (reportData['report_section_name'] === 'data-usage'){
    //data-usage-report-table
    tableHeader = $("#data-usage-report-table > thead tr:last");
    tableBodyElement = $("#data-usage-report-table > tbody");
  }
  tableBodyElement.empty();
  // for(const [key, value] of Object.entries(reportData['report_data'])){
  //   console.log(key, value)
  // }
  // console.log(reportData['report_data'])
  for (let rowKey in reportObj) {
    const newReportData = reportData["report_data"][rowKey]['member_data'];
    const subscriptionData = reportData['report_data'][rowKey]['subscription_data'];
    // console.log(newReportData['member_data']);
    // console.log(Object.keys(subscriptionData));
    for (let name of reportData['table_header']){
      // console.log(fixTableHeadName(name))
      // check if the cancelled_users or active_user is here
      let headName = fixTableHeadName(name);
      if((headName === "cancelled_users") || (headName === 'active_users')){
        headName = "status"
      }
      // check for plan to call the subscription
      if((headName === 'plan') && (Object.keys(subscriptionData).length > 0)){
        // console.log(newReportData[headName])
        tmpTableTd += `
          <td>
            ${subscriptionData['stripe_plan_id']}
          </td>
        `;
      }else{
        // console.log(newReportData[headName])
        tmpTableTd += `
          <td>
            ${newReportData[headName]}
          </td>
        `;
      }

    }
    tableBodyElement.append(`
      <tr>
        ${tmpTableTd}
      </tr>
      `);
    tmpTableTr = "";
    tmpTableTd = "";

  }

  // console.log(tableRow)
  // tableBodyElement.append(tableRow);
  // console.log(reportData['report_data']);
}

// this function will draw the table header
function drawReportTableHeader(columns) {
  let reportSection = window.location.href.split("/");
  reportSection = reportSection.pop();
  // console.log(reportSection)
  // all-users-report-table, data-usage-report-table, profit-share-report-table, revenue-report-table
  let table;
  if (reportSection === "users") {
    table = $("#all-users-report-table > thead");


  }else if (reportSection === "data-usage"){
    table = $("#data-usage-report-table > thead");
    
  }

  table.empty();
  let tableHeader = "<tr>";
  for (let col of columns) {
    tableHeader += `
          <th>${col}</th>
      `;
  }
  tableHeader += "</thead>";
  table.append(tableHeader);
}
