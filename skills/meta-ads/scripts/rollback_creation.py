#!/usr/bin/env python3
"""Roll back a campaign created by create_campaign.py.

Reads a `<spec>_state_<timestamp>.json` file produced by create_campaign.py
and either:
  - Pauses every object (soft rollback, reversible), or
  - Deletes every object in reverse creation order (hard rollback).

Deleting is permanent and shouldn't be the default. Use pause unless you
specifically want the objects gone.

Usage:
  python scripts/rollback_creation.py --state state.json --dry-run
  python scripts/rollback_creation.py --state state.json --pause
  python scripts/rollback_creation.py --state state.json --delete
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from meta_client import MetaAPIError, delete, post, print_json


def pause_object(object_id: str) -> dict:
    return post(object_id, data={"status": "PAUSED"})


def delete_object(object_id: str) -> dict:
    return delete(object_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, help="Path to state JSON from create_campaign.py")
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--dry-run", action="store_true", help="Show what would be acted on")
    grp.add_argument("--pause", action="store_true", help="Set status=PAUSED on every object")
    grp.add_argument("--delete", action="store_true", help="Permanently delete every object (ads → adsets → campaign)")
    args = parser.parse_args()

    state = json.loads(Path(args.state).read_text())
    # Reverse order so children are touched before parents (mainly for delete)
    objs = list(reversed(state.get("objects", [])))

    if args.dry_run:
        print_json({"would_act_on": objs})
        return

    results = []
    action = "pause" if args.pause else "delete"
    for o in objs:
        # Images don't have an individually-deletable endpoint via the same
        # pattern; skip them. Creatives get deleted if the ad using them is gone.
        if o["type"] == "image":
            continue
        try:
            if args.pause:
                # Only campaigns / ad sets / ads have status=PAUSED. Creatives don't.
                if o["type"] in ("campaign", "adset", "ad"):
                    pause_object(o["id"])
                    results.append({"id": o["id"], "type": o["type"], "action": "paused"})
                else:
                    results.append({"id": o["id"], "type": o["type"], "action": "skipped (no status)"})
            else:
                delete_object(o["id"])
                results.append({"id": o["id"], "type": o["type"], "action": "deleted"})
        except MetaAPIError as e:
            results.append({"id": o["id"], "type": o["type"], "error": str(e)})

    print_json({"action": action, "results": results})


if __name__ == "__main__":
    main()
