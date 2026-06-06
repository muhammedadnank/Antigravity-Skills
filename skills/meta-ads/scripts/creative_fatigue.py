#!/usr/bin/env python3
"""Detect creative fatigue at the ad level.

Creative fatigue = an ad's CTR is decaying because the audience has
seen it too many times. Signals to look for:
- Frequency > 3.0 (rule of thumb; varies by objective)
- CTR in the second half of the period < 70% of CTR in the first half
- CPM rising while CTR falls (Meta penalizes low engagement with worse delivery)

This script splits the requested date range in half and compares the
two halves per ad. Output is sorted by fatigue severity.

Usage:
  python scripts/creative_fatigue.py --date-preset last_28d
  python scripts/creative_fatigue.py --since 2026-03-01 --until 2026-04-15 \\
    --frequency-threshold 2.5 --ctr-decay-threshold 0.7
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta

from meta_client import MetaAPIError, normalize_account_id, paginate, print_json


def date_split(since: date, until: date) -> tuple[tuple[date, date], tuple[date, date]]:
    """Split a date range into two equal halves. Returns (first_half, second_half)."""
    days = (until - since).days
    if days < 4:
        raise ValueError("Need at least 4 days of data to detect fatigue trend.")
    mid = since + timedelta(days=days // 2)
    return (since, mid), (mid + timedelta(days=1), until)


def resolve_dates(args) -> tuple[date, date]:
    if args.since and args.until:
        return (
            datetime.strptime(args.since, "%Y-%m-%d").date(),
            datetime.strptime(args.until, "%Y-%m-%d").date(),
        )
    today = date.today()
    presets = {
        "last_7d": 7,
        "last_14d": 14,
        "last_28d": 28,
        "last_30d": 30,
    }
    days = presets.get(args.date_preset, 28)
    until = today - timedelta(days=1)  # yesterday
    since = until - timedelta(days=days - 1)
    return since, until


def fetch_period_insights(account: str, since: date, until: date) -> dict:
    """Return {ad_id: row} for the given period at ad level."""
    params = {
        "level": "ad",
        "fields": ",".join(
            [
                "ad_id",
                "ad_name",
                "campaign_name",
                "adset_name",
                "spend",
                "impressions",
                "reach",
                "frequency",
                "clicks",
                "ctr",
                "cpm",
                "cpc",
            ]
        ),
        "time_range": f'{{"since":"{since.isoformat()}","until":"{until.isoformat()}"}}',
        "limit": 100,
    }
    out = {}
    for row in paginate(f"{account}/insights", params):
        ad_id = row.get("ad_id")
        if ad_id:
            out[ad_id] = row
    return out


def safe_float(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account-id", help="Ad account ID. Defaults to env.")
    parser.add_argument(
        "--date-preset",
        choices=["last_7d", "last_14d", "last_28d", "last_30d"],
        default="last_28d",
    )
    parser.add_argument("--since", help="Custom range start (YYYY-MM-DD).")
    parser.add_argument("--until", help="Custom range end (YYYY-MM-DD).")
    parser.add_argument(
        "--frequency-threshold",
        type=float,
        default=3.0,
        help="Flag ads with frequency above this in the second half. Default 3.0.",
    )
    parser.add_argument(
        "--ctr-decay-threshold",
        type=float,
        default=0.7,
        help="Flag ads where second-half CTR < first-half CTR * this. Default 0.7 (i.e. 30%% drop).",
    )
    parser.add_argument(
        "--min-spend",
        type=float,
        default=10.0,
        help="Ignore ads that spent less than this in the second half (noise floor). Default 10.",
    )
    args = parser.parse_args()

    account = normalize_account_id(args.account_id)

    try:
        since, until = resolve_dates(args)
        first_range, second_range = date_split(since, until)
    except ValueError as e:
        print_json({"ok": False, "error": str(e)})
        return 1

    try:
        first = fetch_period_insights(account, *first_range)
        second = fetch_period_insights(account, *second_range)
    except MetaAPIError as e:
        print_json({"ok": False, "error": str(e), "meta_error": e.body.get("error")})
        return 1

    fatigued = []
    healthy = []

    for ad_id, late in second.items():
        late_spend = safe_float(late.get("spend"))
        if late_spend < args.min_spend:
            continue

        early = first.get(ad_id)
        late_ctr = safe_float(late.get("ctr"))
        late_freq = safe_float(late.get("frequency"))
        late_cpm = safe_float(late.get("cpm"))

        early_ctr = safe_float(early.get("ctr")) if early else None
        early_cpm = safe_float(early.get("cpm")) if early else None

        ctr_decay_ratio = (late_ctr / early_ctr) if early_ctr else None
        cpm_change_ratio = (late_cpm / early_cpm) if early_cpm else None

        flags = []
        if late_freq >= args.frequency_threshold:
            flags.append(f"frequency={late_freq:.2f} >= {args.frequency_threshold}")
        if ctr_decay_ratio is not None and ctr_decay_ratio < args.ctr_decay_threshold:
            flags.append(
                f"CTR fell to {ctr_decay_ratio*100:.0f}% of first-half "
                f"({early_ctr:.3f} → {late_ctr:.3f})"
            )
        if cpm_change_ratio is not None and cpm_change_ratio > 1.2 and ctr_decay_ratio and ctr_decay_ratio < 1:
            flags.append(
                f"CPM rose {(cpm_change_ratio-1)*100:.0f}% while CTR fell "
                "(delivery quality penalty)"
            )

        record = {
            "ad_id": ad_id,
            "ad_name": late.get("ad_name"),
            "campaign_name": late.get("campaign_name"),
            "adset_name": late.get("adset_name"),
            "first_half": {
                "ctr": early_ctr,
                "cpm": early_cpm,
                "spend": safe_float(early.get("spend")) if early else 0,
            },
            "second_half": {
                "ctr": late_ctr,
                "cpm": late_cpm,
                "frequency": late_freq,
                "spend": late_spend,
            },
            "flags": flags,
            # Severity = how many flags fired, weighted by spend (more spend = more urgent)
            "severity_score": len(flags) * late_spend,
        }

        if flags:
            fatigued.append(record)
        else:
            healthy.append(record)

    fatigued.sort(key=lambda r: r["severity_score"], reverse=True)

    print_json(
        {
            "ok": True,
            "account_id": account,
            "first_half": {"since": first_range[0].isoformat(), "until": first_range[1].isoformat()},
            "second_half": {"since": second_range[0].isoformat(), "until": second_range[1].isoformat()},
            "thresholds": {
                "frequency": args.frequency_threshold,
                "ctr_decay_ratio": args.ctr_decay_threshold,
                "min_spend": args.min_spend,
            },
            "fatigued_count": len(fatigued),
            "healthy_count": len(healthy),
            "fatigued_ads": fatigued,
            "healthy_ads_summary": [
                {"ad_id": h["ad_id"], "ad_name": h["ad_name"], "ctr": h["second_half"]["ctr"]}
                for h in healthy[:20]
            ],
        }
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
