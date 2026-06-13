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
    
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    f"{total_txns:,}"
)

col2.metric(
    "Transaction Amount",
    f"₹{total_amount:,.0f}"
)

col3.metric(
    "Success %",
    f"{success_rate}%"
)




daily = (
    filtered_df
    .groupby("txn_date")
    .size()
    .reset_index(name="count")
)

fig = px.line(
    daily,
    x="txn_date",
    y="count",
    title="Daily Transaction Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


col1,col2 = st.columns(2)

bank_data = (
    filtered_df
    .groupby("bank_name")
    .size()
    .reset_index(name="count")
)

fig1 = px.bar(
    bank_data,
    x="bank_name",
    y="count",
    title="Bank-wise Transactions"
)

col1.plotly_chart(
    fig1,
    use_container_width=True
)

status_data = (
    filtered_df["status"]
    .value_counts()
    .reset_index()
)

fig2 = px.pie(
    status_data,
    names="status",
    values="count",
    title="Transaction Status"
)

col2.plotly_chart(
    fig2,
    use_container_width=True
)


failed_df = filtered_df[
    filtered_df["status"]=="Failed"
]

error_data = (
    failed_df
    .groupby("error_code")
    .size()
    .reset_index(name="count")
)

fig3 = px.bar(
    error_data,
    x="error_code",
    y="count",
    title="Failure Reasons"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

filtered_df["hour"] = (
    filtered_df["txn_time"]
    .str[:2]
    .astype(int)
)

hourly = (
    filtered_df
    .groupby("hour")
    .size()
    .reset_index(name="count")
)

fig4 = px.line(
    hourly,
    x="hour",
    y="count",
    title="Hourly Transaction Volume"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


st.subheader("Transaction Details")

st.dataframe(
    filtered_df,
    use_container_width=True
)


csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Data",
    csv,
    "transactions.csv",
    "text/csv"
)
