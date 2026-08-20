from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_SOURCE_DIR = Path(
    os.getenv(
        "KAGGLE_DATASET_PATH",
        r"C:\Users\tanis\.cache\kagglehub\datasets\maramsa\e-commerce-sales-and-customer-analytics-dataset\versions\2",
    )
)
CACHED_SOURCE_DIR = Path(
    r"C:\Users\tanis\.cache\kagglehub\datasets\maramsa\e-commerce-sales-and-customer-analytics-dataset\versions\2"
)

COUNTRY_LOCATION_MAP = {
    "Spain": {
        "region": "Southern Europe",
        "states": [
            ("Madrid", ["Madrid", "Alcala de Henares", "Mostoles"]),
            ("Catalonia", ["Barcelona", "Girona", "Tarragona"]),
            ("Andalusia", ["Seville", "Malaga", "Granada"]),
        ],
    },
    "Italy": {
        "region": "Southern Europe",
        "states": [
            ("Lazio", ["Rome", "Latina", "Viterbo"]),
            ("Lombardy", ["Milan", "Bergamo", "Brescia"]),
            ("Campania", ["Naples", "Salerno", "Caserta"]),
        ],
    },
    "France": {
        "region": "Western Europe",
        "states": [
            ("Ile-de-France", ["Paris", "Versailles", "Boulogne"]),
            ("Provence-Alpes-Cote d'Azur", ["Marseille", "Nice", "Cannes"]),
            ("Auvergne-Rhone-Alpes", ["Lyon", "Grenoble", "Annecy"]),
        ],
    },
    "Germany": {
        "region": "Central Europe",
        "states": [
            ("Bavaria", ["Munich", "Nuremberg", "Augsburg"]),
            ("Berlin", ["Berlin", "Potsdam", "Oranienburg"]),
            ("North Rhine-Westphalia", ["Cologne", "Dortmund", "Bonn"]),
        ],
    },
    "Morocco": {
        "region": "North Africa",
        "states": [
            ("Casablanca-Settat", ["Casablanca", "Settat", "Mohammedia"]),
            ("Rabat-Sale-Kenitra", ["Rabat", "Sale", "Kenitra"]),
            ("Marrakesh-Safi", ["Marrakesh", "Safi", "Essaouira"]),
        ],
    },
}

SUBCATEGORY_MAP = {
    "Hair": [
        "Shampoo",
        "Conditioner",
        "Hair Mask",
        "Hair Oil",
        "Styling",
        "Scalp Care",
    ],
    "Makeup": [
        "Foundation",
        "Lipstick",
        "Mascara",
        "Eyeshadow",
        "Concealer",
        "Blush",
    ],
    "Body": [
        "Body Wash",
        "Body Lotion",
        "Scrub",
        "Hand Care",
        "Deodorant",
    ],
    "Skin": [
        "Cleanser",
        "Serum",
        "Moisturizer",
        "Sunscreen",
        "Toner",
    ],
}

PAYMENT_METHODS = ["Card", "Digital Wallet", "Bank Transfer", "Cash on Delivery"]
GENDER_VALUES = ["Female", "Male", "Non-binary"]


def ensure_directories() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def resolve_source_dir() -> Path:
    candidates = []

    env_path = os.getenv("KAGGLE_DATASET_PATH")
    if env_path:
        candidates.append(Path(env_path))

    candidates.extend([RAW_DIR, DEFAULT_SOURCE_DIR, CACHED_SOURCE_DIR])

    required_files = ["customers.csv", "orders.csv", "order_items.csv", "products.csv"]
    for candidate in candidates:
        if all((candidate / file_name).exists() for file_name in required_files):
            if env_path and candidate != Path(env_path):
                print(
                    "Warning: KAGGLE_DATASET_PATH does not contain the expected files. "
                    f"Falling back to {candidate}."
                )
            return candidate

    raise FileNotFoundError(
        "Could not find the source dataset files. Set KAGGLE_DATASET_PATH to the folder "
        "containing customers.csv, orders.csv, order_items.csv, and products.csv."
    )


