# code_time_tracker/analytics.py

import pandas as pd

def get_summary(log_file):
    df = pd.read_csv(log_file, names=["start_time", "end_time", "duration"])
    df["date"] = pd.to_datetime(df["start_time"]).dt.date
    daily_summary = df.groupby("date")["duration"].sum()
    return daily_summary

