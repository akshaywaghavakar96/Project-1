import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NPCI Dashboard",
    layout="wide"
)
@st.cache_data
def load_data():
    return pd.read_csv("data/transactions.csv")

df = load_data()
st.title("🏦 NPCI Transaction Monitoring Dashboard")

st.markdown("Real-time UPI Transaction Analytics")