def copy_raw_files(source_dir: Path) -> None:
    for file_name in ["customers.csv", "orders.csv", "order_items.csv", "products.csv"]:
        source_file = source_dir / file_name
        if not source_file.exists():
            raise FileNotFoundError(f"Missing source file: {source_file}")
        target_file = RAW_DIR / file_name
        if not target_file.exists() or source_file.read_bytes() != target_file.read_bytes():
            target_file.write_bytes(source_file.read_bytes())


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    customers = customers.drop_duplicates(subset=["customer_id"]).copy()
    customers["customer_id"] = pd.to_numeric(customers["customer_id"], errors="coerce").astype("Int64")
    customers["signup_date"] = pd.to_datetime(customers["signup_date"], errors="coerce")
    customers["country"] = customers["country"].fillna("Unknown")

    missing_locations = []
    enriched_rows = []
    for row in customers.itertuples(index=False):
        customer_id = int(row.customer_id)
        country = row.country
        location = COUNTRY_LOCATION_MAP.get(country)
        if location is None:
            missing_locations.append(country)
            state = "Unknown"
            city = "Unknown"
            region = "Unknown"
        else:
            state_index = customer_id % len(location["states"])
            state, cities = location["states"][state_index]
            city = cities[customer_id % len(cities)]
            region = location["region"]

        enriched_rows.append(
            {
                "customer_id": customer_id,
                "customer_name": f"Customer_{customer_id:04d}",
                "gender": GENDER_VALUES[customer_id % len(GENDER_VALUES)],
                "age": 20 + ((customer_id * 7) % 41),
                "city": city,
                "state": state,
                "region": region,
                "country": country,
                "signup_date": row.signup_date,
            }
        )

    if missing_locations:
        print("Warning: missing location mappings for", sorted(set(missing_locations)))

    customer_dim = pd.DataFrame(enriched_rows).sort_values("customer_id")
    return customer_dim


def clean_products(products: pd.DataFrame, order_items: pd.DataFrame) -> pd.DataFrame:
    products = products.drop_duplicates(subset=["product_id"]).copy()
    products["product_id"] = pd.to_numeric(products["product_id"], errors="coerce").astype("Int64")
    products["product_name"] = products["product_name"].fillna("Unknown Product")
    products["category"] = products["category"].fillna("Other")

    avg_prices = (
        order_items.groupby("product_id", as_index=False)["price"]
        .mean()
        .rename(columns={"price": "selling_price"})
    )

    product_dim = products.merge(avg_prices, on="product_id", how="left")
    product_dim["selling_price"] = product_dim["selling_price"].fillna(product_dim["selling_price"].median())

    sub_categories = []
    cost_prices = []
    for row in product_dim.itertuples(index=False):
        options = SUBCATEGORY_MAP.get(row.category, ["General"])
        sub_categories.append(options[int(row.product_id) % len(options)])
        margin_rate = 0.22 + ((int(row.product_id) % 5) * 0.05)
        cost_prices.append(round(row.selling_price * (1 - margin_rate), 2))

    product_dim["sub_category"] = sub_categories
    product_dim["cost_price"] = np.maximum(np.array(cost_prices), 1.0)
    product_dim["selling_price"] = product_dim["selling_price"].round(2)

    return product_dim[
        [
            "product_id",
            "product_name",
            "category",
            "sub_category",
            "cost_price",
            "selling_price",
        ]
    ].sort_values("product_id")


