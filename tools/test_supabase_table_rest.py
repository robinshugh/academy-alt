import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


TABLE = "connection_tests"


def main():
    url = normalize_url(os.environ.get("SUPABASE_URL", ""))
    key = (
        os.environ.get("SUPABASE_PUBLISHABLE_KEY")
        or os.environ.get("SUPABASE_ANON_KEY")
        or ""
    ).strip()

    if not url or not key:
        print("Missing SUPABASE_URL and/or SUPABASE_PUBLISHABLE_KEY.")
        return 2

    marker = f"academy-alt-{int(time.time())}"
    insert_ok, insert_status, insert_body = insert_row(url, key, marker)
    if not insert_ok:
        print("Supabase table insert failed")
        print(f"HTTP status/reason: {insert_status}")
        print(str(insert_body)[:1000])
        print(f"Expected table: public.{TABLE}")
        return 1

    read_ok, read_status, read_body = read_row(url, key, marker)
    if not read_ok:
        print("Supabase table read failed")
        print(f"HTTP status/reason: {read_status}")
        print(str(read_body)[:1000])
        return 1

    rows = json.loads(read_body)
    if not rows:
        print("Supabase table read returned no rows after insert.")
        return 1

    print("Supabase table insert/read OK")
    print(f"Table: public.{TABLE}")
    print(f"Marker: {marker}")
    print(f"Rows returned: {len(rows)}")
    return 0


def insert_row(url, key, marker):
    endpoint = f"{url}/rest/v1/{TABLE}"
    payload = {
        "source": "academy_alt_connection_test",
        "marker": marker,
        "payload": {"message": "Supabase REST insert/read test"},
    }
    return request(
        endpoint,
        key,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        extra_headers={
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )


def read_row(url, key, marker):
    query = urllib.parse.urlencode(
        {
            "select": "id,source,marker,created_at,payload",
            "marker": f"eq.{marker}",
            "limit": "1",
        }
    )
    endpoint = f"{url}/rest/v1/{TABLE}?{query}"
    return request(endpoint, key, method="GET")


def request(endpoint, key, method, data=None, extra_headers=None):
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    }
    headers.update(extra_headers or {})
    request = urllib.request.Request(endpoint, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            return True, response.status, body
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        return False, error.code, body
    except urllib.error.URLError as error:
        return False, "network error", error.reason


def normalize_url(value):
    value = value.strip().rstrip("/")
    if value and not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


if __name__ == "__main__":
    sys.exit(main())
