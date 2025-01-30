"""Functions for report generating."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def generate_mardown_report(
    raw_df: pd.DataFrame,
    processed_df: pd.DataFrame,
    path: str,
    hist_path: str,
    scatter_path: str,
    heatmap_path: str,
) -> None:
    """Generate a final report for the dataset analysis.

    Args:
        raw_df (pd.DataFrame): dataset before processing
        processed_df (pd.DataFrame): dataset after processing
        path (str): path to save report
        hist_path (str): relative path to distribution plots image
        scatter_path (str): relative path to scatter plots image
        heatmap_path (str): relative path to heatmap plots image

    """
    report = []

    report.append("# Data Analysis Report")

    # 1. Dataset Overview
    numeric_features = raw_df.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = raw_df.select_dtypes(include=["object", "category"]).columns
    report.append("\n## 1. Dataset Overview")
    report.append("### Basic Information")
    report.append(f"- Total Records: {raw_df.shape[0]}")
    report.append(f"- Total Features: {raw_df.shape[1]}")
    report.append(f"- Numeric Features: {len(numeric_features)}")
    report.append(f"- Categorical Features: {len(categorical_features)}")

    # 2. Data Quality Analysis
    report.append("\n## 2. Data Quality Analysis")
    report.append("### Missing Values")
    missing = raw_df.isna().sum()
    missing_pct = (missing / raw_df.shape[0] * 100).round(2)

    if missing.sum() > 0:
        report.append("\n| Feature | Missing Count | Missing Percentage |")
        report.append("| --- | --- | --- |")
        for col in raw_df.columns:
            if missing[col] > 0:
                report.append(f"| {col} | {missing[col]} | {missing_pct[col]}")
    else:
        report.append("No missing values found in the dataset.")

    # 3. Numeric Features Analysis
    if len(numeric_features) > 0:
        report.append("\n## 3. Numeric Features Analysis")

        # Statistical Summary
        report.append("### Statistical Summary")
        report.append("\n| Feature | Mean | Median | Std | Min | Max | Skew |")
        report.append("| --- | --- | --- | --- | --- | --- | --- |")

        for col in numeric_features:
            stats = raw_df[col].describe()
            skew = raw_df[col].skew()
            report.append(
                f"| {col} | {stats['mean']:.2f} | {stats['50%']:.2f} | "
                f"{stats['std']:.2f} | {stats['min']:.2f} | {stats['max']:.2f} | "
                f"{skew:.2f} |",
            )

        # Outliers Summary
        report.append("\n### Outliers Analysis")
        report.append("Using IQR method to detect outliers:")

        for col in numeric_features:
            q1 = raw_df[col].quantile(0.25)
            q3 = raw_df[col].quantile(0.75)
            iqr = q3 - q1
            outliers = raw_df[
                (raw_df[col] < (q1 - 1.5 * iqr)) | (raw_df[col] > (q3 + 1.5 * iqr))
            ][col]

            report.append(f"\n#### {col}")
            report.append(f"- Number of outliers: {len(outliers)}")
            report.append(
                f"- Percentage of outliers: {(len(outliers)/len(raw_df)*100):.2f}%",
            )
            if len(outliers) > 0:
                report.append(
                    "- Outlier values: "
                    + ", ".join([f"{x:.2f}" for x in outliers[:5]]),
                )

    # 4. Categorical Features Analysis
    if len(categorical_features) > 0:
        report.append("\n## 4. Categorical Features Analysis")

        for col in categorical_features:
            report.append(f"\n### {col}")
            value_counts = raw_df[col].value_counts()
            value_percentages = (value_counts / len(raw_df) * 100).round(2)

            report.append("\n| Value | Count | Percentage |")
            report.append("| --- | --- | --- |")
            for val, count in value_counts.items():
                report.append(f"| {val} | {count} | {value_percentages[val]}% |")

    # 5. Preprocessing Summary
    if processed_df is not None:
        report.append("\n## 5. Preprocessing Summary")
        report.append("### Applied Transformations")
        report.append("- Handled missing values")
        report.append("- Standardized numeric features")
        report.append("- Encoded categorical variables")

        # Compare before/after shapes
        report.append("\n### Dataset Transformation")
        report.append(f"- Original shape: {raw_df.shape}")
        report.append(f"- Processed shape: {processed_df.shape}")

        # New feature names
        report.append("\n### Generated Features")
        report.append("| Original Feature | Generated Features |")
        report.append("| --- | --- |")

        for col in categorical_features:
            encoded_cols = [c for c in processed_df.columns if c.startswith(col)]
            report.append(f"| {col} | {', '.join(encoded_cols)} |")

    # 6. Visualizations
    report.append("\n## 6. Visualizations")
    report.append("### Univariate Analysis")
    report.append(f"![Distribution grid plots]({hist_path})")
    report.append("### Bivariate Analysis")
    report.append(f"![Pair plots]({scatter_path})")
    report.append("### Multivariate Analysis")
    report.append(f"![Correlation heatmap]({heatmap_path})")

    # Save the report
    with open(path, "w") as f:
        f.write("\n".join(report))
