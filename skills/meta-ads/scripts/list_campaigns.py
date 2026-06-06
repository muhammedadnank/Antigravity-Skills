#!/usr/bin/env python3
"""List campaigns under an ad account.

Usage:
  python scripts/list_campaigns.py
  python scripts/list_campaigns.py --account-id act_123 --status ACTIVE
  python scripts/list_campaigns.py --status PAUSED ACTIVE
"""

from __future__ import annotations

import argparse
import json
import sys

from meta_client import MetaAPIError, normalize_account_id, paginate, print_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account-id", help="Ad account ID (act_xxx). Defaults to env.")
    parser.add_argument(
        "--status",
        nargs="+",
        choices=["ACTIVE", "PAUSED", "ARCHIVED"],
        default=["ACTIVE", "PAUSED"],
        help=(
            "Effective statuses to include. Default: ACTIVE PAUSED. "
            "Note: DELETED is NOT supported by Meta's campaigns endpoint "
            "(error 1815001). Use Ads Manager UI to see deleted campaigns."
        ),
    )
    parser.add_argument(
        "--limit", type=int, default=200, help="Max campaigns to return. Default 200."
    )
    args = parser.parse_args()

    account = normalize_account_id(args.account_id)

    fields = ",".join(
        [
            "id",
            "name",
            "objective",
            "status",
            "effective_status",
            "buying_type",
            "daily_budget",
            "lifetime_budget",
            "budget_remaining",
            "start_time",
            "stop_time",
            "created_time",
            "updated_time",
            "special_ad_categories",
        ]
    )

    params = {
        "fields": fields,
        "effective_status": json.dumps(args.status),  # Meta expects a JSON array string
        "limit": min(args.limit, 100),  # Meta's max per page
    }

    campaigns = []
    try:
        for c in paginate(f"{account}/campaigns", params):
            campaigns.append(c)
            if len(campaigns) >= args.limit:
                break
    except MetaAPIError as e:
        print_json({"ok": False, "error": str(e), "meta_error": e.body.get("error")})
        return 1

    # Convert budget fields from "minor units" (cents/agorot) to a friendly amount.
    # Meta returns daily_budget="5000" meaning 5000 minor units, i.e. ₪50.00 / $50.00.
    for c in campaigns:
        for k in ("daily_budget", "lifetime_budget", "budget_remaining"):
            if c.get(k):
                try:
                    c[f"{k}_major"] = int(c[k]) / 100
                except (ValueError, TypeError):
                    pass

    print_json({"ok": True, "account_id": account, "count": len(campaigns), "campaigns": campaigns})
    return 0


if __name__ == "__main__":
    sys.exit(main())
