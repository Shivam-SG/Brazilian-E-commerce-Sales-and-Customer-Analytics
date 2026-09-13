# SQL Analysis

## 1. Objective

The SQL phase focuses on analyzing the Brazilian e-commerce dataset using PostgreSQL.

The objective is to validate the dataset, calculate core business KPIs, analyze revenue and customer behavior, evaluate delivery performance, and understand the relationship between delivery performance and customer review scores.

---

## 2. SQL Environment

- Database: PostgreSQL
- Database Name: `olist_ecommerce`
- SQL Client: pgAdmin
- Dataset: Brazilian E-Commerce Public Dataset by Olist

---

## 3. Database Tables

The following core tables were created and analyzed:

| Table | Description |
|---|---|
| `customers` | Customer information and geographic details |
| `orders` | Order-level information and delivery dates |
| `order_items` | Products, sellers, prices and freight for each order |
| `products` | Product attributes and categories |
| `sellers` | Seller information and location |
| `category_translation` | Portuguese-to-English product category mapping |
| `order_reviews` | Customer review scores and comments |

---

## 4. Data Quality Validation

SQL validation checks were performed before analysis.

### Key validation results

| Check | Result |
|---|---:|
| Customers | 99,441 |
| Orders | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |
| Sellers | 3,095 |
| Category Translation Rows | 71 |
| Order Reviews | 99,224 |
| Orders without Customers | 0 |
| Order Items without Orders | 0 |
| Order Items without Products | 0 |
| Order Items without Sellers | 0 |

### Product Category Quality

The products table contains:

- 32,951 total products
- 610 products with missing original category values
- 32,328 product records matched to the translation table
- 13 product records with categories that were not available in the translation table

The two unmatched category values were:

- `portateis_cozinha_e_preparadores_de_alimen...`
- `pc_gamer`

These records are treated as unclassified where an English category mapping is unavailable.

---

## 5. KPI Analysis

Revenue is defined as the sum of product item prices.

Freight value is not included in the project's revenue definition.

### Core KPIs

| KPI | Value |
|---|---:|
| Total Revenue | R$ 13,591,643.70 |
| Total Orders | 99,441 |
| Average Order Value | R$ 136.68 |
| Average Items per Order | 1.13 |
| Average Delivery Time | 12.56 days |

### AOV Definition

The project standardizes Average Order Value as:

`Total Revenue / Total Orders`

This produces an AOV of **R$ 136.68**.

---

## 6. Revenue Analysis

### Monthly Revenue

Monthly revenue was calculated using the order purchase timestamp and the item price.

The SQL analysis identified 24 monthly periods in the dataset.

Some months have very low transaction volume, including:

- September 2016
- December 2016
- September 2018

These periods should be interpreted carefully when evaluating monthly growth or trends because of their low transaction volume.

---

## 7. Top Product Categories

The top 10 product categories generated:

**R$ 8,475,957.56**

This represents:

**62.36% of total revenue.**

### Top 10 Categories

| Rank | Category | Revenue |
|---:|---|---:|
| 1 | health_beauty | R$ 1,258,681.34 |
| 2 | watches_gifts | R$ 1,205,005.68 |
| 3 | bed_bath_table | R$ 1,036,988.68 |
| 4 | sports_leisure | R$ 988,048.97 |
| 5 | computers_accessories | R$ 911,954.32 |
| 6 | furniture_decor | R$ 729,762.49 |
| 7 | cool_stuff | R$ 635,290.85 |
| 8 | housewares | R$ 632,248.66 |
| 9 | auto | R$ 592,720.11 |
| 10 | garden_tools | R$ 485,256.46 |

### Business Insight

Revenue is significantly concentrated among the leading product categories.

The top 10 categories account for **62.36% of total revenue**, indicating that category-level performance is an important driver of overall marketplace revenue.

---

## 8. Seller Analysis

The top 10 sellers generated:

**R$ 1,787,241.74**

This represents:

**13.15% of total revenue.**

### Business Insight

Seller-level revenue is considerably more diversified than category-level revenue.

While the top 10 product categories account for 62.36% of revenue, the top 10 sellers account for only 13.15%.

This suggests that revenue concentration is stronger at the product-category level than at the individual seller level.

---

## 9. Customer Analysis

