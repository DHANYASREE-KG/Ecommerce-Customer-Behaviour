import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

CHART_BLUE = "#2563EB"
CHART_TEAL = "#0F766E"
CHART_AMBER = "#F59E0B"
CHART_CORAL = "#E76F51"
CHART_GREEN = "#15803D"
CHART_RED = "#DC2626"
CHART_PURPLE = "#7C3AED"


def _fig_to_html(fig) -> str:
    """Convert a Matplotlib figure to an inline HTML image."""
    buffer = io.BytesIO()
    try:
        fig.savefig(
            buffer,
            format="png",
            dpi=80,
            bbox_inches="tight",
            pil_kwargs={"optimize": True},
        )
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return (
            '<img src="data:image/png;base64,'
            f'{image_base64}" style="width:100%;height:auto;border-radius:12px;" />'
        )
    finally:
        buffer.close()
        plt.close(fig)


def _prepare_chart_df(df: pd.DataFrame) -> pd.DataFrame:
    if "Month" in df.columns:
        return df

    chart_df = df.copy()
    if "order_date" not in chart_df.columns and "Order Date" in chart_df.columns:
        chart_df["order_date"] = pd.to_datetime(chart_df["Order Date"])
    elif "order_date" in chart_df.columns:
        chart_df["order_date"] = pd.to_datetime(chart_df["order_date"])

    if "Order Date" not in chart_df.columns:
        chart_df["Order Date"] = chart_df["order_date"]

    chart_df["Month"] = chart_df["order_date"].dt.to_period("M").astype(str)

    return chart_df


def build_category_distribution(df: pd.DataFrame) -> str:
    """Bar chart showing category-wise sales."""
    chart_df = _prepare_chart_df(df)
    category_sales = chart_df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x=category_sales.values,
        y=category_sales.index,
        color=CHART_TEAL,
        ax=ax,
    )
    ax.set_title("Sales by Category", fontsize=14, weight="bold")
    ax.set_xlabel("Sales (Rs.)")
    ax.set_ylabel("Category")
    for container in ax.containers:
        ax.bar_label(container, fmt="Rs.%,.0f", padding=3)
    fig.tight_layout()
    return _fig_to_html(fig)


def build_state_heatmap(df: pd.DataFrame) -> str:
    """Heatmap showing monthly sales by state."""
    chart_df = _prepare_chart_df(df)
    pivot_data = chart_df.pivot_table(index="State", columns="Month", values="Sales", aggfunc="sum")
    top_states = pivot_data.sum(axis=1).nlargest(12).index
    pivot_data = pivot_data.loc[top_states]

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(pivot_data, cmap="GnBu", annot=False, ax=ax, linewidths=0.5)
    ax.set_title("Monthly Sales Heatmap by State", fontsize=14, weight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("State")
    fig.tight_layout()
    return _fig_to_html(fig)


def build_profit_by_subcategory(df: pd.DataFrame) -> str:
    """Horizontal bar chart showing profit by sub-category."""
    chart_df = _prepare_chart_df(df)
    profit_data = chart_df.groupby("Sub-Category")["Profit"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(12, 7))
    colors = [CHART_RED if x < 0 else CHART_GREEN for x in profit_data.values]
    profit_data.plot(kind="barh", ax=ax, color=colors, edgecolor="black")
    ax.set_title("Profit by Sub-Category", fontsize=14, weight="bold")
    ax.set_xlabel("Profit (Rs.)")
    ax.set_ylabel("Sub-Category")
    for bar, value in zip(ax.patches, profit_data.values):
        offset = 100 if value >= 0 else -100
        alignment = "left" if value >= 0 else "right"
        ax.text(
            value + offset,
            bar.get_y() + bar.get_height() / 2,
            f"Rs.{value:,.0f}",
            va="center",
            ha=alignment,
        )
    fig.tight_layout()
    return _fig_to_html(fig)


def build_sales_by_region(df: pd.DataFrame) -> str:
    """Bar chart of total sales by region."""
    chart_df = _prepare_chart_df(df)
    region_data = chart_df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=region_data.index,
        y=region_data.values,
        color=CHART_BLUE,
        ax=ax,
    )
    ax.set_title("Total Sales by Region", fontsize=14, weight="bold")
    ax.set_xlabel("Region")
    ax.set_ylabel("Sales (Rs.)")
    for container in ax.containers:
        ax.bar_label(container, fmt="Rs.%,.0f", padding=3)
    plt.setp(ax.get_xticklabels(), rotation=15)
    fig.tight_layout()
    return _fig_to_html(fig)


