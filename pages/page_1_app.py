import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧐 LA Crime Dashboard", layout="wide", page_icon=":monocle:")
sns.set_theme(style="whitegrid")

# -------------------------
# LOAD & CLEAN DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('pages/data/Crime_Data_from_2020_to_Present.csv')

    # -----------------------------------------------------
    # DATA CLEANING PIPELINE
    # -----------------------------------------------------

    # 1. Drop duplicate unique crime report numbers (safe)
    df = df.drop_duplicates(subset=["DR_NO"])

    # 2. Fix and validate date columns
    df["DATE OCC"] = pd.to_datetime(df["DATE OCC"], errors="coerce")
    df["Date Rptd"] = pd.to_datetime(df["Date Rptd"], errors="coerce")

    # Remove rows with invalid or missing dates
    df = df.dropna(subset=["DATE OCC", "Date Rptd"])

    # Create reporting delay safely
    df["delay_reporting"] = (df["Date Rptd"] - df["DATE OCC"]).dt.days

    # 3. Standardize month values
    df["occ_month"] = df["occ_month"].astype(str).str[:3].str.title()

    # Enforce proper month ordering
    df["occ_month"] = pd.Categorical(
        df["occ_month"],
        categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        ordered=True
    )

    # 4. Standardize days of week
    df["occ_day"] = df["occ_day"].astype(str).str.title()

    df["occ_day"] = pd.Categorical(
        df["occ_day"],
        categories=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
        ordered=True
    )

    # 5. Ensure numeric fields are valid
    numeric_cols = ["Vict Age", "Crm Cd", "AREA", "Rpt Dist No"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 6. Remove rows with clearly invalid values
    df = df[df["Vict Age"] >= 0]
    df = df[df["Crm Cd"] > 0]

    # 7. Clean categorical text fields
    text_cols = ["Crm Cd Desc", "AREA NAME"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.title()

    return df

# -------------------------
# LOAD ONCE AND USE CLEAN DATA
# -------------------------
st.title("🧐 LA Crime Dashboard 2020–2025")

df = load_data()

st.success(f"Loaded **{df.shape[0]:,} rows** and **{df.shape[1]} columns**")

df["occ_month"] = df["occ_month"].astype(str).str[:3].str.title()

# --------------------------------
# INITIALIZE DEFAULT FILTER VALUES
# --------------------------------
if "default_years" not in st.session_state:
    st.session_state.default_years = sorted(df["occ_year"].unique())

if "default_months" not in st.session_state:
    st.session_state.default_months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

if "default_days" not in st.session_state:
    st.session_state.default_days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

if "default_areas" not in st.session_state:
    st.session_state.default_areas = sorted(df["AREA NAME"].unique())


st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Select Years",
    sorted(df["occ_year"].unique()),
    default=sorted(df["occ_year"].unique()),
    key="year_filter"
)

month_filter = st.sidebar.multiselect(
    "Select Months",
    st.session_state.default_months,
    default=st.session_state.default_months,
    key="month_filter"
)

day_filter = st.sidebar.multiselect(
    "Select Days of Week",
    st.session_state.default_days,
    default=st.session_state.default_days,
    key="day_filter"
)

area_filter = st.sidebar.multiselect(
    "Select Areas",
    sorted(df["AREA NAME"].unique()),
    default=sorted(df["AREA NAME"].unique()),
    key="area_filter"
)

df = df[df["occ_year"].isin(year_filter)]
df = df[df["AREA NAME"].isin(area_filter)]
df = df[df["occ_month"].isin(month_filter)]
df = df[df["occ_day"].isin(day_filter)]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Project Links")

st.sidebar.markdown(
    """
    **Project Resources:**  

    🔗 [GitHub Repository](https://github.com/storm-jh/ATeamLACrime)  
    📊 [PowerPoint Presentation](https://github.com/storm-jh/ATeamLACrime/blob/main/presentation/crime.pptx)  
    """
)



# -------------------------
# YEARLY CRIME TREND AND BOXPLOT 
# -------------------------
st.subheader("📅 Yearly Crime Distribution")

plot1 = df.groupby("occ_year").size().reset_index(name="count")

col1, col2 = st.columns([3, 1])
with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=plot1, x="occ_year", y="count", marker="o", ax=ax)
    for x, y in zip(plot1["occ_year"], plot1["count"]):
        ax.text(x, y, f"{y:,}", ha="center", va="bottom")
    ax.set_title("Yearly Crime Trend")
    sns.despine()
    st.pyplot(fig)

