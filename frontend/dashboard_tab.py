import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime, date

def dashboard_ui(API_URL, categories):
    st.header("Financial Dashboard")

    try:
        # Fetch data
        monthly_response = requests.get(f"{API_URL}/month/expenses")
        monthly_response.raise_for_status()
        monthly_df = pd.DataFrame(monthly_response.json())

        category_response = requests.post(f"{API_URL}/category/expenses/", json={
            "start_date": date(datetime.now().year, datetime.now().month, 1).isoformat(),
            "end_date": date.today().isoformat()
        })
        category_response.raise_for_status()
        category_df = pd.DataFrame(category_response.json())

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return

    # Initialize variables
    current_month_expenses = 0
    top_category_name = "N/A"
    top_category_amount = 0
    total_expenses = 0

    # Process monthly data
    if not monthly_df.empty:
        monthly_df['date'] = pd.to_datetime(monthly_df['date'], format='%Y-%m')
        current_month_expenses = monthly_df['total'].iloc[-1] if len(monthly_df) > 0 else 0

    # Process category data
    if not category_df.empty:
        total_expenses = category_df['total'].sum()
        if not category_df.empty:
            top_category_row = category_df.nlargest(1, 'total')
            top_category_name = top_category_row['category'].values[0]
            top_category_amount = top_category_row['total'].values[0]

    # Savings Goal Input
    savings_goal = st.number_input("Monthly Savings Goal (₹)", min_value=0, value=5000, step=500)

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Month Expenses", f"₹{current_month_expenses:,.2f}")
    with col2:
        st.metric("Top Spending Category", f"{top_category_name}", f"₹{top_category_amount:,.2f}")
    with col3:
        savings_progress = savings_goal - current_month_expenses
        st.metric("Savings Progress", f"₹{savings_progress:,.2f}")

    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        if not monthly_df.empty:
            fig = px.area(
                monthly_df, 
                x='date', 
                y='total',
                title="Monthly Spending Trend",
                labels={'total': 'Amount (₹)', 'date': 'Month'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not category_df.empty:
            fig = px.sunburst(
                category_df,
                path=['category'],
                values='total',
                title="Spending Distribution",
                color='category'
            )
            st.plotly_chart(fig, use_container_width=True)

    # Progress bar
    if savings_goal > 0:
        progress = min(current_month_expenses / savings_goal, 1)
        st.progress(progress, text=f"Budget Utilization: {progress*100:.1f}%")
