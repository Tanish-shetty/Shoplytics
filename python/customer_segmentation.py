from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def segment_from_score(row: pd.Series) -> str:
    if row["r_score"] >= 4 and row["f_score"] >= 4 and row["m_score"] >= 4:
        return "Champions"
    if row["r_score"] >= 3 and row["f_score"] >= 3 and row["m_score"] >= 3:
        return "Loyal Customers"
    if row["r_score"] >= 4 and row["f_score"] >= 2:
        return "Potential Loyalists"
    if row["r_score"] >= 4 and row["f_score"] <= 2:
        return "New Customers"
    if row["r_score"] <= 2 and row["f_score"] >= 3:
        return "At Risk"
    return "Lost Customers"


def main() -> None:
    orders = pd.read_csv(PROCESSED_DIR / "orders_clean.csv", parse_dates=["order_date"])
    completed = orders.loc[orders["status"].eq("Completed")].copy()
    snapshot_date = completed["order_date"].max() + pd.Timedelta(days=1)

    order_level = (
        completed.groupby(["customer_id", "customer_name", "region"], as_index=False)
        .agg(
            last_purchase_date=("order_date", "max"),
            order_count=("order_id", "nunique"),
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
        )
    )

    order_level["recency_days"] = (snapshot_date - order_level["last_purchase_date"]).dt.days
    order_level["frequency"] = order_level["order_count"]
    order_level["monetary"] = order_level["total_revenue"].round(2)

    order_level["r_score"] = pd.qcut(
        order_level["recency_days"].rank(method="first", ascending=False),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    order_level["f_score"] = pd.qcut(
        order_level["frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    order_level["m_score"] = pd.qcut(
        order_level["monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
    ).astype(int)
    order_level["rfm_score"] = (
        order_level["r_score"].astype(str)
        + order_level["f_score"].astype(str)
        + order_level["m_score"].astype(str)
    )
    order_level["segment"] = order_level.apply(segment_from_score, axis=1)

    order_level = order_level.sort_values(
        ["segment", "monetary"],
        ascending=[True, False],
    )
    order_level.to_csv(PROCESSED_DIR / "customer_segments.csv", index=False)

    segment_summary = (
        order_level.groupby("segment", as_index=False)
        .agg(
            customers=("customer_id", "count"),
            segment_revenue=("total_revenue", "sum"),
            avg_recency_days=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
        )
        .sort_values("segment_revenue", ascending=False)
    )
    segment_summary.to_csv(PROCESSED_DIR / "customer_segment_summary.csv", index=False)

    print("Customer segments:", order_level.shape)
    print(segment_summary.to_string(index=False))


if __name__ == "__main__":
    main()
