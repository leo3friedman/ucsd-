import pandas as pd
# hide warning message (default='warn') TODO: read why this is occurring
pd.options.mode.chained_assignment = None
# convert html file into list of dataframes
dfs = pd.read_html("html-data/anth.html")
# first dataframe in list
df = dfs[0]
# only rows with specific course
df_anar_116 = df[df['Course'].str.contains('ANAR 116')]
# remove columns we don't care about
df_anar_116.drop(['Term', 'Instructor', 'Enroll', 'Rcmnd Class', 'Rcmnd Instr', 'Avg Grade Received', 'Avg Grade Expected'], axis=1, inplace=True)
# simplify course name
df_anar_116['Course'] = 'ANAR 116'

total_evals = df_anar_116['Evals Made'].sum()
study_hrs_avg = round(((df_anar_116['Evals Made'] * df_anar_116['Study Hrs/wk']).sum() / total_evals), 2)
print('\nANAR 116 Avg Study Hours :\n', study_hrs_avg)

# Displays entire dataframe
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print('\nANAR 116 dataframe :\n', df_anar_116)

    