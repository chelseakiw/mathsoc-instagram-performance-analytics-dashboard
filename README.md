# MathSoc Instagram Performance Analytics Dashboard

## Project Overview

This project analyzes MathSoc Instagram content performance using post-level lifetime data exported from Meta Business Suite. The goal is to build a repeatable reporting workflow that helps evaluate which Instagram posts, content formats, event campaigns, and communication strategies generate the strongest student response.

This project was created as part of my role as Vice President, Communication for MathSoc. In this role, I help manage MathSoc’s digital communication channels, including Instagram and Discord, and support promotion for student events, recruitment, governance updates, academic resources, and community initiatives. The purpose of this project is not only to create a portfolio dashboard, but also to develop a practical reporting system that can help future MathSoc communication teams make more data-informed decisions.

Rather than treating this as a daily social media trend analysis, this project focuses on post-level performance. Each row in the dataset represents one Instagram post, with lifetime metrics such as views, reach, likes, comments, shares, saves, and follows. This means the analysis is designed to answer questions such as:

* Which posts performed best?
* Which content formats generated the strongest reach or engagement?
* Which event categories received the strongest student response?
* How did Winter 2026 Instagram performance compare to Winter 2025?

The main comparison in this project focuses on Winter 2025 and Winter 2026 Instagram performance.

---

## Project Goals

The main goals of this project are to:

* Clean and standardize raw Instagram export data from Meta Business Suite.
* Combine Winter 2025 and Winter 2026 post-level datasets into one analysis-ready dataset.
* Calculate post-level KPIs such as total engagements, engagement rate, share rate, save rate, and follow rate.
* Compare performance by academic term, post format, account group, and content category.
* Build a Power BI dashboard to visualize W25 vs W26 Instagram performance.
* Create a privacy-safe public version of the project using anonymized sample data.
* Use the analysis to support future MathSoc communication planning as VP Communication.

---

## Business Questions

This project is guided by the following questions:

1. Which MathSoc Instagram posts generated the highest reach, views, and engagement?
2. How did Winter 2026 performance compare to Winter 2025?
3. Which post formats performed best across images, reels, and carousels?
4. Did collaborative or partner posts perform differently from MathSoc-owned posts?
5. Which content categories generated the strongest student response?
6. What content formats or communication strategies should MathSoc prioritize in future terms?

---

## Data Source

The original dataset was exported from MathSoc’s Meta Business Suite account. The raw files contain post-level lifetime Instagram performance data for Winter 2025 and Winter 2026.

The original raw export includes fields such as:

* Post ID
* Account ID
* Account username
* Account name
* Caption / description
* Publish time
* Permalink
* Post type
* Views
* Reach
* Likes
* Comments
* Shares
* Saves
* Follows

Because the original data contains organization-specific Instagram performance metrics, actual raw exports and actual processed datasets are not included in this public repository.

---

## Data Privacy and Public Sample Data

The public version of this repository uses anonymized sample data instead of actual MathSoc Instagram performance data.

The original dataset was used privately to build the analysis workflow and Power BI dashboard. For the public GitHub version, a sample dataset was generated to preserve the same structure while protecting internal performance data.

The sample generation process replaces or removes sensitive fields as follows:

| Original Field                                        | Public Sample Treatment                                                            |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Post ID                                               | Replaced with synthetic IDs such as `sample_w25_post_001`                          |
| Account ID                                            | Replaced with synthetic account IDs                                                |
| Account username                                      | Replaced with sample labels such as `uwmathsoc_sample` or `partner_account_sample` |
| Account name                                          | Replaced with generic sample account names                                         |
| Caption / description                                 | Replaced with anonymized placeholder captions                                      |
| Permalink                                             | Replaced with non-functional sample Instagram links                                |
| Views, reach, likes, comments, shares, saves, follows | Replaced with synthetic metric values                                              |
| Post type and publish date structure                  | Preserved for realistic dashboard testing                                          |
| Term labels                                           | Preserved as W25 and W26                                                           |

