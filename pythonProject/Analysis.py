from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


from db import get_habits, get_habit_tracker, get_current_streak, get_longest_streak


def all_habits_info(db):
    """
    A list of all saved habits and its data
    :param db: An initialized sqlite3 database connection.
    """
    info = get_habits(db)
    habits_list = [habit for habit in info]
    return habits_list


def all_habits_same_period(db, period):
    """
    Returns all habits with the same periodicity from the habits table (daily or weekly).
    :param db: An initialized sqlite3 database connection.
    :param period: Frequency for the search.
    """
    info = get_habits(db)

    # function to get habits filtered by period
    def per_sort(x):
        return x[2] == period

    # filters info by period
    period_list = list(filter(per_sort, info))
    # Return a list of habit names
    habit_names = [habit[0] for habit in period_list]
    return habit_names


def active_habits(db):
    """
    Returns a list of all habits that were not done today
    """
    info = get_habits(db)
    info_names = [habit[0] for habit in info]  # extract all habit names
    active_habits_list = []
    for name in info_names:
        tracker_dates = get_habit_tracker(db, name)
        if tracker_dates:
            last_check_off_date_time = tracker_dates[-1][1]
            last_check_off_date = datetime.strptime(last_check_off_date_time, "%d-%m-%Y %H:%M")
            # if last check-off date is not today, habit should be done
            if last_check_off_date.date() != datetime.today().date():
                active_habits_list.append(name)
        else:  # if still no checks-off, habit should be done
            active_habits_list.append(name)
    return active_habits_list


def current_streak_of_habit(db, name):
    """
    Returns the current streak of a given habit
    :param db:  a connection to a sqlite3 database
    :param name: name of the habit
    """
    current_streak = get_current_streak(db, name)
    return current_streak


def longest_streak_of_habit(db, name):
    """
    Returns the longest streak of a given habit
    :param db:  a connection to a sqlite3 database
    :param name: name of the habit
    """
    longest_streak = get_longest_streak(db, name)
    return longest_streak


def get_data(db):
    """
    Get data for the further use
    :param db: a connection to a sqlite3 database
    :return: tuple of three lists (names, current_streaks, longest_streaks)
    """
    info = get_habits(db)
    names = [habit[0] for habit in info]
    current_streaks = [habit[4] for habit in info]
    longest_streaks = [habit[5] for habit in info]
    broken = [habit[6] for habit in info]
    return names, current_streaks, longest_streaks, broken


def longest_streak_of_all(db):
    """
    Returns the longest streak of all habits
    :param db:  a connection to a sqlite3 database
    """
    # tuple unpacking
    names, current_streaks, longest_streaks, broken = get_data(db)
    max_streak = max(longest_streaks)

    # find all indexes where max_streak is found
    max_streak_indexes = []
    for x in range(len(longest_streaks)):
        if longest_streaks[x] == max_streak:
            max_streak_indexes.append(x)

    # get habit name for each index
    max_streak_names = []
    for x in max_streak_indexes:
        max_streak_names.append(names[x])

    return max_streak, max_streak_names


def hardest_habit(db):
    """
    Returns habits which ware broken most
    :param db:  a connection to a sqlite3 database
    """
    # tuple unpacking
    names, current_streaks, longest_streaks, broken = get_data(db)
    max_broken = max(broken)

    # find all indexes where max_broken is found
    max_broken_indexes = []
    for x in range(len(broken)):
        if broken[x] == max_broken:
            max_broken_indexes.append(x)

    # get habit name for each index
    max_broken_names = []
    for x in max_broken_indexes:
        max_broken_names.append(names[x])

    return max_broken, max_broken_names


def list_names(db):
    """
    Returns the list of names alphabetically sorted
    """
    names, current_streaks, longest_streaks, broken = get_data(db)
    names.sort()  # sort names alphabetically
    return names


def histogram_long(db):
    """
     Plot a horizontal bar graph,
     showing the longest streaks of habits
    """
    names, current_streaks, longest_streaks, broken = get_data(db)
    x = np.array(names)
    y = np.array(longest_streaks)  # longest_streaks data for y-axis

    plt.barh(x, y, height=0.4, color="cyan")

    plt.title("Longest streaks of habits")
    plt.xlabel("Longest streaks")
    plt.ylabel("Habits")
    plt.grid(axis='x')
    plt.show()


def histogram_current(db):
    """
     Plot a horizontal bar graph,
     showing the current streaks of habits
    """
    names, current_streaks, longest_streaks, broken = get_data(db)
    x = np.array(names)
    y = np.array(current_streaks)  # current_streaks data for y-axis

    plt.barh(x, y, height=0.4, color="green")

    plt.title("Current streaks of habits")
    plt.xlabel("Current streaks")
    plt.ylabel("Habits")
    plt.grid(axis='x')
    plt.show()
