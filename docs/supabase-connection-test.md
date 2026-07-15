# Supabase Connection Test

This test only confirms that this machine can reach a Supabase project and that the publishable/anon key is accepted by the REST API.

Do not use the `service_role` key or any `sb_secret_...` key for this browser/prototype test.

## Values Needed

From the Supabase dashboard:

- `SUPABASE_URL`: your project URL, usually `https://<project-ref>.supabase.co`
- `SUPABASE_PUBLISHABLE_KEY`: the low-privilege publishable key

Legacy projects may show this as the `anon` public key. That is also acceptable for this test.

## Run In PowerShell

```powershell
$env:SUPABASE_URL="https://your-project-ref.supabase.co"
$env:SUPABASE_PUBLISHABLE_KEY="sb_publishable_your_key_here"
python -B tools\test_supabase_connection.py
```

Expected success:

```text
Supabase connection OK
HTTP status: 200
```

## What This Does Not Test Yet

- user login
- table insert/read
- row-level security policies
- parent/student permissions

Those come after the basic project/key connection works.
