from faker import Faker
from predict_me.my_logger import log_exception
from termcolor import cprint
from membership.models import (Subscription, UserMembership, Membership)
from data_handler.models import (DataFile, DataHandlerSession)
from users.models import Member
from django.db.models import Q
import decimal
import json
from django.core.exceptions import ObjectDoesNotExist

# this dict will hold all terms used in the web page and what match in the DB model
DB_TERMS = {
    "gen-filter-state": 'state', 'gen-filter-users-country': 'country',
    'gen-filter-users-city': 'city', 'users-filter-sub-plan': 'sub_plan',
    'gen-filter-total-staff': 'total_staff', "gen-filter-number-volunteer": "num_of_volunteer",
    "annualRevenue": 'annual_revenue', "gen-filter-number-of-board-member": "num_of_board_members",
    "gen-filter-users-status": 'status', "gen-filter-users-org-type": "org_type",
    'gen-filter-other-org-type': 'other_org_type', 'gen-filter-start': 'start_date',
    'gen-filter-end': 'end_date'
}
USERS_STATUS = ("Active", 'Pending', 'Cancel')
SUB_PLANS = ("Starter", 'Professional', 'Expert')

GENERIC_TERMS = []  # this will hold all generic filters name

ALL_MEMBERSHIP = {}  # this will hold all memberships with its own slug

all_membership_obj = Membership.objects.all()
for m in all_membership_obj:
    ALL_MEMBERSHIP[m.slug] = m.id


# this function will return filter name with lower and replaced space with underscore
def report_name(name: str):
    if type(name) is str:
        return name.lower().replace(" ", "_")
    else:
        return name



# this function will return the field name with capitalize case
def capitalize_report_name(name: str):
    return name.replace("_", " ").title()


class ReportFilterGenerator:

    @staticmethod
    def get_generic_filters():
        return [
            {"filter_name": "First Name", "report_section": "users", "input_name": report_name("First Name"),
             "has_options": False, "report_type": "Generic Filter"},
            {"filter_name": "Last Name", "report_section": "users", "input_name": report_name("Last Name"),
             "has_options": False, "report_type": "Generic Filter"},
            {"filter_name": "Email", "report_section": "users", "input_name": report_name("Email"),
             "has_options": False, "report_type": "Generic Filter"},
            {"filter_name": "Plan", "report_section": "users",
             "input_name": report_name("Plan"), "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "Country", "report_section": "users", "input_name": report_name("Country"),
             "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "City", "report_section": "users", "input_name": report_name("City"), "has_options": True,
             "report_type": "Generic Filter"},
            {"filter_name": "Organization Type", "report_section": "users",
             "input_name": report_name("Organization Type"), "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "Organization Name", "report_section": "users",
             "input_name": report_name("Organization Name"), "has_options": False, "report_type": "Generic Filter"},
            {"filter_name": "Register Date", "report_section": "users", "input_name": report_name("Register Date"),
             "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "Job Title", "report_section": "users", "input_name": report_name("Job Title"),
             "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "Annual Revenue", "report_section": "users", "input_name": report_name("Annual Revenue"),
             "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "Total Staff", "report_section": "users", "input_name": report_name("Total Staff"),
             "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "Number of Volunteer", "report_section": "users",
             "input_name": report_name("Number of Volunteer"), "has_options": True, "report_type": "Generic Filter"},
            {"filter_name": "Number of Board Members", "report_section": "users",
             "input_name": report_name("Number of Board Members"), "has_options": True, "report_type": "Generic Filter"}

        ]

    @staticmethod
    def get_custom_filters(report_section_name):
        if report_section_name == "users":
            return [
                {"filter_name": "Active Users", "report_section": "users", "input_name": report_name("Active Users"),
                 "has_options": False, "report_type": "Users Filter"},
                {"filter_name": "Cancelled Users", "report_section": "users",
                 "input_name": report_name("Cancelled Users"),
                 "has_options": False, "report_type": "Users Filter"},
                {"filter_name": "Days Left", "report_section": "users", "input_name": report_name("Days Left"),
                 "has_options": False, "report_type": "Users Filter"},
            ]
        elif report_section_name == "data_usage":
            return [
                {"filter_name": "Last Run", "report_section": "data_usage", "input_name": report_name("Last Run"),
                 "has_options": False, "report_type": "Data Usage Filter"},
                {"filter_name": "Usage", "report_section": "data_usage", "input_name": report_name("Usage"),
                 "has_options": False, "report_type": "Data Usage Filter"},

            ]
        elif report_section_name == "revenue":
            return [
                {"filter_name": "Start Offer Date", "report_section": "revenue",
                 "input_name": report_name("Start Offer Date"),
                 "has_options": True, "report_type": "Revenue Filter"},
                {"filter_name": "Next Revenue Date", "report_section": "revenue",
                 "input_name": report_name("Next Revenue Date"),
                 "has_options": False, "report_type": "Revenue Filter"},

            ]


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


