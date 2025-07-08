from sqlite3 import IntegrityError, OperationalError
from typing import Any, Dict, Union
import logging
import sys
import argparse
import json
from pathlib import Path# do I need metavar?
# actions

class GoalsOption(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Do something custom with `values` here
        setattr(namespace, self.dest, values)


def read_file(pwd: Path) -> Dict[str, Any]:
    with open(pwd, 'r') as file:
        return file.read()


def parser():
    parser = argparse.ArgumentParser(description="A program that calculates\
        the total nutrition consumed from meals and how much is left for\
        the day based on your nutrition goals.",
        usage= "meal_tracking.py [-h] [-v] -g GOALS_PATH -m MEALS_PATH"
    )
    parser.add_argument("-g","--goals",metavar="GOALS_PATH", type=Path, help="Path to a file containing nutrition goals (JSON).", action=GoalsOption)
    parser.add_argument("-ig","--interactive-goals", help="Path to a file containing meals eaten today (JSON).")
    parser.add_argument("-m","--meals",metavar="MEALS_PATH", type=Path,help="Path to a file containing meals eaten today (JSON).")
    parser.add_argument("-im","--interactive-meals", help="Path to a file containing meals eaten today (JSON).")
    parser.add_argument("-e","--create_excel", required=False, type= bool, help="create an excel based on the goals and meals given" )
    #interactive meals/ goals
    #adding argument of the excel that include the goals and meals so par
    
    return parser.parse_args()
    

def main():
    args = parser()
    meals = read_file(args.meals)
    goals = read_file(args.goals)
    print(f"hello {meals=} | {goals=}")
    
    
if __name__ == "__main__":
    main()
