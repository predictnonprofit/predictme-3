from faker import Faker
from predict_me.my_logger import log_exception
from termcolor import cprint
from membership.models import (Subscription, UserMembership, Membership)
from data_handler.models import (DataFile, DataHandlerSession)
from users.models import Member
from django.db.models import Q
from datetime import datetime
from django.db import connection
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
            {"filter_name": "User Status", "report_section": "users",
             "input_name": report_name("User Status"), "has_options": True, "report_type": "Generic Filter"},
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
        if report_section_name == "data_usage":
            return [
                {"filter_name": "Last Run", "report_section": "data_usage", "input_name": report_name("Last Run"),
                 "has_options": False, "report_type": "Data Usage Filter"},
                {"filter_name": "Usage", "report_section": "data_usage", "input_name": report_name("Usage"),
                 "has_options": False, "report_type": "Data Usage Filter"},

            ]
        elif report_section_name == "revenue":
            return [
                {"filter_name": "Plan Start Date", "report_section": "revenue",
                 "input_name": report_name("Plan Start Date"),
                 "has_options": True, "report_type": "Revenue Filter"},
                {"filter_name": "Next Renewal Date", "report_section": "revenue",
                 "input_name": report_name("Next Renewal Date"),
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
        report_data = {}  # this dict will hold every reports information

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
            elif (report_name(r_filter['filter_name']) == "city") or (
                    report_name(r_filter['filter_name']) == "organization_type"):
                filter_keys[report_name(r_filter['filter_name'])] = r_filter['filter_value']
            else:
                filter_keys[report_name(r_filter['filter_name'])] = report_name(r_filter['filter_value'])

            filter_keys["report_section_name"] = report_name(r_filter['report_section_name'])
        # cprint(filter_list, 'magenta')
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
        if filter_d.get("report_section") is not None:
            del filter_d['report_section_name']  # this to delete the section name to get only the field with its values
        cprint(filter_d, 'green')
        lookups = None
        # lookups = lookups | Q(body__icontains='dfkl')
        # cprint(type(lookups), 'yellow')
        # lookups_query = ""
        users_query = ""  # this to hold the Query
        ReportGenerator.test_custom_report_sql_generator(filter_d)
        # check if data usage is the report
        # if report_section_name == "data-usage":
        #     data_usage_obj = DataFile.objects.all()
        #     cprint(data_usage_obj, 'yellow')

        # this if check if the any value not equal all, and it exists in the keys dictionary

        # users_query = Member.objects.filter(lookups)
        users_len = len(users_query)
        users_reports = dict()  # this will hold every information of the report for the user
        # this try to handle if the subscription not exists for members who have not subscription

        if len(users_reports) > 0:
            # cprint(users_reports['ROW_57'], 'blue')
            # cprint(len(users_reports), 'red')
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
                if (type(tmp_member_data_handler_obj.allowed_records_count).__name__ == 'int') and (
                        tmp_data_handler_session_obj is not None):

                    # tmp_usage_percentage
                    cprint(tmp_data_handler_session_obj, 'blue')

                    #    cprint(tmp_data_handler_session_obj.all_records_count, "blue" )
                    if tmp_data_handler_session_obj is not None:
                        # cprint(tmp_data_handler_session_obj.get_fields_as_list, 'cyan')
                        # cprint(tmp_data_handler_session_obj.data_file_path, 'cyan')
                        pass
            # break

        return {"data": "NO DATA TO DISPLAY FOR USERS!!", "table_header": table_header, "total_results": 0}

    @staticmethod
    def test_custom_report_sql_generator(filter_dict: dict):
        WHERE_OPERATOR = "AND"
        if len(filter_dict) > 0:
            read_members_query = read_query("members", **filter_dict)
            cprint(read_members_query, 'cyan')
            user_status_value = filter_dict.get("user_status",
                                                'active')  # this variable will hold the user status active, cancelled, pending, verify
            # cprint(filter_dict, "green")
            register_date = filter_dict.get("register_date", None)
            # cprint(register_date, 'red')
            register_date_query = ""
            if register_date is not None:
                start_date, end_date = register_date.split(" - ")
                start_date = start_date.replace("/", "-")
                start_date = datetime.strptime(start_date, "%m-%d-%Y")
                end_date = end_date.replace("/", "-")
                end_date = datetime.strptime(end_date, "%m-%d-%Y")
                register_date_query = f""" {WHERE_OPERATOR} (date_joined BETWEEN '{start_date}' AND '{end_date}') """
            else:
                register_date_query = f""

            members_query = f"SELECT id, first_name, last_name, full_name, phone, street_address, state, " \
                            f"city, country, zip_code, org_name, job_title, org_website, org_type, " \
                            f"annual_revenue, total_staff, num_of_volunteer, num_of_board_members, status " \
                            f"FROM members WHERE (first_name LIKE %s) {WHERE_OPERATOR} (last_name LIKE %s) " \
                            f"{WHERE_OPERATOR} (email LIKE %s) {WHERE_OPERATOR} (country LIKE %s) " \
                            f"{WHERE_OPERATOR} (org_name LIKE %s) {WHERE_OPERATOR} (org_type LIKE %s) " \
                            f"{WHERE_OPERATOR} (job_title LIKE %s) {WHERE_OPERATOR} (annual_revenue LIKE %s) " \
                            f"{WHERE_OPERATOR} (status = '{user_status_value}') {register_date_query} " \
                            f"{WHERE_OPERATOR} (total_staff BETWEEN 0 AND %s) {WHERE_OPERATOR} (num_of_volunteer BETWEEN 0 AND %s) " \
                            f"{WHERE_OPERATOR} (num_of_board_members BETWEEN 0 AND %s)"

            members_query = members_query.strip()
            members_query_params = [
                "'%'", "'%'", "'%'", get_filter_value(filter_dict, "country"),
                get_filter_value(filter_dict, "organization_name"), get_filter_value(filter_dict, "organization_type"),
                get_filter_value(filter_dict, "job_title"), get_filter_value(filter_dict, "annual_revenue"),
                get_filter_value(filter_dict, "total_staff"), get_filter_value(filter_dict, "num_of_volunteer"),
                get_filter_value(filter_dict, "num_of_board_members")
            ]
            # `mems.id`, `mems.first_name`, `mems.last_name`, `mems.full_name`, `mems.email`, `mems.date_joined`,
            # `mems.phone`, `mems.street_address`, `mems.state`, `mems.city`, `mems.country`, `mems.org_name`,
            # `mems.job_title`, `mems.org_website`, `mems.org_type`, `mems.annual_revenue`, `mems.total_staff`,
            # `mems.num_of_volunteer`, `mems.num_of_board_members`, `mems.status`

            # cprint(members_query_params, 'yellow')
            # get_filter_where_syntax(filter_dict)
            #######
            query_object = Member.objects.raw(members_query, members_query_params)
            for q in query_object:
                cprint(q, 'yellow')
            # 'columns', 'db', 'iterator', 'model', 'model_fields', 'params', 'prefetch_related', 'query', 'raw_query', 'resolve_model_init_order', 'translations', 'using'

            #######
            # cprint(connection.queries[3]['sql'], 'blue')


def read_query(table, **kwargs):
    """ Generates SQL for a SELECT statement matching the kwargs passed. """
    sql = list()
    sql.append("SELECT * FROM %s " % table)
    statement = list()
    del kwargs['report_section_name']
    # cprint("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()), "red")
    if kwargs:
        # print("register_date" in kwargs)
        # cprint(((k, v) for k, v in kwargs.items()), "red")
        sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
    sql.append(";")
    return "".join(sql)


def get_filter_value(filters_dict: dict, filter_name: str):
    # cprint(filters_dict, 'cyan')
    # cprint(len(filters_dict), 'yellow')
    not_allowed_filters = ("register_date", "active_users", "cancelled_users", "days_left")

    # cprint(filter_name, 'yellow')
    # cprint(filters_dict[filter_name], 'red')
    # check if the key of filter send in the filter_names_list to add it to all_filters_list
    try:
        if filter_name not in not_allowed_filters:
            if filters_dict.get(filter_name) == "all":
                # print('%')
                return "'%'"

            else:
                tmp_value = filters_dict.get(filter_name, "")

                if type(tmp_value).__name__ == "int":
                    return tmp_value
                elif (type(tmp_value).__name__ == 'str') and (tmp_value != ""):
                    return f"'%{tmp_value}%'"
                else:
                    return f"'%'"
    except KeyError:
        cprint("key not exists", 'red')
