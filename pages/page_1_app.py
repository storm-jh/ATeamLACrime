import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#import base64

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

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Select Years",
    sorted(df["occ_year"].unique()),
    default=sorted(df["occ_year"].unique())
)

area_filter = st.sidebar.multiselect(
    "Select Areas",
    sorted(df["AREA NAME"].unique()),
    default=sorted(df["AREA NAME"].unique())
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Project Links")

st.sidebar.markdown(
    """
    - [🌐 GitHub Repository](https://github.com/storm-jh/ATeamLACrime)
    - [💼 LinkedIn Profile](https://www.linkedin.com/feed/?trk=guest_homepage-basic_google-one-tap-submit)
    """,
    unsafe_allow_html=True,
)

#st.sidebar.markdown("---")
#st.sidebar.markdown("### 🔗 Project Links")

#github_button = """
#<div style="text-align:center;">
#    <a href="https://github.com/storm-jh/ATeamLACrime" target="_blank">
#        <img src="../data/github.PNG" width="50" style="margin-top:10px;">
#    </a>
#</div>
#"""

#st.sidebar.markdown(github_button, unsafe_allow_html=True)





# Apply filters AFTER sidebar widgets
df = df[df["occ_year"].isin(year_filter)]
df = df[df["AREA NAME"].isin(area_filter)]



# -------------------------
# YEARLY CRIME TREND
# -------------------------
st.subheader("📅 Yearly Crime Distribution")

plot1 = df.groupby("occ_year").size().reset_index(name="count")

fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(data=plot1, x="occ_year", y="count", marker="o", ax=ax)
for x, y in zip(plot1["occ_year"], plot1["count"]):
    ax.text(x, y, f"{y:,}", ha="center", va="bottom")

ax.set_xlabel("Years")
ax.set_ylabel("Crime Count")
ax.set_title("Yearly Crime Trend")
sns.despine()
st.pyplot(fig)


# -------------------------
# MONTH-WISE CRIME
# -------------------------
st.subheader("📆 Month-wise Crime Volume")

df['occ_month'] = pd.Categorical(
    df['occ_month'],
    categories=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True
)

plot2 = df.groupby("occ_month", observed=True).size().reset_index(name="count")

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=plot2, x="occ_month", y="count", marker="o", ax=ax2)

for x, y in zip(plot2["occ_month"], plot2["count"]):
    ax2.text(x, y, f"{y:,}", ha="center", va="bottom")

ax2.set_ylabel("Crime Count")
ax2.set_title("Monthly Crime Volume")
plt.setp(ax2.get_xticklabels(), rotation=45)
sns.despine()
st.pyplot(fig2)


# -------------------------
# DAY-OF-WEEK CRIME TREND
# -------------------------
st.subheader("📅 Crime by Day of Week")

df['occ_day'] = pd.Categorical(
    df['occ_day'],
    categories=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    ordered=True
)

plot3 = df.groupby("occ_day", observed=True).size().reset_index(name="count")

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=plot3, x="occ_day", y="count", marker="o", ax=ax3)

for x, y in zip(plot3["occ_day"], plot3["count"]):
    ax3.text(x, y, f"{y:,}", ha="left", va="bottom")

ax3.set_title("Crime Trend by Day of Week")
sns.despine()
st.pyplot(fig3)

# -------------------------
# REPORTING DELAY
# -------------------------
st.subheader("🐀 Crime Reporting Delay (OCC Date → Reported Date)")

df["Date Rptd"] = pd.to_datetime(df["Date Rptd"])
df["DATE OCC"] = pd.to_datetime(df["DATE OCC"])

df["delay_reporting"] = (df["Date Rptd"] - df["DATE OCC"]).dt.days

bins = [-1, 0, 3, 7, 30, 90, 365, float("inf")]
labels = [
    "same day", "1–3 days", "4–7 days", "8–30 days",
    "31–90 days", "91–365 days", ">365 days"
]

df["rep_lag"] = pd.cut(df["delay_reporting"], bins=bins, labels=labels)

plot5 = df.groupby("rep_lag", observed=True).size().reset_index(name="count")

fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=plot5, x="rep_lag", y="count", marker="o", ax=ax5)

for x, y in zip(plot5["rep_lag"], plot5["count"]):
    ax5.text(x, y, f"{y:,}", ha="center")

ax5.set_title("Reporting Delay Distribution")
sns.despine()
st.pyplot(fig5)


# -------------------------
# TOP 10 CRIME CATEGORIES
# -------------------------
st.subheader("🔝 Top 10 Most Common Crimes")

plot6 = (
    df.groupby("Crm Cd Desc")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="count")
    .head(10)
)

fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.barplot(data=plot6, x="count", y="Crm Cd Desc", palette="dark:b_r", ax=ax6)
ax6.set_title("Top 10 Crime Categories")

for p in ax6.patches:
    ax6.annotate(f"{int(p.get_width()):,}", (p.get_x()+p.get_width()+500, p.get_y()+0.4))

sns.despine()
st.pyplot(fig6)


# -------------------------
# PART 1 VS PART 2
# -------------------------
st.subheader("🥧 Part 1 vs Part 2 Crime Classification")
st.write("These categories come from the Uniform Crime Reporting (UCR) standards used nationwide, including by the LAPD. Part 1 crimes are considered more serious offenses, while Part 2 crimes are less severe.")
plot7 = df.groupby("Part 1-2").size().reset_index(name="count")

fig7, ax7 = plt.subplots(figsize=(7, 7))
ax7.pie(
    plot7["count"],
    labels=plot7["Part 1-2"],
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor": "white"}
)
ax7.set_title("Part 1 vs Part 2 Crimes")
st.pyplot(fig7)


# -------------------------
# AREA-WISE CRIME VOLUME
# -------------------------
st.subheader("🕵 Crime Count by Area")

plot8 = df.groupby("AREA NAME").size().sort_values(ascending=False).reset_index(name="count")

fig8, ax8 = plt.subplots(figsize=(12, 10))
sns.barplot(data=plot8, x="count", y="AREA NAME", palette="dark:b_r", ax=ax8)

for p in ax8.patches:
    ax8.annotate(f"{int(p.get_width()):,}", (p.get_width()+500, p.get_y()+0.3))

ax8.set_title("Crimes by Area")
sns.despine()
st.pyplot(fig8)


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
