from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FRONTEND_DATA_DIR = PROJECT_ROOT / "frontend" / "data"


def build_dashboard_payload() -> dict:
    orders = pd.read_csv(PROCESSED_DIR / "orders_clean.csv", parse_dates=["order_date"])
    segments = pd.read_csv(PROCESSED_DIR / "customer_segments.csv")

    segment_map = {
        str(int(row.customer_id)): row.segment
        for row in segments.itertuples(index=False)
    }

    records = []
    for row in orders.itertuples(index=False):
        records.append(
            {
                "orderId": int(row.order_id),
                "orderDate": row.order_date.strftime("%Y-%m-%d"),
                "orderMonth": row.order_month,
                "customerId": int(row.customer_id),
                "customerName": row.customer_name,
                "region": row.region,
                "state": row.state,
                "country": row.country,
                "category": row.category,
                "subCategory": row.sub_category,
                "productId": int(row.product_id),
                "productName": row.product_name,
                "quantity": int(row.quantity),
                "revenue": round(float(row.revenue), 2),
                "profit": round(float(row.profit), 2),
                "profitMargin": round(float(row.profit_margin), 2),
                "paymentMethod": row.payment_method,
                "status": row.status,
                "segment": segment_map.get(str(int(row.customer_id)), "Unsegmented"),
            }
        )

    filters = {
        "regions": sorted(orders["region"].dropna().unique().tolist()),
        "categories": sorted(orders["category"].dropna().unique().tolist()),
        "paymentMethods": sorted(orders["payment_method"].dropna().unique().tolist()),
        "statuses": sorted(orders["status"].dropna().unique().tolist()),
    }

    metadata = {
        "title": "Shoplytics Dashboard",
        "subtitle": "Interactive e-commerce sales and customer analytics view built from the processed project outputs.",
        "dataset": "maramsa/e-commerce-sales-and-customer-analytics-dataset",
        "recordCount": len(records),
        "dateStart": orders["order_date"].min().strftime("%Y-%m-%d"),
        "dateEnd": orders["order_date"].max().strftime("%Y-%m-%d"),
    }

    return {"metadata": metadata, "filters": filters, "records": records}


def main() -> None:
    FRONTEND_DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_dashboard_payload()
    target = FRONTEND_DATA_DIR / "dashboard_data.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote dashboard payload to {target}")
    print(f"Records exported: {len(payload['records'])}")


if __name__ == "__main__":
    main()
