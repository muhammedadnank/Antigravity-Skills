#!/usr/bin/env python3
"""Update an ad set's or campaign's daily/lifetime budget.

WRITE OPERATION. Read references/write-actions.md before invoking.

Hard rule baked into this script: a single call cannot increase the
budget by more than 100% (2x). For larger increases, run multiple calls.
This protects against runaway spending from a misread Claude analysis
and respects Meta's learning-phase reset behavior on big swings.

Daily budget vs lifetime budget: an object has one or the other, not
both. The script reads the current object first to figure out which
field to update.

Budget values are in MINOR units (cents/agorot). $50.00 = 5000.

Usage:
  # Set daily budget to ₪75
  python scripts/update_budget.py --object-id 12345 --major 75

  # Set in minor units directly
  python scripts/update_budget.py --object-id 12345 --minor 7500

  # Multiplicative change (1.5 = +50%)
  python scripts/update_budget.py --object-id 12345 --multiplier 1.5

  # Always dry-run first
  python scripts/update_budget.py --object-id 12345 --major 75 --dry-run
"""

from __future__ import annotations

import argparse
import sys

from meta_client import MetaAPIError, get, post, print_json


MAX_MULTIPLIER_PER_CALL = 2.0  # Hard cap on a single budget increase.


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--object-id", required=True, help="Campaign or ad set ID.")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--major", type=float, help="New budget in major units (e.g., 75 for ₪75.00).")
    g.add_argument("--minor", type=int, help="New budget in minor units (e.g., 7500 for ₪75.00).")
    g.add_argument(
        "--multiplier",
        type=float,
        help="Multiply current budget by this factor. e.g. 1.5 = +50%%, 0.5 = -50%%.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would change, don't call API.")
    parser.add_argument(
        "--allow-large-increase",
        action="store_true",
        help=(
            f"Override the {MAX_MULTIPLIER_PER_CALL}x safety cap on increases. "
            "Use only with explicit user confirmation."
        ),
    )
    args = parser.parse_args()

    try:
        current = get(
            args.object_id,
            params={"fields": "id,name,daily_budget,lifetime_budget,status"},
        )
    except MetaAPIError as e:
        print_json({"ok": False, "stage": "fetch_current", "error": str(e), "meta_error": e.body.get("error")})
        return 1

    daily = current.get("daily_budget")
    lifetime = current.get("lifetime_budget")
    if daily and not lifetime:
        budget_field = "daily_budget"
        current_minor = int(daily)
    elif lifetime and not daily:
        budget_field = "lifetime_budget"
        current_minor = int(lifetime)
    else:
        print_json(
            {
                "ok": False,
                "stage": "identify_budget_field",
                "error": "Object has neither daily nor lifetime budget set, or has both. Cannot infer which to update.",
                "current": current,
            }
        )
        return 1

    # Compute target.
    if args.major is not None:
        target_minor = int(round(args.major * 100))
    elif args.minor is not None:
        target_minor = args.minor
    else:
        target_minor = int(round(current_minor * args.multiplier))

    multiplier = target_minor / current_minor if current_minor else float("inf")

    if multiplier > MAX_MULTIPLIER_PER_CALL and not args.allow_large_increase:
        print_json(
            {
                "ok": False,
                "stage": "safety_check",
                "error": (
                    f"Refusing to multiply budget by {multiplier:.2f}x in a single call "
                    f"(cap is {MAX_MULTIPLIER_PER_CALL}x). Pass --allow-large-increase "
                    "after explicit user confirmation, or step up gradually."
                ),
                "current_minor": current_minor,
                "target_minor": target_minor,
                "multiplier": multiplier,
            }
        )
        return 1

    if args.dry_run:
        print_json(
            {
                "ok": True,
                "dry_run": True,
                "object_id": args.object_id,
                "name": current.get("name"),
                "budget_field": budget_field,
                "current_minor": current_minor,
                "current_major": current_minor / 100,
                "target_minor": target_minor,
                "target_major": target_minor / 100,
                "multiplier": round(multiplier, 3),
            }
        )
        return 0

    try:
        result = post(args.object_id, data={budget_field: target_minor})
    except MetaAPIError as e:
        print_json({"ok": False, "stage": "update_budget", "error": str(e), "meta_error": e.body.get("error")})
        return 1

    # Re-fetch to confirm.
    try:
        after = get(args.object_id, params={"fields": f"id,name,{budget_field}"})
    except MetaAPIError:
        after = {}

    print_json(
        {
            "ok": True,
            "object_id": args.object_id,
            "name": current.get("name"),
            "budget_field": budget_field,
            "before_minor": current_minor,
            "before_major": current_minor / 100,
            "after_minor": int(after.get(budget_field, target_minor)),
            "after_major": int(after.get(budget_field, target_minor)) / 100,
            "multiplier": round(multiplier, 3),
            "warning": (
                "Budget changes >20% may reset Meta's learning phase. "
                "Expect 3-7 days of unstable performance."
            )
            if abs(multiplier - 1) >= 0.2
            else None,
        }
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
