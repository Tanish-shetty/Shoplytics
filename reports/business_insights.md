# Business Insights

## KPI Snapshot

- Total recognized revenue: `284,741.58`
- Total profit: `53,643.61`
- Total completed orders: `695`
- Total active customers: `267`
- Total units sold: `4,848`
- Average order value: `409.70`
- Profit margin: `18.84%`
- Repeat customer rate: `73.41%`

## Important Definitions

- The project recognizes revenue only for `Completed` orders.
- `Cancelled` and `Returned` orders remain in the fact table for monitoring, but they contribute `0` recognized revenue in the current model because refund timing and realized logistics costs are not provided in the source dataset.
- The public Kaggle dataset was enriched with reproducible business fields such as state, city, region, payment method, discount, shipping cost, sub-category, and cost price so the dataset can support a full analytics dashboard.

## Key Business Insights

1. The business generated `284,741.58` in recognized revenue and `53,643.61` in profit from `695` completed orders, which translates to a healthy `18.84%` profit margin.
2. Revenue was uneven across the year. `October 2024` was the strongest month with `28,484.78` in revenue, while `June 2024` was the weakest at `20,911.98`. The jump from `September` to `October` was `31.80%`, making Q4 planning important.
3. `Hair` was the largest revenue category at `93,056.91`, but it was not the most efficient. `Body` delivered the highest category profit margin at `21.56%`, compared with `17.83%` for Hair.
4. `Skin` underperformed relative to the other categories, generating only `47,958.75` in revenue and the lowest margin at `14.84%`. This category needs pricing, assortment, or discount review.
5. Southern Europe dominated the business with `128,814.19` in revenue across `316` orders, far ahead of North Africa (`59,546.67`) and Central Europe (`45,112.76`). The business is currently dependent on one broad region.
6. The strongest individual states were `Catalonia` (`27,646.27`), `Lombardy` (`26,823.97`), and `Ile-de-France` (`23,799.23`). These markets are good candidates for deeper merchandising or paid acquisition investment.
7. Customer retention is a major growth driver. Although `73.41%` of customers were repeat buyers, they generated `89.62%` of total revenue, which means the business relies heavily on returning customers rather than one-time demand.
8. RFM segmentation shows that `Champions` are the single most valuable group, contributing `95,192.31`, or `33.43%` of customer revenue. At the same time, `At Risk` customers contributed `57,814.18`, which is large enough to justify targeted retention action.
9. Product-level analysis shows several high-revenue but lower-margin items. `Product_16`, `Product_45`, and `Product_25` were among the biggest sellers, yet each posted margins below `15%`, so scale is not automatically translating into strong profitability.
10. Discounting does not show a simple "more discount equals worse profit" pattern in this dataset. The medium-discount band produced the best margin (`21.21%`), while the high-discount band still generated the most revenue (`174,361.20`) but a weaker margin (`17.94%`). This suggests discount strategy should be optimized by product mix, not reduced blindly.
11. Payment revenue is fairly balanced across methods, but `Card` (`73,772.25`) and `Digital Wallet` (`73,331.62`) slightly outperformed the other channels. These methods are good candidates for checkout optimization or loyalty incentives.
12. Operationally, the source data still contains `83` cancelled orders and `83` returned orders after joining valid headers and items. Even though these do not count toward recognized revenue here, they are large enough to track as a service-quality KPI.

## Recommendations

1. Protect and expand the `Body` category because it combines strong revenue with the best margin profile.
2. Review `Skin` pricing, promotional depth, and product mix to improve margin without relying on volume alone.
3. Launch retention campaigns for `At Risk` customers first, because that segment already represents more than `57k` in historical revenue.
4. Build VIP or loyalty journeys for `Champions` and `Loyal Customers`, since repeat buyers already drive almost `90%` of revenue.
5. Audit high-revenue, low-margin products such as `Product_16` and `Product_45` for supplier cost, bundle strategy, and discount leakage.
6. Allocate more marketing and inventory planning attention to top-performing states like `Catalonia`, `Lombardy`, and `Ile-de-France`.
7. Track cancelled and returned orders as a separate dashboard KPI so operational friction is visible alongside sales growth.
