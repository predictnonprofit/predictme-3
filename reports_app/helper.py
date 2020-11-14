from faker import Faker
from predict_me.my_logger import log_exception
from termcolor import cprint
from membership.models import (Subscription, UserMembership, Membership)
from data_handler.models import (DataFile, DataHandlerSession)
from users.models import Member
from django.db.models import Q
from datetime import datetime
from django.forms.models import model_to_dict
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
             "input_name": report_name("Organization Name"), "has_options": True, "report_type": "Generic Filter"},
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
            elif report_name(r_filter['filter_name']) == "city":
                filter_keys[report_name(r_filter['filter_name'])] = r_filter['filter_value']
            else:
                if report_name(r_filter['filter_name']) == "organization_type":
                    filter_keys["org_type"] = r_filter['filter_value']
                elif report_name(r_filter['filter_name']) == "organization_name":
                    filter_keys[report_name("org_name")] = r_filter['filter_value']
                elif report_name(r_filter['filter_name']) == "user_status":
                    filter_keys[report_name("status")] = report_name(r_filter['filter_value'])
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
        users_data = ReportGenerator.test_custom_report_sql_generator(filter_d)
        # check if data usage is the report
        # if report_section_name == "data-usage":
        #     data_usage_obj = DataFile.objects.all()
        #     cprint(data_usage_obj, 'yellow')

        # this if check if the any value not equal all, and it exists in the keys dictionary

        # users_query = Member.objects.filter(lookups)
        users_len = len(users_query)
        users_reports = dict()  # this will hold every information of the report for the user
        # this try to handle if the subscription not exists for members who have not subscription

        # if len(users_reports) > 0:
        return {"data": users_data, "table_header": table_header, "total_results": len(users_data)}
        # else:
        #     return {"data": "NO DATA TO DISPLAY FOR USERS!!", "table_header": table_header, "total_results": 0}

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
        columns_keys = list(filter_dict.keys())
        columns_keys.extend((
            "slug",
            "sub_range",
            "status"
        ))
        # cprint(columns_keys, 'red')
        all_rows = {}
        if len(filter_dict) > 0:
            read_members_query = read_sql_generator("members", **filter_dict)
            # cprint(read_members_query, 'blue')
            # cprint(read_members_query, 'cyan')
            all_data = []
            with connection.cursor() as cursor:
                cursor.execute(read_members_query)
                # columns = [col for col in columns_keys]
                columns = [col[0] for col in cursor.description]
                # row = cursor.fetchall()
                #     for row in cursor.fetchall():
                #         row_dict = dict(zip(columns, row))
                #         # cprint(row_dict, 'red')
                #         for key, value in row_dict.items():
                #             if type(value).__name__ == 'datetime':
                #                 row_dict[key] = value.strftime("%m/%d/%Y")
                #             all_data.append(row_dict)
                # cprint(all_data[0], 'blue')
                row = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            # cprint(row, 'green')
            # cprint(row[0], 'cyan')
            # query_object = Member.objects.raw(read_members_query)
            # # cprint(query_object.columns, 'cyan')
            # for index, q in enumerate(query_object):
            #     # print(index, q)
            #     # cprint(type(q), 'yellow')
            #     query_as_dict = model_to_dict(q)
            #     query_as_dict.pop("password")
            #     # print(query_object, end="\n")
            #     all_rows[f"ROW_{index}"] = query_as_dict
            # 'columns', 'db', 'iterator', 'model', 'model_fields', 'params', 'prefetch_related', 'query', 'raw_query', 'resolve_model_init_order', 'translations', 'using'

        # return all_rows
        return row


def read_sql_generator(table, **kwargs):
    """ Generates SQL for a SELECT statement matching the kwargs passed. """
    sql = list()
    plan = ''
    del kwargs['report_section_name']
    # first get the check the plan in the kwargs
    if "plan" in kwargs:
        plan = kwargs.get("plan", "active")
        # delete the plan from kwargs
        del kwargs['plan']

    membership_columns = ('membership.id', 'membership.slug', 'membership.membership_type',
                          'membership.monthly_fee', 'membership.yearly_fee', 'membership.day_price',
                          'membership.stripe_plane_id', 'membership.additional_fee_per_extra_record',
                          'membership.allowed_records_count')

    members_columns = ('member.id', 'member.first_name', 'member.last_name', 'member.full_name',
                       'member.email', 'member.status', 'member.date_joined', 'member.phone',
                       'member.street_address', 'member.state', 'member.city', 'member.country',
                       'member.org_name', 'member.job_title', 'member.org_website', 'member.org_type',
                       'member.annual_revenue', 'member.total_staff', 'member.num_of_volunteer',
                       'member.num_of_board_members')

    subscription_columns = ('subs.id', 'subs.member_id_id', 'subs.stripe_customer_id', 'subs.stripe_subscription_id',
                            'subs.stripe_plan_id_id', 'subs.subscription_status', 'subs.subscription_period_start',
                            'subs.subscription_period_end', 'subs.card_expire', 'subs.sub_range', 'subs.stripe_card_id')

    members_and_subscription_merge_columns = members_columns + subscription_columns + membership_columns
    # cprint(members_and_subscription_merge_columns, "cyan")
    sql2 = list()
    sql.append("SELECT * FROM %s " % table)
    sql2.append("SELECT DISTINCT {} FROM {} AS member, membership_membership AS membership ".format(
        ", ".join(members_and_subscription_merge_columns), table))
    sql2.append(
        "INNER JOIN subscriptions AS subs ON (member.id = subs.member_id_id) AND (subs.stripe_plan_id_id = membership.id) ")
    sql2.append("WHERE")
    numeric_fields = ('num_of_volunteer', "total_staff", "num_of_board_members")

    if kwargs:
        # first point make the first query
        # va = kwargs.get(columns_name[0]) if kwargs.get(columns_name[0]) != "all" else "'%'"
        # sql2.append(f" WHERE ({columns_name[0]} LIKE {va}) AND")
        de = ((k, v) for k, v in kwargs.items())
        # tt = "WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items())
        for d in de:
            col_name = d[0]
            col_value = ''
            if (type(d[1]).__name__ == "str") and (d[1].lower() != "all"):
                col_value = f" %{d[1].lower()}% ".strip()
            elif type(d[1]).__name__ == "int":
                col_value = d[1]
            else:
                col_value = "%%"

            # check if the column belongs to one of the numeric columns
            if col_name in numeric_fields:
                # (num_of_board_members BETWEEN 0 AND '%')
                sql2.append(f" ({col_name} BETWEEN 0 AND {col_value}) AND")
            # check if the key is register date
            elif col_name == "register_date":
                clean_date_format = col_value[1:-1]
                # cprint(clean_date_format, 'red')
                start_date, end_date = clean_date_format.split(" - ")
                start_date = start_date.replace("/", "-")
                start_date = datetime.strptime(start_date, "%m-%d-%Y")
                end_date = end_date.replace("/", "-")
                end_date = datetime.strptime(end_date, "%m-%d-%Y")

                sql2.append(f" (date_joined BETWEEN '{start_date}' AND '{end_date}') AND")
            else:
                sql2.append(f" ({col_name} LIKE '{col_value}') AND")

        sql_with_no_and = "".join(sql2).rsplit(' ', 1)[0]
        sql2 = sql_with_no_and.split()
        sql2.append("GROUP BY member.id")
        sql2.append(';')
        # cprint(" ".join(sql2), "yellow")

    return " ".join(sql2)


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