with col2:
    fig_box, ax_box = plt.subplots(figsize=(4, 6))
    sns.boxplot(y=plot1["count"], ax=ax_box, width=0.3)
    sns.stripplot(y=plot1["count"], ax=ax_box, color="black", alpha=0.4, jitter=True, size=5)
    ax_box.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box)

# -------------------------
# INSIGHTS: YEARLY CRIME TRENDS
# -------------------------
st.subheader("🧠 Insights for Yearly Crime Trends")

year_counts = plot1.copy()

highest_year = int(year_counts.loc[year_counts["count"].idxmax(), "occ_year"])
highest_value = int(year_counts["count"].max())
lowest_year = int(year_counts.loc[year_counts["count"].idxmin(), "occ_year"])
lowest_value = int(year_counts["count"].min())
avg_yearly = year_counts["count"].mean()

insight_text_year = f"""

- **Highest-crime year:** `{highest_year}` with **{highest_value:,} incidents**
- **Lowest-crime year:** `{lowest_year}` with **{lowest_value:,} incidents**
- **Average yearly crime:** `{avg_yearly:,.0f}` incidents per year
"""

st.markdown(insight_text_year)


# -------------------------
# MONTH-WISE CRIME + BOXPLOT
# -------------------------
st.subheader("📆 Month-wise Crime Volume")

df['occ_month'] = pd.Categorical(
    df['occ_month'],
    categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True
)

plot2 = df.groupby("occ_month", observed=True).size().reset_index(name="count")

col1, col2 = st.columns([3, 1])
with col1:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=plot2, x="occ_month", y="count", marker="o", ax=ax2)
    for x, y in zip(plot2["occ_month"], plot2["count"]):
        ax2.text(x, y, f"{y:,}", ha="center", va="bottom")
    ax2.set_title("Monthly Crime Volume")
    plt.setp(ax2.get_xticklabels(), rotation=45)
    sns.despine()
    st.pyplot(fig2)

with col2:
    fig_box2, ax_box2 = plt.subplots(figsize=(4, 6))
    sns.boxplot(y=plot2["count"], ax=ax_box2, width=0.3)
    sns.stripplot(y=plot2["count"], ax=ax_box2, color="black", alpha=0.4, jitter=True, size=5)
    ax_box2.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box2)

# -------------------------
# INSIGHTS MONTH-WISE CRIME TRENDS
# -------------------------
st.subheader("🧠 Insights for Monthly Crime Trends")

month_counts = plot2.copy()

highest_month = month_counts.loc[month_counts["count"].idxmax(), "occ_month"]
highest_value = int(month_counts["count"].max())
lowest_month = month_counts.loc[month_counts["count"].idxmin(), "occ_month"]
lowest_value = int(month_counts["count"].min())
avg_monthly = month_counts["count"].mean()

insight_text_month = f"""
- **Highest-crime month:** `{highest_month}` with **{highest_value:,} incidents**
- **Lowest-crime month:** `{lowest_month}` with **{lowest_value:,} incidents**
- **Average monthly crime:** `{avg_monthly:,.0f}` incidents per month
"""

st.markdown(insight_text_month)


# -------------------------
# DAY OF WEEK CRIME + BOXPLOT
# -------------------------
st.subheader("📅 Crime by Day of Week")

