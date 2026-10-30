# PROMPT_LOG.md

This task allowed AI assistants. I used Claude throughout, and I'm listing
exactly where, so the evaluation is transparent.

| Section | AI usage |
|---|---|
| 1. Sanitization function | AI-assisted. I reviewed the logic and the edge cases (None, bool, NaN, negatives, the 500.0 cap, non-list input) and ran the tests. |
| 2. CSV summarizer | AI-assisted structure. I reviewed it and checked the output against the sample CSV by hand (e.g. DEV_A average = (45.2+47.8+52.1+44.0)/4 = 47.275 -> 47.27). |
| 3. Chart script | Prompted, tested, found problems, re-prompted (details below). |

## 1. Initial prompt
> Write a Python script that loads `summary.json` (a list of objects with
> `device_id`, `avg_temperature`, `total_records`, `error_count`) and generates
> a bar chart comparing average temperature per device using matplotlib. Save
> it as a PNG.

The first attempt is kept in `ai_drafts/plot_temps_v1.py`, with its output in
`ai_drafts/chart_v1.png`, so the before/after can be compared.

## 2. Bugs / mistakes in the first attempt
I ran the first version and checked the chart. It worked, but it was not usable:
- **No title and no axis labels**, so the chart doesn't say what it shows or in what unit.
- **No value labels on the bars**, so exact averages can't be read.
- **No `tight_layout()` / label rotation**, so with more devices (I tested with
  longer IDs) the x-axis labels would overlap.
- **No error handling**: it crashes with a raw traceback if `summary.json` is
  missing or empty, which matters because Section 2 can filter out every device.
- It also gave no visual reference for the 80.0 filter threshold.

## 3. Follow-up prompt used to fix it
> The chart runs but has formatting problems. Add a title, x/y axis labels with
> the unit (°C), the average value printed on top of each bar, rotated x labels
> with `tight_layout()` so nothing overlaps, and a dashed line at 80°C for the
> filter threshold. Also handle a missing or invalid JSON file with a clear
> error message instead of a traceback, and exit cleanly if there is no data.

The result is `plot_temps.py`. I ran it and confirmed that the title and labels
appear, that the values match `summary.json`, and that deleting the JSON file
now prints a friendly message instead of crashing.

## What I took from this
AI gets you a working first draft fast, but it skips polish and failure
cases. I treated its output as a draft to test and not as a final answer.
