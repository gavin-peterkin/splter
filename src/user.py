import datetime as dt
import os
import re
import json
import sys


class User(object):

    # FIXME: Move to higher-level configuration object
    _users_filepath='{}/../data/users.json'.format(
        os.path.dirname(os.path.realpath(__file__))
    )

    _user_key = 'user'
    _perc_key = 'percentage'
    _group_key = 'group_label'
    _dt_key = 'startDate'
    _dt_format = '%Y-%m-%d'

    def __init__(self, username=None):
        if username == None:
            assert not os.path.isfile(self._users_filepath), "Username arg required for existing user file"
        self.username = username
        self.set_up_user()

    @property
    def _new_user_dict_representation(self):
        return {
            self._user_key: self.username,
            self._perc_key: self.percentage,
            self._dt_key: dt.datetime.now().strftime(self._dt_format),
            self._group_key: self.group_label
        }

    def _update_complete_users_dict(self):
        self._complete_users_dict.update({
            self.username: self._new_user_dict_representation
        })

    @property
    def start_date(self):
        return dt.datetime.strptime(
            self._complete_users_dict[self.username][_dt_key],
            self._dt_format
        )

    @property
    def existing_group_labels(self):
        group_labels = list()
        for user, info in self._complete_users_dict.iteritems():
            group_labels.append(info[self._group_key])
        return list(set(group_labels))

    @property
    def users_group(self):
        return self._complete_users_dict[self.username][self._group_key]

    @property
    def all_users_percentages(self):
        """Return all other users and percentages for individuals belonging to that group"""
        return {
            user: info[self._perc_key] for user, info
            in self._complete_users_dict.iteritems() if info[self._group_key] == self.users_group
        }

    def _get_bool_response(self):
        resp = raw_input("Enter [Yes/No]?")
        return (resp.lower()[0] == 'y')

    def _get_validate_response(self, input_type='username', object_type=str):
        is_okay = False
        while not is_okay:
            resp = object_type(raw_input("Enter your new {}: ".format(input_type)))
            print("You entered {}.".format(resp))
            is_okay = (type(resp) == object_type) and self._get_bool_response()
        return resp

    def _new_user_walkthrough(self):
        # Username creation
        print("""
You will be asked to provide a new username. Note that you will use this username
to identify yourself when entering new amounts. Other user(s) should also be able
to ID you on the basis of this name.
        """)
        self.username = self._get_validate_response(input_type='username', object_type=str)
        # Percentage
        print("""
Thanks, {user}! You are now asked to provide a percentage that will reflect the
payment portion for which you are responsible.
For example, if your social group generally expects you to pay 15% of all costs,
you'd enter '0.15'.
        """.format(user=self.username))
        self.percentage = self._get_validate_response(input_type='percentage', object_type=float)
        # Group setting initialization
        accepted = False
        print("""
The final step is to provide an existing or new group label. If the percentages
for users don't sum to one for this grouping, they'll be normalized when transactions
are entered into the ledger. Example input: "friend_group_1".
        """)
        print("Existing group labels: {}\n".format(self.existing_group_labels))
        while not accepted:
            self.group_label = self._get_validate_response(input_type='group label', object_type=str)
            try:
                if self.group_label in self.existing_group_labels:
                    print("Using existing label {}.".format(self.group_label))
            except:
                print("Not an existing label. Created new group label {}".format(self.group_label))

    def _parse_file_users(self):
        users = self._complete_users_dict.keys()
        # import pdb; pdb.set_trace()
        if self.username not in users:
            print("User '{}' not found. Would you like to set up a new user?".format(self.username))
            set_up_new = self._get_bool_response()
            if set_up_new:
                self._new_user_walkthrough()
                self._update_complete_users_dict()
                self._save_user_file()
            else:
                print('Exiting.')
                sys.exit()
        else:
            self._initialize_existing_user(self._complete_users_dict, self.username)

    def _initialize_existing_user(self, user_dict, user):
        self.username = user_dict[user][self._user_key]
        self.percentage = float(user_dict[user][self._perc_key])
        self.group_label = user_dict[user][self._group_key]

    def _save_user_file(self):
        with open(self._users_filepath, 'w+') as f:
            json.dump(self._complete_users_dict, f)

    def set_up_user(self):
        try:
            with open(self._users_filepath, 'r') as f:
                self._complete_users_dict = json.load(f)
            self._parse_file_users()
        except:
            print("No user data found")
            self._complete_users_dict = dict()
            # There are no users and no file
            self._new_user_walkthrough()
            self._update_complete_users_dict()
            # The file doesn't exist, so create it
            self._save_user_file()

    def remove_user(self):
        _ = self._complete_users_dict.pop(self.username, None)
        self._save_user_file()
        print("User {} removed.".format(self.username))

    def update_percentage(self, percentage):
        self._complete_users_dict[self.username][self._perc_key] = percentage
        self._save_user_file
        print("Default percentage for user {} update to {}".format(self.username, percentage))
