from sqlite3 import IntegrityError, OperationalError
from typing import Any, Dict, Union
import logging
import sys
import argparse
import json
import openpyxl
from pathlib import Path# do I need metavar?
# actions
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class GoalsOption(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Do something custom with `values` here
        setattr(namespace, self.dest, values)


def read_json(pwd: Path) -> Dict[str, Any]:
    try:
        with open(pwd, 'r') as file:
            data = json.load(file)
            logging.info("JSON data loaded successfully:")
            return data
    except FileNotFoundError:
        logging.error("The file 'example.json' was not found.")
    except json.JSONDecodeError:
        logging.error("Error: Could not decode JSON from the file. Check if the file contains valid JSON.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def parser():
    parser = argparse.ArgumentParser(description="A program that calculates\
        the total nutrition consumed from meals and how much is left for\
        the day based on your nutrition goals.",
        usage= "meal_tracking.py [-h] [-v] -g GOALS_PATH -m MEALS_PATH"
    )
    parser.add_argument("-g","--goals",metavar="GOALS_PATH", type=Path, help="Path to a file containing nutrition goals (JSON).", action=GoalsOption)
    # parser.add_argument("-ig","--interactive-goals", help="Path to a file containing meals eaten today (JSON).")
    parser.add_argument("-m","--meals",metavar="MEALS_PATH", type=Path,help="Path to a file containing meals eaten today (JSON).")
    # parser.add_argument("-im","--interactive-meals", help="Path to a file containing meals eaten today (JSON).")
    parser.add_argument("-e","--create_excel", required=False, type= bool, help="create an excel based on the goals and meals given" )
    #interactive meals/ goals
    #adding argument of the excel that include the goals and meals so par
    
    return parser.parse_args()
    

def main():
    args = parser()
    meals = read_json(args.meals)
    goals = read_json(args.goals)
    print(f"hello {meals=} {type(meals)}| {goals=} {type(goals)}|")
    
    
if __name__ == "__main__":
    main()
