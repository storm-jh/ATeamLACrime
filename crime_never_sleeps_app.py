import streamlit as st
import os

st.set_page_config(
    page_title="🧐 LA Crime Dashboard",
    page_icon=":monocle:",
    layout="wide"
)

st.write("🚓 Welcome to the multi-page LA Crime Intelligence Dashboard!")
st.write("Use the sidebar on the left to navigate between pages.")

# --------------------------
# LOAD README.md
# --------------------------
README_PATH = "README.md"

if os.path.exists(README_PATH):
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_text = f.read()

    st.markdown("---")
    st.header("📘 Project README")
    st.markdown(readme_text, unsafe_allow_html=False)
else:
    st.error("❌ README.md not found in project directory.")


# Look too make README live from github