df['occ_day'] = pd.Categorical(
    df['occ_day'],
    categories=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    ordered=True
)

plot3 = df.groupby("occ_day", observed=True).size().reset_index(name="count")

col1, col2 = st.columns([3, 1])
with col1:
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=plot3, x="occ_day", y="count", marker="o", ax=ax3)
    for x, y in zip(plot3["occ_day"], plot3["count"]):
        ax3.text(x, y, f"{y:,}", ha="left", va="bottom")
    ax3.set_title("Crime Trend by Day of Week")
    sns.despine()
    st.pyplot(fig3)

with col2:
    fig_box3, ax_box3 = plt.subplots(figsize=(4, 6))
    sns.boxplot(y=plot3["count"], ax=ax_box3, width=0.3)
    sns.stripplot(y=plot3["count"], ax=ax_box3, color="black", alpha=0.4, jitter=True, size=5)
    ax_box3.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box3)

# -------------------------
# INSIGHTS: DAY-OF-WEEK CRIME TRENDS
# -------------------------
st.subheader("🧠 Insights for Crime by Day of Week")

day_counts = plot3.copy()

highest_day = day_counts.loc[day_counts["count"].idxmax(), "occ_day"]
highest_value = int(day_counts["count"].max())
lowest_day = day_counts.loc[day_counts["count"].idxmin(), "occ_day"]
lowest_value = int(day_counts["count"].min())
avg_day = day_counts["count"].mean()

insight_text_day = f"""
- **Busiest crime day:** `{highest_day}` with **{highest_value:,} incidents**
- **Quietest day:** `{lowest_day}` with **{lowest_value:,} incidents**
- **Average weekday crime:** `{avg_day:,.0f}` incidents
"""

st.markdown(insight_text_day)


# -------------------------
# REPORTING DELAY + BOXPLOT
# -------------------------
st.subheader("🐀 Crime Reporting Delay (OCC Date → Reported Date)")

df["Date Rptd"] = pd.to_datetime(df["Date Rptd"])
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])
df["delay_reporting"] = (df["Date Rptd"] - df["DATE OCC"]).dt.days

bins = [-1, 0, 3, 7, 30, 90, 365, float("inf")]
labels = ["same day", "1–3 days", "4–7 days", "8–30 days", "31–90 days", "91–365 days", ">365 days"]

df["rep_lag"] = pd.cut(df["delay_reporting"], bins=bins, labels=labels)

plot5 = df.groupby("rep_lag", observed=True).size().reset_index(name="count")

col1, col2 = st.columns([3, 1])
with col1:
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=plot5, x="rep_lag", y="count", marker="o", ax=ax5)
    for x, y in zip(plot5["rep_lag"], plot5["count"]):
        ax5.text(x, y, f"{y:,}", ha="center")
    ax5.set_title("Reporting Delay Distribution")
    sns.despine()
    st.pyplot(fig5)

with col2:
    fig_box5, ax_box5 = plt.subplots(figsize=(4, 6))
    sns.boxplot(y=plot5["count"], ax=ax_box5, width=0.3)
    sns.stripplot(y=plot5["count"], ax=ax_box5, color="black", alpha=0.4, jitter=True, size=5)
    ax_box5.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box5)

# -------------------------
# INSIGHTS: REPORTING DELAY
# -------------------------
st.subheader("🧠 Insights for Crime Reporting Delays")

delay_counts = plot5.copy()

highest_delay = delay_counts.loc[delay_counts["count"].idxmax(), "rep_lag"]
highest_value = int(delay_counts["count"].max())
lowest_delay = delay_counts.loc[delay_counts["count"].idxmin(), "rep_lag"]
lowest_value = int(delay_counts["count"].min())

insight_text_delay = f"""
- **Most common reporting delay:** `{highest_delay}` with **{highest_value:,} reports**
- **Least common delay category:** `{lowest_delay}` with **{lowest_value:,} reports**
"""

