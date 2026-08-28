import streamlit as st
import pandas as pd
from database import get_all_queue, service_stats

def analytics_page():
    st.markdown('<div class="main-title">Queue Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Understand demand, waiting patterns and service performance.</div>', unsafe_allow_html=True)

    rows = get_all_queue()
    if not rows:
        st.info("Analytics will appear after queue activity is recorded.")
        return

    df = pd.DataFrame([dict(r) for r in rows])
    df["joined_at"] = pd.to_datetime(df["joined_at"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tokens", len(df))
    c2.metric("Completed", int((df.status == "Completed").sum()))
    c3.metric("Waiting", int((df.status == "Waiting").sum()))
    c4.metric("Cancelled", int((df.status == "Cancelled").sum()))

    st.subheader("Tokens by Service")
    service_counts = df.groupby("service").size().sort_values(ascending=False)
    st.bar_chart(service_counts)

    st.subheader("Queue Status")
    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)

    st.subheader("Hourly Demand")
    hourly = df.groupby(df["joined_at"].dt.hour).size()
    hourly.index = [f"{int(x):02d}:00" for x in hourly.index]
    st.line_chart(hourly)

    st.subheader("Service Performance")
    stats = service_stats()
    table = [dict(x) for x in stats]
    st.dataframe(table, use_container_width=True, hide_index=True)
