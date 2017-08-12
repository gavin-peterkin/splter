from utility import get_bool_response, get_validate_response
from user import User
from ledger import Ledger


import sys


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'username', type=str,
        help='Your username (str). If this is first time setup you will be guided\
        through the process'
    )
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        '-a', '--add',
        help='A new transaction will be added to the ledger.',
        action='store_true'
    )
    action_group.add_argument(
        '-l', '--list',
        help='List all previous transactions invloving user or user\'s groups',
        action='store_true'
    )
    action_group.add_argument(
        '-c', '--calc',
        help='Calculate what the user owes or is owed',
        action='store_true'
    )
    action_group.add_argument(
        '-d', '--delete', type=str,
        help='Delete transaction by it\'s ID'
    )
    action_group.add_argument(
        '-r', '--remove', type=str,
        help='Remove user by their name. Note that their past transactions will remain.'
    )
    action_group.add_argument(
        '-e', '--edit', type=float,
        help='Edit a user\'s default percentage to be a new value'
    )
    return parser.parse_args()


def add_user_transaction(user, ledger):
    print('Please enter the total amount that you paid.')
    total_amount = get_validate_response(input_type='the dollar amount', object_type=float)
    print('Enter an optional message to desribe the transaction.')
    message = get_validate_response(input_type='message', object_type=str)
    ledger.add_transaction(
        user.username, total_amount,
        user.all_users_percentages, message=message
    )


def calc_user_debt(ledger):
    amount_due = ledger.calc_user_debt()
    print("You owe (+) or are owed (-): {:.2f}".format(amount_due))


def perform_action(pargs, user, ledger):
    if pargs.add:
        add_user_transaction(user, ledger)
    elif pargs.list:
        ledger.show_user_transactions()
    elif pargs.calc:
        calc_user_debt(ledger)
    elif pargs.delete != None:
        id_ = str(pargs.delete)
        ledger.delete_transaction(id_)
    elif pargs.remove:
        user.remove_user()
    elif pargs.edit != None:
        user.update_percentage(pargs.edit)


def main():
    try:
        pargs = parse_args()
        user = User(pargs.username)
        ledger = Ledger(user.username, user.group_label)
        perform_action(pargs, user, ledger)
    except KeyboardInterrupt:
        sys.exit('Exiting')


if __name__ == '__main__':
    main()
