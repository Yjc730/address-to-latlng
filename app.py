import time
from typing import List, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from geocoder import geocode_one

app = FastAPI(title="Batch Address Geocoder")


# =========================
# Models
# =========================
class BatchReq(BaseModel):
    addresses: List[str] = Field(default_factory=list)


class BatchItem(BaseModel):
    address: str
    lat: Optional[str] = None
    lng: Optional[str] = None
    status: str
    matched_name: Optional[str] = None


# =========================
# Config
# =========================
MAX_ADDRESSES = 50


# =========================
# API
# =========================
@app.post("/api/geocode/batch", response_model=list[BatchItem])
def geocode_batch(payload: BatchReq):
    # 🔒 後端保護：最多 50 筆
    if len(payload.addresses) > MAX_ADDRESSES:
        return [
            BatchItem(
                address="",
                status=f"ERROR: 一次最多 {MAX_ADDRESSES} 筆地址"
            )
        ]

    results: List[BatchItem] = []

    for raw in payload.addresses:
        addr = (raw or "").strip()
        if not addr:
            continue

        try:
            lat, lon, display_name = geocode_one(addr)
            if lat and lon:
                results.append(BatchItem(
                    address=addr,
                    lat=lat,
                    lng=lon,
                    status="OK",
                    matched_name=display_name
                ))
            else:
                results.append(BatchItem(
                    address=addr,
                    status="NOT_FOUND"
                ))
        except Exception as e:
            results.append(BatchItem(
                address=addr,
                status=f"ERROR: {type(e).__name__}"
            ))

        # ⏱️ 避免 Nominatim 封鎖
        time.sleep(1)

    return results


# =========================
# Static UI（一定要放最後）
# =========================
app.mount("/", StaticFiles(directory="static", html=True), name="static")
