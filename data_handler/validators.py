# this file contain class which will validate the user data file rows
import re
from email_validator import validate_email, EmailNotValidError
from datetime_extractor import DateTimeExtractor


class DataValidator:
    def __init__(self):
        # self.data = data
        self.value_dict = {}

        # call this method will call the validation steps

    def detect_and_validate(self, val=""):
        """
        this method will call all validation methods in this class
        Returns:

        """
        the_value = val.strip()
        # first check if the data is null
        if self.validate_empty(the_value) is True:
            # this mean the input data is empty no need to validate the types
            return self.return_the_error_msg(True, the_value, "Empty Value!", data_type="NAN")
        else:
            # here the data not null, here will be the logic to validate the data type
            # validate date and timestamp
            if self.is_valid_date(the_value) is True:  # mean it is ok the date is validate
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match Date|Date time",
                                                                     data_type="Date|DateTimeStamp")
            # validate url
            elif self.is_valid_url(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match URL", data_type="URL")
            # validate monetary
            elif self.is_valid_monetary(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match monetary",
                                                                     data_type="monetary")
            # validate phone number
            elif self.is_valid_phone(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match phone_number",
                                                                     data_type="phone_number")
            # validate zip code
            elif self.is_valid_zip(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match zip_code",
                                                                     data_type="zip_code")
            # validate email address
            elif self.is_valid_email(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match email", data_type="email")
            # validate alphanumeric
            elif self.is_valid_alphanumeric(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match alphanumeric",
                                                                     data_type="alphanumeric")
            # validate the string
            elif self.is_valid_string(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match string", data_type="string")
            # validate the name
            elif self.is_valid_name(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match Name", data_type="name")
            # validate decimal
            elif self.is_valid_decimal(the_value) is True:
                the_validate_dict_values = self.return_the_error_msg(False, the_value, "Match Decimal", data_type="decimal")
            else:
                the_validate_dict_values = self.return_the_error_msg(True, the_value, "NOT MATCH ANY TYPE!!!",
                                                                     data_type="unkown")

            return the_validate_dict_values

    def validate_empty(self, value):
        tmp_val = value
        if tmp_val == "" or tmp_val is None or tmp_val == "nan" or tmp_val == "Nan":
            return True
        else:
            return False

    def return_the_error_msg(self, is_error: bool, val: str, msg="", data_type=""):
        val = val.strip()
        if msg and data_type:
            return {"is_error": is_error, "value": val, "msg": msg, "data_type": data_type}
        else:
            return {"is_error": is_error, "value": val}

    def is_valid_name(self, the_value):
        the_value = the_value.strip()
        # regex = r"(?=^.{0,40}$)^[a-zA-Z-]+\s[a-zA-Z-]+$"
        regex = r"^[A-Za-z][A-Za-z\'\-]+([\ A-Za-z][A-Za-z\'\-]+)*"
        pattern = re.compile(regex, flags=re.IGNORECASE)
        mt = pattern.search(the_value)
        if mt:
            return True
        else:
            return False
    def is_valid_email(self, value):
        value = value.strip()
        regex = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        # regex = r"[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}"
        pattern = re.compile(regex, flags=re.IGNORECASE)
        mt = pattern.search(value)
        if mt:
            return True
        else:
            return False

    def is_valid_alphanumeric(self, value: str):
        value = value.strip()
        # print(value.isalnum())
        # regex = r"^\w+$"
        regex = r"^[a-zA-Z0-9_]*$"
        pattern = re.compile(regex, re.IGNORECASE)
        match = pattern.search(value)
        if match:
            return True
        else:
            return False

    def is_valid_url(self, value):
        value = value.strip()
        regex = r"([a-z]{1,2}tps?):\/\/((?:(?!(?:\/|#|\?|&)).)+)(?:(\/(?:(?:(?:(?!(?:#|\?|&)).)+\/))?))?(?:((?:(?!(?:\.|$|\?|#)).)+))?(?:(\.(?:(?!(?:\?|$|#)).)+))?(?:(\?(?:(?!(?:$|#)).)+))?(?:(#.+))?"
        pattern = re.compile(regex, re.MULTILINE | re.IGNORECASE)
        matches = pattern.search(value)
        if matches:
            return True
        else:
            return False

    def is_valid_number(self, value):
        value = str(value).strip()
        regex = r"^[-]?[0-9,]+$"
        pattern = re.compile(regex)
        if pattern.search(value):
            # print('this is Number')
            return True
        else:
            return False

    def is_valid_date(self, value):
        value = value.strip()
        regex = r"\b(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\w* )?(\d{1,2})(?:st|nd|th)?[,]? (?:(?:(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\w*)?[,]? )?(\d{2,4})\b"
        regex2 = r"^(?:(?:(?:0[13578]|1[02])(\/|-|\.| ?)31)\1|(?:(?:0[1,3-9]|1[0-2])(\/|-|\.| ?)(?:29|30)\2))(?:(?:1[6-9]|[2-9]\d)\d{2})$|^(?:02(\/|-|\.| ?)29\3(?:(?:(?:1[6-9]|[2-9]\d)(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:(?:0[1-9])|(?:1[0-2]))(\/|-|\.| ?)(?:0[1-9]|1\d|2[0-8])\4(?:(?:1[6-9]|[2-9]\d)\d{2})$"
        match_date_time_list = DateTimeExtractor(value)  # check with timestamp (Jan 1, 2011 00:00:00.00)
        if match_date_time_list:
            return True
        else:
            match_1 = re.search(regex, value, re.IGNORECASE)
            match_2 = re.search(regex2, value, re.IGNORECASE)
            if match_1:
                return True
            elif match_2:
                return True
            else:
                return False

    def is_valid_phone(self, value):
        value = value.strip()
        regex = r"(((\+)\b[1-9]{1,2}[-.]?)|(([^1-9]{2})[1-9]{1,2}[-.]?))?\d{3}[-.]?\d{3}[-.]?\d{4}(\s(#|x|ext|extension|e)?[-.:](\d{0,5}))?"
        pattern = re.compile(regex)
        match = pattern.search(value)
        if match:
            return True
        else:
            return False

    def is_valid_monetary(self, value: str):
        value = value.strip()
        regex_no_dollar = r"^((\d+)|(\d{1,3}(\.\d{3})+)|(\d{1,3}(\.\d{3})(\,\d{3})+))(\,\d{2})?$"
        regex_dollar = r"^(\$)+([0-9]+[\,])?([0-9]+[\.,])+([0-9]{2})+"
        match_1 = re.search(regex_no_dollar, value)
        match_2 = re.search(regex_dollar, value)
        if match_1:
            return True
        elif match_2:
            return True
        else:
            return False

    def is_valid_zip(self, value: str):
        value = value.strip()
        regex = r"^\d{5}$"
        if len(value) == 5 and value.isnumeric():
            pattern = re.compile(regex)
            if pattern.search(value):
                return True
            else:
                return False

    def is_valid_string(self, value: str):
        value = value.strip()
        regex = r"(?:\w+\s+){2}"
        # regex = r"(?:\w+)"
        pattern = re.compile(regex, re.IGNORECASE)
        match = pattern.search(value)
        if match:
            return True
        else:
            return False

    def is_valid_decimal(self, value):
        regex = r"[\d]{1,99}([.]\d{1,99})?"
        pattern = re.compile(regex, re.IGNORECASE)
        match = pattern.search(value)
        if match:
            return True
        else:
            return False

