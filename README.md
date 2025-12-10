# A Team LA Crime 2020 to 2025
Group project

## Overview
Group project involving data analysis consisting of ETL pipeline and interactive visualisations. 

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
| Thomas     |  Running code after each change to maintain good working order        |
| Conor      |          |
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
- I had a big problem commiting to the repo. The csv file was over the 100mb size limit for git hub. I put the csv into .gitignor but still had to use the termial to clear cashed memory as it was still causing a problem. git filter-branch --force --index-filter ^
"git rm --cached --ignore-unmatch pages/data/Crime_Data_from_2020_to_Present.csv" ^
--prune-empty --tag-name-filter cat -- --all (This removed all csv files in the memory.)
- I tried to have a reset button for the filters in the side bar but had some problems with the loading order.
- I tried to have an onclick sound play in the sidebar but Streamlit dosen't allow this.

Conor:
Riaz:

