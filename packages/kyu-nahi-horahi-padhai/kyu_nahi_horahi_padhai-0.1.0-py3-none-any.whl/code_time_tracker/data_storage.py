# code_time_tracker/data_storage.py

import csv

def save_log(file_path, data):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def load_logs(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

