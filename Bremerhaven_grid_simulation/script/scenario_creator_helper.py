"""
data.csv = Load flow from 2017-01-01
scenario.yml = created scenario
"""

import pandas as pd
import yaml


class ScenarioCreatorHelper:
    def create_scenario(self, config, input_path):
        df = pd.read_csv(input_path)
        column_name = "Time"
        if column_name in df.columns:
            df = df.drop([column_name], axis=1)
        df = df.T
        yml_list = []

        df_backup = df
        for conf in config:
            df = df_backup.copy()
            for time_key in df.columns:
                time_from = f"{conf['day']}*24*60*60+{time_key}*{conf['step_size']}"
                time_to = f"{conf['day']}*24*60*60+{time_key}*{conf['step_size']}+{conf['step_size'] - 1}"
                if conf['time_key_start'] <= float(time_key) <= conf['time_key_end']:
                    df[time_key] = [f"{val}*{conf['factor']}" for val in df[time_key].values]
                else:
                    df[time_key] = [f"{val}*{str(1.0)}" for val in df[time_key].values]

                yml_list.append([time_from, time_to, df[time_key].to_dict()])

        yaml.dump(yml_list, open("wind_percentages_summer/all_wind_to_25%.yml", "w"))

    def combine_scenarios(self, yaml_name_1, yaml_name_2, combined_scenario_name, add_ext_grid):

        # Load the first YAML file into a list of dictionaries.
        with open(yaml_name_1, 'r') as file1:
            data1 = yaml.load(file1, Loader=yaml.FullLoader)

        # Load the second YAML file into a list of dictionaries.
        with open(yaml_name_2, 'r') as file2:
            data2 = yaml.load(file2, Loader=yaml.FullLoader)

        ext_grid = {
            '0-ext_grid-13.in_service': True,
            '0-ext_grid-14.in_service': False,
            '0-ext_grid-8.in_service': False,
            '0-ext_grid-1.in_service': False,
        }

        # Create a dictionary to store the merged data.
        merged_data = {}

        # Iterate through the time entries in the first file.
        for entry1 in data1:
            time1 = entry1[0]  # Extract the time value from the first entry.

            # Find the corresponding entry in the second file based on time.
            for entry2 in data2:
                time2 = entry2[0]  # Extract the time value from the second entry.

                if time1 == time2:
                    # Combine the values from both entries.
                    test_entry = entry1[2]
                    for key in test_entry:
                        entry2[2][key] = test_entry[key]
                    if add_ext_grid:
                        for key in ext_grid:
                            entry2[2][key] = ext_grid[key]
                    merged_data[time1] = entry2

                    # merged_entry = [time1] + [x + y for x, y in zip(entry1[1:], entry2[1:])]
                    # merged_data[time1] = merged_entry

        # Add any remaining entries from the second file to the merged data.
        for entry2 in data2:
            time2 = entry2[0]

            if time2 not in merged_data:
                merged_data[time2] = entry2

        # Convert the merged_data dictionary back to a list of lists.
        merged_list = [merged_data[time] for time in sorted(merged_data.keys())]

        # Save the merged data back to a YAML file.
        with open(combined_scenario_name, 'w') as merged_file:
            yaml.dump(merged_list, merged_file, default_flow_style=False)


helper = ScenarioCreatorHelper()
config = [
    {
        "day": 0,
        "factor": 0.25,
        "time_key_start": 0,
        "time_key_end": 95,
        "step_size": 900
    },
]
# helper.create_scenario(config, "sgens_wind_summer.csv")
helper.combine_scenarios("solar_percentages_summer/all_solar_to_275%.yml",
                         "rest_low.yml",
                         "solar_high_rest_low_percentages/rest_low_solar_to_275%.yml",
                         False)
