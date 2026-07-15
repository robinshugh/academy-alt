import json
import os
import sys
import urllib.error
import urllib.request


def main():
    url = normalize_url(os.environ.get("SUPABASE_URL", ""))
    key = (
        os.environ.get("SUPABASE_PUBLISHABLE_KEY")
        or os.environ.get("SUPABASE_ANON_KEY")
        or ""
    ).strip()

    if not url or not key:
        print("Missing SUPABASE_URL and/or SUPABASE_PUBLISHABLE_KEY.")
        print("Set them in the current shell, then rerun this script.")
        return 2

    checks = [
        ("Auth health", f"{url}/auth/v1/health", False),
        ("Auth settings", f"{url}/auth/v1/settings", True),
    ]

    for label, endpoint, require_json_summary in checks:
        ok, status, body_or_reason = request_json(endpoint, key)
        if not ok:
            print("Supabase connection failed")
            print(f"Check: {label}")
            print(f"Endpoint: {endpoint}")
            print(f"HTTP status/reason: {status}")
            print(str(body_or_reason)[:800])
            return 1

        print(f"{label}: OK ({status})")
        if require_json_summary:
            print_summary(body_or_reason)

    print("Supabase connection OK")
    print(f"Project URL: {url}")
    print(f"Key prefix: {key[:14]}...")
    return 0


def normalize_url(value):
    value = value.strip().rstrip("/")
    if value and not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def request_json(endpoint, key):
    request = urllib.request.Request(
        endpoint,
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            return True, response.status, body
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return False, error.code, body
    except urllib.error.URLError as error:
        return False, "network error", error.reason


def print_summary(body):
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        print(f"Response bytes: {len(body.encode('utf-8'))}")
        return

    external = payload.get("external", {})
    if external:
        enabled = sorted(provider for provider, active in external.items() if active)
        print(f"Auth providers enabled: {', '.join(enabled) if enabled else 'none'}")
    if "disable_signup" in payload:
        print(f"Signup disabled: {payload['disable_signup']}")


if __name__ == "__main__":
    sys.exit(main())
