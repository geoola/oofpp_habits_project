# Habit Tracking App
Habit Tracking App help to cultivate positive habits, achieve their goals by providing a systematic and organized approach to monitor behavior.

## Features

- Create a habit - creates a new habit;
- Delete a habit - deletes a specific habit;
- Check-off a habit - check-off a specific habit;
- Analyse habits - analyse all habits together or separately:
  - Habits Info - info about habit:
    - List of all habits;
    - List of active habits;
    - Show habits with same period;
    - Show longest streak of habit;
    - Show current streak of a habit;
  - Best and worst habit - shows habit with the biggest value of longrun or broken streaks:
    - Best habit;
    - Worst habit;
  - Histogram view - plot a horizontal bar graph:
    - Habit's current streaks - current streaks of habits;
    - Habit's longest streaks - longest streaks of habits.

## Installation
This project uses Python version 3.11, ensure that Python 3.11 or higher is installed on your system. 
Use the following command to install the required packages:

    pip install -r requirements.txt

This  command will install the following packages necessary to run the program:
- Pytest - allows to run tests;
- questionary - provides command line interface;
- numpy - enables operations with arrays;
- matplotlib - provides graphing and charting capabilities.

## Usage
Start the application with:

    python main.py

Follow instructions in the terminal to handle habits.

## Tests
To run tests, use the following command:

    python -m pytest
