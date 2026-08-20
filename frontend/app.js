const state = {
  payload: null,
  filters: {
    status: "Completed",
    region: "All",
    category: "All",
    paymentMethod: "All",
  },
};

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

const number = new Intl.NumberFormat("en-US");

const percent = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

function byId(id) {
  return document.getElementById(id);
}

function uniqueOrders(records) {
  return new Set(records.map((record) => record.orderId)).size;
}

function uniqueCustomers(records) {
  return new Set(records.map((record) => record.customerId)).size;
}

function filterRecords(records) {
  return records.filter((record) => {
    if (state.filters.status !== "All" && record.status !== state.filters.status) return false;
    if (state.filters.region !== "All" && record.region !== state.filters.region) return false;
    if (state.filters.category !== "All" && record.category !== state.filters.category) return false;
    if (state.filters.paymentMethod !== "All" && record.paymentMethod !== state.filters.paymentMethod) return false;
    return true;
  });
}

function summarize(records) {
  const revenue = sum(records, "revenue");
  const profit = sum(records, "profit");
  const orders = uniqueOrders(records);
  const customers = uniqueCustomers(records);
  const units = sum(records, "quantity");
  const aov = orders ? revenue / orders : 0;
  const margin = revenue ? (profit / revenue) * 100 : 0;

  const customerOrderMap = new Map();
  const customerRevenueMap = new Map();

  records.forEach((record) => {
    if (!customerOrderMap.has(record.customerId)) customerOrderMap.set(record.customerId, new Set());
    customerOrderMap.get(record.customerId).add(record.orderId);
    customerRevenueMap.set(record.customerId, (customerRevenueMap.get(record.customerId) || 0) + record.revenue);
  });

  let repeatCustomers = 0;
  let repeatRevenue = 0;
  customerOrderMap.forEach((orderSet, customerId) => {
    if (orderSet.size > 1) {
      repeatCustomers += 1;
      repeatRevenue += customerRevenueMap.get(customerId) || 0;
    }
  });

  return {
    revenue,
    profit,
    orders,
    customers,
    units,
    aov,
    margin,
    repeatRate: customers ? (repeatCustomers / customers) * 100 : 0,
    repeatRevenueShare: revenue ? (repeatRevenue / revenue) * 100 : 0,
  };
}

function sum(records, field) {
  return records.reduce((total, record) => total + Number(record[field] || 0), 0);
}

function groupBy(records, key, aggregator) {
  const map = new Map();
  records.forEach((record) => {
    const bucket = record[key];
    if (!map.has(bucket)) map.set(bucket, []);
    map.get(bucket).push(record);
  });
  return Array.from(map.entries()).map(([label, items]) => aggregator(label, items));
}

function topProducts(records) {
  return groupBy(records, "productName", (label, items) => ({
    product: label,
    revenue: sum(items, "revenue"),
    profit: sum(items, "profit"),
    units: sum(items, "quantity"),
    category: items[0]?.category || "",
  }))
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 8);
}

function riskyProducts(records) {
  const products = groupBy(records, "productName", (label, items) => {
    const revenue = sum(items, "revenue");
    const profit = sum(items, "profit");
    return {
      product: label,
      category: items[0]?.category || "",
      revenue,
      margin: revenue ? (profit / revenue) * 100 : 0,
    };
  });
  const avgRevenue = products.reduce((total, item) => total + item.revenue, 0) / (products.length || 1);
  return products
    .filter((item) => item.revenue > avgRevenue && item.margin < 20)
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 8);
}

function monthlyTrend(records) {
  return groupBy(records, "orderMonth", (label, items) => ({
    month: label,
    revenue: sum(items, "revenue"),
    profit: sum(items, "profit"),
  })).sort((a, b) => a.month.localeCompare(b.month));
}

function revenueBy(records, key) {
  return groupBy(records, key, (label, items) => ({
    label,
    revenue: sum(items, "revenue"),
    profit: sum(items, "profit"),
    orders: uniqueOrders(items),
  })).sort((a, b) => b.revenue - a.revenue);
}

function segmentSummary(records) {
  return groupBy(records, "segment", (label, items) => ({
    label,
    revenue: sum(items, "revenue"),
    customers: uniqueCustomers(items),
  })).sort((a, b) => b.revenue - a.revenue);
}

