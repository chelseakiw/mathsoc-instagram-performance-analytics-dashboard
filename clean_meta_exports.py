from pathlib import Path
import numpy as np
import pandas as pd

# =========================================================
# Raw Data Cleaning (W25/W26)
# Expected raw files:
#   data/raw/raw_meta_w25.csv
#   data/raw/raw_meta_w26.csv
# Outputs:
#   data/processed/cleaned_instagram_w25_w26_private.csv
#   data/sample/raw_meta_w25_sample.csv
#   data/sample/raw_meta_w26_sample.csv
#   data/sample/cleaned_instagram_w25_w26_sample.csv
#   outputs/*.csv summary tables
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

W25_RAW = RAW_DIR / "raw_meta_w25.csv"
W26_RAW = RAW_DIR / "raw_meta_w26.csv"


def clean_column_name(col: str) -> str:
    #Convert column names like 'Publish time' into 'publish_time'
    return (
        col.strip()
        .lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .replace("-", "_")
    )


def read_raw_file(path: Path, term: str) -> pd.DataFrame:
    #Read one Meta export and add a term label
    if not path.exist():
        raise FileNotFoundError(f"Cannot find {path}. Check your file name and folder location.")
    
    df = pd.read_csv(path)
    df["term"] = term
    return df


def clean_meta_export(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw Meta export and calculate KPIs."""
    df = df.copy()

    # 1. Clean column names
    df.columns = [clean_column_name(c) for c in df.columns]

    # 2. Convert numeric columns
    numeric_cols = [
        "duration_sec", "views", "likes", "shares", "comments", "saves", "reach", "follows"
    ]
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. Convert publish time to datetime
    df["publish_datetime"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["publish_date"] = df["publish_datetime"].dt.date
    df["publish_month"] = df["publish_datetime"].dt.to_period("M").astype(str)
    df["publish_weekday"] = df["publish_datetime"].dt.day_name()
    df["publish_hour"] = df["publish_datetime"].dt.hour

    # 4. Clean post format
    df["post_format"] = (
        df["post_type"]
        .astype(str)
        .str.lower()
        .str.replace("ig ", "", regex=False)
        .str.strip()
    )

    # 5. Flag MathSoc-owned vs partner/collab posts
    df["account_username_clean"] = df["account_username"].astype(str).str.lower().str.strip()
    df["account_group"] = np.where(
        df["account_username_clean"].eq("uwmathsoc"),
        "MathSoc-owned",
        "Partner/Collaborative"
    )

    # 6. Basic engagement KPI
    df["total_engagements"] = df[["likes", "comments", "shares", "saves"]].sum(axis=1, min_count=1)

    # 7. Safe division helper: returns blank if denominator is missing or 0
    def safe_divide(numerator, denominator):
        return np.where((denominator.notna()) & (denominator > 0), numerator / denominator, np.nan)

    # Reach-based rates: main reporting metrics
    df["engagement_rate_reach"] = safe_divide(df["total_engagements"], df["reach"])
    df["share_rate_reach"] = safe_divide(df["shares"], df["reach"])
    df["save_rate_reach"] = safe_divide(df["saves"], df["reach"])
    df["like_rate_reach"] = safe_divide(df["likes"], df["reach"])
    df["follow_rate_reach"] = safe_divide(df["follows"], df["reach"])

    # Views-based rates: backup metrics for posts with missing reach
    df["engagement_rate_views"] = safe_divide(df["total_engagements"], df["views"])
    df["share_rate_views"] = safe_divide(df["shares"], df["views"])
    df["save_rate_views"] = safe_divide(df["saves"], df["views"])

    # 8. Manual tagging columns: fill these later, not in raw file
    df["event_name_manual"] = ""
    df["content_type_manual"] = ""
    df["cta_type_manual"] = ""
    df["major_event_manual"] = ""

    # 9. Simple auto hint for first draft analysis only
    desc = df["description"].fillna("").str.lower()
    df["auto_content_hint"] = np.select(
        [
            desc.str.contains("resume|career|coop|co-op|interview|review session", regex=True),
            desc.str.contains("election|council|board|general meeting|agm", regex=True),
            desc.str.contains("volunteer|apply|hiring|recruit", regex=True),
            desc.str.contains("game|movie|trivia|cookie|bubble tea|pizza|night", regex=True),
            desc.str.contains("exam|midterm|study|calc|calculus|tutorial", regex=True),
        ],
        [
            "academic_career",
            "governance",
            "recruitment",
            "community_event",
            "academic_support",
        ],
        default="other"
    )

    return df


def create_summary_tables(df: pd.DataFrame) -> None:
    """Create CSV summary tables for quick checking and Power BI support."""
    by_term = (
        df.groupby("term", dropna=False)
        .agg(
            posts=("post_id", "count"),
            total_views=("views", "sum"),
            total_reach=("reach", "sum"),
            total_engagements=("total_engagements", "sum"),
            total_likes=("likes", "sum"),
            total_comments=("comments", "sum"),
            total_shares=("shares", "sum"),
            total_saves=("saves", "sum"),
            avg_engagement_rate_reach=("engagement_rate_reach", "mean"),
            missing_reach_posts=("reach", lambda x: x.isna().sum()),
        )
        .reset_index()
    )
    by_term.to_csv(OUTPUTS_DIR / "summary_by_term.csv", index=False)

    by_format = (
        df.groupby(["term", "post_format"], dropna=False)
        .agg(
            posts=("post_id", "count"),
            total_views=("views", "sum"),
            total_reach=("reach", "sum"),
            total_engagements=("total_engagements", "sum"),
            total_shares=("shares", "sum"),
            total_saves=("saves", "sum"),
            avg_engagement_rate_reach=("engagement_rate_reach", "mean"),
        )
        .reset_index()
    )
    by_format.to_csv(OUTPUTS_DIR / "summary_by_format.csv", index=False)

    by_account = (
        df.groupby(["term", "account_group"], dropna=False)
        .agg(
            posts=("post_id", "count"),
            total_views=("views", "sum"),
            total_reach=("reach", "sum"),
            total_engagements=("total_engagements", "sum"),
            avg_engagement_rate_reach=("engagement_rate_reach", "mean"),
        )
        .reset_index()
    )
    by_account.to_csv(OUTPUTS_DIR / "summary_by_account_group.csv", index=False)

    by_hint = (
        df.groupby(["term", "auto_content_hint"], dropna=False)
        .agg(
            posts=("post_id", "count"),
            total_views=("views", "sum"),
            total_reach=("reach", "sum"),
            total_engagements=("total_engagements", "sum"),
            total_shares=("shares", "sum"),
            total_saves=("saves", "sum"),
            avg_engagement_rate_reach=("engagement_rate_reach", "mean"),
        )
        .reset_index()
    )
    by_hint.to_csv(OUTPUTS_DIR / "summary_by_auto_content_hint.csv", index=False)

    df.sort_values("reach", ascending=False).head(10).to_csv(OUTPUTS_DIR / "top_posts_by_reach.csv", index=False)
    df.sort_values("engagement_rate_reach", ascending=False).head(10).to_csv(OUTPUTS_DIR / "top_posts_by_engagement_rate.csv", index=False)
    df.sort_values("shares", ascending=False).head(10).to_csv(OUTPUTS_DIR / "top_posts_by_shares.csv", index=False)
    df.sort_values("saves", ascending=False).head(10).to_csv(OUTPUTS_DIR / "top_posts_by_saves.csv", index=False)


def make_public_raw_sample(raw_df: pd.DataFrame, term: str, n: int = 12) -> pd.DataFrame:
    """Create anonymized sample raw data for GitHub. Does not expose real captions, IDs, links, or exact metrics."""
    rng = np.random.default_rng(100 if term == "W25" else 200)
    sample = raw_df.sample(n=min(n, len(raw_df)), random_state=100 if term == "W25" else 200).copy().reset_index(drop=True)

    sample["Post ID"] = [f"sample_{term.lower()}_post_{i+1:03d}" for i in range(len(sample))]
    sample["Account ID"] = [f"sample_{term.lower()}_account_{i+1:03d}" for i in range(len(sample))]
    sample["Account username"] = np.where(
        sample["Account username"].astype(str).str.lower().eq("uwmathsoc"),
        "uwmathsoc_sample",
        "partner_account_sample"
    )
    sample["Account name"] = np.where(
        sample["Account username"].eq("uwmathsoc_sample"),
        "MathSoc Sample Account",
        "Partner Sample Account"
    )
    sample["Description"] = [
        f"Sample anonymized {term} caption for Instagram content analysis. Original caption removed for privacy."
        for _ in range(len(sample))
    ]
    sample["Permalink"] = [f"https://www.instagram.com/p/sample_{term.lower()}_{i+1:03d}/" for i in range(len(sample))]

    # Replace metrics with synthetic-but-realistic values.
    views = rng.integers(800, 18000, size=len(sample))
    reach = (views * rng.uniform(0.35, 0.80, size=len(sample))).astype(int)
    likes = (reach * rng.uniform(0.015, 0.080, size=len(sample))).astype(int)
    shares = (reach * rng.uniform(0.002, 0.040, size=len(sample))).astype(int)
    comments = rng.integers(0, 8, size=len(sample))
    saves = (reach * rng.uniform(0.001, 0.020, size=len(sample))).astype(int)
    follows = rng.integers(0, 8, size=len(sample))

    sample["Views"] = views
    sample["Reach"] = reach
    sample["Likes"] = likes
    sample["Shares"] = shares
    sample["Comments"] = comments
    sample["Saves"] = saves
    sample["Follows"] = follows

    return sample


def main():
    print("Reading raw files...")
    w25_raw = read_raw_file(W25_RAW, "W25")
    w26_raw = read_raw_file(W26_RAW, "W26")

    print(f"W25 raw shape: {w25_raw.shape}")
    print(f"W26 raw shape: {w26_raw.shape}")

    print("Cleaning and combining W25/W26...")
    combined_raw = pd.concat([w25_raw, w26_raw], ignore_index=True)
    cleaned = clean_meta_export(combined_raw)

    private_output = PROCESSED_DIR / "cleaned_instagram_w25_w26_private.csv"
    cleaned.to_csv(private_output, index=False)
    print(f"Saved private cleaned file: {private_output}")

    print("Creating summary tables...")
    create_summary_tables(cleaned)
    print(f"Saved summary tables in: {OUTPUTS_DIR}")

    print("Creating anonymized public sample files...")
    w25_sample_raw = make_public_raw_sample(w25_raw, "W25")
    w26_sample_raw = make_public_raw_sample(w26_raw, "W26")
    w25_sample_raw.to_csv(SAMPLE_DIR / "raw_meta_w25_sample.csv", index=False)
    w26_sample_raw.to_csv(SAMPLE_DIR / "raw_meta_w26_sample.csv", index=False)

    sample_combined = pd.concat([w25_sample_raw, w26_sample_raw], ignore_index=True)
    sample_cleaned = clean_meta_export(sample_combined)
    sample_cleaned.to_csv(SAMPLE_DIR / "cleaned_instagram_w25_w26_sample.csv", index=False)
    print(f"Saved public sample files in: {SAMPLE_DIR}")

    print("\nDone. Quick check:")
    print(cleaned.groupby("term").agg(posts=("post_id", "count"), total_views=("views", "sum"), total_reach=("reach", "sum"), total_engagements=("total_engagements", "sum")))


if __name__ == "__main__":
    main()
