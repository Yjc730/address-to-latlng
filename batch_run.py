import time
import pandas as pd
from geocoder import geocode

with open("data/addresses.txt", "r", encoding="utf-8") as f:
    addresses = [line.strip() for line in f if line.strip()]

results = []

for addr in addresses:
    lat, lng = geocode(addr)
    results.append({
        "address": addr,
        "latitude": lat,
        "longitude": lng
    })
    time.sleep(1)  # 避免 API 封鎖

df = pd.DataFrame(results)
df.to_csv("output/result.csv", index=False, encoding="utf-8-sig")

print(df)
