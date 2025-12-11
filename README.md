# A Team LA Crime 2020 to 2025

## Overview
Group project involving data analysis of crime data from Los Angeles from years 2020 to 2025, consisting of python ETL pipeline and interactive visualisations using Tableau and Streamlit. 

## Resources
https://www.kaggle.com/datasets/utkarsh1093/crime-data-from-2020-to-nov2025/data
https://dataconverter.io/convert/parquet-to-csv
https://pixabay.com/sound-effects/search/car/

## Business Requirements
Explore the Crime Dataset to aid in making decision on resource allocation of LAPD, discover trends in the data, and make the LAPD more efficient in responding to crime.

## Installation / Setup
1. Clone the repo
2. Create a virtual environment
3. Install requirements: `pip install -r requirements.txt`
4. Required to add "Crime_Data_from_2020_to_Present.csv" to data folder. Available from https://www.kaggle.com/datasets/utkarsh1093/crime-data-from-2020-to-nov2025/data

## Data
- Data consists of 1,004,991 rows, with each row representing one instance of a reported crime and 28 columns, as follows:

DR_NO:
Unique LAPD incident number used to identify each crime report.

Date Rptd:
The date the crime was reported to the police.

DATE OCC:
The date the crime occurred.

TIME OCC:
Time of occurrence in 24-hour format.

AREA:
Numerical code for the LAPD geographic division where the incident occurred.

AREA NAME:
Name of the LAPD division (for example, N Hollywood, Central, Pacific).

Rpt Dist No:
Reporting district number, representing a smaller neighborhood unit within an LAPD area.

Part 1-2:
Crime classification category.
Part I includes serious crimes such as homicide, robbery, burglary, and aggravated assault.
Part II includes less severe offenses such as fraud, vandalism, and simple assault.

Crm Cd:
Numeric code identifying the primary crime.

Crm Cd Desc:
Description of the primary crime type (for example, Theft of Identity, Burglary, Simple Assault).

Mocodes:
Method of Operation codes that describe how the crime was committed.

Vict Age:
Age of the victim.

Vict Sex:
Sex of the victim (Male, Female, Unknown).

Vict Descent:
Victim’s descent or ethnic background (for example, Hispanic/Latin/Mexican, White, Black, Asian).

Premis Cd:
Numeric code for the type of location where the crime occurred.

Premis Desc:
Description of the premise or location type (for example, Sidewalk, Single Family Dwelling).

Weapon Used Cd:
Numeric code for the weapon used, if any.

Weapon Desc:
Description of the weapon used (for example, Knife, Handgun, Unknown).

Status:
Case status code.

Status Desc:
Full description of the case status (for example, Invest Cont, Adult Arrest, Juvenile Arrest).

Crm Cd 1:
Additional crime code associated with the incident (if applicable). Often the same as Crm Cd for single-offense cases.

LOCATION:
Address or block description where the incident occurred.

LAT:
Latitude coordinate for the location.

LON:
Longitude coordinate for the location.

occ_year:
Year extracted from DATE OCC.

occ_month:
Month extracted from DATE OCC.

occ_date:
Day of the month extracted from DATE OCC.

occ_day:
Day of the week of the occurrence date (for example, Mon, Tue, Sat).

- Victim age shows a clear spike at 0, indicating missing or unrecorded data. These records were flagged as ‘Unknown’ and excluded from age-based distribution analysis, but retained in overall counts.

## Data Apps / Dashboards
- Tableau
- Streamlit

## Team Members
- Ben Brown
- Thomas Overment
- Storm GH
- Conor O'Brien
- Riaz Unar

## Conclusions
- January is the month with the highest total crime count (92,701) and December is the lowest (78,226)
- Friday is the day with the highest total crime count (153,676) and Tuesday is the lowest (138,151)
- Stolen Vehicles make up the most frequently reported crimes (115,190), ahead of Battery - Simple Assault (74,839)
- Rates of shoplifting are increasing steadily over time. 

## Business Requirements
Explore the Crime Dataset to aid in making decision on resource allocation of LAPD, discover trends in the data, and make the LAPD more efficient in responding to crime.

## Installation / Setup
1. Clone the repo
2. Create a virtual environment
3. Install requirements: `pip install -r requirements.txt`
4. Required to add "Crime_Data_from_2020_to_Present.csv" to data folder. Available from https://www.kaggle.com/datasets/utkarsh1093/crime-data-from-2020-to-nov2025/data

## Data
- Victim age shows a clear spike at 0, indicating missing or unrecorded data. These records were flagged as ‘Unknown’ and excluded from age-based distribution analysis, but retained in overall counts.

## Data Apps / Dashboards
- Tableau
- Streamlit

## Team Members
- Ben Brown
- Thomas Overment
- Storm GH
- Conor O'Brien
- Riaz Unar

## Resilience Behaviours

### 1. Solution-Oriented Mindset

| Participant | Measure |
|------------|----------|
| Ben        |          |
| Storm      |          |
| Thomas     | Putting new skills in practice         |
| Conor      | Focussing just on the task at hand to avoid overwhelm. |
| Riaz       |          |


### 2. Task Estimation

| Participant | Measure |
|------------|----------|
| Ben        |          |
| Storm      |          |
| Thomas     | Create streamlit app in VSC         |
| Conor      | 1 Day to create basic and advanced visualisation in Tableau         |
| Riaz       |          |

### 3. Personal Accountability

| Participant | Measure |
|------------|----------|
| Ben        |          |
| Storm      |          |
| Thomas     | Streamlit         |
| Conor      | Checking Trello board, assigning and completing tasks         |
| Riaz       |          |

### 4. Dealing With Distractions

| Participant | Measure |
|------------|----------|
| Ben        |          |
| Storm      |          |
| Thomas     | Earplugs         |
| Conor      | Work focus mode on phone.         |
| Riaz       |          |

### 5. Problem Solving

| Participant | Measure |
|------------|----------|
| Ben        |          |
| Storm      |          |
| Thomas     | Watching tutorials and researching other projects for inspiration         |
| Conor      | Returning to tutorials to progress with use of Tableau. Meetings with group to discuss and help solve issues         |
| Riaz       |          |


### 6. Consistent Coding Practices:

| Participant | Measure |
|------------|----------|
| Ben        |          |
| Storm      |          |
| Thomas     |   Running code after each change to maintain good working order          |
| Conor      | Checking over other members code for inconsistencies         |
| Riaz       |          |

### 7. Project Management Methodology Adoption:

| Participant | Measure |
|------------|----------|
| Ben        |          |
| Storm      |          |
| Thomas     |   Trello       |
| Conor      |   Trello       |
| Riaz       |          |

## Problems

Ben:
Storm:
Thomas:
- I had a big problem commiting to the repo. The csv file was over the 100mb size limit for git hub. I put the csv into .gitignore but still had to use the termial to clear cached memory as it was still causing a problem. git filter-branch --force --index-filter ^
"git rm --cached --ignore-unmatch pages/data/Crime_Data_from_2020_to_Present.csv" ^
--prune-empty --tag-name-filter cat -- --all (This removed all csv files in the memory.)
- I tried to have a reset button for the filters in the side bar but had some problems with the loading order.
- I tried to have an onclick sound play in the sidebar but Streamlit dosen't allow this.

Conor:
-  I had issue with merging branches in VS Code to the main branch in git hub. I spent some time watching videos, consolidating learning points and brought the issue to data coach where it was finally resolved.