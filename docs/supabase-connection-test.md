# Supabase Connection Test

This test only confirms that this machine can reach a Supabase project and that the publishable/anon key is accepted by Supabase Auth.

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
Auth health: OK (200)
Auth settings: OK (200)
Supabase connection OK
```

## What This Does Not Test Yet

- user login
- table insert/read
- row-level security policies
- parent/student permissions

Those come after the basic project/key connection works.

## Email Send Smoke Test

This sends a Supabase Auth OTP/magic-link email. It is only a connectivity test for Supabase email delivery, not the final parent activity alert implementation.

```powershell
$env:SUPABASE_TEST_EMAIL="robin.shu@gmail.com"
python -B tools\test_supabase_auth_email.py
```

## REST Insert/Read Smoke Test

First run `supabase/connection_tests.sql` in the Supabase SQL Editor. It creates a tiny `connection_tests` table and permissive test-only RLS policies for rows whose source is `academy_alt_connection_test`.

Then run:

```powershell
python -B tools\test_supabase_table_rest.py
```
