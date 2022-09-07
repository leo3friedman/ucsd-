import pandas as pd
import os
import numpy as np

# hide warning message (default='warn') TODO: read why this is occurring
pd.options.mode.chained_assignment = None


def generate_all_data(directory):
    data = pd.DataFrame()
    file_names = os.listdir(directory)
    for file_name in file_names:
        print('generating file: ' + file_name)
        # convert html file into list of dataframes
        file_path = 'html-data/' + file_name
        new_data = pd.read_html(file_path)[0]
        data = pd.concat([data, new_data])
    # remove columns we don't care about
    print('dropping columns from data')
    data.drop(
        ['Term', 'Instructor', 'Enroll', 'Rcmnd Class', 'Rcmnd Instr', 'Avg Grade Received', 'Avg Grade Expected'],
        axis=1, inplace=True)
    print('simplifying course names')
    # simplify course names
    data['Course'] = data['Course'].str.replace(r'.-.*', '', regex=True)
    return data

# convert html file into list of dataframes
# dataframe_list = pd.read_html("html-data/anth.html")
# first dataframe in list
# dataframe = dataframe_list[0]
# remove columns we don't care about
# dataframe.drop(['Term', 'Instructor', 'Enroll', 'Rcmnd Class', 'Rcmnd Instr', 'Avg Grade Received', 'Avg Grade Expected'], axis=1, inplace=True)
# Simplify course name
# dataframe['Course'] = dataframe['Course'].str.replace(r'.-.*', '', regex=True)
# courses = dataframe['Course'].unique().tolist()


def calc_avg_study_hours(df):
    total_evaluations = df['Evals Made'].sum()
    study_hrs_avg = round(((df['Evals Made'] * df['Study Hrs/wk']).sum() / total_evaluations), 2)
    return study_hrs_avg


def generate_succinct_df(df, course):
    # only rows with specific course
    df_course = df[df['Course'].str.contains(course)]
    study_hours = calc_avg_study_hours(df_course)
    d = {'Course': [course], 'Study Hrs/wk': [study_hours]}
    succinct_df = pd.DataFrame(data=d)
    return succinct_df


def generate_final_df(df, cl):
    fdf = pd.DataFrame()
    for course in cl:
        print('concatenating course ' + course)
        fdf = pd.concat([fdf, generate_succinct_df(df, course)])
    return fdf


# running the program ...
all_data = generate_all_data('html-data')
print('generating course list')
course_list = all_data['Course'].unique().tolist()
print('generating final df')
final_df = generate_final_df(all_data, course_list)
final_df_sorted = final_df.sort_values(by=['Study Hrs/wk'])
# print('saving to txt file')
# numpy_array = final_df.to_numpy()
# np.savetxt("test_file.txt", numpy_array, fmt="%s")
# test_data = {'col1': [1, 46, 7, 2], 'col2': ['a', 'c', 'd', 'b']}
# test_df = pd.DataFrame(test_data)
# test_df = test_df.sort_values(by=['col1'])



# Displays entire dataframe
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print('\nfinal dataframe :\n', final_df_sorted)
    # print('\ndataframe :\n', dataframe)
    # print('\nclasses :\n', courses)
    # print('\nANAR 116 dataframe :\n', anar_116_courses)
    # print('\nANAR 116 avg study hours :\n', anar_116_avg_study_hours)

