#!/usr/bin/env python3
"""Detect anomalies by comparing the current period to the prior equivalent.

For example, last 7 days vs the 7 days before that. Flags significant
changes in spend, CTR, CPM, CPC, and ROAS at the campaign level.

The threshold for "significant" is configurable. By default, a metric
must change by >= 25% AND the absolute change must matter (e.g. spend
must move at least $X in either direction). This avoids screaming about
a campaign that went from $0.50 to $0.75 spend.

Usage:
  python scripts/anomaly_detect.py --window-days 7
  python scripts/anomaly_detect.py --window-days 14 --pct-threshold 0.30
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta

from meta_client import MetaAPIError, normalize_account_id, paginate, print_json


def fetch_window(account: str, since: date, until: date) -> dict:
    params = {
        "level": "campaign",
        "fields": ",".join(
            [
                "campaign_id",
                "campaign_name",
                "spend",
                "impressions",
                "clicks",
                "ctr",
                "cpm",
                "cpc",
                "purchase_roas",
                "actions",
            ]
        ),
        "time_range": f'{{"since":"{since.isoformat()}","until":"{until.isoformat()}"}}',
        "limit": 100,
    }
    return {row["campaign_id"]: row for row in paginate(f"{account}/insights", params) if "campaign_id" in row}


def safe_float(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def extract_purchase_roas(row) -> float:
    """purchase_roas is a list like [{"action_type":"omni_purchase","value":"3.4"}]."""
    roas_list = row.get("purchase_roas") or []
    for r in roas_list:
        if r.get("action_type") in ("omni_purchase", "purchase"):
            return safe_float(r.get("value"))
    return 0.0


def pct_change(current: float, prior: float) -> float | None:
    """Return the percent change as a fraction (0.5 = +50%). None if undefined."""
    if prior == 0:
        return None if current == 0 else float("inf")
    return (current - prior) / prior


def classify_change(metric: str, change: float | None, current: float, prior: float, abs_floor: dict) -> dict | None:
    """Return an anomaly dict if this change is worth flagging, else None."""
    if change is None or change == 0:
        return None
    floor = abs_floor.get(metric, 0)
    if abs(current - prior) < floor:
        return None
    return {
        "metric": metric,
        "prior": prior,
        "current": current,
        "abs_change": current - prior,
        "pct_change": change,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account-id", help="Ad account ID. Defaults to env.")
    parser.add_argument(
        "--window-days", type=int, default=7, help="Length of comparison window in days. Default 7."
    )
    parser.add_argument(
        "--pct-threshold",
        type=float,
        default=0.25,
        help="Minimum percent change to flag (0.25 = 25%%). Default 0.25.",
    )
    parser.add_argument(
        "--min-spend",
        type=float,
        default=10.0,
        help="Skip campaigns with less than this spend in either window. Default 10.",
    )
    args = parser.parse_args()

    account = normalize_account_id(args.account_id)

    today = date.today()
    current_until = today - timedelta(days=1)  # yesterday
    current_since = current_until - timedelta(days=args.window_days - 1)
    prior_until = current_since - timedelta(days=1)
    prior_since = prior_until - timedelta(days=args.window_days - 1)

    try:
        current = fetch_window(account, current_since, current_until)
        prior = fetch_window(account, prior_since, prior_until)
    except MetaAPIError as e:
        print_json({"ok": False, "error": str(e), "meta_error": e.body.get("error")})
        return 1

    # Floors for "absolute change worth caring about" so we don't alert on noise.
    abs_floor = {
        "spend": args.min_spend / 2,  # at least half the min-spend in absolute movement
        "ctr": 0.005,  # 0.5 percentage points
        "cpm": 1.0,  # $1 CPM swing
        "cpc": 0.10,
        "purchase_roas": 0.3,
    }

    anomalies = []
    all_campaign_ids = set(current.keys()) | set(prior.keys())

    for cid in all_campaign_ids:
        c_row = current.get(cid, {})
        p_row = prior.get(cid, {})
        c_spend = safe_float(c_row.get("spend"))
        p_spend = safe_float(p_row.get("spend"))

        if c_spend < args.min_spend and p_spend < args.min_spend:
            continue

        flags: list[dict] = []

        for metric, get_value in [
            ("spend", lambda r: safe_float(r.get("spend"))),
            ("ctr", lambda r: safe_float(r.get("ctr"))),
            ("cpm", lambda r: safe_float(r.get("cpm"))),
            ("cpc", lambda r: safe_float(r.get("cpc"))),
            ("purchase_roas", extract_purchase_roas),
        ]:
            cv = get_value(c_row)
            pv = get_value(p_row)
            change = pct_change(cv, pv)
            if change is None:
                continue
            if change != float("inf") and abs(change) < args.pct_threshold:
                continue
            classified = classify_change(metric, change, cv, pv, abs_floor)
            if classified:
                flags.append(classified)

        if not flags:
            continue

        # Check for "campaign disappeared" or "new campaign appeared" cases.
        if c_spend == 0 and p_spend > 0:
            status = "stopped_spending"
        elif p_spend == 0 and c_spend > 0:
            status = "started_spending"
        else:
            status = "active_change"

        anomalies.append(
            {
                "campaign_id": cid,
                "campaign_name": c_row.get("campaign_name") or p_row.get("campaign_name"),
                "status": status,
                "current_spend": c_spend,
                "prior_spend": p_spend,
                "anomalies": flags,
                # severity = number of metrics flagged, weighted by total spend
                "severity_score": len(flags) * (c_spend + p_spend),
            }
        )

    anomalies.sort(key=lambda a: a["severity_score"], reverse=True)

    print_json(
        {
            "ok": True,
            "account_id": account,
            "current_window": {
                "since": current_since.isoformat(),
                "until": current_until.isoformat(),
            },
            "prior_window": {
                "since": prior_since.isoformat(),
                "until": prior_until.isoformat(),
            },
            "thresholds": {
                "pct_change": args.pct_threshold,
                "min_spend": args.min_spend,
            },
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
        }
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