function renderFilters() {
  const config = [
    ["status-filter", "status", state.payload.filters.statuses],
    ["region-filter", "region", state.payload.filters.regions],
    ["category-filter", "category", state.payload.filters.categories],
    ["payment-filter", "paymentMethod", state.payload.filters.paymentMethods],
  ];

  config.forEach(([id, key, values]) => {
    const select = byId(id);
    select.innerHTML = "";
    const allOption = document.createElement("option");
    allOption.value = "All";
    allOption.textContent = "All";
    select.appendChild(allOption);
    values.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
    select.value = state.filters[key];
    select.onchange = (event) => {
      state.filters[key] = event.target.value;
      render();
    };
  });

  byId("reset-filters").onclick = () => {
    state.filters = {
      status: "Completed",
      region: "All",
      category: "All",
      paymentMethod: "All",
    };
    renderFilters();
    render();
  };
}

function renderKpis(summary) {
  const cards = [
    ["Revenue", currency.format(summary.revenue), `${number.format(summary.orders)} orders in view`],
    ["Profit", currency.format(summary.profit), `${percent.format(summary.margin)}% margin`],
    ["Customers", number.format(summary.customers), `${percent.format(summary.repeatRate)}% repeat rate`],
    ["Average Order Value", currency.format(summary.aov), `${number.format(summary.units)} units sold`],
  ];

  byId("kpi-grid").innerHTML = cards
    .map(
      ([label, value, note]) => `
        <article class="kpi-card">
          <div class="kpi-label">${label}</div>
          <div class="kpi-value">${value}</div>
          <div class="kpi-note">${note}</div>
        </article>
      `
    )
    .join("");
}

function lineChart(points) {
  if (!points.length) return emptyState();
  const width = 620;
  const height = 290;
  const padding = 36;
  const maxValue = Math.max(...points.map((point) => Math.max(point.revenue, point.profit)), 1);
  const xStep = points.length > 1 ? (width - padding * 2) / (points.length - 1) : 0;

  const pathFor = (key) =>
    points
      .map((point, index) => {
        const x = padding + index * xStep;
        const y = height - padding - (point[key] / maxValue) * (height - padding * 2);
        return `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`;
      })
      .join(" ");

  const dots = points
    .map((point, index) => {
      const x = padding + index * xStep;
      const y = height - padding - (point.revenue / maxValue) * (height - padding * 2);
      return `<circle cx="${x}" cy="${y}" r="4" fill="#b8501f"></circle>`;
    })
    .join("");

  const labels = points
    .map((point, index) => {
      const x = padding + index * xStep;
      return `<text class="axis-label" x="${x}" y="${height - 10}" text-anchor="middle">${point.month.slice(5)}</text>`;
    })
    .join("");

  return `
    <svg class="chart-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Monthly revenue and profit line chart">
      <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" stroke="rgba(23,33,33,0.18)" />
      <line x1="${padding}" y1="${padding}" x2="${padding}" y2="${height - padding}" stroke="rgba(23,33,33,0.18)" />
      <path d="${pathFor("profit")}" fill="none" stroke="#185f63" stroke-width="3" />
      <path d="${pathFor("revenue")}" fill="none" stroke="#b8501f" stroke-width="4" />
      ${dots}
      ${labels}
      <text class="axis-label" x="${padding}" y="${padding - 12}">Revenue</text>
      <text class="axis-label" x="${padding + 68}" y="${padding - 12}" fill="#185f63">Profit</text>
    </svg>
  `;
}

function barChart(items, color, formatter = currency.format) {
  if (!items.length) return emptyState();
  const width = 620;
  const height = 290;
  const padding = 26;
  const rowHeight = (height - padding * 2) / items.length;
  const maxValue = Math.max(...items.map((item) => item.revenue), 1);

  const bars = items
    .map((item, index) => {
      const y = padding + index * rowHeight;
      const barWidth = (item.revenue / maxValue) * (width - 220);
      return `
        <text class="axis-label" x="0" y="${y + 16}">${item.label}</text>
        <rect x="170" y="${y}" width="${barWidth}" height="${rowHeight - 10}" rx="10" fill="${color}" opacity="${0.9 - index * 0.05}"></rect>
        <text class="axis-label" x="${180 + barWidth}" y="${y + 16}">${formatter(item.revenue)}</text>
      `;
    })
    .join("");

  return `<svg class="chart-svg" viewBox="0 0 ${width} ${height}" role="img">${bars}</svg>`;
}

