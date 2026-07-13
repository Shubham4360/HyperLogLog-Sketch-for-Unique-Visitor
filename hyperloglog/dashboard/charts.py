import plotly.express as px


def user_count_chart(df):
    fig = px.line(
        df,
        x="timestamp",
        y=[
            "exact_users",
            "hll_users"
        ],
        title="Exact Users vs HyperLogLog Estimate"
    )
    return fig


def error_chart(df):
    df = df.copy()
    #df["error_percentage"] = df["error_percentage"] * 100
    fig = px.line(
        df,
        x="timestamp",
        y="error_percentage",
        title="HyperLogLog Error Percentage",
        #markers=True,
    )


    fig.update_yaxes(
        title="Error (%)",
        range=[0, 100],
        ticksuffix="%",
    )
    return fig


def event_chart(df):
    fig = px.line(
        df,
        x="timestamp",
        y="events_processed",
        title="Processed Events"
    )
    return fig