def build_discount_impact(df: pd.DataFrame) -> str:
    """Scatter plot showing the impact of discount on profit."""
    chart_df = _prepare_chart_df(df)
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(
        data=chart_df,
        x=chart_df["Discount"] * 100,
        y=chart_df["Profit"],
        hue=chart_df["Sales"],
        palette="crest",
        size=chart_df["Sales"],
        sizes=(20, 180),
        alpha=0.7,
        ax=ax,
    )
    ax.axhline(0, color=CHART_RED, linestyle="--", linewidth=1)
    ax.set_title("Discount vs Profit", fontsize=14, weight="bold")
    ax.set_xlabel("Discount (%)")
    ax.set_ylabel("Profit (Rs.)")
    fig.tight_layout()
    return _fig_to_html(fig)


def build_rfm_segment_heatmap(rfm: pd.DataFrame) -> str:
    """Heatmap of average RFM scores by segment."""
    if rfm.empty:
        return ""
    segment_data = rfm.groupby("Segment")[["R_Score", "F_Score", "M_Score"]].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        segment_data.T,
        annot=True,
        fmt=".1f",
        cmap="YlGn",
        cbar_kws={"label": "Score"},
        ax=ax,
    )
    ax.set_title("Average RFM Scores by Segment", fontsize=14, weight="bold")
    ax.set_xlabel("Segment")
    ax.set_ylabel("RFM Score")
    fig.tight_layout()
    return _fig_to_html(fig)


def build_monthly_trend(df: pd.DataFrame) -> str:
    """Line chart of monthly sales and profit trends."""
    chart_df = _prepare_chart_df(df)
    monthly_data = chart_df.groupby("Month").agg({"Sales": "sum", "Profit": "sum"}).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        monthly_data["Month"],
        monthly_data["Sales"],
        marker="o",
        linewidth=2.5,
        color=CHART_BLUE,
        label="Sales",
    )
    ax2 = ax.twinx()
    ax2.plot(
        monthly_data["Month"],
        monthly_data["Profit"],
        marker="s",
        linewidth=2.5,
        color=CHART_CORAL,
        label="Profit",
    )
    ax.set_title("Monthly Sales and Profit Trend", fontsize=14, weight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales (Rs.)", color=CHART_BLUE)
    ax2.set_ylabel("Profit (Rs.)", color=CHART_CORAL)
    plt.setp(ax.get_xticklabels(), rotation=45)
    fig.tight_layout()
    return _fig_to_html(fig)


def build_customer_segment_distribution(rfm: pd.DataFrame) -> str:
    """Bar chart showing customer counts per segment."""
    if rfm.empty:
        return ""
    segment_counts = rfm["Segment"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=segment_counts.index,
        y=segment_counts.values,
        color=CHART_AMBER,
        ax=ax,
    )
    ax.set_title("Customer Segment Distribution", fontsize=14, weight="bold")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Customers")
    for container in ax.containers:
        ax.bar_label(container, padding=3)
    plt.setp(ax.get_xticklabels(), rotation=15)
    fig.tight_layout()
    return _fig_to_html(fig)


def build_customer_spending_distribution(df: pd.DataFrame) -> str:
    """Histogram of customer spending behavior."""
    chart_df = _prepare_chart_df(df)
    customer_spend = chart_df.groupby("Customer ID")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(customer_spend, bins=20, kde=True, color=CHART_PURPLE, ax=ax)
    ax.set_title("Customer Spending Distribution", fontsize=14, weight="bold")
    ax.set_xlabel("Total Spend per Customer (Rs.)")
    ax.set_ylabel("Customers")
    fig.tight_layout()
    return _fig_to_html(fig)
