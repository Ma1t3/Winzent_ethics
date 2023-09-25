import csv
import os
import sys
from os.path import exists

"""
Script to analyze the log file of winzent experiments 
which prints out and/or writes information about the runtime, negotiation quality and the amount of messages
in a .csv-file.
The string readouts are set for the log file version that is implemented in the 
"PGASC-Winzent-Changes" (commit: 7a76cd2a, 18.08.2022) branch in the mango-library repository.

Usage:
python winzent_log_analysis.py <<log file path>> <<Boolean to write results into .csv-files>>

If none of the parameters are specified, the script will analyze all .log-files in the current 
working directory and write them into a .csv-file.
"""


def calc_runtime(file_name):
    """
    Returns a dict that contains the average runtime over all steps taken as well as
    the max. and the min. runtime.
    """
    runtime = {
        "min": 0.0,
        "max": 0.0,
        "avg": 0.0
    }
    step_counter = 0
    with open(file_name) as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        if 'Runtime: ' in line:
            curr_runtime = float(line.split(' ')[1])
            if runtime["min"] > curr_runtime or runtime["min"] == 0.0:
                runtime["min"] = curr_runtime
            if runtime["max"] < curr_runtime or runtime["min"] == 0.0:
                runtime["max"] = curr_runtime
            step_counter += 1
            runtime["avg"] += curr_runtime
    runtime["avg"] = runtime["avg"] / step_counter
    return runtime


def calc_messages(file_name):
    """
    Returns a dict that contains the average amount of messages over all steps taken as well as
    the max. and the min. amount of messages.
    """
    messages = {
        "min": 0.0,
        "max": 0.0,
        "avg": 0.0
    }
    step_counter = 0
    with open(file_name, encoding="utf8") as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        if 'Messages sent: ' in line:
            curr_messages = float(line.split(' ')[2])
            if messages["min"] > curr_messages or messages["min"] == 0.0:
                messages["min"] = curr_messages
            if messages["max"] < curr_messages or messages["min"] == 0.0:
                messages["max"] = curr_messages
            step_counter += 1
            messages["avg"] += curr_messages
    messages["avg"] = messages["avg"] / step_counter
    return messages


def calc_negotiation_percent(file_name):
    """
    Returns a dict that contains the average negotiation result
    ((amount of negotiated power / power needed by loads)) over all steps taken as well as
    the max. and the min. negotiation result.
    """
    neg_pct = {
        'min': 0.0,
        'max': 0.0,
        'avg': 0.0
    }
    step_counter = 0
    needed_loads = -1
    with open(file_name) as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        if 'Needed Loads: ' in line:
            step_counter += 1
            needed_loads = float(line.split(' ')[2])
            continue
        if needed_loads > -1:
            neg_value = float(line.split(' ')[4])
            curr_neg_pct = neg_value / needed_loads
            neg_pct['avg'] += curr_neg_pct
            if neg_pct["min"] > curr_neg_pct or neg_pct["min"] == 0.0:
                neg_pct["min"] = curr_neg_pct
            if neg_pct["max"] < curr_neg_pct or neg_pct["min"] == 0.0:
                neg_pct["max"] = curr_neg_pct
            needed_loads = -1
    neg_pct['avg'] = neg_pct['avg'] / step_counter
    return neg_pct


def put_results_into_csv(messages, runtime, negotiation_results, filename, log_name):
    fieldnames = ["log_name", "max. runtime", "min_runtime", "avg_runtime",
                  "max_messages", "min_messages", "avg_messages",
                  "max. neg", "min. neg", "avg. neg"]
    data_list = {"log_name": log_name,
                 "max. runtime": runtime['max'],
                 "min_runtime": runtime['min'],
                 "avg_runtime": runtime['avg'],
                 "max_messages": messages['max'],
                 "min_messages": messages['min'],
                 "avg_messages": messages['avg'],
                 "max. neg": negotiation_results['max'],
                 "min. neg": negotiation_results['min'],
                 "avg. neg": negotiation_results['avg']}
    if not exists(filename + ".csv"):
        with open(filename + ".csv", 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    with open(filename + ".csv", 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data_list)


def main():
    try:
        log_name = str(sys.argv[1])
    except:
        log_name = 'all'
        print("All .log-files in this folder will be analyzed.")
    try:
        write_to_csv = bool(sys.argv[2])
    except:
        write_to_csv = True
        print("Results will be written to .csv.")
    curr_dir = str(os.getcwd())
    for file in os.listdir(curr_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".log"):
            if log_name != 'all':
                filename = log_name
            messages = calc_messages(filename)
            runtime = calc_runtime(filename)
            negotiation_results = calc_negotiation_percent(filename)
            if write_to_csv:
                put_results_into_csv(messages, runtime, negotiation_results, "winzent_log_results", filename)
            else:
                print(f"max. runtime: {runtime['max']}\n"
                      f"min. runtime: {runtime['min']}\n"
                      f"avg. runtime {runtime['avg']}")
                print(f"max. messages: {messages['max']}\n"
                      f"min. messages: {messages['min']}\n"
                      f"avg. messages: {messages['avg']}")
                print(f"max. neg: {negotiation_results['max']}\n"
                      f"min. neg: {negotiation_results['min']}\n"
                      f"avg. neg: {negotiation_results['avg']}")
            if log_name != 'all':
                break
            else:
                continue
        else:
            continue


if __name__ == "__main__":
    main()
    print("Desired .log-files have been successfully analyzed.")
