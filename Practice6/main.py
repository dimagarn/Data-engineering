import json
import numpy as np
import pandas as pd
from plots import *

df_list = []

def read_and_concat_data(file_path, columns):
    df = pd.concat(
        pd.read_csv(file_path, chunksize=10000, usecols=columns, low_memory=False, index_col=False),
        ignore_index=True
    )
    return df

df_columns = [
        ["h_score", "v_score", "day_of_week", "h_name", "length_outs", "v_hits", "v_doubles", "v_triples",
         "v_homeruns", "v_rbi"],
        ["FLIGHT_NUMBER", "ORIGIN_AIRPORT", "DAY_OF_WEEK", "DESTINATION_AIRPORT", "DISTANCE", "AIR_TIME",
         "TAXI_OUT", "ARRIVAL_DELAY", "AIRLINE", "TAXI_IN"],
        ["vf_Make", "stockNum", "vf_EngineCylinders", "vf_EngineKW", "vf_EngineModel", "vf_EntertainmentSystem",
         "vf_ForwardCollisionWarning", "vf_FuelInjectionType", "vf_FuelTypePrimary", "vf_FuelTypeSecondary"],
        ["name", "spkid", "class", "diameter", "albedo", "diameter_sigma", "epoch", "epoch_cal", "om", "w"],
        ["id", "key_skills", "schedule_name", "experience_id", "experience_name", "salary_from", "salary_to",
         "employer_name", "employer_industries", "schedule_id"],
    ]
paths = ["data/[1]game_logs.csv", "data/[3]flights.csv", "data/CIS_Automotive_Kaggle_Sample.csv", "data/dataset.csv", "data/vacancies_2020.csv"]
df_list = [read_and_concat_data(paths[i], cols) for i, cols in enumerate(df_columns, start=0)]


def memory_compare(source_data, optimized_data):
	source_data_memory = source_data.memory_usage(deep=True).sum()
	optimized_data_memory = optimized_data.memory_usage(deep=True).sum()
	if source_data_memory > optimized_data_memory:
		print("success optimization diff between src data and optimized data - " + str(
			source_data_memory - optimized_data_memory))
	else:
		print("fail optimization diff between src data and optimized data - " + str(
			optimized_data_memory - source_data_memory))

def data_converter(df):
	converted_data = df.copy()
	for column in converted_data.columns:
		if converted_data[column].dtype == 'object':
			unique_values = converted_data[column].unique()
			if len(unique_values) < 50:
				converted_data[column] = converted_data[column].astype('category')
			if converted_data[column].dtype == 'int64':
				converted_data[column] = converted_data[column].astype(np.int32)
			elif converted_data[column].dtype == 'float64':
				converted_data[column] = converted_data[column].astype(np.float32)
	return converted_data

def data_analyzer(source_dataframe: pd.DataFrame):
	file_size = source_dataframe.memory_usage(deep=True).sum()
	memory_usage = source_dataframe.memory_usage(deep=True).sum()
	col_sizes = []
	for col in source_dataframe.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		col_sizes.append({'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	sorted_df = source_dataframe.loc[:, source_dataframe.dtypes != object]
	sorted_sizes = []
	for col in sorted_df.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		sorted_sizes.append(
			{'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	return {'file_size': file_size, 'memory_usage': memory_usage, 'col_sizes': col_sizes, 'sorted_sizes': sorted_sizes}


result_analyze = []
for df in df_list:
	result_analyze.append(data_analyzer(df))

with open('out/results.json', 'a') as f:
	for index, data in enumerate(result_analyze):
		json.dump({f'df{index}_memory_usage': data['col_sizes']}, f)

for index, data in enumerate(df_list):
	optimized_data = data_converter(data)
	memory_compare(data, optimized_data)
	optimized_data.to_csv(f'optimized_df_{index + 1}.csv')


plot_line(df_list[0], "v_score", "h_score", "df_1_plot_1")
plot_line(df_list[0], "v_hits", "v_doubles", "df_1_plot_2")
plot_line(df_list[0], "v_hits", "v_triples", "df_1_plot_3")
plot_strip(df_list[0], "v_homeruns", "v_hits", "df_1_plot_4")
plot_strip(df_list[0], "v_homeruns", "v_score", "df_1_plot_5")

plot_line(df_list[1], "DISTANCE", "AIR_TIME", "df_2_plot_1")
plot_line(df_list[1], "FLIGHT_NUMBER", "TAXI_IN", "df_2_plot_2")
plot_hist(df_list[1], "DISTANCE", "TAXI_OUT", "df_2_plot_3")
plot_hist(df_list[1], "FLIGHT_NUMBER", "TAXI_OUT", "df_2_plot_4")
plot_hist(df_list[1], "FLIGHT_NUMBER", "AIR_TIME", "df_2_plot_5")

plot_line(df_list[2], "vf_ForwardCollisionWarning", "vf_EngineCylinders", "df_3_plot_1")
plot_line(df_list[2], "vf_EngineCylinders", "vf_FuelTypePrimary", "df_3_plot_2")
plot_strip(df_list[2], "vf_EngineKW", "vf_FuelTypeSecondary", "df_3_plot_3")
plot_line(df_list[2], "vf_EngineCylinders", "vf_FuelTypeSecondary", "df_3_plot_4")
plot_hist(df_list[2], "vf_EngineCylinders", "vf_EngineKW", "df_3_plot_5")

plot_line(df_list[3], "class", "diameter", "df_4_plot_1")
plot_strip(df_list[3], "spkid", "class", "df_4_plot_2")
plot_hist(df_list[3], "spkid", "diameter", "df_4_plot_3")
plot_box(df_list[3], "class", "albedo", "df_4_plot_4")
plot_hist(df_list[3], "diameter", "diameter_sigma", "df_4_plot_5")

plot_line(df_list[4], "id", "salary_to", "df_5_plot_1")
plot_line(df_list[4], "id", "salary_from", "df_5_plot_2")
plot_strip(df_list[4], "schedule_id", "experience_id", "df_5_plot_3")
plot_box(df_list[4], "experience_id", "salary_to", "df_5_plot_4")
plot_hist(df_list[4], "experience_id", "salary_from", "df_5_plot_5")

