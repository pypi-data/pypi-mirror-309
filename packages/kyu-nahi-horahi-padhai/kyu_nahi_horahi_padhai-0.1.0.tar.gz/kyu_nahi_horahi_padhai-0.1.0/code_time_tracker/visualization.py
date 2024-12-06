# code_time_tracker/visualization.py

import matplotlib.pyplot as plt

def plot_daily_activity(daily_summary):
    daily_summary.plot(kind="bar")
    plt.title("Daily Coding Time")
    plt.xlabel("Date")
    plt.ylabel("Coding Duration (seconds)")
    plt.show()