function tableHtml(headers, rows) {
  if (!rows.length) return emptyState();
  return `
    <table class="table">
      <thead>
        <tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr>
      </thead>
      <tbody>
        ${rows.join("")}
      </tbody>
    </table>
  `;
}

function emptyState() {
  return `<div class="empty-state">No records match the current filter combination.</div>`;
}

function renderInsights(records, summary, regions, categories, segments, trend) {
  const bestMonth = [...trend].sort((a, b) => b.revenue - a.revenue)[0];
  const bestRegion = regions[0];
  const bestCategory = categories[0];
  const bestSegment = segments[0];
  const insights = [
    {
      title: "Retention leverage",
      copy: `${percent.format(summary.repeatRevenueShare)}% of visible revenue comes from repeat customers.`,
    },
    {
      title: "Peak month",
      copy: bestMonth ? `${bestMonth.month} leads with ${currency.format(bestMonth.revenue)} in revenue.` : "No monthly trend available.",
    },
    {
      title: "Top region",
      copy: bestRegion ? `${bestRegion.label} contributes ${currency.format(bestRegion.revenue)}.` : "No regional data available.",
    },
    {
      title: "Best category",
      copy: bestCategory ? `${bestCategory.label} is the largest category in the current view.` : "No category data available.",
    },
    {
      title: "Top segment",
      copy: bestSegment ? `${bestSegment.label} customers generate ${currency.format(bestSegment.revenue)}.` : "No segment data available.",
    },
    {
      title: "Current scope",
      copy: `${number.format(summary.orders)} orders and ${number.format(summary.customers)} customers match these filters.`,
    },
  ];

  byId("insights-grid").innerHTML = insights
    .map(
      (insight) => `
        <article class="insight">
          <strong>${insight.title}</strong>
          <span>${insight.copy}</span>
        </article>
      `
    )
    .join("");
}

function render() {
  const records = filterRecords(state.payload.records);
  const summary = summarize(records);
  const trend = monthlyTrend(records);
  const categories = revenueBy(records, "category").map((item) => ({ ...item, label: item.label }));
  const regions = revenueBy(records, "region").map((item) => ({ ...item, label: item.label }));
  const segments = segmentSummary(records);
  const top = topProducts(records);
  const risky = riskyProducts(records);

  renderKpis(summary);
  byId("trend-chart").innerHTML = lineChart(trend);
  byId("category-chart").innerHTML = barChart(categories.slice(0, 6), "#b8501f");
  byId("region-chart").innerHTML = barChart(regions.slice(0, 6), "#185f63");
  byId("segment-chart").innerHTML = barChart(
    segments.map((segment) => ({ label: segment.label, revenue: segment.revenue })),
    "#c19034"
  );

  byId("products-table").innerHTML = tableHtml(
    ["Product", "Category", "Revenue", "Profit", "Units"],
    top.map(
      (item) => `
        <tr>
          <td>${item.product}</td>
          <td><span class="pill">${item.category}</span></td>
          <td>${currency.format(item.revenue)}</td>
          <td>${currency.format(item.profit)}</td>
          <td>${number.format(item.units)}</td>
        </tr>
      `
    )
  );

  byId("risk-table").innerHTML = tableHtml(
    ["Product", "Category", "Revenue", "Margin"],
    risky.map(
      (item) => `
        <tr>
          <td>${item.product}</td>
          <td><span class="pill">${item.category}</span></td>
          <td>${currency.format(item.revenue)}</td>
          <td>${percent.format(item.margin)}%</td>
        </tr>
      `
    )
  );

  renderInsights(records, summary, regions, categories, segments, trend);
}

async function init() {
  const response = await fetch("./data/dashboard_data.json");
  state.payload = await response.json();

  byId("dataset-name").textContent = state.payload.metadata.dataset;
  byId("date-range").textContent = `${state.payload.metadata.dateStart} to ${state.payload.metadata.dateEnd}`;
  byId("hero-subtitle").textContent = state.payload.metadata.subtitle;

  renderFilters();
  render();
}

init().catch((error) => {
  document.body.innerHTML = `<div class="shell"><div class="card"><h2>Dashboard failed to load</h2><p>${error.message}</p></div></div>`;
});
