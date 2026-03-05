#!/usr/bin/env python3
"""Garmin health snapshot + basic alerts.

Reads Garmin Connect data via garth tokens (no API key).
Default token path: memory/garmin_tokens
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import garth


class GarminClient:
    def __init__(self) -> None:
        self.display_name: str | None = None

    def connect(self, tokens_dir: str) -> None:
        garth.resume(tokens_dir)
        profile = self._get("/userprofile-service/userprofile") or {}
        self.display_name = profile.get("displayName")

    def _get(self, endpoint: str) -> Any:
        try:
            return garth.connectapi(endpoint)
        except Exception:
            return None

    def get_with_display_name(self, endpoint_tmpl: str) -> Any:
        if self.display_name:
            return self._get(endpoint_tmpl.format(display_name=self.display_name))
        return None


def val(d: Any, *keys: str) -> Any:
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokens", default="memory/garmin_tokens")
    parser.add_argument("--date", default=str(date.today()))
    parser.add_argument("--activities", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    d = datetime.strptime(args.date, "%Y-%m-%d").date()
    ds = d.isoformat()
    week_ago = (d - timedelta(days=7)).isoformat()

    c = GarminClient()
    try:
        c.connect(args.tokens)
    except FileNotFoundError:
        print(
            "No Garmin tokens found. Run:\n"
            "  python3 scripts/garmin-login.py --tokens memory/garmin_tokens"
        )
        return 1

    daily = c.get_with_display_name(
        "/wellness-service/wellness/dailySummaryChart/{display_name}?date={date}"
        .replace("{date}", ds)
    ) or {}

    sleep = c.get_with_display_name(
        "/wellness-service/wellness/dailySleepData/{display_name}?date={date}".replace("{date}", ds)
    ) or {}

    hr = c.get_with_display_name(
        "/wellness-service/wellness/dailyHeartRate/{display_name}?date={date}".replace("{date}", ds)
    ) or {}

    stress = c.get_with_display_name(
        "/wellness-service/wellness/dailyStress/{display_name}?date={date}".replace("{date}", ds)
    ) or {}

    body_battery = c.get_with_display_name(
        "/wellness-service/wellness/dailyBodyBattery/{display_name}?date={date}".replace("{date}", ds)
    ) or {}

    pulse_ox = c.get_with_display_name(
        "/wellness-service/wellness/dailyPulseOx/{display_name}?date={date}".replace("{date}", ds)
    ) or {}

    hrv = c._get(f"/wellness-service/wellness/hrvData?fromDate={week_ago}&toDate={ds}") or {}

    activities = c._get(
        f"/activitylist-service/activities/search/activities?start=0&limit={args.activities}"
    ) or []

    # Normalize a compact output structure (keys may vary by account/device)
    out = {
        "date": ds,
        "profile": {"display_name": c.display_name},
        "sleep": {
            "score": val(sleep, "sleepScores", "overall", "value") or val(sleep, "dailySleepDTO", "sleepScore"),
            "duration_sec": val(sleep, "dailySleepDTO", "sleepTimeSeconds"),
            "deep_sec": val(sleep, "dailySleepDTO", "deepSleepSeconds"),
            "light_sec": val(sleep, "dailySleepDTO", "lightSleepSeconds"),
            "rem_sec": val(sleep, "dailySleepDTO", "remSleepSeconds"),
            "avg_hr": val(sleep, "dailySleepDTO", "averageRespiration") or val(sleep, "dailySleepDTO", "avgSleepHr"),
            "spo2_avg": val(sleep, "dailySleepDTO", "averageSpO2"),
            "stress_avg": val(sleep, "dailySleepDTO", "avgSleepStress"),
        },
        "heart_rate": {
            "resting": val(daily, "rhr") or val(hr, "restingHeartRate"),
            "min": val(hr, "heartRateValuesArray", 0, 1) if isinstance(val(hr, "heartRateValuesArray"), list) else None,
            "max": val(daily, "maxHeartRate") or val(hr, "maxHeartRate"),
        },
        "hrv": {
            "status": val(hrv, "status"),
            "last_night_avg": val(hrv, "lastNightAvg"),
            "weekly_avg": val(hrv, "weeklyAvg"),
        },
        "stress": {
            "avg": val(daily, "averageStressLevel") or val(stress, "avgStressLevel"),
            "max": val(daily, "maxStressLevel") or val(stress, "maxStressLevel"),
        },
        "steps": val(daily, "steps") or val(daily, "totalSteps"),
        "spo2": {
            "avg": val(pulse_ox, "averageSpO2"),
            "lowest": val(pulse_ox, "lowestSpO2"),
        },
        "body_battery": {
            "charged": val(body_battery, "chargedValue"),
            "drained": val(body_battery, "drainedValue"),
            "high": val(body_battery, "highValue"),
            "low": val(body_battery, "lowValue"),
        },
        "activities": activities if isinstance(activities, list) else activities.get("activities", []),
    }

    alerts: list[str] = []
    rhr = out["heart_rate"]["resting"]
    if isinstance(rhr, (int, float)) and rhr >= 65:
        alerts.append(f"Elevated resting HR: {rhr}")

    sleep_score = out["sleep"]["score"]
    if isinstance(sleep_score, (int, float)) and sleep_score < 60:
        alerts.append(f"Low sleep score: {sleep_score}")

    hrv_status = out["hrv"]["status"]
    if isinstance(hrv_status, str) and hrv_status.lower() in {"low", "unbalanced", "poor"}:
        alerts.append(f"HRV status: {hrv_status}")

    spo2_low = out["spo2"]["lowest"]
    if isinstance(spo2_low, (int, float)) and spo2_low < 92:
        alerts.append(f"Low SpO2: {spo2_low}%")

    out["alerts"] = alerts

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"Garmin health check — {ds}")
        print(f"Display name: {c.display_name or '-'}")
        print(f"Sleep score: {sleep_score}")
        print(f"Resting HR: {rhr}")
        print(f"HRV status: {hrv_status}")
        print(f"Steps: {out['steps']}")
        print(f"SpO2 avg/low: {out['spo2']['avg']} / {out['spo2']['lowest']}")
        print(f"Activities fetched: {len(out['activities']) if isinstance(out['activities'], list) else 0}")
        if alerts:
            print("Alerts:")
            for a in alerts:
                print(f"- {a}")
        else:
            print("Alerts: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
