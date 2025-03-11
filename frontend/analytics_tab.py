import streamlit as st
from datetime import datetime
import pandas as pd

def analytics_ui():
    with st.form(key="date-selection-form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.date_input(label="Start date", value=datetime(2024, 8, 1))
        
        with col2:
            st.date_input(label="End date", value=datetime.now())
        
        st.form_submit_button(label="Get Analytics")
    
    st.subheader("Expense Breakdown By Category")
    
    df = pd.DataFrame({
        "Category": ["Rent", "Food", "Shopping"],
        "Total": [1200, 100, 200],
        "Percentage": [70, 10, 20]
    })
    
    st.bar_chart(data=df[["Category", "Total"]].set_index("Category"))
    
    st.table(df)