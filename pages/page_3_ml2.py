import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
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

st.header("Random Forest Model")
    
def prepare_data(dataframe):
        
    X = dataframe.drop('clean_la_crime', axis=1).copy()
    y = dataframe['clean_la_crime'].copy()
        
    # Encode categorical variables
    label_encoders = {}
    categorical_cols = X.select_dtypes(include=['object']).columns
        
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
        
        return X, y, label_encoders
    
    # Train model button
    if st.button("Train Model"):
        with st.spinner("Training Random Forest..."):
            # Prepare data
            X, y, encoders = prepare_data(df)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Train model
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Store in session state
            st.session_state['model'] = model
            st.session_state['encoders'] = encoders
            st.session_state['features'] = X.columns.tolist()
            
            # Display metrics
            TIME_OCC, LOCATION = st.columns(2)
            
            with TIME_OCC:
                st.subheader("Model Performance")
                accuracy = accuracy_score(y_test, y_pred)
                st.metric("Accuracy", f"{accuracy:.2%}")
                
                # Confusion Matrix
                st.subheader("Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred)
                fig, ax = plt.subplots()
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
                ax.set_xlabel('Predicted')
                ax.set_ylabel('Actual')
                st.pyplot(fig)
            
            with LOCATION:
                st.subheader("Feature Importance")
                importance_df = pd.DataFrame({
                    'feature': X.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False).head(10)
                
                fig2, ax2 = plt.subplots()
                ax2.barh(importance_df['feature'], importance_df['importance'])
                ax2.set_xlabel('Importance')
                st.pyplot(fig2)