The sample data is not intended to represent actual MathSoc performance. It is included only to demonstrate the data cleaning, KPI calculation, and Power BI reporting workflow in a privacy-safe way.

---

## Methodology

The analysis follows a reporting workflow inspired by digital marketing performance reporting.

### 1. Raw Data Organization

The Winter 2025 and Winter 2026 Meta Business Suite exports were stored as raw CSV files. These files were kept unchanged so that the original export structure remained intact.

```text
data/raw/raw_meta_w25.csv
data/raw/raw_meta_w26.csv
```

The raw files were not edited manually. All cleaning and transformations were handled in Python.

### 2. Python Data Cleaning

A Python script was used to clean and standardize the raw exports.

The cleaning process included:

* Reading the W25 and W26 raw CSV files.
* Adding a `term` column to distinguish W25 and W26.
* Standardizing column names into Python-friendly snake case.
* Converting publish times into usable date fields.
* Creating date features such as year, month, weekday, and publish hour.
* Standardizing post format values such as image, reel, and carousel.
* Separating MathSoc-owned posts from partner or collaborative posts.
* Handling missing reach values without incorrectly replacing them with zero.
* Adding empty manual tagging columns for future content classification.

### 3. KPI Calculation

The script calculated post-level KPIs, including:

| KPI                         | Formula                           |
| --------------------------- | --------------------------------- |
| Total engagements           | likes + comments + shares + saves |
| Engagement rate             | total engagements / reach         |
| Share rate                  | shares / reach                    |
| Save rate                   | saves / reach                     |
| Like rate                   | likes / reach                     |
| Follow rate                 | follows / reach                   |
| Views-based engagement rate | total engagements / views         |

Reach-based rates were only calculated when reach data was available. Some collaborative or partner posts did not include reach values in the export, so those rows were handled carefully rather than being treated as zero-reach posts.

### 4. Content Classification

The project includes both automated and manual tagging fields.

The current workflow includes an initial `auto_content_hint` field generated from caption-based keyword logic. This provides a first-pass content category such as:

* community_event
* academic_career
* academic_support
* governance
* recruitment
* other

Additional manual tagging columns were also created for future refinement:

* `event_name_manual`
* `content_type_manual`
* `cta_type_manual`
* `major_event_manual`

These fields are designed to support more detailed analysis of event performance, campaign type, and call-to-action strategy in future iterations.

### 5. Processed Dataset Export

After cleaning and KPI calculation, the script exports a processed dataset for private analysis and Power BI visualization.

A separate anonymized sample dataset is also generated for the public repository.

### 6. Power BI Dashboard Development

The cleaned dataset was imported into Power BI to build a multi-page dashboard.

The dashboard currently includes the following pages:

1. Executive Overview
2. Format Analysis
3. Collaboration & Content Category Analysis
4. Top Performing Posts

The dashboard is used to compare W25 and W26 performance across total reach, total views, total engagements, average post performance, post format, account group, and content category.

---

## Key Metrics

| Metric            | Purpose                                                              |
| ----------------- | -------------------------------------------------------------------- |
| Views             | Measures total visibility or video/reel plays                        |
| Reach             | Measures how many unique accounts saw the post                       |
| Likes             | Captures basic positive engagement                                   |
| Comments          | Captures active audience participation                               |
| Shares            | Indicates relevance and student-to-student distribution              |
| Saves             | Indicates usefulness or future reference value                       |
| Follows           | Measures follower conversion from a post, where available            |
| Total engagements | Combines likes, comments, shares, and saves                          |
| Engagement rate   | Measures total engagement relative to reach                          |
| Share rate        | Measures how shareable a post was relative to reach                  |
| Save rate         | Measures how useful or reference-worthy a post was relative to reach |

---

## Power BI Dashboard Sections

### 1. Executive Overview

This page summarizes overall Instagram performance across Winter 2025 and Winter 2026.

It includes:

* Total posts
* Total views
* Total reach
* Total engagements
* Average views per post
* Average reach per post
* Average engagements per post
* Engagements by post format

