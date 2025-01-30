"""Functions for data processing."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler


def detect_outliers(df: pd.DataFrame, threshold: float) -> dict:
    """Detect global outliers based on given threshold.

    Args:
        df (pd.DataFrame): input dataset
        threshold (float): multiplier for outlier detection

    Returns:
        dict: outliers information for each column

    """
    outliers = {}
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

    # Iterate over each col, compute bounds, detect outliers, and write them in a dict
    for col in numeric_columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr

        column_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outliers[col] = {
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_count": column_outliers.shape[0],
            "outlier_percentage": column_outliers.shape[0] / df.shape[0] * 100,
        }

    return outliers


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply preprocessing steps on a provided dataset.

    Steps like:
        - handling missing values,
        - normalizing numerical data,
        - and encoding categorical variables.

    Args:
        df (pd.DataFrame): input unprocessed dataset

    Returns:
        pd.DataFrame: processed dataset

    """
    # Identify column types and group them
    numeric_features = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = df.select_dtypes(include=["object", "category"]).columns

    # Set up a pipeline with necessary preprocessing steps
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ],
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="warn")),
        ],
    )

    # Apply transfomer steps
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
    )

    # Fit and tranform the data
    processed_array = preprocessor.fit_transform(df)

    # Reconstruct dataframe with processed data
    feature_names = list(numeric_features) + list(
        preprocessor.named_transformers_["cat"]["onehot"].get_feature_names_out(
            categorical_features,
        ),
    )

    return pd.DataFrame(processed_array, columns=feature_names)
