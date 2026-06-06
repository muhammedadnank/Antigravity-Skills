#!/usr/bin/env python3
"""Create a complete Meta ad campaign from a spec JSON.

Builds the full object tree in one shot:
  campaign -> ad sets -> creatives + ads

Why a script and not Ads Manager UI? Campaigns built from a spec are
reproducible, reviewable (dry-run), and rollback-able (every ID is
logged to a state file). Good for A/B testing flights, agency handoffs,
and any time you want the exact same structure twice.

Safety:
  - Refuses to write without either --dry-run or --confirm.
  - Defaults the created campaign, ad sets, and ads all to PAUSED so
    nothing delivers until you explicitly enable them in Ads Manager.
  - Every object created is recorded in the returned state JSON with
    its ID, so you can delete/pause everything if something went wrong.

Usage:
  python scripts/create_campaign.py --spec spec.json --dry-run
  python scripts/create_campaign.py --spec spec.json --confirm

See references/campaign-creation.md for the spec format.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from meta_client import (
    GRAPH_BASE,
    MetaAPIError,
    get,
    get_token,
    get_version,
    normalize_account_id,
    post,
    print_json,
)

# Currencies with no minor unit (Meta returns/accepts whole-unit amounts).
# Source: ISO 4217 zero-decimal list, aligned with Meta's docs.
ZERO_DECIMAL = {"JPY", "KRW", "VND", "ISK", "TWD", "XAF", "XOF", "CLP"}

DEFAULT_PLACEMENTS = {
    "publisher_platforms": ["instagram"],
    "instagram_positions": ["stream", "story", "reels"],
}

VALID_CTAS = {
    "LEARN_MORE", "SIGN_UP", "SHOP_NOW", "BOOK_TRAVEL", "DOWNLOAD",
    "GET_OFFER", "GET_QUOTE", "SUBSCRIBE", "CONTACT_US", "APPLY_NOW",
    "WATCH_MORE", "INSTALL_MOBILE_APP", "USE_APP", "MESSAGE_PAGE",
    "WHATSAPP_MESSAGE", "NO_BUTTON",
}


# ─── Helpers ───────────────────────────────────────────────────────────────
def get_account_currency(account_id: str) -> str:
    """Fetch the account's currency so we can do major→minor conversion correctly."""
    resp = get(account_id, {"fields": "currency"})
    return resp.get("currency", "USD")


def major_to_minor(amount_major: float, currency: str) -> int:
    """Convert 50.00 ILS → 5000 agorot. 1000 JPY → 1000."""
    if currency.upper() in ZERO_DECIMAL:
        return int(round(amount_major))
    return int(round(amount_major * 100))


def resolve_interest_ids(interest_names: list[str]) -> list[dict]:
    """Resolve interest names → {id, name} dicts via Meta's ad interest search.

    Keeps the first match per name. Names with no match are dropped and
    surfaced to the caller as an issue.
    """
    out = []
    seen = set()
    missing = []
    for name in interest_names:
        resp = get("search", {"type": "adinterest", "q": name, "limit": 3})
        hits = resp.get("data", [])
        if not hits:
            missing.append(name)
            continue
        top = hits[0]
        tid = top.get("id")
        if tid and tid not in seen:
            out.append({"id": tid, "name": top.get("name")})
            seen.add(tid)
    if missing:
        print(f"[warn] No interest match for: {missing}", file=sys.stderr)
    return out


def upload_image(account_id: str, image_path: Path) -> str:
    """POST image bytes to /act_.../adimages. Returns the hash Meta assigns."""
    import requests

    url = f"{GRAPH_BASE}/{get_version()}/{account_id}/adimages"
    with image_path.open("rb") as f:
        files = {image_path.name: (image_path.name, f, "image/png")}
        data = {"access_token": get_token()}
        resp = requests.post(url, data=data, files=files, timeout=120)
    if not resp.ok:
        raise RuntimeError(f"Image upload failed ({resp.status_code}): {resp.text[:500]}")
    body = resp.json()
    info = body.get("images", {}).get(image_path.name)
    if not info or not info.get("hash"):
        raise RuntimeError(f"No hash in upload response: {body}")
    return info["hash"]


