from datetime import datetime, timedelta

from db import (add_habit, delete_a_habit, increment_check_off,
                update_current_streak, update_longest_streak,
                update_broken, get_habit_tracker)


class Habits:

    def __init__(self, name: str, description: str, period: str, created: str = None,
                 current_streak: int = 0, longest_streak: int = 0, broken: int = 0):
        """
        Initialize a new Habit object.
        :param name (str): name of the habit
        :param description (str): description of the habit
        :param period (str): periodicity of the habit ("daily" or "weekly")
        :param created (str): date when the habit was created
        :param current_streak (int): current streak of the habit
        :param longest_streak (int): longest streak of the habit
        :param broken (int): number of times the habit was broken
        """
        self.name = name
        self.description = description
        self.period = period
        self.created = created
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.broken = broken

    def __str__(self):
        return f"The habit {self.name} to {self.description} should be done {self.period}"

    def create_habit(self, db):
        """
        Function to store a new habit into the Database, static table
        :param db: a connection to a sqlite3 database
        """
        if not self.created:
            self.created = datetime.now().strftime("%d-%m-%Y %H:%M")  # create a string from today date
        self.current_streak = 0           # sets current streak to 0
        self.longest_streak = 0           # sets longest streak to 0
        self.broken = 0                   # sets broken habit to 0
        add_habit(db, self.name, self.description, self.period, self.created,
                  self.current_streak, self.longest_streak, self.broken)

    def delete_habit(self, db):
        """
        Delete the habit from all the tables in the database
        :param db: a connection to a sqlite3 database
        """
        delete_a_habit(db, self.name)

    def increase_current_streak(self, db):
        """
        increment current streak by 1, evaluates if longest streak should be updated
        :param db: a connection to a sqlite3 database
        """
        self.current_streak += 1
        update_current_streak(db, self.name, self.current_streak)

        # checks if longest_streak has to be updated
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
            update_longest_streak(db, self.name, self.longest_streak)

    def reset_current_streak(self, db):
        """
        set current streak by 1 and increment broken by 1
        :param db: a connection to a sqlite3 database
        """
        self.current_streak = 1
        self.broken += 1
        update_current_streak(db, self.name, self.current_streak)
        update_broken(db, self.name, self.broken)

    def add_check_off(self, db, check_off_date=None):
        """
        adds a new check-off event to a given habit to the database
        :param db: a connection to a sqlite3 database
        :param check_off_date:  date and time of check-off
        """
        if not check_off_date:
            check_off_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        # if checked-off is counted as True
        if self.evaluate_check_off(db, check_off_date):  # get method from this class
            increment_check_off(db, self.name, check_off_date)
            return True
        # if habit was already checked off today
        else:
            return False

    def evaluate_check_off(self, db, check_off_date=None):
        """
        Evaluates whether check-off meet set period and writes info in database
        :param db:  a connection to a sqlite3 database
        :param check_off_date:  date and time of check-off
        """
        if not check_off_date:
            today = datetime.now()
        else:
            today = datetime.strptime(check_off_date, "%d-%m-%Y %H:%M")

        # count an amount of days in period for timedelta
        days_period = 7 if self.period == 'weekly' else 1

        habit_tracker = get_habit_tracker(db, self.name)
        # if tracker_dates exists
        if habit_tracker:
            # extracting from the last line [-1] date value [1]
            last_check_off_date_time = habit_tracker[-1][1]
            # converting string  into a datetime object
            last_check_off_date = datetime.strptime(last_check_off_date_time, "%d-%m-%Y %H:%M")

            # was already checked today
            if last_check_off_date.date() == today.date():
                return False

            # check inside given period - increase current streak
            elif last_check_off_date.date() >= today.date() - timedelta(days=days_period):
                self.increase_current_streak(db)  # get method from this class
                return True

            # checked outside the given period - habit is broken, reset current streak
            else:
                self.reset_current_streak(db)  # get method from this class
                return True

        # if tracker_dates empty - new start, increase current streak
        else:
            self.increase_current_streak(db)  # get method from this class
            return True
