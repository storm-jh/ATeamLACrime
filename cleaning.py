import pandas as pd 

df = pd.read_csv(r'Crime_Data_from_2020_to_Present.csv', low_memory=False)

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

### Removing 2000 or so results with 0 for both longtidue and lattitude
df1 = df1[(df1["LAT"] != 0) | (df1["LON"] != 0)]



### Checking it all worked
#print(df1.dtypes)
#print(df1["Vict Age"].min())
#print(df1["LAT"].min())
#print("----------")



## Saving cleaned CSV so we're all using the same dataset, though 
## this changes date/time occured coulumns back to objects, use above code
## and df1 for analysis, or uncomment below to save your file then use that 
## one for dashboarding software.

#df1.to_csv('crimedatacleaned.csv', index=False)

##checking csv export
#df2=pd.read_csv(r'crimedatacleaned.csv')
#print(df2.dtypes)
#print(df2.head)


