

import sys

"""
A file containing core utility functions useful throughout the codebase
"""

def get_bool_response():
    resp = raw_input("Okay [Yes/No]?")
    return (resp.lower()[0] == 'y')

def get_validate_response(input_type='username', object_type=str):
    is_okay = False
    while not is_okay:
        resp = object_type(raw_input("Enter {}: ".format(input_type)))
        print("You entered '{}'.".format(resp))
        is_okay = (type(resp) == object_type) and get_bool_response()
    return resp

def normalize_user_group(user_group_dict):
    total = sum(user_group_dict.values())
    if total > 1.001 or total < 0.999:
        print("Percentages don't sum to 1, so they'll be normalized.")
        resp = get_bool_response()
        if resp:
            user_group_dict = {
                k: v / float(total) for k, v in user_group_dict.iteritems()
            }
        else:
            sys.exit()
    return user_group_dict
