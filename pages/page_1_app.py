import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧐 LA Crime Dashboard", layout="wide", page_icon=":monocle:")
sns.set_theme(style="whitegrid")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('pages/data/Crime_Data_from_2020_to_Present.csv')
    return df

st.title("🧐 LA Crime Dashboard (2020–Present)")
df = load_data()

st.success(f"Loaded **{df.shape[0]:,} rows** and **{df.shape[1]} columns**")

# Convert month format (make consistent for filtering)
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

# YEAR FILTER
year_filter = st.sidebar.multiselect(
    "Select Years",
    sorted(df["occ_year"].unique()),
    default=sorted(df["occ_year"].unique()),
    key="year_filter"
)

# MONTH FILTER
month_filter = st.sidebar.multiselect(
    "Select Months",
    st.session_state.default_months,
    default=st.session_state.default_months,
    key="month_filter"
)

# DAY OF WEEK FILTER
day_filter = st.sidebar.multiselect(
    "Select Days of Week",
    st.session_state.default_days,
    default=st.session_state.default_days,
    key="day_filter"
)

# AREA FILTER
area_filter = st.sidebar.multiselect(
    "Select Areas",
    sorted(df["AREA NAME"].unique()),
    default=sorted(df["AREA NAME"].unique()),
    key="area_filter"
)

# Apply filters
df = df[df["occ_year"].isin(year_filter)]
df = df[df["AREA NAME"].isin(area_filter)]
df = df[df["occ_month"].isin(month_filter)]
df = df[df["occ_day"].isin(day_filter)]


# -------------------------
# YEARLY CRIME TREND + BOXPLOT
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
    sns.boxplot(y=plot1["count"], ax=ax_box)
    ax_box.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box)


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
    sns.boxplot(y=plot2["count"], ax=ax_box2)
    ax_box2.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box2)


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
    sns.boxplot(y=plot3["count"], ax=ax_box3)
    ax_box3.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box3)


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
    sns.boxplot(y=plot5["count"], ax=ax_box5)
    ax_box5.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box5)


# -------------------------
# TOP 10 CRIME CATEGORIES + BOXPLOT
# -------------------------
st.subheader("🔝 Top 10 Most Common Crimes")

plot6 = (
    df.groupby("Crm Cd Desc")
    .size()
    .sort_values(ascending=True)
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
    sns.boxplot(y=plot6["count"], ax=ax_box6)
    ax_box6.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box6)


# -------------------------
# AREA-WISE CRIME + BOXPLOT
# -------------------------
st.subheader("🕵 Crime Count by Area")

plot8 = df.groupby("AREA NAME").size().sort_values().reset_index(name="count")

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
    sns.boxplot(y=plot8["count"], ax=ax_box8)
    ax_box8.set_title("Distribution")
    sns.despine()
    st.pyplot(fig_box8)


# -------------------------
# CRIME TREND BY AREA PER YEAR
# ⚠️ Boxplot NOT meaningful → multiseries trend (skip)
# -------------------------
st.subheader("📊 Crime Trend Over Years by Area")

plot9 = df.groupby("occ_year")["AREA NAME"].value_counts().reset_index(name="count")

fig9, ax9 = plt.subplots(figsize=(16, 7))
sns.lineplot(
    data=plot9,
    x="AREA NAME",
    y="count",
    hue="occ_year",
    marker="o",
    palette="tab10",
    ax=ax9
)
plt.setp(ax9.get_xticklabels(), rotation=45)
ax9.set_title("Crime Trend by Area & Year")
sns.despine()
st.pyplot(fig9)
