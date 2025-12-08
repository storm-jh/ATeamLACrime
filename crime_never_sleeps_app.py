import streamlit as st
import requests

st.set_page_config(
    page_title="🧐 LA Crime Dashboard",
    page_icon=":monocle:",
    layout="wide"
)

st.write("🚓 Welcome to the multi-page LA Crime Intelligence Dashboard!")

st.write("Use the sidebar on the left to navigate between pages.")

#README from project file

import glob
import os
with open("README.md", "r") as f:
    #st.markdown(f.read(), unsafe_allow_html=True)
    readme_lines = f.readlines()
    readme.buffer = []
    resource_folder = [os.path.basename(x) for x in glob.glob("f'Resources/*")]
for line in readme_lines:
        if any(folder in line for folder in reasource_folder):
            readme_buffer.append(line)
            for image in resource_files:
                 if image in line:
                      st.markdown(''.jion9(readme_buffer[:-1]))
                      st.image(f'Resources/{image}')

# Look too make README live link from github






