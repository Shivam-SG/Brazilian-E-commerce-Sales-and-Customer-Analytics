# Excel Analysis

## 1. Objective

The objective of this analysis is to evaluate the performance of a Brazilian e-commerce marketplace using Microsoft Excel.

The analysis focuses on:

- Overall sales and revenue performance
- Monthly revenue trends and growth
- Average Order Value (AOV)
- Product and product-category performance
- Customer and seller geographic performance
- Order delivery performance
- Late delivery trends
- Data quality and consistency

The final output is an interactive Excel dashboard containing key performance indicators (KPIs), PivotTable analyses, charts, and slicers to support business decision-making.

## 2. Dataset Overview

The analysis is based on the Brazilian E-Commerce Public Dataset, which contains transactional, customer, seller, product, order, and category information.

The main datasets used in the Excel analysis are:

| Dataset | Purpose |
|---|---|
| Orders | Order dates, delivery dates, and order status |
| Order Items | Product-level sales, price, freight, and seller information |
| Products | Product categories and product attributes |
| Customers | Customer location and customer identifiers |
| Sellers | Seller location and seller identifiers |
| Product Category Translation | Portuguese-to-English product category mapping |

### Key Data Volumes

| Dataset | Records |
|---|---:|
| Customers | 99,441 |
| Products | 32,951 |
| Sellers | 3,095 |
| Product Category Translation | 71 |
| Orders | 99,441* |

> *Order-level counts are based on the dataset used in the analysis.

The datasets were combined and transformed to create a consolidated analysis table containing order, product, customer, seller, revenue, delivery, and geographic information.

## 3. Data Quality Checks

Before performing the analysis, data quality checks were carried out in Excel to identify missing values, duplicate identifiers, and inconsistent category information.

### Product Data Quality

| Check | Result |
|---|---:|
| Number of Products | 32,951 |
| Number of Columns | 9 |
| Missing Product IDs | 0 |
| Duplicate Product IDs | 0 |
| Missing Product Categories | 610 |
| Number of Product Categories | 74 |
| Unclassified Product Records after translation | 623 |

### Product Category Translation Quality

| Check | Result |
|---|---:|
| Number of Rows | 71 |
| Number of Columns | 2 |
| Missing Portuguese Categories | 0 |
| Missing English Categories | 0 |
| Duplicate Portuguese Categories | 0 |

### Seller Data Quality

| Check | Result |
|---|---:|
| Number of Sellers | 3,095 |
| Number of Columns | 4 |
| Missing Seller IDs | 0 |
| Duplicate Seller IDs | 0 |
| Missing Seller City | 0 |
| Missing Seller State | 0 |

### Customer Data Quality

| Check | Result |
|---|---:|
| Number of Customers | 99,441 |
| Number of Columns | 5 |
| Missing Customer IDs | 0 |
| Duplicate Customer IDs | 0 |
| Duplicate Customer Unique IDs | 3,345 |
| Missing Customer City | 0 |
| Missing Customer State | 0 |

### Order Item Data Quality

| Check | Result |
|---|---:|
| Missing Seller State | 0 |
| Unknown Seller State | 0 |
| Unknown Customer State | 0 |
| Missing Customer State | 0 |

### Data Quality Summary

The majority of key identifiers and geographic fields were complete and consistent.

The main data quality issues identified were missing product categories and duplicate customer unique identifiers. Missing product categories were handled through category translation and an `Unclassified` category where an English category could not be mapped.

Duplicate `customer_unique_id` values were retained because the same customer can place multiple orders. Therefore, `customer_unique_id` should be treated as a customer-level identifier rather than an order-level unique key.

## 4. Data Cleaning & Transformation

The raw datasets were reviewed and transformed in Microsoft Excel before performing the analysis.

### 4.1 Product Category Translation

The product category translation dataset was used to convert Portuguese product category names into English.

An `XLOOKUP` formula was used to map the Portuguese category to its corresponding English category.

Example:

