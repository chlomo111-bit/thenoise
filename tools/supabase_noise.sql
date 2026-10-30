-- The Noise : tables séparées (préfixe noise_), aucune table de la ruche n'est modifiée.
-- Le mot de passe admin est le même que celui de l'admin de la ruche (table admin_secret existante).

create table if not exists public.noise_people (
  handle      text primary key,
  role        text not null default 'public' check (role in ('public','judge','contestant')),
  status      text not null default 'active',
  song        text,
  chair       int,
  votes       int not null default 0,
  sort        int not null default 0,
  created_at  timestamptz not null default now()
);

create table if not exists public.noise_state (
  key   text primary key,
  value jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.noise_people enable row level security;
alter table public.noise_state  enable row level security;
drop policy if exists noise_people_read on public.noise_people;
create policy noise_people_read on public.noise_people for select to anon, authenticated using (true);
drop policy if exists noise_state_read on public.noise_state;
create policy noise_state_read on public.noise_state for select to anon, authenticated using (true);

-- items: [{"handle":"x","role":"contestant","status":"casting","song":"...","chair":1,"votes":3,"sort":2,"remove":false}]
create or replace function public.noise_admin_upsert(pass text, items jsonb)
returns int language plpgsql security definer set search_path = public, extensions as $$
declare it jsonb; n int := 0; h text;
begin
  if not exists (select 1 from admin_secret where pass_hash = crypt(pass, pass_hash)) then
    raise exception 'bad password';
  end if;
  for it in select * from jsonb_array_elements(items) loop
    h := lower(regexp_replace(trim(it->>'handle'), '^@', ''));
    if h is null or h = '' then continue; end if;
    if coalesce((it->>'remove')::boolean, false) then
      delete from noise_people where handle = h;
    else
      insert into noise_people(handle, role, status, song, chair, votes, sort)
      values (h, coalesce(it->>'role','public'), coalesce(it->>'status','active'), it->>'song',
              (it->>'chair')::int, coalesce((it->>'votes')::int,0), coalesce((it->>'sort')::int,0))
      on conflict (handle) do update set
        role   = coalesce(it->>'role',   noise_people.role),
        status = coalesce(it->>'status', noise_people.status),
        song   = coalesce(it->>'song',   noise_people.song),
        chair  = coalesce((it->>'chair')::int, noise_people.chair),
        votes  = coalesce((it->>'votes')::int, noise_people.votes),
        sort   = coalesce((it->>'sort')::int,  noise_people.sort);
    end if;
    n := n + 1;
  end loop;
  return n;
end $$;

create or replace function public.noise_admin_set_state(pass text, k text, v jsonb)
returns void language plpgsql security definer set search_path = public, extensions as $$
begin
  if not exists (select 1 from admin_secret where pass_hash = crypt(pass, pass_hash)) then
    raise exception 'bad password';
  end if;
  insert into noise_state(key, value, updated_at) values (k, v, now())
  on conflict (key) do update set value = excluded.value, updated_at = now();
end $$;

grant select on public.noise_people, public.noise_state to anon, authenticated;
grant execute on function public.noise_admin_upsert(text, jsonb) to anon, authenticated;
grant execute on function public.noise_admin_set_state(text, text, jsonb) to anon, authenticated;

insert into public.noise_state(key, value) values
  ('phase', '"teaser"'::jsonb),
  ('news',  '{"title":"ברוכים הבאים ל-The Noise!","body":"התוכנית הכי מזייפת באינסטגרם מתחילה. עקבו אחרי @the_noise_2026 ותפסו מקום בקהל."}'::jsonb)
on conflict (key) do nothing;

-- 29.10.2026 : réactions (applaudissements / tomates) + score pour la première rangée
alter table public.noise_people add column if not exists score int not null default 0;
create table if not exists public.noise_reactions (day date not null, kind text not null check (kind in ('clap','tomato')), n bigint not null default 0, primary key (day, kind));
-- + fonction noise_react(k text, cnt int) security definer (max 30 par appel)
-- tables privées de la routine : noise_ig_seen, noise_ig_welcomed

-- 30.10.2026 : inscription depuis le site (fenêtre « מה ה־@ שלכם? » à la première visite)
alter table public.noise_people add column if not exists src text;  -- 'site' = inscrit via le site
-- noise_join(h text) security definer : valide le @ (^[a-z0-9._]{1,30}$), crée la ligne noise_people (src='site') si absente,
-- max 40 inscriptions site / 10 min ; côté navigateur max 3 inscriptions par appareil. Retour {ok, handle, existed} ou {ok:false, err}.
