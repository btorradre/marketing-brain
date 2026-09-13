#!/usr/bin/env python3
"""Append a concept to the Net New Concepts tab of the Velantra Creative Tracker.

Run this every time a new concept is agreed on in conversation:

  python3 push_concept.py \
    --product "Weekender" \
    --concept "Airport outfit check" \
    --angle "POV outfit-check at the gate" \
    --thesis "Outfit-check format is trend-native and the bag reads as the hero accessory" \
    --format video --type net-new --source "convo 2026-08-08" [--notes "..."]
"""
import argparse
from datetime import date

from sheets_common import sheet_id, sheets_service


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--product", required=True)
    p.add_argument("--concept", required=True)
    p.add_argument("--angle", required=True)
    p.add_argument("--thesis", required=True)
    p.add_argument("--format", required=True, choices=["video", "image", "dynamic"])
    p.add_argument("--type", default="net-new", choices=["net-new", "iteration"])
    p.add_argument("--source", default="convo")
    p.add_argument("--status", default="idea")
    p.add_argument("--notes", default="")
    a = p.parse_args()

    row = [date.today().isoformat(), a.product, a.concept, a.angle, a.thesis,
           a.format.capitalize(), a.type, a.source, a.status, "", a.notes]
    sheets_service().spreadsheets().values().append(
        spreadsheetId=sheet_id(), range="Net New Concepts!A:K",
        valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS",
        body={"values": [row]}).execute()
    print(f"Pushed: {a.product} / {a.concept}")


if __name__ == "__main__":
    main()
