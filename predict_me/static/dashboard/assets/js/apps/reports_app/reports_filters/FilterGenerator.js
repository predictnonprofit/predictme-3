class InputGenerator {
  constructor(inputDataID, inputID, inputName, inputType, placeholder, reportSectionName) {
    this.inputDataID = inputDataID;
    this.inputID = inputID;
    this.inputName = inputName;
    this.inputType = inputType;
    this.placeholder = placeholder;
    this.reportSectionName = reportSectionName;
    this.allCities = fetchCities();
    // console.log(inputDataID, inputID, inputName, inputType, placeholder, reportSectionName)
  }
  cityInputGenerator() {
    let input;
    let cityOptions = "";
    let parent = this;
    // console.log(parent)
    $.when(this.allCities).done(function(data, textStatus, jqXHR) {
      const allCities = data['all_cities'];

      for (let city of allCities) {
        cityOptions += `
            <option value="${city}">${city}</option>
          `;
      }
      console.log(parent.reportSectionName)
      // this method will return only text input
      input = `
        <div class="filter-options-wrapper" data-filter-name="${parent.inputID}">
        <div class="form-group m-2">
            <label>${parent.placeholder}</label>
           <select multiple data-report-section-name="${parent.reportSectionName}" name="${parent.inputName}" class="form-control filter-input gen-filter-input" id="${parent.inputID}" placeholder="${parent.placeholder}" data-filter-name="${parent.placeholder}" data-has-options="true">
              ${cityOptions}
           </select>
       </div>
       <div class="btn-group" role="group" aria-label="Basic example">
           <button data-gen-filter-item-id="${parent.inputDataID}" type="button" class="btn btn-light-danger deSelectFilterBtn" data-toggle="tooltip" title="Deselect the filter" font-weight-bold" data-filter-input-id="${parent.inputID}">
           <i class="icon-xl la la-long-arrow-left"></i>
           </button>

           <button data-gen-filter-item-id="${parent.inputDataID}" data-toggle="tooltip" title="Select the filter" type="button" class="btn btn-light-primary font-weight-bold selectFilterBtn" data-filter-input-id="${parent.inputID}">
                   <i class="icon-xl la la-long-arrow-right"></i>
               </button>
       </div>
        </div>

    `;

    $("#filterOptionsBlock").html(input);
  });
    // console.log(input)
    // return input;


  }
  textInputGenerator() {
    // this method will return only text input
    const input = `
        <div class="filter-options-wrapper" data-filter-name="${this.inputID}">
        <div class="form-group m-2">
            <label>${this.placeholder}</label>
           <input type="${this.inputType}" data-report-section-name="${this.reportSectionName}" name="${this.inputName}" class="form-control filter-input gen-filter-input" id="${this.inputID}" placeholder="${this.placeholder}" data-filter-name="${this.placeholder}" data-has-options="true"/>
       </div>
       <div class="btn-group" role="group" aria-label="Basic example">
           <button data-gen-filter-item-id="${this.inputDataID}" type="button" class="btn btn-light-danger deSelectFilterBtn" data-toggle="tooltip" title="Deselect the filter" font-weight-bold" data-filter-input-id="${this.inputID}">
           <i class="icon-xl la la-long-arrow-left"></i>
           </button>

           <button data-gen-filter-item-id="${this.inputDataID}" data-toggle="tooltip" title="Select the filter" type="button" class="btn btn-light-primary font-weight-bold selectFilterBtn" data-filter-input-id="${this.inputID}">
                   <i class="icon-xl la la-long-arrow-right"></i>
               </button>
       </div>
        </div>

    `;

    return input;
  }

  countrySelectGenerator() {
    const input = allCountrySelect(this.inputDataID, this.inputID);
    return input;
  }

  registerDateInputGenerator() {
    const input = `
        <div class="filter-options-wrapper" data-filter-name="register-date">
        <div class="form-group">
            <label>Register Date:</label>
                    <div class="input-daterange input-group">
                        <input data-input-id='li_${this.inputID}' data-input-full-name="${this.placeholder}" type="text" class="form-control filter-input gen-filter-input datePickerInputs reports-filter-input" name="register-filter-start"
                            id="register-filter-start" data-common-name="${this.inputName}" data-filter-name="${this.inputName}_start_date" data-has-options="true">
                        <div class="input-group-append">
                                    <span class="input-group-text">
                                        <i class="la la-ellipsis-h"></i>
                                    </span>
                        </div>
                        <input data-input-id='li_${this.inputID}' data-input-full-name="${this.placeholder}" data-common-name="${this.inputName}" type="text" class="form-control filter-input datePickerInputs reports-filter-input" data-report-section-name="${this.reportSectionName}" name="register-filter-end" data-filter-name="${this.inputName}_end_date" data-has-options="true"
                            id="register-filter-end">
                    </div>
        </div>

        <div class="btn-group" role="group" aria-label="Basic example">
            <button data-gen-filter-item-id="${this.inputDataID}" type="button" class="btn btn-light-danger deSelectFilterBtn" data-toggle="tooltip" title="Deselect the filter" font-weight-bold" data-filter-input-id="${this.inputID}">
            <i class="icon-xl la la-long-arrow-left"></i>
            </button>

            <button data-gen-filter-item-id="${this.inputDataID}" data-toggle="tooltip" title="Select the filter" type="button" class="btn btn-light-primary font-weight-bold selectFilterBtn" data-filter-input-id="${this.inputID}">
                    <i class="icon-xl la la-long-arrow-right"></i>
                </button>
        </div>

        </div>
        `;
    $(document.getElementsByClassName('datePickerInputs')[0]).ready(function() {
      $('.datePickerInputs').datepicker({
        autoclose: true,
        todayHighlight: true,
        format: {

          toDisplay: function(date, format, language) {
            const d = new Date(date);
            d.setDate(d.getDate());
            return d.toISOString().slice(0, 10);
          },
          toValue: function(date, format, language) {
            const d = new Date(date);
            d.setDate(d.getDate());
            return new Date(d);
          }
        }
      });
    });

    return input;
  }

  dateInputsGenerator() {
    const input = `
        <div class="filter-options-wrapper" data-filter-name="${this.inputName}_date">
        <div class="form-group">
            <label>${this.placeholder}:</label>
                    <div class="input-daterange input-group">
                        <input data-input-id='li_${this.inputID}' data-common-name="${this.inputName}" type="text" class="form-control filter-input gen-filter-input datePickerInputs reports-filter-input" name="pay-filter-start" data-input-full-name="${this.placeholder}"
                            id="${this.inputName}_start_date" data-filter-name="${this.inputName}_start_date" data-has-options="true">
                        <div class="input-group-append">
                                    <span class="input-group-text">
                                        <i class="la la-ellipsis-h"></i>
                                    </span>
                        </div>
                        <input data-input-id='li_${this.inputID}' data-common-name="${this.inputName}" data-input-full-name="${this.placeholder}" type="text" class="form-control filter-input datePickerInputs reports-filter-input" data-report-section-name="${this.reportSectionName}" name="${this.inputName}_end_date" data-filter-name="${this.inputName}_end_date" data-has-options="true"
                            id="${this.inputName}_end_date">
                    </div>
        </div>

        <div class="btn-group" role="group" aria-label="Basic example">
            <button data-gen-filter-item-id="${this.inputDataID}" type="button" class="btn btn-light-danger deSelectFilterBtn" data-toggle="tooltip" title="Deselect the filter" font-weight-bold" data-filter-input-id="${this.inputID}">
            <i class="icon-xl la la-long-arrow-left"></i>
            </button>

            <button data-gen-filter-item-id="${this.inputDataID}" data-toggle="tooltip" title="Select the filter" type="button" class="btn btn-light-primary font-weight-bold selectFilterBtn" data-filter-input-id="${this.inputID}">
                    <i class="icon-xl la la-long-arrow-right"></i>
                </button>
        </div>

        </div>
        `;
    $(document.getElementsByClassName('datePickerInputs')[0]).ready(function() {
      $('.datePickerInputs').datepicker({
        autoclose: true,
        todayHighlight: true,
      });
    });

    return input;
  }

  orgTypeInputGenerator() {
    const input = `
        <div class="filter-options-wrapper" data-filter-name="org-type">
        <div class="form-group m-2">
            <label>${this.placeholder}</label>
            <select data-input-id='li_${this.inputID}' data-has-options="true" multiple data-report-section-name="${this.reportSectionName}" data-filter-name="${this.placeholder}" name="gen_filter_org_type" id="gen_filter_org_type" class="select-filter filter-input form-control gen-filter-input">
                <option selected>All</option>
                <option value="Higher Education">Higher Education</option>
                <option value="Arts and Culture">Arts and Culture</option>
                <option value="Other Education">Other Education</option>
                <option value="Health related">Health related</option>
                <option value="Hospitals and Primary Care">Hospitals and Primary Care
                </option>
                <option value="Human and Social Services">Human and Social Services
                </option>
                <option value="Environment">Environment</option>
                <option value="Animal">Animal</option>
                <option value="International">International</option>
                <option value="Religion">Religion related</option>
                <option value="Other">
                    <b>Other (Enter it manually)</b>
                </option>
            </select>
       </div>

       <div class="form-group mt-8">
            <label>Other ${this.placeholder}</label>
           <input data-has-options="true" data-report-section-name="${this.reportSectionName}" type="text" name="gen_filter_other_org_type" class="form-control gen-filter-input" disabled id="gen_filter_other_org_type" placeholder="Other Organization Type" />
       </div>

       <div class="btn-group" role="group" aria-label="Basic example">
           <button data-gen-filter-item-id="${this.inputDataID}" type="button" class="btn btn-light-danger deSelectFilterBtn" data-toggle="tooltip" title="Deselect the filter" font-weight-bold" data-filter-input-id="${this.inputID}">
           <i class="icon-xl la la-long-arrow-left"></i>
           </button>

           <button data-gen-filter-item-id="${this.inputDataID}" data-toggle="tooltip" title="Select the filter" type="button" class="btn btn-light-primary font-weight-bold selectFilterBtn" data-filter-input-id="${this.inputID}">
                   <i class="icon-xl la la-long-arrow-right"></i>
               </button>
       </div>

        </div>
       `;

    return input;
  }

  annoualInputGenerator() {
    const input = `
        <div class="filter-options-wrapper" data-filter-name="annoual-revenue">
        <div class="form-group mt-8">
        <label>Other ${this.placeholder}</label>
        <select data-input-id='li_${this.inputID}' data-has-options="true" multiple data-report-section-name="${this.reportSectionName}" data-filter-name="${this.placeholder}" class="form-control filter-input select-filter form-control-solid gen-filter-input" id="annualRevenue" name="annual_revenue">
             <option selected value="All">All</option>
             <option value="$5,000 - $50,000">$5,000 - $50,000</option>
             <option value="$50,000 - $100,000">$50,000 - $100,000</option>
             <option value="$100,000 - $250,000">$100,000 - $250,000</option>
             <option value="$250,000 - $500,000">$250,000 - $500,000</option>
             <option value="$500,000 - $1 million">$500,000 - $1 million</option>
             <option value="$1 million - $5 million">$1 million - $5 million</option>
             <option value="$5 million - $10 million">$5 million - $10 million</option>
             <option value="$10 million or more">$10 million or more</option>
         </select>
   </div>
   <div class="btn-group" role="group" aria-label="Basic example">
       <button data-gen-filter-item-id="${this.inputDataID}" type="button" class="btn btn-light-danger deSelectFilterBtn" data-toggle="tooltip" title="Deselect the filter" font-weight-bold" data-filter-input-id="${this.inputID}">
       <i class="icon-xl la la-long-arrow-left"></i>
       </button>

       <button data-gen-filter-item-id="${this.inputDataID}" data-toggle="tooltip" title="Select the filter" type="button" class="btn btn-light-primary font-weight-bold selectFilterBtn" data-filter-input-id="${this.inputID}">
               <i class="icon-xl la la-long-arrow-right"></i>
           </button>
   </div>
        </div>
       `;

    return input;
  }

  planSelectGenerator() {
    const input = `
        <div class="filter-options-wrapper" data-filter-name="annoual-revenue">
        <div class="form-group mt-8">
        <label>Other ${this.placeholder}</label>
        <select data-input-id='li_${this.inputID}' data-has-options="true" multiple data-report-section-name="${this.reportSectionName}" data-filter-name="${this.placeholder}" class="form-control filter-input select-filter form-control-solid gen-filter-input" data-has-options="true" id="plan" name="plan">
             <option selected value="All">All</option>
             <option value="starter">Starter</option>
             <option value="professional">Professional</option>
             <option value="expert">Expert</option>
         </select>
   </div>
   <div class="btn-group" role="group" aria-label="Basic example">
       <button data-gen-filter-item-id="${this.inputDataID}" type="button" class="btn btn-light-danger deSelectFilterBtn" data-toggle="tooltip" title="Deselect the filter" font-weight-bold" data-filter-input-id="${this.inputID}">
       <i class="icon-xl la la-long-arrow-left"></i>
       </button>

       <button data-gen-filter-item-id="${this.inputDataID}" data-toggle="tooltip" title="Select the filter" type="button" class="btn btn-light-primary font-weight-bold selectFilterBtn" data-filter-input-id="${this.inputID}">
               <i class="icon-xl la la-long-arrow-right"></i>
           </button>
   </div>
        </div>
       `;

    return input;
  }
}
