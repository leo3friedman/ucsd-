import pandas as pd
# hide warning message (default='warn') TODO: read why this is occurring
pd.options.mode.chained_assignment = None
# convert html file into list of dataframes
dataframe_list = pd.read_html("html-data/anth.html")
# first dataframe in list
dataframe = dataframe_list[0]
# remove columns we don't care about
dataframe.drop(['Term', 'Instructor', 'Enroll', 'Rcmnd Class', 'Rcmnd Instr', 'Avg Grade Received', 'Avg Grade Expected'], axis=1, inplace=True)


def locate_course(df, course):
    # only rows with specific course
    df_course = df[df['Course'].str.contains(course)]
    # simplify course name
    df_course['Course'] = course
    return df_course


def calc_avg_study_hours(df):
    total_evaluations = df['Evals Made'].sum()
    study_hrs_avg = round(((df['Evals Made'] * df['Study Hrs/wk']).sum() / total_evaluations), 2)
    return study_hrs_avg


anar_116_courses = locate_course(dataframe, 'ANAR 116')
anar_116_avg_study_hours = calc_avg_study_hours(anar_116_courses)

# Displays entire dataframe
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print('\nANAR 116 dataframe :\n', anar_116_courses)
    print('\nANAR 116 avg study hours :\n', anar_116_avg_study_hours)

