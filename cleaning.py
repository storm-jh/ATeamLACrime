import pandas as pd 

df = pd.read_csv(r'ATeamLACrime\Crime_Data_from_2020_to_Present.csv')

#print(df.info)
#print(df.dtypes)
#print(df.columns)

df1=df.astype({"Date Rptd":"datetime64[ns]",
            "DATE OCC":"datetime64[ns]",
            "TIME OCC":"datetime64[ns]"})

df1["Vict Age"] = df1["Vict Age"].clip(lower=0)

#print(df1["Vict Age"].min())
#print("----------")
#print(df1.dtypes)
