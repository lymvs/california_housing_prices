"""Functions for generating plots."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def kde_grid_plot(df: pd.DataFrame, path: str) -> None:
    """Create a grid of Kernel Density Estimation (KDE) plots.

    Args:
        df (pd.DataFrame): input dataset for creating kde plots
        path (str): path name for saving the figure

    """
    sns.set_style("darkgrid")

    numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns
    num_features = len(numerical_columns)
    rows = (num_features + 1) // 2  # Ensure enough rows for 2 columns

    fig, axes = plt.subplots(rows, 2, figsize=(14, rows * 3))  # Create subplots
    axes = axes.flatten()

    for idx, feature in enumerate(numerical_columns):
        sns.histplot(df[feature], kde=True, color="darksalmon", ax=axes[idx])
        axes[idx].set_title(f"{feature} | Skewness: {round(df[feature].skew(), 2)}")

    plt.tight_layout()
    plt.savefig(path)


def scatter_plot_grid(df: pd.DataFrame, path: str) -> None:
    """Create a grid of scatter plots.

    Args:
        df (pd.DataFrame): input dataset
        path (str): path name for saving the figure

    """
    sns.set_palette("Pastel1")

    plt.figure(figsize=(13, 17))
    sns.pairplot(data=df)

    plt.tight_layout()
    plt.savefig(path)


def correlation_heatmap(df: pd.DataFrame, path: str) -> None:
    """Create a correlation heatmap plot.

    Args:
        df (pd.DataFrame): input dataset
        path (str): path name for saving the figure

    """
    plt.figure(figsize=(12, 7))
    correlation_matrix = df.corr()

    sns.heatmap(correlation_matrix, annot=True, vmin=-1, vmax=1)
    plt.savefig(path)
