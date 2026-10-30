# Device Log Summarizer

CLI tool that reads device telemetry from a CSV, summarizes it per device, and charts it.

## Files
- `clean_readings.py` - Section 1: sensor value cleaning + tests
- `summarizer.py` - Section 2: CSV -> aggregation -> filter -> JSON + terminal table
- `plot_temps.py` - Section 3: bar chart from the JSON
- `device_telemetry.csv` - sample input
- `summary.json`, `sample_output.txt`, `temperature_chart.png` - sample outputs
- `PROMPT_LOG.md` - AI usage log
- `ai_drafts/` - first AI draft of the chart script and its output (for the log)

## How to run
```
pip install matplotlib
python clean_readings.py        # runs the tests
python summarizer.py            # or: python summarizer.py my.csv out.json
python plot_temps.py
```

## Notes
- Rows with a missing/invalid temperature or empty device_id are skipped (count is printed).
- Devices with average temperature above 80.0 are removed from the output.
- Missing file or wrong columns gives an error message instead of a crash.
