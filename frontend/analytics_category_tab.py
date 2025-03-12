import streamlit as st
from datetime import date
import pandas as pd
import requests
import plotly.express as px

def analytics_category_ui(API_URL):
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("📅 Start date", value=date(2024, 8, 1))

    with col2:
        end_date = st.date_input("📅 End date", value=date.today())

    button = st.button("Get Analytics")

    if button:
        st.subheader("📊 Expense Breakdown By Category")

        user_inputs = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        response = requests.post(f"{API_URL}/category/expenses/", json=user_inputs)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
        else:
            st.error("❌ Could not fetch analytics!")
            df = pd.DataFrame({
                "category": [],
                "total": [],
                "percentage": []
            })

        # Pie Chart
        fig_pie = px.pie(
            df,
            values="percentage",
            names="category",
            title="Expense Distribution by Category",
        )
        st.plotly_chart(fig_pie)

        # Bar Chart

        fig_bar = px.bar(
            df,
            x="percentage",
            y="category",
            orientation='h',
            title="Expenses by Category",
            labels={"percentage": "Total Expenses (%)", "category": "Expense Category"}
        )

        st.plotly_chart(fig_bar)

        st.table(df.style.format({"total": "{:.2f}", "percentage": "{:.2f}"}))
