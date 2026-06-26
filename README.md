# MathSoc-Social-Media-Analytics-Report

## Project Initiative

### MathSoc Instagram Event & Content Performance Analytics

This project aims to analyze MathSoc Instagram content performance using post-level lifetime data exported from Meta Business Suite. The main goal is to identify which events, content formats, and campaign types generated the strongest student engagement, reach, shares, and saves, then translate those findings into data-driven recommendations for future MathSoc communication strategy.

Rather than treating this as a daily social media trend analysis, this project focuses on post-level performance. Each row in the dataset represents an Instagram post, and metrics such as reach, views, likes, comments, shares, saves, and follows reflect cumulative performance since publication. This means the analysis is designed to answer questions such as “Which posts performed best?” and “Which event types generated the most engagement?” rather than “How did account traffic change each day?”

The first phase of this project focuses on Winter 2026 as a pilot analysis. Winter 2025 will then be used as a benchmark to compare year-over-year winter term performance. Once the pipeline is finalized, the same framework can be extended to broader comparisons such as 2024 vs. 2025 and Spring 2026 vs. Winter 2026.

## Objectives

The main objectives of this project are to:

* Identify the top-performing MathSoc Instagram posts and events based on reach, views, shares, saves, and engagement rate.
* Compare performance across Instagram formats, including reels, images, and carousels.
* Analyze whether event-related content, recruitment posts, governance announcements, academic/career resources, or community-focused posts generate stronger student response.
* Separate collaborative posts from MathSoc-owned posts to better understand partnership-driven reach.
* Build a repeatable reporting workflow using Python for data cleaning and KPI calculation.
* Create a Power BI dashboard to visualize content performance by term, format, content type, and event.
* Produce an executive-style performance report with key findings and recommendations for future MathSoc Instagram strategy.

## Key Business Questions

This project is guided by the following questions:

1. Which MathSoc Instagram posts generated the highest reach and visibility?
2. Which events received the strongest student response based on shares, saves, and engagement rate?
3. Do reels, images, or carousels perform better for different communication goals?
4. Are collaborative posts associated with stronger reach compared to MathSoc-only posts?
5. Which content types should MathSoc prioritize in future terms to improve engagement and account growth?
6. How did Winter 2026 Instagram performance compare to Winter 2025?

## Data Source

The dataset is collected from Meta Business Suite Instagram exports. The raw data includes post-level lifetime metrics for MathSoc Instagram content, including:

* Publish time
* Post type
* Account username
* Caption/description
* Views
* Reach
* Likes
* Comments
* Shares
* Saves
* Follows

Additional manual tagging is added to support deeper analysis. These tags include:

* Event name
* Content type
* Call-to-action type
* Collaboration status
* Major event indicator

## Methodology

The analysis follows a reporting workflow inspired by quarterly digital marketing performance reporting:

1. Export raw post-level Instagram data from Meta Business Suite.
2. Clean and standardize the raw data using Python.
3. Convert publish times into usable date, month, weekday, and term fields.
4. Calculate key performance indicators, including:

   * Total engagements
   * Engagement rate
   * Share rate
   * Save rate
   * Like rate
   * Follow rate, where available
5. Manually tag each post by event name, content type, and collaboration status.
6. Analyze top-performing posts by reach, shares, saves, and engagement rate.
7. Compare performance across post formats and content categories.
8. Export the cleaned dataset for Power BI visualization.
9. Build an executive-style report summarizing key findings and recommendations.

## Key Metrics

The project focuses on the following metrics:

| Metric          | Purpose                                                              |
| --------------- | -------------------------------------------------------------------- |
| Reach           | Measures how many unique accounts saw the post                       |
| Views           | Measures total visibility or video/reel plays                        |
| Likes           | Captures basic positive engagement                                   |
| Comments        | Captures active audience participation                               |
| Shares          | Indicates relevance and virality among students                      |
| Saves           | Indicates usefulness and future reference value                      |
| Engagement Rate | Measures total engagement relative to reach                          |
| Share Rate      | Measures how shareable a post was relative to reach                  |
| Save Rate       | Measures how useful or reference-worthy a post was relative to reach |

## Analysis Sections

The final analysis is organized into the following sections:

### 1. Overall Performance

This section summarizes total posts, total reach, total views, total engagements, and average engagement rate for the selected term.

### 2. Top Performing Events

This section identifies which events generated the highest reach, shares, saves, and engagement rate. The goal is to understand which MathSoc events created the strongest student response.

### 3. Format Performance

This section compares reels, images, and carousels to understand which formats are most effective for different communication goals. Reels are evaluated mainly for reach and visibility, while carousels are evaluated for saves and information engagement.

### 4. Content Type Performance

This section compares categories such as event promotion, event recap, recruitment, academic/career resources, governance, community/fun content, and advocacy/announcements.

### 5. Collaboration Analysis

This section compares collaborative posts with MathSoc-owned posts to understand whether partnership-driven content contributed to stronger reach or engagement.

### 6. Winter-over-Winter Benchmark

After the Winter 2026 pilot analysis, Winter 2025 data is added as a benchmark to compare posting volume, format mix, reach, engagement, and content performance across winter terms.

## Tools Used

* **Meta Business Suite**: Data collection and Instagram post-level export
* **Python**: Data cleaning, KPI calculation, feature engineering, and analysis
* **Pandas**: Data manipulation and summary tables
* **Power BI**: Dashboard creation and performance visualization
* **Excel**: Optional manual review and content tagging
* **GitHub**: Project documentation and portfolio presentation

## Expected Deliverables

The final project will include:

* Cleaned Instagram performance dataset
* Python notebooks for data cleaning and analysis
* Content tagging dictionary
* Power BI dashboard
* Executive-style PDF report
* README documentation explaining project goals, methodology, findings, and recommendations

## Repository Structure

```text
mathsoc-instagram-content-analytics/
│
├── README.md
│
├── data/
│   ├── raw/
│   │   ├── raw_meta_w25_sample.csv
│   │   └── raw_meta_w26_sample.csv
│   │
│   ├── processed/
│   │   └── cleaned_mathsoc_instagram_w25_w26.csv
│   │
│   └── content_tagging_dictionary.csv
│
├── notebooks/
│   ├── 01_clean_meta_exports.ipynb
│   ├── 02_w26_content_deep_dive.ipynb
│   └── 03_w25_w26_benchmark_analysis.ipynb
│
├── powerbi/
│   └── mathsoc_instagram_dashboard.pbix
│
├── report/
│   └── winter_2025_vs_2026_instagram_report.pdf
│
└── src/
    ├── clean_meta_export.py
    ├── calculate_kpis.py
    └── generate_summary_tables.py
```

## Data Privacy Note

The original dataset was exported from MathSoc’s Meta Business Suite account and contains organization-specific Instagram performance metrics. To protect organizational data privacy, raw exports and actual cleaned datasets are not included in this public repository.

This repository includes anonymized sample data with the same schema used in the analysis. The notebooks demonstrate the data cleaning, KPI calculation, and reporting workflow without exposing internal performance data.

## Project Outcome

The outcome of this project is a repeatable Instagram performance reporting system for MathSoc. The analysis will help identify which content formats, events, and communication styles drive the strongest student response, allowing future communication teams to make more data-informed decisions about Instagram content planning.
