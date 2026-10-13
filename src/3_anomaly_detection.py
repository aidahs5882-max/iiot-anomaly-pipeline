from pathlib import Path

import pandas as pd
from scipy.stats import zscore
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "factory_telemetry.db"


def main() -> None:
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql_table("processed_features", con=engine)

    power_zscore = zscore(df["Power"].astype(float), nan_policy="omit")
    df["Stat_Anomaly"] = (power_zscore.abs() > 3).astype(bool)

    features = ["Temperature_Difference", "Power", "Tool wear [min]"]
    model = IsolationForest(contamination=0.035, random_state=42)
    model.fit(df[features])

    df["ML_Anomaly"] = model.predict(df[features]) == -1
    df["ML_Anomaly"] = df["ML_Anomaly"].astype(bool)

    df.to_sql("anomaly_results", con=engine, index=False, if_exists="replace")

    y_true = df["Machine failure"].astype(int).to_numpy()
    y_pred = df["ML_Anomaly"].astype(int).to_numpy()
    print(classification_report(y_true, y_pred, target_names=["No Failure", "Failure"]))


if __name__ == "__main__":
    main()
