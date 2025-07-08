from sqlite3 import IntegrityError, OperationalError
from typing import Union
import logging
import sys
import argparse


class GoalsOption(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Do something custom with `values` here
        setattr(namespace, self.dest, values)

def parser():
    pass


def goals_option(pwd: str):
    print("goals")

def meals_option(meals_path: str):
    print(f"meals {meals_path}")
    


def user_input():
    pass
        



def main():
    logging.info("starting..")
    parser = argparse.ArgumentParser(description="A program that calculates\
        the total nutrition consumed from meals and how much is left for\
        the day based on your nutrition goals.",
        usage= "meal_tracking.py [-h] [-v] -g GOALS_PATH -m MEALS_PATH"
    )
    parser.add_argument("-g","--goals",metavar="GOALS_PATH", help="Path to a file containing nutrition goals (JSON).", action=GoalsOption)
    parser.add_argument("-m","--meals",metavar="MEALS_PATH", help="Path to a file containing meals eaten today (JSON).")
    parser.add_argument("-e","--create_excel", required=False, help="create an excel based on the goals and meals given" )
    args = parser.parse_args()
    print(args)
    
    
if __name__ == "__main__":
    main()