```excel
=XLOOKUP(B2,Product_table[product_category_name],Product_table[product_category_name_english],"Unclassified")

If a category could not be matched, it was assigned the value Unclassified.

### 4.2 Handling Missing Product Categories

The product dataset contained 610 missing product category values.

After applying the category mapping logic, unmatched category values were represented as Unclassified rather than being left blank. This ensured that records were retained during revenue analysis.

### 4.3 Order Month

A monthly period field, order_month, was created from the order purchase timestamp.

The field was used to analyze:

Monthly revenue
Month-over-month (MoM) revenue growth
Monthly order volume
Monthly delivery performance

The month format used was:

YYYY-MM

Example:

2017-01, 2017-02, 2017-03

### 4.4 Delivery Performance Classification

Order delivery performance was classified using the estimated delivery date and actual delivery date.

Orders were categorized into:

On Time — delivered on or before the estimated delivery date
Late — delivered after the estimated delivery date
Delivery Date Missing — actual delivery date was unavailable

This classification was used to calculate monthly delivery performance and late delivery rates.

### 4.5 Revenue Calculation

Item-level revenue was analyzed using the item_revenue field from the order items data.

Revenue was aggregated using Excel PivotTables to calculate:

Total revenue
Monthly revenue
Revenue by product category
Revenue by product
Revenue by customer state
Revenue by seller state

### 4.6 Data Validation

After cleaning and transformation, the resulting data was checked again using Excel functions such as:

COUNTBLANK
COUNTIF
XLOOKUP

These checks helped confirm that important fields did not contain unexpected blank or Unknown values.

## 5. KPI Analysis

The Excel dashboard was built around key business performance indicators (KPIs) to provide a high-level view of marketplace performance.

### 5.1 Total Revenue

**Total Revenue:** R$13,591,643.70

Total revenue represents the aggregated `item_revenue` across the order items dataset.

This KPI provides the overall revenue generated during the analysis period.

### 5.2 Total Orders

**Total Orders:** 99,441

Total orders represents the number of unique orders in the dataset.

This metric was used as the primary measure of transaction volume.

### 5.3 Average Order Value (AOV)

**AOV:** R$136.68

Average Order Value measures the average revenue generated per order.

Formula:

```text
AOV = Total Revenue / Total Orders

Using the calculated values:

AOV = R$13,591,643.70 / 99,441
    ≈ R$136.68

A higher AOV indicates that customers are generating more revenue per transaction.

5.4 On-Time Delivery Rate

On-Time Delivery Rate: 93.23%

The on-time delivery rate represents the proportion of orders delivered on or before the estimated delivery date.

Formula:

On-Time Delivery Rate =
On-Time Orders / (On-Time Orders + Late Orders)

The dashboard shows that the majority of delivered orders were completed on time.

5.5 Late Delivery Rate

Late Delivery Rate: 6.77%

The late delivery rate represents the proportion of delivered orders that arrived after the estimated delivery date.

Formula:

Late Delivery Rate =
Late Orders / (On-Time Orders + Late Orders)

A lower late delivery rate indicates better delivery performance.

5.6 Average Items per Order

Average Items per Order: 1.13

This metric measures the average number of items purchased per order.

Formula:

Average Items per Order =
Total Order Items / Total Orders

The result indicates that customers purchased slightly more than one item per order on average.

KPI Summary
KPI	Value
Total Revenue	R$13,591,643.70
Total Orders	99,441
Average Order Value	R$136.68
On-Time Delivery Rate	93.23%
Late Delivery Rate	6.77%
Average Items per Order	1.13


## 6. Revenue Analysis

Revenue performance was analyzed across time, product categories, individual products, and customer locations using Excel PivotTables and PivotCharts.

### 6.1 Monthly Revenue Trend

A monthly revenue analysis was created using the `order_month` field.

The analysis shows that monthly revenue generally increased over the observed period, with noticeable fluctuations between individual months.

Revenue reached its stronger levels during 2018, indicating an overall expansion in sales activity compared with the earlier period.

The monthly trend was visualized using a line chart in the Excel dashboard.

### 6.2 Top 10 Product Categories by Revenue

A PivotTable was created by grouping `product_category_name_english` and aggregating `item_revenue`.

The top revenue-generating product categories were:

1. `health_beauty`
2. `watches_gifts`
3. `bed_bath_table`
4. `sports_leisure`
5. `computers_accessories`
6. `furniture_decor`
7. `cool_stuff`
8. `housewares`
9. `auto`
10. `garden_tools`

These categories represent the strongest contributors to marketplace revenue.

### 6.3 Top 10 Products by Revenue

Product-level revenue was analyzed by grouping `product_id` and summing `item_revenue`.

A Top 10 filter was applied to identify the individual products generating the highest revenue.

This analysis helps identify high-value products that may require additional inventory, marketing, or pricing analysis.

### 6.4 Revenue by Customer State

Customer geographic performance was analyzed by grouping `customer_state` and aggregating revenue.

The highest-revenue customer states were:

1. `SP`
2. `RJ`
3. `MG`
4. `RS`
5. `PR`
6. `SC`
7. `BA`
8. `DF`
9. `GO`
10. `ES`

São Paulo (`SP`) was the largest contributor by a significant margin.

This indicates a strong geographic concentration of revenue in Brazil's major commercial markets.

