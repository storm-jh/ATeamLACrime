import pandas as pd 

df = pd.read_csv(r'ATeamLACrime\Crime_Data_from_2020_to_Present.csv')

## Just checking stuff
#print(df.info)
#print(df.dtypes)
#print(df.columns)


### Setting date and time columns to datetime

df1=df.astype({"Date Rptd":"datetime64[ns]",
            "DATE OCC":"datetime64[ns]",
            "TIME OCC":"datetime64[ns]"})

### setting negative values in Vict Age column to 0
df1["Vict Age"] = df1["Vict Age"].clip(lower=0)

### Checking it all worked
#print(df1["Vict Age"].min())
#print("----------")
#print(df1.dtypes)

## Saving cleaned CSV so we're all using the same dataset, but 
## this changes date/time occured coulumns back to objects.

#df1.to_csv('crimedata.csv', index=False)

#df2=pd.read_csv(r'ATeamLACrime/crimedata.csv')
#print(df2.dtypes)