def build_targeting(t: dict, resolved_interests: list[dict]) -> dict:
    out = {}

    # Geo
    geo = t.get("geo_locations")
    if not geo:
        countries = t.get("countries")
        if countries:
            geo = {"countries": countries}
    if geo:
        out["geo_locations"] = geo

    # Age/gender
    if "age_min" in t:
        out["age_min"] = int(t["age_min"])
    if "age_max" in t:
        out["age_max"] = int(t["age_max"])
    if "genders" in t:
        out["genders"] = t["genders"]

    # Interests via flexible_spec (AND of interest group + other criteria)
    if resolved_interests:
        out["flexible_spec"] = [
            {"interests": [{"id": i["id"], "name": i["name"]} for i in resolved_interests]}
        ]

    # Placements
    out["publisher_platforms"] = t.get("publisher_platforms", DEFAULT_PLACEMENTS["publisher_platforms"])
    if "instagram" in out["publisher_platforms"]:
        out["instagram_positions"] = t.get(
            "instagram_positions", DEFAULT_PLACEMENTS["instagram_positions"]
        )
    if "facebook" in out["publisher_platforms"]:
        out["facebook_positions"] = t.get("facebook_positions", ["feed", "story", "video_feeds"])

    # Advantage+ audience expansion (default ON)
    if t.get("advantage_audience", True):
        out["targeting_automation"] = {"advantage_audience": 1}

    # Custom audiences + excluded audiences (optional)
    if "custom_audiences" in t:
        out["custom_audiences"] = t["custom_audiences"]
    if "excluded_custom_audiences" in t:
        out["excluded_custom_audiences"] = t["excluded_custom_audiences"]

    return out


# ─── Validation ────────────────────────────────────────────────────────────
def validate_spec(spec: dict) -> list[str]:
    """Return a list of human-readable errors. Empty list = valid."""
    errs = []
    if not spec.get("campaign_name"):
        errs.append("campaign_name is required")
    if not spec.get("objective"):
        errs.append("objective is required (e.g. OUTCOME_TRAFFIC, OUTCOME_SALES, OUTCOME_ENGAGEMENT)")
    if not spec.get("landing_url") and spec.get("objective", "").startswith("OUTCOME_TRAFFIC"):
        errs.append("landing_url is required for traffic campaigns")
    identity = spec.get("identity", {})
    if not identity.get("page_id"):
        errs.append("identity.page_id is required")
    if not spec.get("ad_sets"):
        errs.append("at least one ad_set is required")

    for i, a in enumerate(spec.get("ad_sets", [])):
        prefix = f"ad_sets[{i}]"
        if not a.get("name"):
            errs.append(f"{prefix}.name is required")
        if "daily_budget" not in a and "lifetime_budget" not in a:
            errs.append(f"{prefix} needs daily_budget or lifetime_budget (in major units)")
        if not a.get("ads"):
            errs.append(f"{prefix}.ads must have at least one ad")
        # Image required unless image_hash is pre-supplied
        if not a.get("image_hash") and not a.get("image_path"):
            errs.append(f"{prefix} needs either image_path or image_hash")
        if a.get("image_path"):
            p = Path(a["image_path"]).expanduser()
            if not p.is_absolute():
                p = (Path.cwd() / p).resolve()
            if not p.exists():
                errs.append(f"{prefix}.image_path does not exist: {p}")
        for j, ad in enumerate(a.get("ads", [])):
            ap = f"{prefix}.ads[{j}]"
            for f in ("name", "message", "headline"):
                if not ad.get(f):
                    errs.append(f"{ap}.{f} is required")
            cta = ad.get("cta", "LEARN_MORE")
            if cta not in VALID_CTAS:
                errs.append(f"{ap}.cta '{cta}' is not a recognized CTA type")
    return errs