### 6.5 Revenue by Seller State

Seller performance was also analyzed by grouping sellers according to `seller_state`.

The analysis showed that São Paulo (`SP`) generated the highest seller-side revenue, followed by other major states.

This geographic concentration can help management evaluate seller acquisition opportunities, regional operations, and marketplace coverage.

### Revenue Analysis Summary

The revenue analysis indicates that:

- Revenue increased substantially over the analysis period.
- A relatively small group of product categories contributes a large share of revenue.
- Revenue is geographically concentrated, particularly in São Paulo.
- Top-performing individual products can be identified for further commercial analysis.
- Product and geographic performance can be monitored through the interactive Excel dashboard.


## 7. Delivery Performance Analysis

Delivery performance was analyzed to evaluate the marketplace's ability to fulfill orders within the estimated delivery timeframe.

### 7.1 Overall Delivery Performance

The dashboard shows:

| Delivery KPI | Value |
|---|---:|
| On-Time Delivery Rate | 93.23% |
| Late Delivery Rate | 6.77% |

The results indicate that the majority of delivered orders were completed on time.

### 7.2 Delivery Status Classification

Orders were classified into three groups:

- **On Time** — delivered on or before the estimated delivery date.
- **Late** — delivered after the estimated delivery date.
- **Delivery Date Missing** — an actual delivery date was not available.

The analysis identified:

| Delivery Status | Orders |
|---|---:|
| Delivery Date Missing | 2,965 |
| Late | 6,535 |
| On Time | 89,941 |
| Total Orders | 99,441 |

### 7.3 Monthly Late Delivery Rate

Monthly late delivery rates were calculated to identify periods with delivery-performance issues.

The monthly analysis showed noticeable variation in late delivery rates.

The highest observed late delivery rate among the analyzed months was:

**2018-03 — 18.96%**

Other months with relatively high late delivery rates included:

- 2018-02 — 14.14%
- 2017-11 — 12.40%
- 2017-12 — 7.46%

These periods may require additional investigation into logistics capacity, shipping delays, seller performance, and seasonal demand.

### 7.4 Delivery Date Missing

A total of **2,965 orders** did not have an actual delivery date available.

These records were kept separately rather than being classified as either late or on-time.

This prevents missing delivery information from incorrectly affecting delivery-performance calculations.

### Delivery Performance Summary

The overall delivery performance is strong, with more than 93% of classified deliveries being completed on time.

However, the monthly analysis reveals specific periods where late delivery rates increased substantially. These periods should be investigated further to identify operational or seasonal causes.

## 8. Customer & Seller Analysis

Customer and seller data was analyzed to understand geographic distribution, customer concentration, and seller revenue contribution.

### 8.1 Customer Distribution by State

Customer records were grouped by `customer_state` and counted using the distinct `customer_unique_id` field.

The analysis identified the following states as the largest customer markets:

| State | Unique Customers |
|---|---:|
| SP | 40,302 |
| RJ | 12,384 |
| MG | 11,259 |
| RS | 5,277 |
| PR | 4,882 |
| SC | 3,534 |
| BA | 3,277 |
| DF | 2,075 |
| ES | 1,964 |
| GO | 1,952 |

São Paulo (`SP`) has the largest customer base by a significant margin.

### 8.2 Customer Unique ID Analysis

The customer dataset contains **99,441 customer records**.

The analysis identified **3,345 duplicate `customer_unique_id` values**.

These duplicates were not treated as data errors because a single customer can place multiple orders.

Therefore:

- `customer_id` identifies a customer record associated with an order.
- `customer_unique_id` identifies the underlying customer across multiple orders.

For customer-level analysis, `customer_unique_id` should therefore be used for distinct customer counts.

### 8.3 Seller Distribution

The seller dataset contains **3,095 sellers**.

Data quality checks showed:

- Missing Seller IDs: 0
- Duplicate Seller IDs: 0
- Missing Seller City: 0
- Missing Seller State: 0

This indicates that the core seller identification and geographic fields are complete.

### 8.4 Seller Revenue Analysis

Seller performance was analyzed by grouping `seller_id` and aggregating `item_revenue`.

A Top 10 Seller analysis was created using an Excel PivotTable.

The analysis helps identify sellers contributing the highest revenue to the marketplace.

These sellers may be candidates for:

- Key-account management
- Seller retention programs
- Increased promotional support
- Inventory and fulfillment monitoring

### 8.5 Geographic Revenue Concentration

Customer-state revenue analysis showed a strong concentration of revenue in São Paulo (`SP`), followed by Rio de Janeiro (`RJ`) and Minas Gerais (`MG`).