The dataset contains:

- 99,441 customer records
- 96,096 unique customers
- 93,099 one-time customers
- 2,997 repeat customers

### Repeat Customer Rate

The repeat customer rate is:

**3.12%**

### Business Insight

The marketplace has a very high proportion of one-time customers.

This suggests that customer retention and repeat purchasing could represent an important business opportunity.

Potential areas for further investigation include:

- Customer retention
- Repeat purchase behavior
- Customer lifetime value
- Purchase frequency
- Category-level repeat behavior

---

## 10. Customer Geography

São Paulo (`SP`) has the largest customer base.

### Unique Customers by State

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

São Paulo represents approximately **41.9% of unique customers**.

### Customer Revenue

São Paulo also generated the highest customer-side revenue:

**R$ 5,202,955.05**

This represents approximately **38.28% of total revenue**.

---

## 11. Seller Geography

São Paulo is also the dominant seller state.

### Revenue by Seller State

| State | Revenue |
|---|---:|
| SP | R$ 8,753,396.21 |
| PR | R$ 1,261,887.21 |
| MG | R$ 1,011,564.74 |
| RJ | R$ 843,984.22 |
| SC | R$ 632,427.06 |

São Paulo sellers generated approximately **64.40% of total revenue**.

### Business Insight

There is a strong geographic concentration on the seller side.

São Paulo accounts for approximately 64.4% of seller-side revenue, compared with approximately 38.3% of customer-side revenue.

This difference may be relevant when evaluating marketplace supply concentration and logistics strategy.

---

## 12. Delivery Performance

SQL delivery performance was calculated using the following logic:

- **On Time:** Delivered on or before the estimated delivery date
- **Late:** Delivered after the estimated delivery date
- **Missing Delivery Date:** No customer delivery date available

### SQL Results

| Metric | Result |
|---|---:|
| Total Orders | 99,441 |
| Delivered Orders | 96,476 |
| Missing Delivery Date | 2,965 |
| On-Time Orders | 88,649 |
| Late Orders | 7,827 |
| On-Time Rate | 91.89% |
| Late Rate | 8.11% |
| Average Delivery Time | 12.56 days |

### Highest Meaningful Late-Delivery Months

Only months with at least 1,000 delivered orders were considered to reduce the impact of small samples.

| Month | Late Rate |
|---|---:|
| 2018-03 | 21.36% |
| 2018-02 | 16.00% |
| 2017-11 | 14.31% |
| 2018-08 | 10.39% |
| 2017-12 | 8.38% |

### Business Insight

Delivery performance varies considerably by month.

March 2018 recorded the highest meaningful late-delivery rate at **21.36%**, followed by February 2018 at **16.00%**.

These periods may require further investigation into operational, seasonal, seller, or logistics-related factors.

---

## 13. Delivery Delay

For orders delivered after the estimated delivery date, the average delivery delay was calculated separately.

The metric measures the difference between:

`Actual Delivery Date - Estimated Delivery Date`

Only late orders are included in this calculation.

This provides a more focused measure of the severity of delivery delays.

---

## 14. Customer Review Analysis

The review table contains **99,224 reviews**.

### Review Score Distribution

| Review Score | Reviews | Share |
|---:|---:|---:|
| 1 | 11,424 | 11.51% |
| 2 | 3,151 | 3.18% |
| 3 | 8,179 | 8.24% |
| 4 | 19,142 | 19.29% |
| 5 | 57,328 | 57.78% |

The overall average review score is approximately **4.09**.

---

## 15. Delivery Performance vs Customer Reviews

Review scores were compared across delivery-status groups.

### Results

| Delivery Status | Reviewed Orders | Average Review Score | 5-Star Share |
|---|---:|---:|---:|
| On Time | 88,658 | 4.29 | 62.43% |
| Late | 7,701 | 2.57 | 22.22% |
| Delivery Date Missing | 2,865 | 1.76 | 9.35% |

### Business Insight

There is a strong association between delivery performance and customer review scores.

Orders classified as **On Time** have a substantially higher average review score than **Late** orders.

Late orders also have a much lower 5-star review share.

This indicates that delivery experience is strongly associated with customer satisfaction.

**Important:** This analysis identifies an association, not causation.

---

