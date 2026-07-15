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

    endpoint = f"{url}/rest/v1/"
    request = urllib.request.Request(
        endpoint,
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Accept": "application/openapi+json, application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            print("Supabase connection OK")
            print(f"Endpoint: {endpoint}")
            print(f"HTTP status: {response.status}")
            print(f"Key prefix: {key[:14]}...")
            print_summary(body)
            return 0
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print("Supabase connection failed")
        print(f"Endpoint: {endpoint}")
        print(f"HTTP status: {error.code}")
        print(f"Reason: {error.reason}")
        print(body[:800])
        return 1
    except urllib.error.URLError as error:
        print("Supabase connection failed")
        print(f"Endpoint: {endpoint}")
        print(f"Reason: {error.reason}")
        return 1


def normalize_url(value):
    value = value.strip().rstrip("/")
    if value and not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def print_summary(body):
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        print(f"Response bytes: {len(body.encode('utf-8'))}")
        return

    title = payload.get("info", {}).get("title")
    version = payload.get("info", {}).get("version")
    paths = payload.get("paths", {})
    if title:
        print(f"API title: {title}")
    if version:
        print(f"API version: {version}")
    print(f"REST paths visible: {len(paths)}")


if __name__ == "__main__":
    sys.exit(main())
