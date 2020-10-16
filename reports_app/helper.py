from faker import Faker
from predict_me.my_logger import log_exception
from termcolor import cprint
from membership.models import (Subscription, UserMembership)
from data_handler.models import (DataFile, DataHandlerSession)
from users.models import Member
from django.db.models import Q
from collections import defaultdict

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


# this function will return filter name with lower and replaced space with underscore
def report_name(name: str):
    return name.lower().replace(" ", "_")


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
                 "has_options": False, "report_type": "Custom Filter"},
                {"filter_name": "Cancelled Users", "report_section": "users",
                 "input_name": report_name("Cancelled Users"),
                 "has_options": False, "report_type": "Custom Filter"},
                {"filter_name": "Days Left", "report_section": "users", "input_name": report_name("Days Left"),
                 "has_options": False, "report_type": "Custom Filter"},
            ]
        elif report_section_name == "data_usage":
            return [
                {"filter_name": "Last Run", "report_section": "data_usage", "input_name": report_name("Last Run"),
                 "has_options": False, "report_type": "Custom Filter"},
                {"filter_name": "Usage", "report_section": "data_usage", "input_name": report_name("Usage"),
                 "has_options": False, "report_type": "Custom Filter"},

            ]
        elif report_section_name == "revenue":
            return [
                {"filter_name": "Start Offer Date", "report_section": "revenue",
                 "input_name": report_name("Start Offer Date"),
                 "has_options": True, "report_type": "Custom Filter"},
                {"filter_name": "Next Revenue Date", "report_section": "revenue",
                 "input_name": report_name("Next Revenue Date"),
                 "has_options": False, "report_type": "Custom Filter"},

            ]


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
        filter_keys = {}
        # all_filters = defaultdict(list)
        all_filters = {}
        # cprint(type(filter_list), 'yellow')
        for r_filter in filter_list:
            # print(r_filter)
            filter_keys[r_filter['filter_name']] = r_filter['filter_value']

        # member = Member.objects.get(id=user_id)
        # subscription = Subscription.objects.get(member_id=member)
        all_members = list(Member.objects.all())
        all_subscriptions = list(Subscription.objects.all())
        # cprint(report_table_header, 'red')
        for head in report_table_header:
            head_name = head.lower().replace(" ", "_")
            for index, member in enumerate(all_members):
                ReportGenerator.report_maker(member, report_section_name, filter_list)
                # all_filters['first_name'].append(member.first_name)
                # all_filters['last_name'].append(member.last_name)
                member_subscription = Subscription.objects.filter(member_id=member).first()
                # usermembership = UserMembership.objects.filter(member=member).first()
                if member_subscription is not None:
                    member_plan = str(member_subscription.stripe_plan_id)

                else:
                    member_plan = "No Plan Yet"

                all_filters[f"ROW_{index}"] = {
                    "row": [
                        member.first_name,
                        member.last_name,
                        member.email,
                        member_plan,

                    ]
                }

        # check the report section name
        # cprint(all_filters, "green")
        if report_section_name == 'users':
            pass

        return all_filters

    @staticmethod
    def report_maker(member_entity: Member, report_section_name: str, filter_list: list):
        filter_map = dict()
        member_subscription = Subscription.objects.filter(member_id=member_entity).first()
        member_main_data_obj = DataFile.objects.filter(member=member_entity).first()
        member_data_session = DataHandlerSession.objects.filter(data_handler_id=member_main_data_obj).first()
        # cprint(member_subscription, "cyan")
        # a = Member.objects.get_users_by_register_date('2020-09-27 - 2020-09-30')
        # cprint(a[2].date_joined, 'green')
        if member_entity is not None:
            filter_map['Member'] = member_entity.get_fields_as_list
        if member_subscription is not None:
            filter_map['Subscription'] = member_subscription.get_fields_as_list
        if member_main_data_obj is not None:
            filter_map['Main_Data'] = member_main_data_obj.get_fields_as_list
        if member_data_session is not None:
            filter_map['Data_Session'] = member_data_session.get_fields_as_list
        # cprint(member_data_session, "magenta")
        filter_keys = {}
        all_filters = {}
        # cprint(type(filter_list), 'yellow')
        for r_filter in filter_list:
            # print(r_filter)
            # cprint(report_name(r_filter['filter_name']))
            if report_name(r_filter['filter_name']) == "register_date":
                filter_keys[report_name(r_filter['filter_name'])] = r_filter['filter_value']
                # cprint("_" in r_filter['filter_value'], 'red')
                # cprint(report_name(r_filter['filter_value']), 'green')
            else:
                filter_keys[report_name(r_filter['filter_name'])] = report_name(r_filter['filter_value'])

            filter_keys["report_section_name"] = report_name(r_filter['report_section_name'])

        # loop through filter_map to determine which model filters belongs to
        for map_key, map_value in filter_map.items():
            # print(map_key, "---> ", map_value)
            for filter_key, filter_value in filter_keys.items():
                # print(filter_key, "--> ", filter_value)
                if filter_key in map_value:

                    msg = f"The {filter_key} belongs to {map_key} "
                    # cprint(msg, 'blue')
