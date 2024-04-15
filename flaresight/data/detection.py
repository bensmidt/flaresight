"""
Exploring and Visualization Fire Detection Datasets
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_label_distribution(y_train: pd.DataFrame, y_test: pd.DataFrame) -> None:
    """
    Plot the distribution of the training and testing labels.

    Parameters
    ----------
    y_train: pd.DataFrame
        Training labels.
    y_test: pd.DataFrame
        Testing labels.

    Returns
    -------
    None
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Plot distribution of y_train
    ax1.pie(
        y_train.value_counts(),
        labels=["No Fire", "Fire"],
        autopct='%1.1f%%',
        startangle=90
    )
    ax1.set_title('Train Distribution')
    ax1.annotate(
        f"{y_train.count()} samples",
        xy=(0, -1.2),
        ha='center',
        va='center',
        fontsize=12,
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3')
    )

    # Plot distribution of y_test
    ax2.pie(
        y_test.value_counts(),
        labels=["No Fire", "Fire"],
        autopct='%1.1f%%',
        startangle=90
    )
    ax2.set_title('Test Distribution')
    ax2.annotate(
        f"{y_test.count()} samples",
        xy=(0, -1.2),
        ha='center',
        va='center',
        fontsize=12,
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3')
    )

    plt.tight_layout()
    plt.show()


def plot_feature_scatterplots(X_train: pd.DataFrame, n_cols: int = 3) -> None:
    """
    Plot scatter plots of the features.

    Parameters
    ----------
    X_train: pd.DataFrame
        Training features.
    n_cols: int
        Number of columns to use in the plot.

    Returns
    -------
    None
    """
    N, d = X_train.shape
    rows = (d // n_cols) + (d % n_cols > 0)
    cols = min(n_cols, d)

    feature_names = X_train.columns

    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 5))

    # Iterate over features and plot scatter plots
    for i in range(d):
        row = i // cols  # Calculate row index
        col = i % cols  # Calculate column index
        ax = axes[row, col]  # Get the current axis

        data = X_train.iloc[:, i]
        ax.scatter(np.arange(N), data)
        ax.set_title(f"{feature_names[i]} Scatter Plot")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Value")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()


def plot_feature_vs_fire(
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    n_cols: int = 3
) -> None:
    N, d = X_train.shape
    rows = (d // n_cols) + (d % n_cols > 0)
    cols = min(n_cols, d)

    feature_names = X_train.columns

    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 5))

    for i in range(d):
        row = i // cols  # Calculate row index
        col = i % cols  # Calculate column index
        ax = axes[row, col]  # Get the current axis
        data = X_train.iloc[:, i]

        # scatter plot
        ax.scatter(data, y_train)
        ax.set_title("{} vs. Fire / No Fire".format(feature_names[i]))
        ax.set_xlabel("Value")
        ax.set_ylabel("Fire / No Fire")
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()


def standardize_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the DataFrame to have mean 0 and std 1.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to standardize.

    Returns
    -------
    pd.DataFrame
        Standardized DataFrame.
    """
    return (df - df.mean(axis=0)) / df.std(axis=0)


def standardize(arr: np.array, mean: float = None, std: float = None) -> np.array:
    """
    Standardize the array to have mean 0 and std 1.

    Parameters
    ----------
    arr: np.array
        Array to standardize.
    mean: float
        Mean of the array.
    std: float
        Standard deviation of the array.

    Returns
    -------
    np.array
        Standardized array.
    """
    if mean is None:
        mean = np.mean(arr)
    if std is None:
        std = np.std(arr)
    return (arr - np.mean(arr)) / np.std(arr)
