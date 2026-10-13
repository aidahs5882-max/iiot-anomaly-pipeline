from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "factory_telemetry.db"
OUTPUT_PATH = PROJECT_ROOT / "output" / "anomaly_plot.png"


def main() -> None:
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql_table("anomaly_results", con=engine)

    plt.figure(figsize=(12, 6))
    plt.plot(df["UDI"], df["Power"], color="blue", linewidth=1.5, label="Normal operation")

    anomaly_points = df[df["ML_Anomaly"] == True]
    if not anomaly_points.empty:
        plt.scatter(
            anomaly_points["UDI"],
            anomaly_points["Power"],
            color="red",
            s=45,
            label="ML-detected anomaly",
            alpha=0.85,
        )

    plt.title("IIoT Power Signal and ML-Detected Anomalies")
    plt.xlabel("UDI")
    plt.ylabel("Power (Rotational Speed × Torque)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300)
    plt.close()

    print(f"Plot saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