st.markdown(insight_text_delay)


# -------------------------
# TOP 10 CRIME CATEGORIES + BOXPLOT
# -------------------------
st.subheader("🔝 Top 10 Most Common Crimes")

plot6 = (
    df.groupby("Crm Cd Desc")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="count")
    .head(10)
)

col1, col2 = st.columns([3, 1])
with col1:
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=plot6, x="count", y="Crm Cd Desc", palette="dark:b_r", ax=ax6)
    ax6.set_title("Top 10 Crime Categories")
    for p in ax6.patches:
        ax6.annotate(f"{int(p.get_width()):,}", (p.get_x()+p.get_width()+500, p.get_y()+0.4))
    sns.despine()
    st.pyplot(fig6)

with col2:
    fig_box6, ax_box6 = plt.subplots(figsize=(4, 6))
    sns.boxplot(y=plot6["count"], ax=ax_box6, width=0.3)
    sns.stripplot(y=plot6["count"], ax=ax_box6, color="black", alpha=0.4, jitter=True, size=5)
    ax_box6.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box6)

# -------------------------
# AREA-WISE CRIME + BOXPLOT
# -------------------------
st.subheader("🕵 Crime Count by Area")

plot8 = (
    df.groupby("AREA NAME")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="count")
)

col1, col2 = st.columns([3, 1])
with col1:
    fig8, ax8 = plt.subplots(figsize=(12, 10))
    sns.barplot(data=plot8, x="count", y="AREA NAME", palette="dark:b_r", ax=ax8)
    for p in ax8.patches:
        ax8.annotate(f"{int(p.get_width()):,}", (p.get_width()+500, p.get_y()+0.3))
    ax8.set_title("Crimes by Area")
    sns.despine()
    st.pyplot(fig8)

with col2:
    fig_box8, ax_box8 = plt.subplots(figsize=(4, 6))
    sns.boxplot(y=plot8["count"], ax=ax_box8, width=0.3)
    sns.stripplot(y=plot8["count"], ax=ax_box8, color="black", alpha=0.4, jitter=True, size=5)
    ax_box8.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box8)

# -------------------------
# INSIGHTS: CRIME CATEGORIES + AREAS
# -------------------------
st.subheader("🧠 Insights for Crime Categories and Areas")

top_category = plot6.iloc[0]["Crm Cd Desc"]
top_category_value = int(plot6.iloc[0]["count"])
low_category = plot6.iloc[-1]["Crm Cd Desc"]
low_category_value = int(plot6.iloc[-1]["count"])
top_area = plot8.iloc[0]["AREA NAME"]
top_area_value = int(plot8.iloc[0]["count"])
low_area = plot8.iloc[-1]["AREA NAME"]
low_area_value = int(plot8.iloc[-1]["count"])

combined_insights = f"""
- **Most common crime type:** `{top_category}` with **{top_category_value:,} incidents**  
- **Least common among the top 10:** `{low_category}` with **{low_category_value:,} incidents**
- **Area with the highest crime volume:** `{top_area}` with **{top_area_value:,} incidents**  
- **Area with the lowest crime volume:** `{low_area}` with **{low_area_value:,} incidents**
"""

st.markdown(combined_insights)




# -------------------------
# CRIME TREND BY AREA PER YEAR
# -------------------------
st.subheader("📊 Crime Trend Over Years by Area")

plot9 = df.groupby("AREA NAME")["occ_year"].value_counts().reset_index(name="count")

fig9, ax9 = plt.subplots(figsize=(16, 7))
sns.lineplot(
    data=plot9,
    x="occ_year",
    y="count",
    hue="AREA NAME",
    marker="o",
    palette="tab10",
    ax=ax9
)
plt.setp(ax9.get_xticklabels(), rotation=45)
ax9.set_title("Crime Trend by Area & Year")
sns.despine()
st.pyplot(fig9)

