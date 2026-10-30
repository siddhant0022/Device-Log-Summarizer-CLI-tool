# Section 3 - bar chart of average temperature per device
# usage: python plot_temps.py [summary.json] [chart.png]

import json
import sys

import matplotlib
matplotlib.use("Agg")  # so it works without a display
import matplotlib.pyplot as plt


def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else "summary.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "temperature_chart.png"

    try:
        with open(json_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{json_path}' not found. Run summarizer.py first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{json_path}' is not valid JSON.")
        sys.exit(1)

    if not data:
        print("Nothing to plot.")
        sys.exit(1)

    devices = [d["device_id"] for d in data]
    temps = [d["avg_temperature"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(devices, temps, color="steelblue", edgecolor="black")

    # write the value on top of each bar
    for bar, t in zip(bars, temps):
        ax.text(bar.get_x() + bar.get_width() / 2, t + 0.8, f"{t:.1f}",
                ha="center", va="bottom", fontsize=9)

    ax.axhline(80, color="red", linestyle="--", label="Threshold (80°C)")
    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.set_ylim(0, max(temps + [80]) + 10)
    ax.legend()

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"Chart saved to {out_path}")


if __name__ == "__main__":
    main()
