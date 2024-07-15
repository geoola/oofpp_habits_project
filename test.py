from Habit import Habits
from db import (get_db,  get_habits, get_habit_tracker, get_tracker_names,
                get_current_streak, get_longest_streak, get_broken)
from Analysis import (all_habits_info, all_habits_same_period, active_habits, get_data,
                      current_streak_of_habit, longest_streak_of_habit,
                      longest_streak_of_all, hardest_habit, list_names)
import os


class TestHabits:

    def setup_method(self):
        self.db = get_db("test1113.db")
        # daily habits
        daily_habit_1 = Habits("doing sport", "do at least 30 min spot", "daily", "01-05-2024 12:00")
        daily_habit_1.create_habit(self.db)
        daily_habit_2 = Habits("drinking water", "drink at least 2 l of water", "daily", "01-05-2024 12:00")
        daily_habit_2.create_habit(self.db)
        daily_habit_3 = Habits("avoiding sweets", "avoid eating sweets", "daily", "01-05-2024 12:00")
        daily_habit_3.create_habit(self.db)
        # weekly habits
        daily_habit_4 = Habits("meeting friends", "go out with friends", "weekly", "01-05-2024 12:00")
        daily_habit_4.create_habit(self.db)
        daily_habit_5 = Habits("reading", "read one book per week", "weekly", "01-05-2024 12:00")
        daily_habit_5.create_habit(self.db)

        # testing creation in db
        assert get_habits(self.db) == [("doing sport", "do at least 30 min spot", "daily", "01-05-2024 12:00", 0, 0, 0),
                                       ("drinking water", "drink at least 2 l of water", "daily", "01-05-2024 12:00", 0, 0, 0),
                                       ("avoiding sweets", "avoid eating sweets", "daily", "01-05-2024 12:00", 0, 0, 0),
                                       ("meeting friends", "go out with friends", "weekly", "01-05-2024 12:00", 0, 0, 0),
                                       ("reading", "read one book per week", "weekly", "01-05-2024 12:00", 0, 0, 0)]

        # daily habit check off
        daily_habit_1.add_check_off(self.db, "01-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "03-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "04-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "05-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "06-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "07-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "12-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "13-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "14-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "16-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "19-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "22-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "23-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "24-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "26-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "27-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "28-05-2024 12:00")
        daily_habit_1.add_check_off(self.db, "29-05-2024 12:00")
        # daily habit check off
        daily_habit_2.add_check_off(self.db, "01-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "02-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "04-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "05-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "06-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "07-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "12-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "13-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "14-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "15-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "16-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "22-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "23-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "24-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "26-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "27-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "28-05-2024 12:00")
        daily_habit_2.add_check_off(self.db, "29-05-2024 12:00")
        # daily habit check off
        daily_habit_3.add_check_off(self.db, "01-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "02-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "08-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "15-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "16-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "17-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "23-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "24-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "25-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "29-05-2024 12:00")
        daily_habit_3.add_check_off(self.db, "30-05-2024 12:00")
        # weekly habit 4
        daily_habit_4.add_check_off(self.db, "01-05-2024 12:00")
        daily_habit_4.add_check_off(self.db, "06-05-2024 12:00")
        daily_habit_4.add_check_off(self.db, "12-05-2024 12:00")
        daily_habit_4.add_check_off(self.db, "18-05-2024 12:00")
        daily_habit_4.add_check_off(self.db, "24-05-2024 12:00")
        daily_habit_4.add_check_off(self.db, "30-05-2024 12:00")
        # weekly habit 5 - broken
        daily_habit_5.add_check_off(self.db, "01-05-2024 12:00")
        daily_habit_5.add_check_off(self.db, "08-05-2024 12:00")
        daily_habit_5.add_check_off(self.db, "14-05-2024 12:00")
        daily_habit_5.add_check_off(self.db, "22-05-2024 12:00")
        daily_habit_5.add_check_off(self.db, "29-05-2024 12:00")

    def test_habit_class(self):
        habit_daily = Habits("test_habit_daily", "test_description", "daily")
        habit_weekly = Habits("test_habit_weekly", "test_description", "weekly")

        # testing create
        habit_daily.create_habit(self.db)
        habit_weekly.create_habit(self.db)
        expected_str_daily = "The habit test_habit_daily to test_description should be done daily"
        expected_str_weekly = "The habit test_habit_weekly to test_description should be done weekly"
        assert str(habit_daily) == expected_str_daily
        assert str(habit_weekly) == expected_str_weekly

        # tests if new check-off is provided
        habit_daily.add_check_off(self.db)
        habit_weekly.add_check_off(self.db)
        assert len(get_habit_tracker(self.db, "test_habit_daily")) == 1
        assert len(get_habit_tracker(self.db, "test_habit_weekly")) == 1
        assert habit_daily.current_streak == 1
        assert habit_weekly.current_streak == 1

        # tests if streak can get incremented twice a day
        habit_daily.add_check_off(self.db)
        habit_weekly.add_check_off(self.db)
        assert habit_daily.current_streak == 1
        assert habit_weekly.current_streak == 1

        # extra tests for increase_current_streak
        habit_daily.increase_current_streak(self.db)
        habit_weekly.increase_current_streak(self.db)
        assert habit_daily.current_streak == 2
        assert habit_weekly.current_streak == 2
        assert habit_daily.longest_streak == 2
        assert habit_weekly.longest_streak == 2

        # tests for reset_current_streak
        habit_daily.reset_current_streak(self.db)
        habit_weekly.reset_current_streak(self.db)
        assert habit_daily.current_streak == 1
        assert habit_weekly.current_streak == 1
        assert habit_daily.broken == 1
        assert habit_weekly.broken == 1

        # tests if deleted
        habit_daily.delete_habit(self.db)
        habit_weekly.delete_habit(self.db)
        # to ensure that the habit does not exist in the table Habits
        remaining_habits = get_habits(self.db)
        assert ("test_habit_daily", "test_description", "daily") not in remaining_habits
        assert ("test_habit_weekly", "test_description", "weekly") not in remaining_habits
        # to ensure that the habit does not exist in the table Tracker
        remaining_tracker = get_tracker_names(self.db)
        assert ("test_habit_daily",) not in remaining_tracker
        assert ("test_habit_weekly",) not in remaining_tracker

    def test_add_check_off_daily(self):
        # create the habit
        habit = Habits("test_habit_daily", "test_description", "daily")
        habit.create_habit(self.db)

        # add a new check-off and ensure it was added
        assert habit.add_check_off(self.db, "01-01-2022 12:00") is True
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 1

        # Validate the current streak
        assert habit.current_streak == 1
        assert habit.longest_streak == 1

        # Add a check-off for the same day and ensure it wasn't added
        assert habit.add_check_off(self.db, "01-01-2022 12:00") is False
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 1

        # validate the current streak is still 1
        assert habit.current_streak == 1
        assert habit.longest_streak == 1

        # test for next day, it should increase the current streak
        assert habit.add_check_off(self.db, "02-01-2022 12:00") is True
        assert habit.current_streak == 2
        assert habit.longest_streak == 2
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 2

        # test for outside the period (over a day later for a daily habit)
        # it should reset the current streak and still add the check-off
        assert habit.add_check_off(self.db, "04-01-2022 12:00") is True
        assert habit.current_streak == 1
        assert habit.longest_streak == 2
        assert habit.broken == 1
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 3

    def test_add_check_off_weekly(self):
        # create the habit
        habit = Habits("test_habit_daily", "test_description", "weekly")
        habit.create_habit(self.db)

        # add a new check-off and ensure it was added
        assert habit.add_check_off(self.db, "01-01-2022 12:00") is True
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 1

        # validate the current streak
        assert habit.current_streak == 1
        assert habit.longest_streak == 1

        # add a check-off for the same day and ensure it wasn't added
        assert habit.add_check_off(self.db, "01-01-2022 12:00") is False
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 1
        # current streak should be still 1
        assert habit.current_streak == 1
        assert habit.longest_streak == 1

        # test for next day. It should increase the current streak
        assert habit.add_check_off(self.db, "06-01-2022 12:00") is True
        # current streak should be 2
        assert habit.current_streak == 2
        assert habit.longest_streak == 2
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 2

        # test for outside the period
        assert habit.add_check_off(self.db, "14-01-2022 12:00") is True
        # reset the current streak to 1 and increase the broken to 1
        assert habit.current_streak == 1
        assert habit.longest_streak == 2
        assert habit.broken == 1
        habit_tracker = get_habit_tracker(self.db, habit.name)
        assert len(habit_tracker) == 3

    def test_db(self):
        assert len(get_habit_tracker(self.db, "doing sport")) == 18
        assert len(get_habit_tracker(self.db, "drinking water")) == 18
        assert len(get_habit_tracker(self.db, "avoiding sweets")) == 11
        assert len(get_habit_tracker(self.db, "meeting friends")) == 6
        assert len(get_habit_tracker(self.db, "reading")) == 5

        assert len(get_habits(self.db)) == 5

        assert get_current_streak(self.db, "doing sport") == 4
        assert get_current_streak(self.db, "drinking water") == 4
        assert get_current_streak(self.db, "avoiding sweets") == 2
        assert get_current_streak(self.db, "meeting friends") == 6
        assert get_current_streak(self.db, "reading") == 2

        assert get_longest_streak(self.db, "doing sport") == 5
        assert get_longest_streak(self.db, "drinking water") == 5
        assert get_longest_streak(self.db, "avoiding sweets") == 3
        assert get_longest_streak(self.db, "meeting friends") == 6
        assert get_longest_streak(self.db, "reading") == 3

        assert get_broken(self.db, "doing sport") == 6
        assert get_broken(self.db, "drinking water") == 4
        assert get_broken(self.db, "avoiding sweets") == 4
        assert get_broken(self.db, "meeting friends") == 0
        assert get_broken(self.db, "reading") == 1

    def test_analysis(self):

        assert all_habits_info(self.db) == [
            ("doing sport", "do at least 30 min spot", "daily", "01-05-2024 12:00", 4, 5, 6),
            ("drinking water", "drink at least 2 l of water", "daily", "01-05-2024 12:00", 4, 5, 4),
            ("avoiding sweets", "avoid eating sweets", "daily", "01-05-2024 12:00", 2, 3, 4),
            ("meeting friends", "go out with friends", "weekly", "01-05-2024 12:00", 6, 6, 0),
            ("reading", "read one book per week", "weekly", "01-05-2024 12:00", 2, 3, 1)]

        assert all_habits_same_period(self.db, "daily") == ["doing sport", "drinking water", "avoiding sweets"]
        assert all_habits_same_period(self.db, "weekly") == ["meeting friends", "reading"]

        assert len(active_habits(self.db)) == 5

        assert current_streak_of_habit(self.db, "doing sport") == 4
        assert current_streak_of_habit(self.db, "meeting friends") == 6
        assert longest_streak_of_habit(self.db, "doing sport") == 5
        assert longest_streak_of_habit(self.db, "meeting friends") == 6

        assert len(get_data(self.db)) == 4  # 4 values names, current_streaks, longest_streaks, broken
        assert get_data(self.db) == (['doing sport', 'drinking water', 'avoiding sweets', 'meeting friends', 'reading'],
                                     [4, 4, 2, 6, 2], [5, 5, 3, 6, 3], [6, 4, 4, 0, 1])

        assert longest_streak_of_all(self.db) == (6, ["meeting friends"])
        assert hardest_habit(self.db) == (6, ["doing sport"])

        assert list_names(self.db) == ["avoiding sweets", "doing sport", "drinking water", "meeting friends", "reading"]

    def teardown_method(self):
        self.db.close()
        os.remove("test1113.db")
