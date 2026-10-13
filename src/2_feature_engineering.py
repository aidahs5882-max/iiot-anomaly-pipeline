from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "factory_telemetry.db"


def main() -> None:
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql_table("raw_telemetry", con=engine)

    df["Temperature_Difference"] = df["Process temperature [K]"] - df["Air temperature [K]"]
    df["Power"] = df["Rotational speed [rpm]"] * df["Torque [Nm]"]

    df["Temperature_Difference_RollingMean"] = (
        df["Temperature_Difference"].rolling(window=5, min_periods=1).mean()
    )
    df["Power_RollingMean"] = df["Power"].rolling(window=5, min_periods=1).mean()

    df.to_sql("processed_features", con=engine, index=False, if_exists="replace")
    print("Feature engineering complete. Data written to processed_features.")


if __name__ == "__main__":
    main()
