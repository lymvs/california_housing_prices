"""Perform exploratory data analysis (EDA) on California housing prices case study.

Author:
    Lysandros Mavropoulos
"""

import pandas as pd

from scripts import data_analysis, data_preprocessing, report

# Constants
DATA_PATH = "data/housing.csv"
REPORT_FILE = "markdown_report.md"
PLOT_FOLDER = "visualizations/"
HIST_PLOT_PATH = PLOT_FOLDER + "distribution_plots.png"
SCATTER_PLOT_PATH = PLOT_FOLDER + "scatter_plots.png"
HEATMAP_PLOT_PATH = PLOT_FOLDER + "correlation_heatmap.png"


def main() -> None:
    """Run main workflow."""
    data = pd.read_csv(DATA_PATH)

    # Data Preprocessing
    processed_data = data_preprocessing.preprocess_data(data)

    # Univariate Analysis
    data_analysis.kde_grid_plot(processed_data, HIST_PLOT_PATH)

    # Bivariate Analysis
    drop_columns = [x for x in processed_data.columns if "ocean_proximity" in x]
    data_analysis.scatter_plot_grid(
        processed_data.drop(drop_columns, axis=1),
        SCATTER_PLOT_PATH,
    )

    # Multivariate Analysis
    data_analysis.correlation_heatmap(
        processed_data.drop(drop_columns, axis=1),
        HEATMAP_PLOT_PATH,
    )

    # Generate Final Report
    report.generate_mardown_report(
        data,
        processed_data,
        REPORT_FILE,
        HIST_PLOT_PATH,
        SCATTER_PLOT_PATH,
        HEATMAP_PLOT_PATH,
        )

if __name__ == "__main__":
    main()
