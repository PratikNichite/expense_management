import streamlit as st
from datetime import datetime, date
import pandas as pd
import requests

def analytics_category_ui(API_URL):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(label="Start date", value=date(2024, 8, 1))
        
        with col2:
            end_date = st.date_input(label="End date", value=date.today())
        
        button = st.button(label="Get Analytics")
        
        if button:
            st.subheader("Expense Breakdown By Category")
            
            user_inputs = {
                "start_date":start_date.isoformat(), 
                "end_date":end_date.isoformat()
            }
            
            response = requests.post(f"{API_URL}/expenses/category/", json=user_inputs)
            
            if response.status_code == 200:    
                data = response.json()
                df = pd.DataFrame(data)
            else:
                st.error("Could not fetch analytics!")
                df = pd.DataFrame({
                        "category": [],
                        "total": [],
                        "percentage": []
                    })
            
            st.bar_chart(
                data=df[["category", "percentage"]].set_index("category"),
                x_label="Expense Category",
                y_label="Total Expenses (%)",
            )
            
            
            st.table(df.style.format({"total": "{:.2f}", "percentage": "{:.2f}"}))
