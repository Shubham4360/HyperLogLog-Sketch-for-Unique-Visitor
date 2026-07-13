import time
import pandas as pd
import streamlit as st

from database.postgres import PostgreSQL
from dashboard.charts import (
    user_count_chart,
    error_chart,
    event_chart,
)

st.set_page_config(
    page_title="HyperLogLog GitHub Stream",
    layout="wide",
)

st.title("HyperLogLog Real-Time GitHub Visitor Analytics")

database = PostgreSQL()

placeholder = st.empty()

while True:

    try:

        data = database.fetch_latest(100)

        with placeholder.container():

            if not data:

                st.warning("No data found in stream_metrics table.")

            else:

                df = pd.DataFrame(data)

                df["timestamp"] = pd.to_datetime(df["timestamp"])

                df = df.sort_values("timestamp")

                latest = df.iloc[-1]

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Events Processed",
                    int(latest["events_processed"]),
                )

                col2.metric(
                    "Exact Users",
                    int(latest["exact_users"]),
                )

                col3.metric(
                    "HLL Estimate",
                    int(latest["hll_users"]),
                )

                col4.metric(
                    "Error %",
                    round(float(latest["error_percentage"]), 4),
                    
                )

                st.divider()

                st.subheader("Latest Metrics")

                st.dataframe(df.tail(10), use_container_width=True)

                st.plotly_chart(
                    event_chart(df),
                    use_container_width=True,
                )

                st.plotly_chart(
                    user_count_chart(df),
                    use_container_width=True,
                )

                st.plotly_chart(
                    error_chart(df),
                    use_container_width=True,
                )

    except Exception as e:

        st.error(f"Error: {e}")

    time.sleep(5)