This suggests that Brazil's major population and commercial centers are important revenue markets for the marketplace.

### Customer & Seller Analysis Summary

The analysis shows that:

- São Paulo is the largest customer market.
- Customer activity is concentrated in a relatively small number of states.
- Duplicate `customer_unique_id` values represent repeat purchasing behavior rather than duplicate customer records.
- The seller dataset has complete core identification and location information.
- A small group of high-performing sellers contributes significantly to marketplace revenue.


## 9. Business Insights & Recommendations

The analysis was used to identify key business patterns and translate them into actionable recommendations.

### 9.1 Revenue Concentration by Product Category

The Top 10 product categories generated approximately **62.36% of total revenue**.

This indicates that a relatively small number of product categories are responsible for a large proportion of marketplace revenue.

**Recommendation:**

The business should prioritize inventory availability, promotions, and marketing efforts for high-performing categories while continuing to evaluate opportunities in lower-performing categories.

### 9.2 Seller Revenue Concentration

The Top 10 sellers contributed approximately **13.15% of total revenue**.

Compared with the concentration of revenue across product categories, seller-level revenue is relatively diversified.

**Recommendation:**

The marketplace should continue expanding and retaining its broad seller network rather than becoming overly dependent on a small number of sellers.

### 9.3 Geographic Concentration

São Paulo (`SP`) is the dominant market on both the customer and seller sides.

SP accounted for approximately **41.9% of unique customers**, while seller-side revenue from SP represented approximately **64.4% of total revenue**.

**Recommendation:**

The company should maintain strong operational and logistics capabilities in São Paulo while exploring growth opportunities in other states to reduce geographic concentration risk.

### 9.4 Delivery Performance

The overall on-time delivery rate was **93.23%**, while the late delivery rate was **6.77%**.

However, monthly analysis identified periods with significantly higher late delivery rates. The highest meaningful monthly late delivery rate was **18.96% in March 2018**.

**Recommendation:**

Management should investigate high-delay periods by examining seller performance, shipping capacity, logistics partners, and seasonal demand patterns.

### 9.5 Customer Base

The dataset contains **96,096 unique customers** after accounting for repeated `customer_unique_id` values.

The presence of repeat customer records indicates that some customers placed multiple orders during the analysis period.

**Recommendation:**

The business can develop customer retention and repeat-purchase strategies such as personalized promotions, category-based recommendations, and loyalty programs.

### 9.6 Average Order Value

The Average Order Value (AOV) was **R$136.68**.

**Recommendation:**

The marketplace could attempt to increase AOV through cross-selling, product bundles, minimum-order promotions, and recommendations for complementary products.

### 9.7 Overall Business Takeaway

The analysis suggests that the marketplace has a broad seller base and strong revenue concentration across specific product categories and geographic markets.

The strongest opportunities are:

- Protecting high-performing product categories
- Improving delivery performance during high-delay periods
- Expanding customer demand outside the dominant states
- Increasing repeat purchases
- Improving AOV through cross-selling and bundling
- Maintaining a diversified seller ecosystem

## 10. Excel Dashboard

An interactive Excel dashboard was created to provide a consolidated view of the Brazilian e-commerce marketplace performance.

### Dashboard KPIs

The dashboard includes the following key performance indicators:

| KPI | Value |
|---|---:|
| Total Revenue | R$ 13,591,643.70 |
| Total Orders | 99,441 |
| Average Order Value | R$ 136.68 |
| On-Time Delivery | 93.23% |
| Late Delivery | 6.77% |
| Average Items per Order | 1.13 |

### Dashboard Visualizations

The dashboard contains the following visualizations:

- Monthly Revenue Trend
- Monthly Late Delivery Rate
- Top 10 Product Categories by Revenue
- Top 10 Customer States by Revenue
- Top 10 Products by Revenue

### Interactive Filters

Two slicers were added to make the dashboard interactive:

- Order Month
- Customer State

These filters allow users to explore sales performance across different time periods and customer locations.

### Dashboard Design

The dashboard was designed to provide a simple business-oriented view of the dataset rather than displaying raw tables.

The layout combines:

- KPI cards for high-level performance
- Charts for trend analysis
- Ranking charts for product and category performance
- Geographic analysis using customer and seller state information
- Slicers for interactive exploration

### Dashboard Purpose

The dashboard can be used by business stakeholders to quickly identify:

- Revenue trends
- High-performing product categories
- Important customer markets
- Top-performing products
- Delivery performance issues
- Areas requiring further investigation

The Excel dashboard serves as the first business intelligence layer of the project. The same business questions will later be explored using SQL, Python, statistical analysis, and Power BI.