from questionary import select, text

from Analysis import (all_habits_info, all_habits_same_period, active_habits, list_names,
                      longest_streak_of_habit, current_streak_of_habit,
                      longest_streak_of_all, hardest_habit, histogram_current, histogram_long)
from Habit import Habits
from db import get_db


def cli():
    db = get_db()
    '''the whole menu is inserted in a while-loop. Thus, whatever the user decides to do, they will be returned to the
    main menu, referred to below as "path", unless they choose the option "Exit the app". Should they choose
    the option "Exit the app", a goodbye-statement will be printed and the loop will break'''

    stop = False
    while not stop:
        choice = select("What would you like to do?",
                        choices=["Create a habit", "Delete a habit", "Check-off a habit",
                                 "Analyse habits", "Exit"]).ask()
        # if the user chooses the first option "Create a habit"
        if choice == "Create a habit":
            print(f"Here are existing habits:")
            # retrieve list of all habit names
            existing_habits = list_names(db)
            for habit_name in existing_habits:
                print(habit_name)
            # input name in lower case
            name = (text("What's the name of your new habit?").ask()).lower()
            if name not in existing_habits:
                # input description
                description = text("Describe your habit in few words").ask()
                # input period
                period = select("How often should it be checked-off?",
                                choices=["daily", "weekly"]).ask()
                # create a new Habit object with the input name, description and period
                new_habit = Habits(name, description, period)
                # call the create_habit method of the Habit class to store the new habit in the database
                new_habit.create_habit(db)
                print(f"Habit {name} is created. It should be done {period}")
            else:
                print(f"Habit {name} already exists in the database. Please enter another habit name.")
                continue

        elif choice == "Delete a habit":
            existing_habits = list_names(db)
            print("Your habits:")
            for habit_name in existing_habits:
                print(habit_name)
            # input name in lower case
            habit_to_delete = text("Type the name of the habit you would like to delete:").ask().lower()
            if habit_to_delete in existing_habits:
                confirmation = select("Are you sure you want to delete the habit?",
                                      choices=['Yes', 'No']).ask()
                if confirmation == 'Yes':
                    to_delete = Habits(habit_to_delete, "", "")
                    # call delete_habit method
                    to_delete.delete_habit(db)
                    print(f"Habit {habit_to_delete} has been deleted from the database")
                else:
                    print(f"Habit {habit_to_delete} is still in the database")
            else:
                print(f"Sorry, the name {habit_to_delete} does not exist on the database!")

        elif choice == "Check-off a habit":
            existing_habits = all_habits_info(db)
            # show list of habit names to the user
            print("Your habits:")
            for habit_name in existing_habits:
                print(habit_name[0])
            habit_to_check_off = text("Enter the name of the habit you would like to check-off: ").ask().lower()
            # checking the user's selected habit from the list of provided habits
            for habit_item in existing_habits:
                if habit_item[0] == habit_to_check_off:
                    habit_details = habit_item
                    name = habit_details[0]
                    description = habit_details[1]
                    period = habit_details[2]
                    created = habit_details[3]
                    current_streak = habit_details[4]
                    longest_streak = habit_details[5]
                    broken = habit_details[6]
                    # create a new Habit object with these details from database
                    new_check = Habits(name, description, period, created, current_streak, longest_streak, broken)
                    check_off_result = new_check.add_check_off(db)
                    # if checked off was done
                    if check_off_result:
                        print(f"You successfully checked off the {name}!")
                    # if checked off was not done, as it was done before today
                    else:
                        print(f"You have already checked off {name} today.")
                    break
            else:
                print("Please select a habit to check-off")

        elif choice == "Analyse habits":
            # submenu is displayed that allows the user to choose the type of analysis
            back_to_main_menu = False
            while not back_to_main_menu:
                choice_sub = select("What would you like to watch?",
                                    choices=["Habits Info", "Best and worst habit",
                                             "Histogram view", "Back to main menu"]).ask()

                if choice_sub == "Habits Info":
                    info = select("What analysis would you like to perform?",
                                  choices=["List of all habits", "List of active habits",
                                           "Show habits with same period", "Show longest streak of habit",
                                           "Show current streak of a habit"]).ask()

                    if info == "List of all habits":
                        # retrieve list of all habits
                        all_habits = all_habits_info(db)
                        if all_habits:
                            print(f"You have {len(all_habits)} habit(s):\n")
                            for habit in all_habits:
                                print(f"Habit             : {habit[0]}")
                                print(f"Description       : {habit[1]}")
                                print(f"Period            : {habit[2]}")
                                print(f"Created on        : {habit[3]}")
                                print(f"Current Streak    : {habit[4]}")
                                print(f"Longest Streak    : {habit[5]}")
                                print(f"Broken            : {habit[6]}")
                                print("\n")
                        # if there is no data
                        else:
                            print(f"You have no habits")

                    elif info == "List of active habits":
                        # retrieve list of all active habits
                        active_habits_list = active_habits(db)
                        if active_habits_list:
                            print(f"You have {len(active_habits_list)} habit(s) to do:")
                            for every_habit in active_habits_list:
                                print(every_habit)
                        else:
                            print("No habits for today")

                    elif info == "Show habits with same period":
                        # retrieve list of all habits with the same periodicity
                        period = (text("What periodicity:daily or weekly?").ask()).lower()
                        if period:
                            period_list = all_habits_same_period(db, period)
                            print(f"You have {len(period_list)} {period} habits:")
                            for x in period_list:
                                print(f"Habit  : {x}")
                        else:
                            print(f"You have no {period} habits")

                    elif info == "Show longest streak of habit":
                        # show list of habit names
                        habit_list = list_names(db)
                        for habit_name in habit_list:
                            print(habit_name)
                        # asking the name of the habit
                        name = (text("Please enter the name of the habit:").ask()).lower()
                        if name:
                            try:
                                show_longest_streak = longest_streak_of_habit(db, name)
                                print(f"The longest streak of {name} is: {show_longest_streak}")
                            except ValueError as e:
                                print(e)  # prints the error message from the exception
                        else:
                            print("Please enter the correct name")

                    elif info == "Show current streak of a habit":
                        # show list of habit names
                        habit_list = list_names(db)
                        for habit_name in habit_list:
                            print(habit_name)
                        # asking the name of the habit
                        name = (text("Please enter the name of the habit:").ask()).lower()
                        if name:
                            try:
                                show_current_streak = current_streak_of_habit(db, name)
                                print(f"Current streak of {name} is: {show_current_streak}")
                            except ValueError as e:
                                print(e)  # prints the error message from the exception
                        else:
                            print("Please enter the correct name")

                elif choice_sub == "Best and worst habit":
                    choice_bw = select("Do you want to see best or worst of your habits?:",
                                       choices=["Best habit", "Worst habit"]).ask()

                    if choice_bw == "Best habit":
                        max_streak, max_streak_names = longest_streak_of_all(db)  # unpacking
                        if max_streak:  # if no data in the table
                            print(f"The highest streak {max_streak} belongs to: {max_streak_names}")
                        else:
                            print("There are no records in the database")

                    elif choice_bw == "Worst habit":
                        max_broken, max_broken_names = hardest_habit(db)  # unpacking
                        if max_broken:  # if no data in the table
                            print(f"The most broken habit(s) with {max_broken} breaks: {max_broken_names}")
                        else:
                            print("There are no records in the database")

                elif choice_sub == "Histogram view":
                    choice_his = select("Choose a histogram:",
                                        choices=["Habit's current streaks", "Habit's longest streaks"]).ask()

                    if choice_his == "Habit's current streaks":
                        histogram_current(db)

                    elif choice_his == "Habit's longest streaks":
                        histogram_long(db)

                elif choice_sub == "Back to main menu":
                    # stop the 'analyse habits' loop and return to the main menu
                    back_to_main_menu = True

        elif choice == "Exit":
            print("Hope to see you soon!")
            stop = True


if __name__ == '__main__':
    cli()
