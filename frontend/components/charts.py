import pandas as pd
import plotly.express as px


PLOTLY_TEMPLATE = "plotly_white"
ROUTE_COLORS = {
    "calculator": "#0f766e",
    "rule_engine": "#0ea5e9",
    "search": "#f97316",
    "local_llm": "#f59e0b",
    "large_llm": "#ef4444",
}


def pie_chart(df: pd.DataFrame, names: str, values: str, title: str):
    fig = px.pie(df, names=names, values=values, hole=0.55, title=title, color=names, color_discrete_map=ROUTE_COLORS)
    fig.update_layout(template=PLOTLY_TEMPLATE, margin=dict(l=10, r=10, t=60, b=10), legend_title_text="")
    return fig


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str | None = None):
    fig = px.bar(df, x=x, y=y, title=title, color=color or x, color_discrete_map=ROUTE_COLORS, text_auto=".2s")
    fig.update_layout(template=PLOTLY_TEMPLATE, margin=dict(l=10, r=10, t=60, b=10), showlegend=bool(color))
    return fig


def line_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str | None = None):
    fig = px.line(df, x=x, y=y, title=title, color=color, markers=True, color_discrete_map=ROUTE_COLORS)
    fig.update_layout(template=PLOTLY_TEMPLATE, margin=dict(l=10, r=10, t=60, b=10))
    return fig
