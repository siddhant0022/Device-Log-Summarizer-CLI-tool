# Section 2 - Device Log Summarizer CLI
# usage: python summarizer.py [csv_file] [output_json]

import csv
import json
import sys

TEMP_LIMIT = 80.0


def read_csv(path):
    """Reads the csv and returns a list of valid rows. Bad rows are skipped."""
    rows = []
    skipped = 0

    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)

            needed = {"device_id", "status", "temperature"}
            if reader.fieldnames is None or not needed.issubset(reader.fieldnames):
                print("Error: CSV must have columns:", ", ".join(sorted(needed)))
                return None

            for line in reader:
                device = (line["device_id"] or "").strip()
                status = (line["status"] or "").strip().upper()
                try:
                    temp = float(line["temperature"])
                except (ValueError, TypeError):
                    skipped += 1
                    continue

                if device == "":
                    skipped += 1
                    continue

                rows.append({"device_id": device, "status": status, "temperature": temp})
    except FileNotFoundError:
        print(f"Error: file '{path}' not found.")
        return None
    except OSError as e:
        print(f"Error reading file: {e}")
        return None

    if skipped > 0:
        print(f"Note: skipped {skipped} bad row(s).")
    return rows


def aggregate(rows):
    """Groups rows by device_id and calculates the stats."""
    groups = {}
    for r in rows:
        d = r["device_id"]
        if d not in groups:
            groups[d] = {"temps": [], "errors": 0}
        groups[d]["temps"].append(r["temperature"])
        if r["status"] == "ERROR":
            groups[d]["errors"] += 1

    results = []
    for device, info in sorted(groups.items()):
        temps = info["temps"]
        results.append({
            "device_id": device,
            "total_records": len(temps),
            "avg_temperature": round(sum(temps) / len(temps), 2),
            "error_count": info["errors"],
        })
    return results


def filter_hot_devices(results, limit=TEMP_LIMIT):
    # keep only devices whose average temp is NOT above the limit
    return [r for r in results if r["avg_temperature"] <= limit]


def print_table(results):
    print()
    print(f"{'Device':<10}{'Records':>10}{'Avg Temp':>12}{'Errors':>10}")
    print("-" * 42)
    for r in results:
        print(f"{r['device_id']:<10}{r['total_records']:>10}"
              f"{r['avg_temperature']:>12.2f}{r['error_count']:>10}")
    print()


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "device_telemetry.csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "summary.json"

    rows = read_csv(csv_path)
    if rows is None:
        sys.exit(1)
    if len(rows) == 0:
        print("No valid data found in the file.")
        sys.exit(1)

    all_results = aggregate(rows)
    final = filter_hot_devices(all_results)

    removed = len(all_results) - len(final)
    print(f"Processed {len(rows)} rows, {len(all_results)} devices.")
    print(f"Removed {removed} device(s) with avg temp above {TEMP_LIMIT}.")

    with open(out_path, "w") as f:
        json.dump(final, f, indent=4)
    print(f"Saved results to {out_path}")

    print_table(final)


if __name__ == "__main__":
    main()
