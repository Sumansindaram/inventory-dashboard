import streamlit as st
import pandas as pd

# Function to calculate running stock
def calculate_running_stock(df):
    df['Updated Stock'] = df['Stock Held']
    for i in range(1, len(df)):
        if df.loc[i, 'ITEM'] == df.loc[i-1, 'ITEM']:
            df.loc[i, 'Updated Stock'] = df.loc[i-1, 'Updated Stock'] - df.loc[i, 'QTY Demanded']
    return df

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read the Excel file
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # Calculate running stock
    df = calculate_running_stock(df)
    
    # Display updated inventory table
    st.write("Updated Inventory Table")
    st.dataframe(df)
    
    # Bar chart of current stock levels
    st.write("Current Stock Levels")
    st.bar_chart(df.groupby('ITEM')['Updated Stock'].sum())
    
    # Line chart of total demand per item
    st.write("Total Demand per Item")
    st.line_chart(df.groupby('ITEM')['QTY Demanded'].sum())
    
    # Table of low stock alerts
    st.write("Low Stock Alerts")
    low_stock_df = df[df['Updated Stock'] < df['Max Issue']]
    st.dataframe(low_stock_df)
