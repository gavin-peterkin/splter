# Splitwiser

## Requirements:
* Python 3.5 or better
* Pandas
* Tabulate

(pip install packages if necessary)

## Usage:
Command line utility for splitting and tracking purchases for two or more people.


### Syntax:
*usage*: splt [-h] [-a ADD | -c | -l | -d DELETE] [-p PERCENTAGE] [-m MESSAGE]
            user

#### Positional arguments:  
  `setup` Walks user through default set up.  
  `user` The user.

#### Optional arguments:
  -h, --help            show this help message and exit  
  -a ADD, --add ADD     The dollar amount that the user paid  
  -c, --calc            Calculate what the user owes or is owed  
  -l, --list            List all previous transactions  
  -d DELETE, --delete DELETE  
                        Delete row by index  
  -p PERCENTAGE, --percentage PERCENTAGE  
                        The fraction that the payer is responsible for. Must  
                        be between 0 and 1 inclusive.  
  -m MESSAGE, --message MESSAGE  
                        Optional message about the transaction  
