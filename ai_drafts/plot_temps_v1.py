import json
import matplotlib.pyplot as plt

with open("summary.json") as f:
    data = json.load(f)

devices = [d["device_id"] for d in data]
temps = [d["avg_temperature"] for d in data]

plt.bar(devices, temps)
plt.savefig("chart_v1.png")
