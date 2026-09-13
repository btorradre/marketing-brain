"""GetHookd resolver — share URL / ad id -> video URL + metadata.

Ported from the shared replicator utility. The key comes from the workspace's
'gethookd' credential; nothing is cached on disk here — the worker streams the
video URL into a blob.
"""
from __future__ import annotations

import re
import time

import requests

from adengine.core.errors import ProviderError

BASE = "https://app.gethookd.ai/api/v1"


def _headers(key: str) -> dict:
    return {"Authorization": f"Bearer {key}", "Accept": "application/json"}


def is_gethookd_url(input_str: str | None) -> bool:
    """True for a GetHookd URL or a bare numeric ad id."""
    if not input_str:
        return False
    if "gethookd.ai" in input_str:
        return True
    return bool(re.match(r"^\d{7,}$", input_str.strip()))


def extract_ad_id(input_str: str) -> str | None:
    input_str = input_str.strip()
    if re.match(r"^\d+$", input_str):
        return input_str
    m = re.search(r"gethookd\.ai/share/ad/(\d+)", input_str)
    if m:
        return m.group(1)
    m = re.search(r"gethookd\.ai/(?:ads?|swipefile|brandspy)/.*?(\d{7,})", input_str)
    if m:
        return m.group(1)
    m = re.search(r"(\d{7,})", input_str)
    return m.group(1) if m else None


def fetch_ad_metadata(ad_id: str, key: str, sleep=time.sleep) -> dict | None:
    """Tries the direct endpoints, then pages the swipe file."""
    for url in (f"{BASE}/ads/{ad_id}", f"{BASE}/swipefile/{ad_id}"):
        try:
            resp = requests.get(url, headers=_headers(key), timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if not data.get("errors"):
                    ad = data.get("data", data)
                    if isinstance(ad, dict) and ad.get("id"):
                        return ad
        except Exception:  # noqa: BLE001
            continue
    try:
        page = 1
        while page <= 10:
            resp = requests.get(f"{BASE}/swipefile?page={page}&per_page=100",
                                headers=_headers(key), timeout=15)
            if resp.status_code != 200:
                break
            ads = resp.json().get("data", [])
            if not ads:
                break
            for ad in ads:
                if str(ad.get("id")) == str(ad_id):
                    return ad
            page += 1
            sleep(0.3)
    except Exception:  # noqa: BLE001
        pass
    return None


def get_video_url(ad_data: dict) -> str | None:
    for m in ad_data.get("media", []) or []:
        if m.get("type") == "video" and m.get("url"):
            return m["url"]
    return None


def build_metadata(ad_data: dict) -> dict:
    brand = ad_data.get("brand")
    meta = {
        "ad_id": ad_data.get("id"),
        "brand": brand.get("name", "Unknown") if isinstance(brand, dict) else "Unknown",
        "title": ad_data.get("title", ""),
        "body": ad_data.get("body", ""),
        "score": ad_data.get("performance_score"),
        "score_title": ad_data.get("performance_score_title", ""),
        "days_active": ad_data.get("days_active"),
        "landing_page": ad_data.get("landing_page", ""),
        "platform": ad_data.get("platform", ""),
        "start_date": ad_data.get("start_date", ""),
        "cta_type": ad_data.get("cta_type", ""),
        "share_url": ad_data.get("share_url", ""),
        "video_length": None,
    }
    for m in ad_data.get("media", []) or []:
        if m.get("type") == "video" and m.get("video_length"):
            meta["video_length"] = m["video_length"]
            break
    return meta


def resolve(input_str: str, key: str) -> tuple[str, dict]:
    """Returns (video_url, metadata) for a GetHookd URL / ad id."""
    ad_id = extract_ad_id(input_str)
    if not ad_id:
        raise ProviderError(f"could not extract a GetHookd ad id from: {input_str[:120]}")
    ad = fetch_ad_metadata(ad_id, key)
    if not ad:
        raise ProviderError(
            f"could not fetch GetHookd ad {ad_id}; it may not be in the swipe file or brand spy")
    url = get_video_url(ad)
    if not url:
        raise ProviderError(f"GetHookd ad {ad_id} has no video media attached")
    return url, build_metadata(ad)