This page helps separate total performance from average post-level performance, since posting volume differs across terms.

### 2. Format Analysis

This page compares performance across Instagram formats:

* Images
* Reels
* Carousels

The analysis compares total views, total reach, average engagement rate, and saves by post format. This helps identify whether certain formats are better suited for visibility, engagement, or informational content.

### 3. Collaboration & Content Category Analysis

This page compares:

* MathSoc-owned posts
* Partner or collaborative posts
* Auto-tagged content categories

This section helps evaluate whether partnership-driven content contributed additional visibility or engagement and which broad content categories generated stronger student response.

### 4. Top Performing Posts

This page lists top-performing posts based on metrics such as total engagements, views, reach, shares, saves, and engagement rate.

This section is intended to help identify specific examples of high-performing content and support future content planning decisions.

---

## Current Progress

The following project components have been completed:

* Organized raw Meta Business Suite exports for W25 and W26.
* Built a Python cleaning script for combining and standardizing both terms.
* Created calculated KPI fields for post-level analysis.
* Generated a private cleaned dataset for internal analysis.
* Generated anonymized sample datasets for the public GitHub repository.
* Built a Power BI dashboard with four analysis pages.
* Created a repeatable workflow that can be reused for future MathSoc communication reporting.

---

## Tools Used

* **Meta Business Suite**: Source of Instagram post-level export data
* **Python**: Data cleaning, feature engineering, KPI calculation, and sample generation
* **Pandas**: Data manipulation and summary table creation
* **Power BI**: Dashboard creation and performance visualization
* **Excel / CSV review**: Manual inspection and optional tagging support
* **GitHub**: Project documentation and portfolio presentation

---

## Repository Structure

```
MathSoc-Social-Media-Analytics-Report/
│
├── README.md
├── clean_meta_exports.py
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   │
│   ├── processed/
│   │   └── .gitkeep
│   │
│   └── sample/
│       ├── raw_meta_w25_sample.csv
│       ├── raw_meta_w26_sample.csv
│       └── cleaned_instagram_w25_w26_sample.csv
│
├── powerbi/
│   ├── sample_dashboard_overview.png
│   ├── sample_dashboard_format_analysis.png
│   └── sample_dashboard_content_analysis.png
│
├── report/
│   └── instagram_performance_summary_sample.pdf
│
└── outputs/
    └── .gitkeep
```

Private files such as actual raw exports, actual processed datasets, and internal summary outputs are intentionally excluded from the public repository.

---

## Public Repository Files

The public repository includes:

* Python cleaning script
* Anonymized sample raw data
* Anonymized cleaned sample data
* Sample Power BI dashboard screenshots
* Project documentation
* Privacy-safe report summary

The public repository does not include:

* Actual MathSoc Meta Business Suite exports
* Actual cleaned performance dataset
* Actual post-level performance metrics
* Actual captions or post links
* Internal Power BI dashboard based on real data

---

## Project Outcome

The outcome of this project is a repeatable Instagram performance reporting workflow for MathSoc.

From a communication strategy perspective, this project helps MathSoc better understand which content formats, event types, and posting strategies generate stronger student response. As VP Communication, this analysis supports more intentional planning for future event promotion, recruitment campaigns, academic resources, governance announcements, and community engagement.

From a data analytics perspective, this project demonstrates a complete workflow from raw data cleaning to KPI calculation and dashboard reporting. It shows practical experience using Python, pandas, Power BI, and data storytelling to transform social media export data into actionable communication insights.

---

## Future Improvements

Future improvements may include:

* Completing manual tagging for all posts by event name and content type.
* Adding Spring 2026 data for term-over-term comparison.
* Comparing broader year-over-year performance across 2024 and 2025.
* Creating a standardized monthly or termly reporting template for future MathSoc communication teams.
* Expanding the dashboard to include Instagram Stories or Discord engagement data if reliable exports are available.
* Building a final executive-style PDF report with privacy-safe visuals and recommendations.
