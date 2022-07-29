# -*- coding: utf-8 -*-
"""
A library of some useful functions for calculating dates

Created on Sun Apr 24 10:56:35 2022

@author: Dylan Munro
"""

import pandas as pd
JANUARY = 1
FEBRUARY = 2
MARCH = 3
APRIL = 4
MAY = 5
JUNE = 6
JULY = 7
AUGUST = 8
SEPTEMBER = 9
OCTOBER = 10
NOVEMBER = 11
DECEMBER = 12

# Days in each month for a non-leap year
DAYS_PER_MONTH = {
    JANUARY: 31,
    FEBRUARY: 28,
    MARCH: 31,
    APRIL: 30,
    MAY: 31,
    JUNE: 30,
    JULY: 31,
    AUGUST: 31,
    SEPTEMBER: 30,
    OCTOBER: 31,
    NOVEMBER: 30,
    DECEMBER: 31
}


def is_leap_year(year):
    """
    Determines if a year is a leap year
    """
    # Is leap year if the year is a multiple of 400, or
    # the year is a multiple of 4 but not of 100
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    return False


def get_tomorrow(date):
    """
    Returns tomorrows date in the format (yyyy-mm-dd)

    Args:
        date - The current date in the format (yyyy-mm-dd)
    """
    if not _is_valid_format(date):
        raise ValueError("The date {} is invalid".format(date))
    components = date.split("-")
    year = int(components[0])
    month = int(components[1])
    day = int(components[2])

    # Get tomorrow's date on New Year's Eve
    if month == DECEMBER and day == DAYS_PER_MONTH.get(DECEMBER):
        year = year + 1
        month = JANUARY
        day = 1

    # Get tomorrow's date for February 29 on a leap year
    elif month == FEBRUARY and day == 29:
        month = month + 1
        day = 1

    # Get tomorrow's date for February 28 on a leap year
    elif is_leap_year(year) and month == FEBRUARY and day == 28:
        day = day + 1

    # Get tomorrow's date for any other last day of the month
    elif DAYS_PER_MONTH.get(month) == day:
        month = month + 1
        day = 1

    # Get tomorrow's date for any other day
    else:
        day = day + 1

    days_into_year = _get_num_of_days_into_year(year, month, day)
    return _get_new_date(year, days_into_year)


def get_future_date(date, days_into_future):
    """
    Returns the date a certain number of days into the future

    Args:
        date - The current date in the format (yyyy-mm-dd)
        days_into_future - The number of days into the future of the new date

    Returns: New date the associated number of days into the future
    """
    if not _is_valid_format(date):
        raise ValueError("The date {} is invalid".format(date))
    components = date.split("-")
    year = int(components[0])
    month = int(components[1])
    day = int(components[2])
    days_into_year = _get_num_of_days_into_year(year, month, day)
    days_into_year = days_into_year + days_into_future
    return _get_new_date(year, days_into_year)


def _get_days_in_year(year):
    """
    Returns the number of days in the specified year
    """
    if is_leap_year(year):
        return 366
    return 365


def _get_new_date(current_year, days_remaining):
    """
    Returns the date of a day a certain number of days into the year
    """
    # Get year
    days_in_current_year = _get_days_in_year(current_year)
    while days_remaining > days_in_current_year:
        days_remaining = days_remaining - days_in_current_year
        current_year = current_year + 1
        days_in_current_year = _get_days_in_year(current_year)

    # Get month
    current_month = JANUARY
    days_in_current_month = DAYS_PER_MONTH[current_month]
    while days_remaining > days_in_current_month:
        days_remaining = days_remaining - days_in_current_month
        current_month = current_month + 1
        days_in_current_month = DAYS_PER_MONTH[current_month]
        if (current_month == FEBRUARY and is_leap_year(current_year)):
            days_in_current_month = days_in_current_month + 1

    # Adjust month into format mm
    month_str = str(current_month)
    if len(month_str) == 1:
        month_str = "".join(["0", month_str])

    # Adjust day into format dd
    day_str = str(days_remaining)
    if len(day_str) == 1:
        day_str = "".join(["0", day_str])

    return "-".join([str(current_year), month_str, day_str])


def _get_num_of_days_into_year(year, month, day):
    """
    Determines how many days into a year a date is

    Returns: The number of days the date is into the year
    """
    days_into_year = 0
    days_into_year = days_into_year + day
    leap_year = is_leap_year(year)
    # Are no days left in current month, so start at previous month
    for current in range(month - 1, 0, -1):
        days_into_year = days_into_year + DAYS_PER_MONTH[current]
        if leap_year and current == FEBRUARY:
            days_into_year = days_into_year + 1
    return days_into_year


def _is_valid_format(date):
    """
    Determines if a date is in the format yyyy-mm-dd
    """
    components = date.split("-")

    # Check length of date, month, and year
    if (len(components) != 3 or len(components[0]) != 4 or
            len(components[1]) != 2 or len(components[2]) != 2):
        return False

    # Check if date, month and year are numeric
    for component in components:
        if not component.isnumeric():
            return False

    year = int(components[0])
    month = int(components[1])
    day = int(components[2])
    if month < JANUARY or month > DECEMBER:
        return False

    # Check if the month contains specified number of days
    if ((day > DAYS_PER_MONTH[month])
            and (not (is_leap_year(year) and month == FEBRUARY and day == 29))):
        return False

    return True