# ─── Planning (dry-run) ────────────────────────────────────────────────────
def plan(spec: dict, account_id: str) -> dict:
    currency = get_account_currency(account_id)
    out = {
        "account_id": account_id,
        "currency": currency,
        "campaign": {
            "name": spec["campaign_name"],
            "objective": spec["objective"],
            "status": spec.get("status", "PAUSED"),
            "special_ad_categories": spec.get("special_ad_categories", []),
        },
        "identity": spec["identity"],
        "landing_url": spec.get("landing_url"),
        "ad_sets": [],
    }
    total_daily_minor = 0
    total_ads = 0
    for a in spec["ad_sets"]:
        targeting = a.get("targeting", {})

        # Resolve interests now so the dry-run tells the user the real IDs
        interests = []
        if targeting.get("interest_ids"):
            interests = [{"id": i, "name": f"<preset:{i}>"} for i in targeting["interest_ids"]]
        elif targeting.get("interests"):
            interests = resolve_interest_ids(targeting["interests"])

        daily_minor = None
        if "daily_budget" in a:
            daily_minor = major_to_minor(a["daily_budget"], currency)
            total_daily_minor += daily_minor

        out["ad_sets"].append(
            {
                "name": a["name"],
                "daily_budget_major": a.get("daily_budget"),
                "daily_budget_minor": daily_minor,
                "lifetime_budget_major": a.get("lifetime_budget"),
                "billing_event": a.get("billing_event", "LINK_CLICKS"),
                "optimization_goal": a.get("optimization_goal", "LINK_CLICKS"),
                "targeting_summary": {
                    "countries": targeting.get("geo_locations", {}).get("countries")
                    or targeting.get("countries"),
                    "age_range": [targeting.get("age_min"), targeting.get("age_max")],
                    "resolved_interests": interests,
                    "placements": targeting.get(
                        "publisher_platforms", DEFAULT_PLACEMENTS["publisher_platforms"]
                    ),
                },
                "image": a.get("image_path") or f"<prehashed:{a.get('image_hash')}>",
                "ads": [
                    {
                        "name": ad["name"],
                        "headline": ad["headline"],
                        "message_preview": ad["message"].split("\n", 1)[0][:100] + " …",
                        "cta": ad.get("cta", "LEARN_MORE"),
                    }
                    for ad in a["ads"]
                ],
            }
        )
        total_ads += len(a["ads"])

    out["totals"] = {
        "ad_sets": len(spec["ad_sets"]),
        "ads": total_ads,
        "total_daily_budget_minor": total_daily_minor,
        "total_daily_budget_major": total_daily_minor / (1 if currency.upper() in ZERO_DECIMAL else 100),
    }
    return out


