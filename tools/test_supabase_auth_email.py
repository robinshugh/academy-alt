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
    email = (os.environ.get("SUPABASE_TEST_EMAIL") or "").strip()

    if not url or not key or not email:
        print("Missing SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, or SUPABASE_TEST_EMAIL.")
        return 2

    endpoint = f"{url}/auth/v1/otp"
    payload = {
        "email": email,
        "create_user": True,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            print("Supabase auth email request OK")
            print(f"Endpoint: {endpoint}")
            print(f"HTTP status: {response.status}")
            print(f"Recipient: {email}")
            if body.strip():
                print(body[:800])
            else:
                print("Response body: empty")
            return 0
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print("Supabase auth email request failed")
        print(f"Endpoint: {endpoint}")
        print(f"HTTP status: {error.code}")
        print(f"Reason: {error.reason}")
        print(body[:1000])
        return 1
    except urllib.error.URLError as error:
        print("Supabase auth email request failed")
        print(f"Endpoint: {endpoint}")
        print(f"Reason: {error.reason}")
        return 1


def normalize_url(value):
    value = value.strip().rstrip("/")
    if value and not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


if __name__ == "__main__":
    sys.exit(main())
