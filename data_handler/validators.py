# this file contain functions which will validate the user data file rows



def validate_empty(value):
    value_dict = {}
    if value == "" or value is None or value == "nan":
        value_dict = {"is_error": True, "value": value}
    else:
        value_dict = {"is_error": False, "value": value}

    return value_dict