## 16. Product Category Satisfaction

Product categories were evaluated using a minimum threshold of 100 reviewed orders to reduce the influence of very small samples.

### Lowest-Rated Categories

| Category | Reviewed Orders | Average Review Score | Low Score Share |
|---|---:|---:|---:|
| office_furniture | 1,687 | 3.49 | 26.08% |
| fashion_male_clothing | 131 | 3.64 | 28.24% |
| fixed_telephony | 262 | 3.68 | 25.57% |
| home_comfort | 435 | 3.83 | 20.23% |
| Unclassified | 1,622 | 3.83 | 22.26% |
| audio | 361 | 3.83 | 21.88% |
| construction_tools_safety | 193 | 3.84 | 20.21% |
| bed_bath_table | 11,137 | 3.90 | 18.96% |
| furniture_decor | 8,331 | 3.90 | 19.46% |
| furniture_living_room | 502 | 3.90 | 18.13% |

### Business Insight

`office_furniture` stands out as an important category for further investigation because it combines substantial review volume with a relatively low average review score.

Potential areas for investigation include:

- Product quality
- Seller performance
- Delivery performance
- Product descriptions
- Customer expectations

---

## 17. Key SQL Findings

### Revenue

- Total revenue: **R$ 13.59M**
- Top 10 categories contribute **62.36%** of revenue.
- Top 10 sellers contribute **13.15%** of revenue.

### Customers

- **96,096 unique customers**
- **3.12% repeat customer rate**
- São Paulo has the largest customer base.

### Geography

- São Paulo represents approximately **38.28% of customer-side revenue**.
- São Paulo sellers represent approximately **64.40% of seller-side revenue**.

### Delivery

- SQL on-time delivery rate: **91.89%**
- SQL late delivery rate: **8.11%**
- Average delivery time: **12.56 days**
- March 2018 had the highest meaningful late-delivery rate at **21.36%**.

### Customer Satisfaction

- Overall average review score: approximately **4.09**
- On-time orders: **4.29 average review score**
- Late orders: **2.57 average review score**
- Late orders have a substantially lower 5-star review share.

---

## 18. Business Recommendations

### 1. Improve Customer Retention

The repeat customer rate is only **3.12%**.

Potential actions:

- Personalized offers
- Post-purchase engagement
- Repeat-purchase campaigns
- Category-based recommendations
- Customer segmentation

### 2. Investigate Delivery Bottlenecks

The SQL analysis identifies meaningful periods with elevated late-delivery rates.

Operational analysis should focus on:

- Seller performance
- Logistics partners
- Geographic routes
- Seasonal demand
- Order processing time

### 3. Investigate Low-Satisfaction Categories

Categories such as `office_furniture` show relatively low customer satisfaction.

These categories should be investigated at the:

- Seller level
- Product level
- Delivery level
- Review/comment level

### 4. Monitor Category Concentration

The top 10 categories contribute 62.36% of revenue.

The business should continue monitoring category concentration while evaluating opportunities to grow underrepresented categories.

### 5. Evaluate Geographic Concentration

São Paulo dominates seller-side revenue.

This concentration may create both operational advantages and geographic dependency, making geographic diversification worth evaluating.

---

## 19. SQL Files

The SQL analysis is organized into separate files:

| File | Purpose |
|---|---|
| `01_data_quality.sql` | Data quality and relationship validation |
| `02_kpi_analysis.sql` | Core business KPIs |
| `03_revenue_analysis.sql` | Revenue, categories and sellers |
| `04_customer_analysis.sql` | Customer behavior and geography |
| `05_delivery_analysis.sql` | Delivery performance |
| `06_review_analysis.sql` | Reviews and customer satisfaction |

---

## 20. Methodology Note

SQL results are based on the raw PostgreSQL tables created from the Olist dataset.

Revenue is defined as the sum of `order_items.price` and does not include freight value.

Delivery performance uses the actual customer delivery date compared with the estimated delivery date.

For delivery analysis, orders without a customer delivery date are excluded from on-time/late rate denominators.

Small-volume months are treated cautiously when identifying delivery-performance trends.

The SQL delivery results currently differ from the earlier Excel delivery classification. This difference has been retained rather than silently reconciled and will be investigated separately as part of the project's methodology and data-validation work.