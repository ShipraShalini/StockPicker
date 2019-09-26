import difflib
import sys

import arrow
from arrow.parser import ParserError

from constants import FORMATS_DATE_ARROW


class UserInput:

    BOOL_DICT = {'y': True}
    NO_OF_MATCHES = 5

    OPTION_NONE = 'None of these.'

    MESSAGE_STOCK_NAME = 'Which stock you need to process:\t'
    MESSAGE_START_DATE = 'From which date you want to start:\t'
    MESSAGE_END_DATE = 'Till which date you want to analyze:\t'
    MESSAGE_SUGGESTION = 'Sorry! Did you mean any of the following?'
    MESSAGE_NOT_FOUND = ('Sorry! Data for {} is not present. Would you like '
                         'to process any other stock? (Y or N):\t')
    MESSAGE_TRY_AGAIN = 'Would you like to try again? (Y or N):\t'

    MESSAGE_ENTER_STOCK_NUMBER = 'Please enter the stock number:\t'
    MESSAGE_ENTER_VALID_OPTION = 'Please enter a valid option:\t'
    MESSAGE_ENTER_VALID_DATE = 'Please enter a valid date:\t'

    def __init__(self, stock_names):
        self.stock_names = stock_names

    def __call__(self):
        name = self.get_stock_name()
        start_date, end_date = self.get_dates()

        return {
            'name': name,
            'start_date': start_date,
            'end_date': end_date
        }

    def get_stock_name(self):
        name = input(self.MESSAGE_STOCK_NAME).upper()
        if name in self.stock_names:
            return name
        close_matches = difflib.get_close_matches(name, self.stock_names,
                                                  self.NO_OF_MATCHES)
        if not close_matches:
            if self._get_boolean_answer(self.MESSAGE_NOT_FOUND):
                self.get_stock_name()
            self.abort()

        print(self.MESSAGE_SUGGESTION)
        print('0: {}'.format(self.OPTION_NONE))
        for i, match in enumerate(close_matches, start=1):
            print('{}: {}'.format(i, match))

        message = self.MESSAGE_ENTER_STOCK_NUMBER
        while True:
            try:
                stock_number = int(input(message))
                break
            except ValueError:
                message = self.MESSAGE_ENTER_VALID_OPTION

        if stock_number == 0:
            if self._get_boolean_answer(self.MESSAGE_TRY_AGAIN):
                self.get_stock_name()
            self.abort()
        return close_matches[stock_number - 1]

    def get_dates(self):
        start_date = self._get_date(self.MESSAGE_START_DATE)
        end_date = self._get_date(self.MESSAGE_END_DATE)

        if start_date > end_date:
            return end_date, start_date
        return start_date, end_date

    def _get_date(self, message):
        while True:
            date_str = input(message)
            try:
                return arrow.get(date_str, FORMATS_DATE_ARROW)
            except (ParserError, ValueError):
                message = self.MESSAGE_ENTER_VALID_DATE

    @staticmethod
    def abort():
        sys.exit(1)

    def _get_boolean_answer(self, message):
        choice = input(message).lower()
        return self.BOOL_DICT.get(choice, False)
