# Statistical Analysis

## 1. Objective

The statistical analysis evaluates the relationship between delivery performance and customer satisfaction.

The primary objective is to determine whether review scores differ significantly between on-time and late orders, and whether greater delivery delays are associated with lower customer review scores.

---

## 2. Statistical Approach

Two statistical methods were used:

1. **Mann-Whitney U Test**
2. **Spearman Rank Correlation**

A significance level of:

**α = 0.05**

was used for hypothesis testing.

---

## 3. Why Mann-Whitney U Test?

Customer review scores range from 1 to 5 and are ordinal in nature.

Therefore, a non-parametric test was selected instead of assuming that review scores follow a normal distribution.

The Mann-Whitney U test compares the review-score distributions of:

- On-Time orders
- Late orders

### Hypotheses

**Null Hypothesis (H₀):**

There is no statistically significant difference in review-score distributions between on-time and late orders.

**Alternative Hypothesis (H₁):**

There is a statistically significant difference in review-score distributions between on-time and late orders.

---

## 4. Descriptive Statistics

Overall review statistics:

| Metric | Value |
|---|---:|
| Total Reviews | 99,224 |
| Mean Review Score | 4.09 |
| Standard Deviation | 1.35 |
| Minimum Score | 1 |
| Median Score | 5 |
| Maximum Score | 5 |

---

## 5. Review Score by Delivery Status

| Delivery Status | Reviews | Mean | Median | Std. Dev. |
|---|---:|---:|---:|---:|
| Delivery Date Missing | 2,865 | 1.76 | 1.0 | 1.33 |
| Late | 7,701 | 2.57 | 2.0 | 1.66 |
| On Time | 88,658 | 4.29 | 5.0 | 1.15 |

The descriptive statistics show a substantial difference in customer review scores across delivery-status groups.

On-time orders have a considerably higher average and median review score than late orders.

---

## 6. Mann-Whitney U Test

### Test Results

| Statistic | Result |
|---|---:|
| U Statistic | 530,299,366.50 |
| P-value | < 0.0000000001 |
| Significance Level | 0.05 |

The terminal displayed the p-value as `0.0000000000` due to rounding. This does **not** mean the true p-value is exactly zero.

### Result

The p-value is substantially below the 0.05 significance level.

Therefore:

**Reject the Null Hypothesis (H₀).**

### Interpretation

There is a statistically significant difference between the review-score distributions of on-time and late orders.

The descriptive statistics show that late orders have substantially lower review scores than on-time orders.

---

## 7. Spearman Rank Correlation

The Spearman correlation was used to examine the relationship between:

- Delivery delay in days
- Customer review score

The analysis focuses on orders classified as late.

### Hypotheses

**Null Hypothesis (H₀):**

There is no monotonic relationship between delivery delay and review score.

**Alternative Hypothesis (H₁):**

A monotonic relationship exists between delivery delay and review score.

---

## 8. Spearman Correlation Results

| Metric | Result |
|---|---:|
| Spearman ρ | -0.5204 |
| P-value | < 0.0000000001 |
| Significance Level | 0.05 |

### Interpretation

The Spearman correlation coefficient is:

**ρ = -0.5204**

This indicates a statistically significant **negative association** between delivery delay and customer review score.

In practical terms:

> As delivery delay increases, review scores generally tend to decrease.

The relationship is statistically significant because the p-value is substantially below 0.05.

---

## 9. Statistical Conclusion

Both statistical analyses provide evidence of a strong relationship between delivery performance and customer satisfaction.

### Evidence

- On-time orders have an average review score of **4.29**.
- Late orders have an average review score of **2.57**.
- The Mann-Whitney U test identifies a statistically significant difference between the groups.
- Spearman correlation shows a significant negative association between delivery delay and review score.
- Spearman ρ = **-0.5204**.

### Overall Conclusion

Delivery performance is strongly associated with customer satisfaction in the analyzed dataset.

Orders with late delivery tend to receive substantially lower customer review scores, and larger delivery delays are associated with lower review scores.

---

## 10. Business Implications

The statistical findings suggest that delivery performance should be treated as an important customer-experience metric.

Potential business actions include:

### Improve Delivery Reliability

Monitor late-delivery rates by:

- Month
- Seller
- Customer state
- Logistics route
- Product category

### Investigate High-Delay Orders

Identify operational factors associated with larger delivery delays.

### Monitor Customer Satisfaction

Track review scores alongside delivery KPIs rather than evaluating delivery performance independently.

### Prioritize High-Impact Problems

Focus improvement efforts on areas where:

- Late-delivery rates are high
- Delivery delays are large
- Customer review scores are low

---

## 11. Limitations

The statistical analysis identifies **association**, not causation.

A significant relationship between delivery delay and review score does not prove that delivery delay alone caused lower customer satisfaction.

Other factors may influence review scores, including:

- Product quality
- Seller performance
- Product expectations
- Pricing
- Customer service
- Order issues
- Product category

Therefore, the results should be interpreted as evidence of a strong statistical relationship rather than a causal claim.

---

## 12. Reproducibility

The statistical analysis was performed in Python using:

- `pandas`
- `scipy.stats.mannwhitneyu`
- `scipy.stats.spearmanr`

The analysis script is available in:

`python/06_statistical_analysis.py`

---

## 13. Key Takeaway

> **Delivery performance is strongly associated with customer satisfaction. Late orders receive substantially lower review scores, and increasing delivery delay is associated with decreasing review scores.**

This finding provides a strong basis for further operational and customer-experience analysis in the Power BI phase.