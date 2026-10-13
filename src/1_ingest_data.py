from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
CSV_PATH = DATA_DIR / "ai4i2020.csv"
DB_PATH = PROJECT_ROOT / "factory_telemetry.db"


def main() -> None:
    if not CSV_PATH.exists():
        print(f"Error: Missing dataset at {CSV_PATH}.")
        print("Please download the AI4I 2020 Predictive Maintenance Dataset and place it in data/raw/ai4i2020.csv.")
        raise SystemExit(1)

    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_csv(CSV_PATH)
    df.to_sql("raw_telemetry", con=engine, index=False, if_exists="replace")

    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM raw_telemetry LIMIT 5"))
        print("First 5 rows from raw_telemetry:")
        for row in result:
            print(row)


if __name__ == "__main__":
    main()