# ─── Execution (write) ─────────────────────────────────────────────────────
def execute(spec: dict, account_id: str) -> dict:
    currency = get_account_currency(account_id)
    state: dict = {
        "ok": True,
        "account_id": account_id,
        "currency": currency,
        "created_at": int(time.time()),
        "objects": [],
    }

    # 1. Campaign
    camp_data = {
        "name": spec["campaign_name"],
        "objective": spec["objective"],
        "status": spec.get("status", "PAUSED"),
        "special_ad_categories": json.dumps(spec.get("special_ad_categories", [])),
        "buying_type": spec.get("buying_type", "AUCTION"),
    }
    camp = post(f"{account_id}/campaigns", data=camp_data)
    campaign_id = camp["id"]
    state["campaign_id"] = campaign_id
    state["objects"].append({"type": "campaign", "id": campaign_id, "name": spec["campaign_name"]})
    print(f"[+] campaign: {campaign_id} — {spec['campaign_name']}", file=sys.stderr)

    page_id = spec["identity"]["page_id"]
    ig_user_id = spec["identity"].get("instagram_user_id")
    landing_url = spec.get("landing_url")

    out_ad_sets = []
    for a in spec["ad_sets"]:
        targeting_cfg = a.get("targeting", {})

        # Resolve interests
        if targeting_cfg.get("interest_ids"):
            interests = [{"id": i, "name": f"preset-{i}"} for i in targeting_cfg["interest_ids"]]
        elif targeting_cfg.get("interests"):
            interests = resolve_interest_ids(targeting_cfg["interests"])
        else:
            interests = []

        targeting = build_targeting(targeting_cfg, interests)

        # Image
        if a.get("image_hash"):
            image_hash = a["image_hash"]
        else:
            img_path = Path(a["image_path"]).expanduser()
            if not img_path.is_absolute():
                img_path = (Path.cwd() / img_path).resolve()
            image_hash = upload_image(account_id, img_path)
            state["objects"].append(
                {"type": "image", "hash": image_hash, "file": img_path.name}
            )
            print(f"[+] image: {img_path.name} -> {image_hash[:16]}…", file=sys.stderr)

        # Ad set
        adset_data = {
            "name": a["name"],
            "campaign_id": campaign_id,
            "billing_event": a.get("billing_event", "LINK_CLICKS"),
            "optimization_goal": a.get("optimization_goal", "LINK_CLICKS"),
            "bid_strategy": a.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
            "targeting": json.dumps(targeting),
            "status": a.get("status", "PAUSED"),
            "start_time": str(int(time.time()) + 3600),
        }
        if "daily_budget" in a:
            adset_data["daily_budget"] = str(major_to_minor(a["daily_budget"], currency))
        if "lifetime_budget" in a:
            adset_data["lifetime_budget"] = str(major_to_minor(a["lifetime_budget"], currency))
            adset_data["end_time"] = a["end_time"]
        if "bid_amount" in a:
            adset_data["bid_amount"] = str(major_to_minor(a["bid_amount"], currency))

        adset = post(f"{account_id}/adsets", data=adset_data)
        adset_id = adset["id"]
        state["objects"].append({"type": "adset", "id": adset_id, "name": a["name"]})
        print(f"[+] ad set: {adset_id} — {a['name']}", file=sys.stderr)

        ads_created = []
        for ad_cfg in a["ads"]:
            creative_spec = {
                "page_id": page_id,
                "link_data": {
                    "link": landing_url,
                    "message": ad_cfg["message"],
                    "name": ad_cfg["headline"],
                    "image_hash": image_hash,
                    "call_to_action": {
                        "type": ad_cfg.get("cta", "LEARN_MORE"),
                        "value": {"link": landing_url},
                    },
                },
            }
            if ad_cfg.get("description"):
                creative_spec["link_data"]["description"] = ad_cfg["description"]
            if ig_user_id:
                creative_spec["instagram_user_id"] = ig_user_id

            creative_payload = {
                "name": f"Creative_{ad_cfg['name']}",
                "object_story_spec": json.dumps(creative_spec),
            }
            # Opt-out of Meta auto-enhancements by default; enable via ad_cfg
            if not ad_cfg.get("standard_enhancements", False):
                creative_payload["degrees_of_freedom_spec"] = json.dumps(
                    {"creative_features_spec": {"standard_enhancements": {"enroll_status": "OPT_OUT"}}}
                )
            creative = post(f"{account_id}/adcreatives", data=creative_payload)
            creative_id = creative["id"]
            state["objects"].append(
                {"type": "creative", "id": creative_id, "name": f"Creative_{ad_cfg['name']}"}
            )

            ad = post(
                f"{account_id}/ads",
                data={
                    "name": f"Ad_{ad_cfg['name']}",
                    "adset_id": adset_id,
                    "creative": json.dumps({"creative_id": creative_id}),
                    "status": ad_cfg.get("status", "PAUSED"),
                },
            )
            ad_id = ad["id"]
            state["objects"].append({"type": "ad", "id": ad_id, "name": f"Ad_{ad_cfg['name']}"})
            ads_created.append({"ad_id": ad_id, "creative_id": creative_id, "name": ad_cfg["name"]})
            print(f"[+] ad: {ad_id} — {ad_cfg['name']}", file=sys.stderr)

        out_ad_sets.append(
            {"adset_id": adset_id, "image_hash": image_hash, "ads": ads_created}
        )

    state["ad_sets"] = out_ad_sets
    return state


# ─── Entry point ───────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Create a Meta ad campaign from a spec JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--spec", required=True, help="Path to campaign spec JSON")
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--dry-run", action="store_true", help="Plan only, no writes")
    grp.add_argument("--confirm", action="store_true", help="Actually create everything")
    parser.add_argument("--account-id", default=None, help="Override META_AD_ACCOUNT_ID")
    parser.add_argument(
        "--state-out",
        default=None,
        help="Where to write the state JSON (default: alongside spec with _state suffix)",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec).expanduser().resolve()
    if not spec_path.exists():
        print(f"spec not found: {spec_path}", file=sys.stderr)
        sys.exit(2)
    spec = json.loads(spec_path.read_text())

    errs = validate_spec(spec)
    if errs:
        print("Spec validation failed:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(2)

    account_id = normalize_account_id(args.account_id)

    if args.dry_run:
        try:
            p = plan(spec, account_id)
        except MetaAPIError as e:
            print_json({"ok": False, "error": str(e), "body": e.body})
            sys.exit(1)
        print_json(p)
        return

    # --confirm path
    state_file = Path(args.state_out) if args.state_out else spec_path.with_name(
        f"{spec_path.stem}_state_{int(time.time())}.json"
    )
    try:
        state = execute(spec, account_id)
    except Exception as e:
        state = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))
        print_json(state)
        raise
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    print(f"[state] -> {state_file}", file=sys.stderr)
    print_json(state)


if __name__ == "__main__":
    main()
