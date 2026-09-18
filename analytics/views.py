import logging

import pandas as pd
from django.shortcuts import render

from .analysis.matplotlib_charts import (
    build_category_distribution,
    build_customer_segment_distribution,
    build_customer_spending_distribution,
    build_discount_impact,
    build_monthly_trend,
    build_profit_by_subcategory,
    build_rfm_segment_heatmap,
    build_sales_by_region,
    build_state_heatmap,
)
from .models import Customer, Order, RfmSegment

logger = logging.getLogger(__name__)


def _safe_chart(builder, *args, **kwargs):
    try:
        return builder(*args, **kwargs)
    except Exception as exc:
        logger.error("Chart error in %s: %s", builder.__name__, exc)
        return ""


def _prepare_data(state=None, category=None, segment=None):
    filters = {}
    if state:
        filters["state"] = state
    if category:
        filters["category"] = category

    orders = Order.objects.select_related("customer").filter(**filters).values(
        "order_id",
        "order_date",
        "ship_date",
        "category",
        "sub_category",
        "state",
        "region",
        "sales",
        "profit",
        "discount",
        "quantity",
        "customer__customer_id",
    )
    df = pd.DataFrame(list(orders))

    if df.empty:
        return df, pd.DataFrame()

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])
    df.rename(
        columns={
            "category": "Category",
            "sub_category": "Sub-Category",
            "state": "State",
            "region": "Region",
            "sales": "Sales",
            "profit": "Profit",
            "discount": "Discount",
            "quantity": "Quantity",
            "order_id": "Order ID",
            "customer__customer_id": "Customer ID",
        },
        inplace=True,
    )
    df["Order Date"] = df["order_date"]
    df["Month"] = df["order_date"].dt.to_period("M").astype(str)

    rfm_qs = RfmSegment.objects.all().values(
        "customer__customer_id",
        "recency",
        "frequency",
        "monetary",
        "r_score",
        "f_score",
        "m_score",
        "rfm_score",
        "segment",
    )
    rfm = pd.DataFrame(list(rfm_qs))

    if not rfm.empty:
        rfm.rename(
            columns={
                "customer__customer_id": "Customer ID",
                "segment": "Segment",
                "recency": "Recency",
                "frequency": "Frequency",
                "monetary": "Monetary",
                "r_score": "R_Score",
                "f_score": "F_Score",
                "m_score": "M_Score",
                "rfm_score": "RFM_Score",
            },
            inplace=True,
        )

    if segment:
        if rfm.empty:
            return df.iloc[0:0], rfm
        rfm = rfm[rfm["Segment"] == segment].copy()
        customer_ids = rfm["Customer ID"].tolist()
        if not customer_ids:
            return df.iloc[0:0], rfm
        df = df[df["Customer ID"].isin(customer_ids)].copy()

    if not rfm.empty:
        rfm = rfm[rfm["Customer ID"].isin(df["Customer ID"].unique())].copy()

    return df, rfm


def _dashboard_context(request, state=None, category=None, segment=None):
    df, rfm = _prepare_data(state=state, category=category, segment=segment)

    if df.empty:
        return {
            "error": "No data matches the selected filters. Try another option.",
            "selected_state": state or "",
            "selected_category": category or "",
            "selected_segment": segment or "",
            "states": list(Order.objects.order_by("state").values_list("state", flat=True).distinct()),
            "categories": list(Order.objects.order_by("category").values_list("category", flat=True).distinct()),
            "segments": list(RfmSegment.objects.order_by("segment").values_list("segment", flat=True).distinct()),
        }

    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_orders = int(df["Order ID"].nunique())
    total_customers = int(df["Customer ID"].nunique())
    avg_order_value = total_sales / total_orders if total_orders else 0

    context = {
        "fig_category": _safe_chart(build_category_distribution, df),
        "fig_customer_spend": _safe_chart(build_customer_spending_distribution, df),
        "fig_trend": _safe_chart(build_monthly_trend, df),
        "fig_discount": _safe_chart(build_discount_impact, df),
        "fig_region": _safe_chart(build_sales_by_region, df),
        "fig_profit": _safe_chart(build_profit_by_subcategory, df),
        "fig_rfm_heat": _safe_chart(build_rfm_segment_heatmap, rfm) if not rfm.empty else "",
        "fig_customer_dist": _safe_chart(build_customer_segment_distribution, rfm) if not rfm.empty else "",
        "fig_state_heatmap": _safe_chart(build_state_heatmap, df),
        "kpi_sales": f"₹{total_sales:,.0f}",
        "kpi_orders": f"{total_orders:,}",
        "kpi_customers": f"{total_customers:,}",
        "kpi_aov": f"₹{avg_order_value:,.0f}",
        "kpi_margin": f"{(total_profit / total_sales * 100) if total_sales else 0:.1f}%",
        "selected_state": state or "",
        "selected_category": category or "",
        "selected_segment": segment or "",
        "states": list(Order.objects.order_by("state").values_list("state", flat=True).distinct()),
        "categories": list(Order.objects.order_by("category").values_list("category", flat=True).distinct()),
        "segments": list(RfmSegment.objects.order_by("segment").values_list("segment", flat=True).distinct()),
    }
    return context


def dashboard(request):
    state = request.GET.get("state")
    category = request.GET.get("category")
    segment = request.GET.get("segment")
    context = _dashboard_context(request, state=state, category=category, segment=segment)
    return render(request, "analytics/dashboard.html", context)


def state_dashboard(request, state_name):
    request.GET = request.GET.copy()
    request.GET["state"] = state_name
    return dashboard(request)

