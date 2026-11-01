-- The Noise v3 (01/11/2026) : parrainage, bonus de série, auditions en avant-première, jeu des masques.

-- ---------- parrainage : +50 🎟️ au parrain par ami arrivé avec son lien (max 10/jour) ----------
create table if not exists public.noise_refs (
  friend     text primary key,
  referrer   text not null,
  day        date not null default noise_today(),
  created_at timestamptz not null default now()
);
alter table public.noise_refs enable row level security;
drop policy if exists noise_refs_read on public.noise_refs;
create policy noise_refs_read on public.noise_refs for select to anon, authenticated using (true);
grant select on public.noise_refs to anon, authenticated;

create or replace function public.noise_join(h text, ref text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare r jsonb; x text; rf text := lower(regexp_replace(trim(coalesce(ref,'')), '^@', '')); dd date := noise_today(); n int;
begin
  r := noise_join(h);
  if not coalesce((r->>'ok')::boolean, false) or coalesce((r->>'existed')::boolean, true) then return r; end if;
  x := r->>'handle';
  if rf = '' or rf = x or not exists (select 1 from noise_people where handle = rf) then return r; end if;
  select count(*) into n from noise_refs where referrer = rf and day = dd;
  insert into noise_refs(friend, referrer) values (x, rf) on conflict do nothing;
  if n < 10 then
    insert into noise_tickets(day, handle) values (dd, rf) on conflict do nothing;
    update noise_tickets set tickets = tickets + 50, updated_at = now() where day = dd and handle = rf;
    update noise_people set score = coalesce(score,0) + 3 where handle = rf;
  end if;
  return r || jsonb_build_object('ref', rf);
end $$;
grant execute on function public.noise_join(text, text) to anon, authenticated;

-- ---------- bonus de série de connexions (1re visite du jour) ----------
create or replace function public.noise_visit(h text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); dd date := noise_today(); p noise_players; was boolean; bonus int := 0;
begin
  if not exists (select 1 from noise_people where handle = hh) then raise exception 'not_in_audience'; end if;
  insert into noise_players(handle) values (hh) on conflict do nothing;
  select * into p from noise_players where handle = hh for update;
  if p.last_day is distinct from dd then
    p.streak := case when p.last_day = dd - 1 then p.streak + 1 else 1 end;
    update noise_players set streak = p.streak, best_streak = greatest(best_streak, p.streak), last_day = dd where handle = hh;
  end if;
  insert into noise_tickets(day, handle) values (dd, hh) on conflict do nothing;
  select visited into was from noise_tickets where day = dd and handle = hh for update;
  if not was then
    bonus := least(greatest(p.streak - 1, 0) * 10, 100);   -- jour 1 : 0 · jour 2 : +10 … jour 11+ : +100
    update noise_tickets set visited = true, tickets = tickets + 10 + bonus, updated_at = now() where day = dd and handle = hh;
  end if;
  return noise_me(hh, noise_sync(hh, dd)) || jsonb_build_object('streak_bonus', bonus, 'first_visit', not was);
end $$;

-- ---------- auditions en avant-première : 1 candidat par jour, vote ✅/❌ (1 vote / joueur / jour, +5 🎟️) ----------
create table if not exists public.noise_aud_votes (
  day        date not null,
  voter      text not null,
  candidate  text not null,
  vote       text not null check (vote in ('yes','no')),
  created_at timestamptz not null default now(),
  primary key (day, voter)
);
alter table public.noise_aud_votes enable row level security;

create or replace function public.noise_aud_live(d date default null) returns jsonb
language sql stable security definer set search_path = public as $$
  select jsonb_build_object(
    'aud', (select value from noise_state where key = 'audition'),
    'yes', (select count(*) from noise_aud_votes where day = coalesce(d, noise_today()) and vote = 'yes'),
    'no',  (select count(*) from noise_aud_votes where day = coalesce(d, noise_today()) and vote = 'no'));
$$;

create or replace function public.noise_aud_vote(h text, v text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); dd date := noise_today(); a jsonb; c text;
begin
  if v not in ('yes','no') then return jsonb_build_object('ok',false,'err','bad'); end if;
  if not exists (select 1 from noise_people where handle = hh) then return jsonb_build_object('ok',false,'err','not_in_audience'); end if;
  select value into a from noise_state where key = 'audition';
  if a is null or (a->>'day')::date is distinct from dd then return jsonb_build_object('ok',false,'err','closed'); end if;
  c := a->>'handle';
  if c = hh then return jsonb_build_object('ok',false,'err','self'); end if;
  insert into noise_aud_votes(day, voter, candidate, vote) values (dd, hh, c, v) on conflict do nothing;
  if not found then return jsonb_build_object('ok',false,'err','already') || noise_aud_live(dd); end if;
  insert into noise_tickets(day, handle) values (dd, hh) on conflict do nothing;
  update noise_tickets set tickets = tickets + 5, updated_at = now() where day = dd and handle = hh;
  return jsonb_build_object('ok',true) || noise_aud_live(dd);
end $$;

-- ---------- jeu des masques : deviner qui chante sous le masque (1 essai / jour, +30 🎟️ si juste, révélé par l'automatisation) ----------
create table if not exists public.noise_mask_answer (day date primary key, answer text not null, revealed boolean not null default false);
alter table public.noise_mask_answer enable row level security;   -- aucune lecture publique
create table if not exists public.noise_mask_guesses (
  day date not null, handle text not null, guess text not null, created_at timestamptz not null default now(),
  primary key (day, handle));
alter table public.noise_mask_guesses enable row level security;

create or replace function public.noise_mask_guess(h text, g text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); dd date := noise_today(); m jsonb; gg text := lower(regexp_replace(trim(coalesce(g,'')), '^@', ''));
begin
  if not exists (select 1 from noise_people where handle = hh) then return jsonb_build_object('ok',false,'err','not_in_audience'); end if;
  select value into m from noise_state where key = 'mask';
  if m is null or (m->>'day')::date is distinct from dd or not (m->'options' ? gg) then return jsonb_build_object('ok',false,'err','closed'); end if;
  insert into noise_mask_guesses(day, handle, guess) values (dd, hh, gg) on conflict do nothing;
  if not found then return jsonb_build_object('ok',false,'err','already'); end if;
  return jsonb_build_object('ok',true,'n',(select count(*) from noise_mask_guesses where day = dd));
end $$;

create or replace function public.noise_mask_count(d date default null) returns int
language sql stable security definer set search_path = public as $$
  select count(*)::int from noise_mask_guesses where day = coalesce(d, noise_today());
$$;

-- révélation (automatisation uniquement) : +30 🎟️ aux bons devineurs
create or replace function public.noise_mask_reveal(d date default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare dd date := coalesce(d, noise_today()); a noise_mask_answer; w text[];
begin
  select * into a from noise_mask_answer where day = dd;
  if not found then return jsonb_build_object('ok',false); end if;
  select coalesce(array_agg(handle), '{}') into w from noise_mask_guesses where day = dd and guess = a.answer;
  if not a.revealed then
    insert into noise_tickets(day, handle) select dd, x from unnest(w) x on conflict do nothing;
    update noise_tickets set tickets = tickets + 30, updated_at = now() where day = dd and handle = any(w);
    update noise_mask_answer set revealed = true where day = dd;
    update noise_state set value = value || jsonb_build_object('revealed', a.answer, 'winners', to_jsonb(w)) where key = 'mask';
  end if;
  return jsonb_build_object('ok',true,'answer',a.answer,'winners',to_jsonb(w),'n',(select count(*) from noise_mask_guesses where day = dd));
end $$;

grant execute on function public.noise_aud_live(date), public.noise_aud_vote(text, text), public.noise_mask_guess(text, text), public.noise_mask_count(date) to anon, authenticated;
revoke all on function public.noise_mask_reveal(date) from public, anon, authenticated;