class ReportGenerator:
    def __init__(self, section_name, displayed_columns, filter_cookies):
        self.section_name = section_name
        if not filter_cookies:
            self.report_filters = "Empty filters!!"
        else:
            self.report_filters = filter_cookies

        if not displayed_columns:
            self.report_filters = "NO columns to display!!"
        else:
            self.displayed_columns = displayed_columns

    def __str__(self):
        return f"Reports Section: {self.section_name}, Displayed Columns: {self.displayed_columns} --> Report Filter: {self.report_filters}"

    def get_columns_data(self):
        """
            this method will return every column with its data based on the report section name
            @return {"column_name": ""}
        """
        pass

    def get_displayed_columns(self):
        """
            this method will return the displayed columns only
            @return list of columns
        """
        return self.displayed_columns

    def get_rows_file(self):
        """
            this method will return the rows of displayed columns or based on the reports filters
            @return list of dict
        """
        faker_obj = Faker()
        faker_holder = []
        for _ in range(1, 20):
            faker_holder.append({
                "id": _,
                "name": faker_obj.name(),
                "email": faker_obj.email(),
                "reg_date": faker_obj.date_this_year(),
                "status": faker_obj.word(USERS_STATUS),
                "sub_plan": faker_obj.word(SUB_PLANS),
            })
        return faker_holder

    @staticmethod
    def generate_reports(filters_array):
        print(filters_array)

    @staticmethod
    def generate_reports_table_header(filters_array):
        all_columns = []
        for col in filters_array:
            all_columns.append(col['filter_name'])

        return all_columns

    @staticmethod
    def generate_report(report_section_name, filter_list, report_table_header, user_id):
        # cprint(filter_list, "blue")
        # cprint(report_table_header, 'red')
        filter_keys = {}
        reports_holder = ''  # this to hold every report in single loop
        all_filters = {}
        # cprint(type(filter_list), 'yellow')
        for r_filter in filter_list:
            # print(r_filter)
            filter_keys[r_filter['filter_name']] = r_filter['filter_value']

        # cprint(report_table_header, 'red')
        # cprint(report_section_name, 'red')
        reports_holder = ReportGenerator.report_maker(report_section_name, filter_list, report_table_header)

        return reports_holder

    @staticmethod
    def report_maker(report_section_name: str, filter_list: list, report_table_header):
        filter_map = dict()
        report_data = {}  # this dict will hold every reports information
        all_members = Member.objects.all()

        filter_keys = {}
        # cprint(filter_list, 'yellow')
        for r_filter in filter_list:
            # print(r_filter)
            # cprint(report_name(r_filter['filter_name']))
            if (report_name(r_filter['filter_name']) == "register_date") or (
                    report_name(r_filter['filter_name']) == "annual_revenue"):
                filter_keys[report_name(r_filter['filter_name'])] = r_filter['filter_value']
                # cprint("_" in r_filter['filter_value'], 'red')
                # cprint(report_name(r_filter['filter_value']), 'green')
            else:
                filter_keys[report_name(r_filter['filter_name'])] = report_name(r_filter['filter_value'])

            filter_keys["report_section_name"] = report_name(r_filter['report_section_name'])

        # first check the section of the report to call the convenient method for it
        if report_section_name == "users":
            report_data = ReportGenerator.get_all_user_query(filter_keys, report_table_header, 'users')
        elif report_section_name == 'data-usage':
            report_data = ReportGenerator.get_data_usage_query(filter_keys, report_table_header, 'data-usage')

        return report_data

    @staticmethod
    def get_all_user_query(filter_dict: dict, table_header: list, report_section_name: str):
        # section_name = filter_dict['report_section_name']
        filter_d = filter_dict
        del filter_d['report_section_name']  # this to delete the section name to get only the field with its values
        # cprint(filter_d, 'green')
        lookups = None
        # lookups = lookups | Q(body__icontains='dfkl')
        # cprint(type(lookups), 'yellow')
        # lookups_query = ""
        users_query = ""  # this to hold the Query

        # check if data usage is the report
        # if report_section_name == "data-usage":
        #     data_usage_obj = DataFile.objects.all()
        #     cprint(data_usage_obj, 'yellow')

        # this if check if the any value not equal all, and it exists in the keys dictionary
        if (filter_d.get("plan") != "all") and ("plan" in filter_d.keys()):
            # users_query = Subscription.objects.filter(stripe_plan_id=ALL_MEMBERSHIP.get(filter_d['plan']))
            tmp_subs = Subscription.objects.filter(stripe_plan_id=ALL_MEMBERSHIP.get(filter_d['plan']))
            # cprint(tmp_subs, 'green')
            # lookups = Q(member_subscription__in=tmp_subs)
            lookups = Q(member_subscription__in=tmp_subs)
            # cprint(tmp_subs.last().stripe_plan_id, "green")
        if (filter_d.get("country") != "all") and ("country" in filter_d.keys()):
            # users_query = Member.objects.filter(country=filter_d.get("country").capitalize())
            lookups &= Q(country=filter_d.get("country").title())
        if (filter_d.get("city") != "all") and ("city" in filter_d.keys()):
            # users_query = Member.objects.filter(city__icontains=filter_d.get("city").capitalize())
            lookups |= Q(city__icontains=filter_d.get("city").title())
        if (filter_d.get("organization_type") != "all") and ("organization_type" in filter_d.keys()):
            lookups |= Q(org_type__icontains=capitalize_report_name(filter_d.get("organization_type")))
        if (filter_d.get("register_date") != "all") and ("register_date" in filter_d.keys()):
            # users_query = Member.objects.get_users_by_register_date(filter_d.get("register_date"))
            start_date, end_date = filter_d.get("register_date").split(" - ")
            lookups |= Q(date_joined__range=[start_date, end_date])
        if (filter_d.get("job_title") != "all") and ("job_title" in filter_d.keys()):
            # users_query = Member.objects.filter(job_title__icontains=filter_d.get("job_title"))
            lookups |= Q(job_title__icontains=filter_d.get("job_title"))
        if (filter_d.get("annual_revenue") != "all") and ("annual_revenue" in filter_d.keys()):
            # users_query = Member.objects.filter(job_title__icontains=filter_d.get("job_title"))
            lookups |= Q(annual_revenue__icontains=filter_d.get("annual_revenue"))
        if (filter_d.get("total_staff") != "all") and ("total_staff" in filter_d.keys()):
            # users_query = Member.objects.filter(job_title__icontains=filter_d.get("job_title"))
            lookups |= Q(annual_revenue__exact=filter_d.get("total_staff"))
        if (filter_d.get("number_of_volunteer") != "all") and ("number_of_volunteer" in filter_d.keys()):
            # users_query = Member.objects.filter(job_title__icontains=filter_d.get("job_title"))
            lookups |= Q(annual_revenue__exact=filter_d.get("number_of_volunteer"))
        if (filter_d.get("number_of_board_members") != "all") and ("number_of_board_members" in filter_d.keys()):
            # users_query = Member.objects.filter(job_title__icontains=filter_d.get("job_title"))
            lookups |= Q(annual_revenue__exact=filter_d.get("number_of_board_members"))
        if (filter_d.get("cancelled_users") != "all") and ("cancelled_users" in filter_d.keys()):
            lookups |= Q(status__iexact="pending") | Q(status__iexact="unverified")
        if (filter_d.get("active_users") != "all") and ("active_users" in filter_d.keys()):
            lookups |= Q(status__iexact="active")

        users_query = Member.objects.filter(lookups)
        users_len = len(users_query)
        users_reports = dict()  # this will hold every information of the report for the user
        # this try to handle if the subscription not exists for members who have not subscription
        for idx, member in enumerate(users_query):
            # first check if the member has subscription or not
            subscript_details = {}
            tmp_mem_sub = Subscription.objects.filter(member_id=member).first()
            if tmp_mem_sub is not None:
                subscript_details = {
                        "stripe_plan_id": tmp_subs.first().stripe_plan_id.slug,
                        "subscription_status": tmp_subs.first().subscription_status,
                        "subscription_period_start": tmp_subs.first().subscription_period_start.strftime("%d-%m-%Y"),
                        "subscription_period_end": tmp_subs.first().subscription_period_end.strftime("%d-%m-%Y"),
                        "stripe_card_id": tmp_subs.first().stripe_card_id
                    }


            tmp_mem_sub_dict = {
                "member_data": {
                    "id": member.pk,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "full_name": member.full_name,
                    "email": member.email,
                    "register_date": member.date_joined.strftime("%d-%m-%Y"),
                    "phone": member.phone,
                    "country": member.country,
                    "state": member.state,
                    "street_address": member.street_address,
                    "org_name": member.org_name,
                    "organization_type": member.org_type,
                    "org_website": member.org_website,
                    "job_title": member.job_title,
                    "annual_revenue": member.annual_revenue,
                    "zip_code": member.zip_code,
                    "total_staff": float(member.total_staff),
                    "num_of_volunteer": member.num_of_volunteer,
                    "num_of_board_members": member.num_of_board_members,
                    "status": member.status,
                    "plan": "NOT READY YET"
                },
                "subscription_data": subscript_details
            }
            users_reports[f"ROW_{idx}"] = tmp_mem_sub_dict


        if len(users_reports) > 0:
            # cprint(users_reports['ROW_57'], 'blue')
            cprint(len(users_reports), 'red')
            return {"data": users_reports, "table_header": table_header, "total_results": len(users_reports)}
        else:
            return {"data": "NO DATA TO DISPLAY FOR USERS!!", "table_header": table_header, "total_results": 0}

    @staticmethod
    def get_data_usage_query(filter_dict: dict, table_header: list, report_section_name: str):
        # section_name = filter_dict['report_section_name']
        global GENERIC_TERMS
        users_reports_dict = ReportGenerator.get_all_user_query(filter_dict, table_header, 'users')['data']
        # cprint(users_reports_dict.keys(), 'cyan')
        filter_d = filter_dict
        GENERIC_TERMS = list(filter_d.keys())
        # cprint(report_section_name, "blue")
        # del filter_d['report_section_name']  # this to delete the section name to get only the field with its values
        # cprint(GENERIC_TERMS, 'green')
        for key, value in users_reports_dict.items():
            # cprint(value, 'yellow')
            tmp_member_data_handler_obj = DataFile.objects.filter(member=value['member_data']['id']).first()
            # check if the member has data file object
            if tmp_member_data_handler_obj is not None:
                tmp_usage_percentage = 0
                tmp_data_handler_session_obj = DataHandlerSession.objects.filter(
                    data_handler_id=tmp_member_data_handler_obj).first()
                # cprint(tmp_member_data_handler_obj.allowed_records_count, 'yellow')
                # check if data is int
                if (type(tmp_member_data_handler_obj.allowed_records_count).__name__ == 'int') and (tmp_data_handler_session_obj is not None):

                    # tmp_usage_percentage
                    cprint(tmp_data_handler_session_obj, 'blue')

                #    cprint(tmp_data_handler_session_obj.all_records_count, "blue" )
                    if tmp_data_handler_session_obj is not None:
                        # cprint(tmp_data_handler_session_obj.get_fields_as_list, 'cyan')
                        # cprint(tmp_data_handler_session_obj.data_file_path, 'cyan')
                        pass
            # break


        return {"data": "NO DATA TO DISPLAY FOR USERS!!", "table_header": table_header, "total_results": 0}