def build_orders_fact(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    orders = orders.drop_duplicates(subset=["order_id"]).copy()
    orders["order_id"] = pd.to_numeric(orders["order_id"], errors="coerce").astype("Int64")
    orders["customer_id"] = pd.to_numeric(orders["customer_id"], errors="coerce").astype("Int64")
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["status"] = orders["status"].fillna("Unknown")

    order_items = order_items.copy()
    order_items["order_id"] = pd.to_numeric(order_items["order_id"], errors="coerce").astype("Int64")
    order_items["product_id"] = pd.to_numeric(order_items["product_id"], errors="coerce").astype("Int64")
    order_items["quantity"] = pd.to_numeric(order_items["quantity"], errors="coerce").clip(lower=0)
    order_items["unit_price"] = pd.to_numeric(order_items["price"], errors="coerce").clip(lower=0)

    fact = (
        order_items.merge(
            orders[["order_id", "customer_id", "order_date", "status"]],
            on="order_id",
            how="left",
        )
        .merge(products, on="product_id", how="left")
        .merge(
            customers[["customer_id", "customer_name", "gender", "age", "city", "state", "region", "country", "signup_date"]],
            on="customer_id",
            how="left",
        )
    )

    fact = fact.dropna(subset=["customer_id", "product_id", "order_date"]).copy()
    fact["order_month"] = fact["order_date"].dt.to_period("M").astype(str)
    fact["order_year"] = fact["order_date"].dt.year
    fact["order_week"] = fact["order_date"].dt.isocalendar().week.astype(int)

    payment_codes = (fact["order_id"].astype(int) + fact["customer_id"].astype(int)) % len(PAYMENT_METHODS)
    fact["payment_method"] = payment_codes.map(lambda idx: PAYMENT_METHODS[int(idx)])

    base_discount = np.select(
        [fact["quantity"] >= 4, fact["quantity"] == 3, fact["quantity"] == 2],
        [0.10, 0.07, 0.04],
        default=0.02,
    )
    seasonal_discount = np.where(fact["order_date"].dt.month.isin([11, 12]), 0.03, 0.0)
    returned_discount = np.where(fact["status"].eq("Returned"), 0.02, 0.0)
    fact["discount"] = np.minimum(base_discount + seasonal_discount + returned_discount, 0.18).round(4)

    fact["gross_revenue"] = (fact["quantity"] * fact["unit_price"]).round(2)
    fact["discount_amount"] = (fact["gross_revenue"] * fact["discount"]).round(2)

    shipping_base = 5 + (fact["quantity"] * 1.25) + (fact["order_id"].astype(int) % 4)
    shipping_multiplier = np.where(fact["country"].eq("Morocco"), 1.12, 1.0)
    fact["shipping_cost"] = (shipping_base * shipping_multiplier).round(2)

    completed_mask = fact["status"].eq("Completed")
    fact["revenue"] = np.where(completed_mask, fact["gross_revenue"] - fact["discount_amount"], 0.0).round(2)
    fact["cost"] = np.where(completed_mask, fact["quantity"] * fact["cost_price"], 0.0).round(2)
    fact["profit"] = (fact["revenue"] - fact["cost"] - np.where(completed_mask, fact["shipping_cost"], 0.0)).round(2)
    fact["profit_margin"] = np.where(fact["revenue"] > 0, (fact["profit"] / fact["revenue"]) * 100, 0.0).round(2)

    completed_counts = (
        fact.loc[completed_mask, ["customer_id", "order_id"]]
        .drop_duplicates()
        .groupby("customer_id")
        .size()
        .rename("customer_order_count")
    )
    fact = fact.merge(completed_counts, on="customer_id", how="left")
    fact["customer_order_count"] = fact["customer_order_count"].fillna(0).astype(int)

    return fact[
        [
            "order_id",
            "order_date",
            "order_year",
            "order_month",
            "order_week",
            "customer_id",
            "customer_name",
            "gender",
            "age",
            "city",
            "state",
            "region",
            "country",
            "signup_date",
            "product_id",
            "product_name",
            "category",
            "sub_category",
            "quantity",
            "unit_price",
            "discount",
            "discount_amount",
            "gross_revenue",
            "revenue",
            "cost",
            "shipping_cost",
            "profit",
            "profit_margin",
            "payment_method",
            "status",
            "customer_order_count",
        ]
    ].sort_values(["order_date", "order_id", "product_id"])


def build_date_table(orders_fact: pd.DataFrame) -> pd.DataFrame:
    date_range = pd.date_range(orders_fact["order_date"].min(), orders_fact["order_date"].max(), freq="D")
    date_table = pd.DataFrame({"date": date_range})
    date_table["year"] = date_table["date"].dt.year
    date_table["quarter"] = "Q" + date_table["date"].dt.quarter.astype(str)
    date_table["month_number"] = date_table["date"].dt.month
    date_table["month_name"] = date_table["date"].dt.strftime("%B")
    date_table["month_start"] = date_table["date"].dt.to_period("M").dt.to_timestamp()
    date_table["week_of_year"] = date_table["date"].dt.isocalendar().week.astype(int)
    date_table["day_name"] = date_table["date"].dt.strftime("%A")
    return date_table


def build_summary(orders_fact: pd.DataFrame, customers: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    completed_orders = orders_fact.loc[orders_fact["status"].eq("Completed")].copy()
    unique_orders = completed_orders["order_id"].nunique()
    total_revenue = completed_orders["revenue"].sum()
    total_profit = completed_orders["profit"].sum()
    total_customers = completed_orders["customer_id"].nunique()
    repeat_customers = (
        completed_orders[["customer_id", "order_id"]]
        .drop_duplicates()
        .groupby("customer_id")
        .size()
        .gt(1)
        .sum()
    )
    summary = {
        "metric": [
            "source_dataset",
            "total_rows_in_fact",
            "completed_orders",
            "cancelled_orders",
            "returned_orders",
            "total_customers",
            "total_products",
            "total_revenue",
            "total_profit",
            "average_order_value",
            "profit_margin_percent",
            "repeat_customer_rate_percent",
        ],
        "value": [
            "maramsa/e-commerce-sales-and-customer-analytics-dataset",
            len(orders_fact),
            unique_orders,
            orders_fact.loc[orders_fact["status"].eq("Cancelled"), "order_id"].nunique(),
            orders_fact.loc[orders_fact["status"].eq("Returned"), "order_id"].nunique(),
            total_customers,
            products["product_id"].nunique(),
            round(total_revenue, 2),
            round(total_profit, 2),
            round(total_revenue / unique_orders, 2) if unique_orders else 0,
            round((total_profit / total_revenue) * 100, 2) if total_revenue else 0,
            round((repeat_customers / total_customers) * 100, 2) if total_customers else 0,
        ],
    }
    return pd.DataFrame(summary)


def main() -> None:
    ensure_directories()
    source_dir = resolve_source_dir()
    copy_raw_files(source_dir)

    customers_raw = pd.read_csv(RAW_DIR / "customers.csv")
    orders_raw = pd.read_csv(RAW_DIR / "orders.csv")
    order_items_raw = pd.read_csv(RAW_DIR / "order_items.csv")
    products_raw = pd.read_csv(RAW_DIR / "products.csv")

    customers = clean_customers(customers_raw)
    products = clean_products(products_raw, order_items_raw)
    orders_fact = build_orders_fact(orders_raw, order_items_raw, customers, products)
    date_table = build_date_table(orders_fact)
    summary = build_summary(orders_fact, customers, products)

    customers.to_csv(PROCESSED_DIR / "customers_clean.csv", index=False)
    products.to_csv(PROCESSED_DIR / "products_clean.csv", index=False)
    orders_fact.to_csv(PROCESSED_DIR / "orders_clean.csv", index=False)
    date_table.to_csv(PROCESSED_DIR / "date_dim.csv", index=False)
    summary.to_csv(PROCESSED_DIR / "project_summary.csv", index=False)

    print("Processed customers:", customers.shape)
    print("Processed products:", products.shape)
    print("Processed orders:", orders_fact.shape)
    print("Date dimension:", date_table.shape)


if __name__ == "__main__":
    main()
