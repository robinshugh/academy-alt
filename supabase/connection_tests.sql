create table if not exists public.connection_tests (
  id uuid primary key default gen_random_uuid(),
  source text not null,
  marker text not null unique,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

alter table public.connection_tests enable row level security;

drop policy if exists "connection_tests_insert_from_anon" on public.connection_tests;
create policy "connection_tests_insert_from_anon"
on public.connection_tests
for insert
to anon
with check (source = 'academy_alt_connection_test');

drop policy if exists "connection_tests_select_from_anon" on public.connection_tests;
create policy "connection_tests_select_from_anon"
on public.connection_tests
for select
to anon
using (source = 'academy_alt_connection_test');
