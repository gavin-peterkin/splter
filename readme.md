# Splter

## A CLI application for keeping track of transactions with friends

A simple transparent way for splitting costs equitably among groups of people.

### Storage

All transaction entries and users are stored in a simple human-readable JSON format.
If you wanted to edit the files for some reason manually, you could do that, and the
application would perform as expected afterwards.

### Example use case

You go out for drinks every week with the same group of friends.
Rather than split the check somehow each time, one person picks it up, but without
tracking who has paid in the past and who hasn't, it's hard to tell who's getting
the sweet end of the deal.

Using the `splt` command, you set up a user account which is associated with a group.
Your user account also has a percentage associated with it, which allows you to scale
your burden relative to everyone else's. For example, if there's a multi-millionaire
in the group he/she could set his/her percentage to 5 million, and everyone else could set it
to say 100. The millionaire would have a much higher burden than the others.

Once a user enters a transaction, the ledger is "balanced" by adding a debt/credit to
all users associated with that grouping. Rather than having to continually have people
pay back other people, users can consult the ledger to see who should pay next, so a level
of equality can be achieved without any users ever having to exchange money amongst
themselves.

## Installation and Setup

It makes the most sense to install this on a shared computer or a server, so users
can remote in and enter their purchases into the ledger as they're accrued.

It requires unix and python2.

1. `git clone <path_to_this_repo>`
2. `cd` into `splter/src` and run `chmod +x setup.sh`
3. Execute `./setup.sh` or `./setup.sh <path_to_bashrc>` if you're bashrc is not `~/.bash_profile`
4. You're done! Run `splt <your_new_username>`

## Usage:

Your username is always required for any type of interaction with the ledger.

**usage**: `splt [-h] [-a | -l | -c | -d DELETE | -r REMOVE | -e EDIT] username`

positional arguments:
  username              Your username (str). If this is first time setup you
                        will be guided through the process
```
optional arguments:
  -h, --help            show this help message and exit
  -a, --add             A new transaction will be added to the ledger.
  -l, --list            List all previous transactions involving user or
                        user's groups
  -c, --calc            Calculate what the user owes or is owed
  -d DELETE, --delete DELETE
                        Delete transaction by it's ID
  -r REMOVE, --remove REMOVE
                        Remove user by their name. Note that their past
                        transactions will remain.
  -e EDIT, --edit EDIT  Edit a user's default percentage to be a new value
```
