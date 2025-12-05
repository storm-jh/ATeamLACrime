import pandas as pd 
from ydata_profiling import ProfileReport

### Initial ydata report, takes a few minutes

df = pd.read_csv(r'C:\Users\storm\Documents\VS Code projects\group project 1\Crime_Data_from_2020_to_Present.csv')


profile = ProfileReport(df=df, minimal=False)
#profile.to_notebook_iframe()
profile.to_file("report.html")
