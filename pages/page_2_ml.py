import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------
# STREAMLIT CONFIG
# ---------------------------------
st.set_page_config(
    page_title="🧠 LA Crime ML - Random Forest",
    layout="wide",
    page_icon="🤖"
)

st.title("🤖 Machine Learning: Crime Classification with Random Forest")

# ---------------------------------
# LOAD DATA
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("pages/data/Crime_Data_from_2020_to_Present.csv")
    return df

df = load_data()

st.success(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")


# ---------------------------------
# PREPARE DATA FOR ML
# ---------------------------------
st.subheader("🔧 Preparing Data for Training")

features = ["AREA", "Rpt Dist No", "Crm Cd", "Vict Age"]
target = "Part 1-2"

df_ml = df[features + [target]].dropna()

X = df_ml[features]
y = df_ml[target]

st.write("📌 **Features used:**", features)
st.write("📌 **Target being predicted:**", target)


# ---------------------------------
# TRAIN TEST SPLIT
# ---------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ---------------------------------
# RANDOM FOREST MODEL
# ---------------------------------
st.subheader("🌲 Training Random Forest Model")

rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
proba = rf.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_pred)

st.success(f"🎯 Model Accuracy: **{accuracy*100:.2f}%**")


# ---------------------------------------------------
# TARGET CLASS DISTRIBUTION
# ---------------------------------------------------
st.subheader("⚖️ Distribution of Crime Categories")

fig_tgt, ax_tgt = plt.subplots(figsize=(5, 4))
sns.countplot(x=y, ax=ax_tgt, palette="Set2")
ax_tgt.set_title("Part 1 vs Part 2 Frequency")
st.pyplot(fig_tgt)


# ---------------------------------------------------
# FEATURE IMPORTANCE
# ---------------------------------------------------
st.subheader("🔥 Feature Importance")

importances = rf.feature_importances_
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

fig_imp, ax_imp = plt.subplots(figsize=(7, 5))
sns.barplot(data=importance_df, x="Importance", y="Feature", ax=ax_imp, palette="viridis")
ax_imp.set_title("Random Forest Feature Importance")
st.pyplot(fig_imp)


# ---------------------------------------------------
# CONFUSION MATRIX
# ---------------------------------------------------
st.subheader("📉 Confusion Matrix")

cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(
    cm,
    index=[f"Actual {cls}" for cls in rf.classes_],
    columns=[f"Pred {cls}" for cls in rf.classes_]
)

fig_cm, ax_cm = plt.subplots(figsize=(6, 4))
sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues", ax=ax_cm)
ax_cm.set_title("Confusion Matrix")
st.pyplot(fig_cm)


# ---------------------------------------------------
# PREDICTION PROBABILITY DISTRIBUTION
# ---------------------------------------------------
st.subheader("📊 Model Prediction Confidence Distribution")

proba_df = pd.DataFrame(proba, columns=rf.classes_)

fig_prob, ax_prob = plt.subplots(figsize=(7, 4))
proba_df.plot(kind="density", ax=ax_prob)
ax_prob.set_title("Prediction Probability Density")
ax_prob.set_xlabel("Probability")
st.pyplot(fig_prob)


# ---------------------------------------------------
# USER INPUT PREDICTION
# ---------------------------------------------------
st.subheader("🧪 Try Your Own Prediction")

col1, col2, col3, col4 = st.columns(4)

area = col1.number_input("AREA (1–21)", min_value=1, max_value=100, value=1)
rpt = col2.number_input("Report District No", min_value=0, max_value=9999, value=100)
crime_code = col3.number_input("Crime Code", min_value=100, max_value=999, value=510)
age = col4.number_input("Victim Age", min_value=0, max_value=100, value=30)

user_input = pd.DataFrame([{
    "AREA": area,
    "Rpt Dist No": rpt,
    "Crm Cd": crime_code,
    "Vict Age": age
}])

user_pred = rf.predict(user_input)[0]
user_proba = rf.predict_proba(user_input)[0]

st.info(f"🔮 **Predicted Crime Category (Part 1 vs Part 2):** `{user_pred}`")

# Show confidence
proba_dict = dict(zip(rf.classes_, user_proba))
st.write("### 🔬 Prediction Confidence:")
st.json(proba_dict)