# -------------------------
# INSIGHTS: CRIME TREND BY AREA & YEAR
# -------------------------
st.subheader("🧠 Insights for Crime Trends Across Areas and Years")

area_totals = plot9.groupby("AREA NAME")["count"].sum()
top_area = area_totals.idxmax()
top_area_value = int(area_totals.max())
low_area = area_totals.idxmin()
low_area_value = int(area_totals.min())
year_totals = plot9.groupby("occ_year")["count"].sum()
top_year = int(year_totals.idxmax())
top_year_value = int(year_totals.max())
low_year = int(year_totals.idxmin())
low_year_value = int(year_totals.min())

insight_text_area_year = f"""
- **Area with the highest crime overall:** `{top_area}` with **{top_area_value:,} incidents**
- **Area with the lowest crime overall:** `{low_area}` with **{low_area_value:,} incidents**
- **Year with the highest total crime:** `{top_year}` with **{top_year_value:,} incidents**
- **Year with the lowest total crime:** `{low_year}` with **{low_year_value:,} incidents**
"""

st.markdown(insight_text_area_year)



# -------------------------
# BUILD DAILY CRIME DATAFRAME
# -------------------------
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])
df["day"] = df["DATE OCC"].dt.day

daily_area = (
    df.groupby(["day", "AREA NAME"])
      .size()
      .reset_index(name="count")
)

# -------------------------
# DAILY CRIME TREND BY AREA
# -------------------------
st.subheader("📈 Daily Crime Trend by Area")

fig_daily2, ax_daily2 = plt.subplots(figsize=(16, 7))

sns.lineplot(
    data=daily_area,
    x="day",
    y="count",
    hue="AREA NAME",
    marker="o",
    ax=ax_daily2,
    palette="tab20"
)

ax_daily2.set_title("Daily Crime Trend Across Areas")
ax_daily2.set_xlabel("Day of Month")
ax_daily2.set_ylabel("Crime Count")
ax_daily2.set_xticks(range(1, 32))

# MOVE LEGEND OUTSIDE THE PLOT
ax_daily2.legend(
    title="Area",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    borderaxespad=0,
)

sns.despine()

st.pyplot(fig_daily2)



# -------------------------
# HEATMAP: DAILY CRIME LEVELS BY AREA
# -------------------------
st.subheader("🔥 Daily Crime Heatmap by Area")

df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])

df["day"] = df["DATE OCC"].dt.day

heatmap_data = df.pivot_table(
    index="AREA NAME",
    columns="day",
    values="DR_NO",
    aggfunc="count",
    fill_value=0
)

fig_hm, ax_hm = plt.subplots(figsize=(18, 10))

sns.heatmap(
    heatmap_data,
    cmap="Reds",
    linewidths=0.4,
    linecolor="gray",
    cbar_kws={'label': 'Crime Count'},
    ax=ax_hm
)

ax_hm.set_title("Daily Crime Heatmap by Area", fontsize=16)
ax_hm.set_xlabel("Day of Month")
ax_hm.set_ylabel("Area")

st.pyplot(fig_hm)

# -------------------------
# LOGIC FOR INSIGHTS
# -------------------------
st.subheader("🧠 Insights for Daily Crime Trends")
# Total crime per area
area_totals = daily_area.groupby("AREA NAME")["count"].sum()
top_area = area_totals.idxmax()
top_area_value = int(area_totals.max())
day_totals = daily_area.groupby("day")["count"].sum()
top_day = int(day_totals.idxmax())
top_day_value = int(day_totals.max())
avg_daily = day_totals.mean()
spikes = day_totals[day_totals > avg_daily * 1.5]

insight_text = f"""
- **Most active area:** `{top_area}` with **{top_area_value} incidents**
- **Highest-crime day:** `{top_day}` with **{top_day_value} incidents**
- **Average daily crime:** {avg_daily:.1f}
"""

st.markdown(insight_text)


