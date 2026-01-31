import pandas as pd
from pathlib import Path


# ---------------------------
# File I/O utilities
# ---------------------------

def load_dataset(path: str) -> pd.DataFrame:
    """
    Load a CSV dataset with basic error handling.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load dataset: {e}")

    return df


# ---------------------------
# Schema utilities
# ---------------------------

REQUIRED_COLUMNS = [
    "record_type",
    "indicator",
    "indicator_code",
    "observation_date",
    "value_numeric",
    "confidence"
]


def validate_schema(df: pd.DataFrame) -> None:
    """
    Validate that required columns exist in the dataset.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


# ---------------------------
# Filtering utilities
# ---------------------------

def split_by_record_type(df: pd.DataFrame) -> dict:
    """
    Split unified dataset by record_type.
    """
    return {
        "observations": df[df["record_type"] == "observation"].copy(),
        "events": df[df["record_type"] == "event"].copy(),
        "impact_links": df[df["record_type"] == "impact_link"].copy(),
        "targets": df[df["record_type"] == "target"].copy()
    }


# ---------------------------
# Plotting utilities
# ---------------------------

def plot_time_series(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    title: str,
    ylabel: str,
    marker: str = "o"
):
    """
    Standardized time-series plotting.
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    plt.figure(figsize=(8, 4))
    plt.plot(df[date_col], df[value_col], marker=marker)
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
