import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NPCI Dashboard",
    layout="wide"
)
@st.cache_data
def load_data():
    return pd.read_csv("transactions.csv")

df = load_data()
st.title("🏦 NPCI Transaction Monitoring Dashboard")

st.markdown("Real-time UPI Transaction Analytics")

st.sidebar.header("Filters")

selected_bank = st.sidebar.multiselect(
    "Select Bank",
    options=df["bank_name"].unique(),
    default=df["bank_name"].unique()
)

selected_status = st.sidebar.multiselect(
    "Select Status",
    options=df["status"].unique(),
    default=df["status"].unique()
)

filtered_df = df[
    (df["bank_name"].isin(selected_bank)) &
    (df["status"].isin(selected_status))
]

total_txns = len(filtered_df)

total_amount = filtered_df["amount"].sum()

if total_txns > 0:
    success_rate = round(
        (
            len(filtered_df[filtered_df["status"] == "Success"])
            / total_txns
        ) * 100,
        2,
    )

    failed_rate = round(
        (
            len(filtered_df[filtered_df["status"] == "Failed"])
            / total_txns
        ) * 100,
        2,
    )
else:
    success_rate = 0
    failed_rate = 0
