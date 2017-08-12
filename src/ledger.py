from utility import normalize_user_group, get_bool_response

from terminaltables import AsciiTable

import datetime as dt
import os
import json
import sys


class Ledger(object):

    # FIXME: Move to higher-level configuration object
    _ledger_filepath='{}/../data/ledger.json'.format(
        os.path.dirname(os.path.realpath(__file__))
    )
    _dt_format = '%Y-%m-%d/%H:%M:%s'

    _metadata_key = 'metadata'
    _creator_key = 'ledger_creator'
    _dt_creation_key = 'dt_created'

    _user_entry_key = 'username'
    _group_entry_key = 'group_label'
    _total_amount_entry_key = 'total_amount'
    _norm_perc_entry_key = 'normalized_percentage'
    _total_due_entry_key = 'actual_amount_due'
    _message_entry_key = 'message'

    def __init__(self, username, group_label, create_new=False):
        self.username = username
        self.group_label = group_label

        if not os.path.isfile(self._ledger_filepath):
            self._initialize_new_ledger()
        elif create_new:
            # Add a new ledger to the file
            # New feature: add support for multiple ledgers
            pass
        else:
            # reload existing ledger
            self._load_ledger()

    @property
    def _new_ledger_metadata(self):
        # New metadata
        now_str = dt.datetime.now().strftime(self._dt_format)
        return {
            self._creator_key: self.username,
            self._dt_creation_key: now_str
        }

    def _initialize_new_ledger(self):
        print("Initializing a new ledger")
        self.complete_ledger = {}
        self.complete_ledger.update({self._metadata_key: self._new_ledger_metadata})
        self._save_ledger()

    def _save_ledger(self):
        with open(self._ledger_filepath, 'w+') as f:
            json.dump(self.complete_ledger, f)

    def _load_ledger(self):
        with open(self._ledger_filepath, 'r') as f:
            self.complete_ledger = json.load(f)

    def _get_current_commit_id(self):
        try:
            last_entry_id = max([int(id_) for id_ in self.complete_ledger.keys() if id_ != self._metadata_key])
        except:
            last_entry_id = -1
        return last_entry_id

    def _add_entry(self, entry_dict):
        current_entry_id = self._get_current_commit_id() + 1
        self.complete_ledger[current_entry_id] = entry_dict

    def _balance_books(self, other_users_dict, amount, message):
        for user, normed_percentage in other_users_dict.iteritems():
            new_entry = {
                self._dt_creation_key: dt.datetime.now().strftime(self._dt_format),
                self._user_entry_key: user,
                self._group_entry_key: self.group_label,
                self._total_amount_entry_key: 0,
                self._norm_perc_entry_key: normed_percentage,
                self._total_due_entry_key: normed_percentage * amount,
                self._message_entry_key: str(self.username) + ': ' + message
            }
            self._add_entry(new_entry)

    def add_transaction(
        self, username, total_amount,
        all_users_percentages, message=''
    ):
        start_commit_id = self._get_current_commit_id()
        all_users_percentages = normalize_user_group(all_users_percentages)
        norm_percentage = all_users_percentages[self.username]
        new_entry = {
            self._dt_creation_key: dt.datetime.now().strftime(self._dt_format),
            self._user_entry_key: username,
            self._group_entry_key: self.group_label,
            self._total_amount_entry_key: total_amount,
            self._norm_perc_entry_key: norm_percentage,
            self._total_due_entry_key: (1. - norm_percentage) * -total_amount,
            self._message_entry_key: message
        }
        self._add_entry(new_entry)
        _ = all_users_percentages.pop(self.username)
        self._balance_books(all_users_percentages, total_amount, message)
        print("The following information will be committed:")
        self._pretty_print([
            id_ for id_ in self.complete_ledger.keys() if type(id_) == int and id_ > start_commit_id
        ])
        print('\n')
        is_okay = get_bool_response()
        if is_okay:
            self._save_ledger()
        else:
            sys.exit('Exiting')

    def show_user_transactions(self):
        # TODO: Filter by datetime and other things as well
        ids = [
            id_ for id_ in self.complete_ledger.keys() if (self.complete_ledger[id_].get(self._group_entry_key, None) == self.group_label)
        ]
        self._pretty_print(ids)

    def _filter_transactions(self, key, value):
        ids = [
            id_ for id_ in self.complete_ledger.keys()
            if (self.complete_ledger[id_].get(key, None) == value)
        ]
        return {id_: self.complete_ledger[id_] for id_ in ids}

    def calc_user_debt(self):
        user_transactions = self._filter_transactions(self._user_entry_key, self.username)
        return sum([entry[self._total_due_entry_key] for entry in user_transactions.values()])

    def delete_transaction(self, id_):
        user_ids = [
            id_l for id_l in self.complete_ledger.keys()
            if ((self.complete_ledger[id_l].get(self._user_entry_key, None) == self.username)
            and (id_l != self._metadata_key))
        ]
        assert id_ in user_ids, "Transaction {} does not belong to user {}".format(id_, self.username)

        print("Delete transaction: \n")
        self._pretty_print([id_])
        resp = get_bool_response()
        if resp:
            _ = self.complete_ledger.pop(id_)
            self._save_ledger()
            print("Done.")
        else:
            sys.exit("Exiting")

    def _pretty_print(self, ids):
        non_id_cols = [
            self._dt_creation_key,
            self._user_entry_key,
            self._group_entry_key,
            self._total_amount_entry_key,
            self._norm_perc_entry_key,
            self._total_due_entry_key,
            self._message_entry_key
        ]
        headers = ['Transaction_ID']
        headers.extend(non_id_cols)
        data = [headers]

        values = list()
        for id_ in ids:
            value = [id_]
            lookup_dict = self.complete_ledger[id_]
            value.extend([
                lookup_dict[key] for key in non_id_cols
            ])
            values.append(value)
        data.extend(values)
        table = AsciiTable(data)
        print(table.table)
