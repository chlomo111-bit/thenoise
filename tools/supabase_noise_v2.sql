-- The Noise — V2 (29.10.2026) : fonctions communes à tous les jeux
-- 🎟️ כרטיסים (monnaie), מעריץ היום (tirage quotidien), 3 missions du jour, boîte à idées,
-- chat public modéré (realtime), statistiques, classement.
-- UNIQUEMENT des objets préfixés noise_. Aucune table d'un autre jeu n'est modifiée.
-- Toutes les écritures passent par des fonctions security definer ; les tables ne sont pas modifiables par anon.

-- ---------- helpers ----------
create or replace function public.noise_today() returns date language sql stable as
$$ select (now() at time zone 'Asia/Jerusalem')::date $$;
create or replace function public.noise_h(h text) returns text language sql immutable as
$$ select lower(regexp_replace(btrim(coalesce(h,'')), '^@', '')) $$;

-- ---------- tables ----------
create table if not exists public.noise_players (
  handle      text primary key,
  streak      int not null default 0,
  best_streak int not null default 0,
  last_day    date,
  wins        int not null default 0,
  last_play   timestamptz,
  last_chat   timestamptz,
  created_at  timestamptz not null default now()
);
create table if not exists public.noise_tickets (
  day           date not null,
  handle        text not null,
  tickets       int  not null default 0,   -- 🎟️ gagnés ce jour-là (toutes sources)
  react_tickets int  not null default 0,   -- part venant des 👏/🍅 (plafond 50/jour)
  ig_tickets    int  not null default 0,   -- part venant d'Instagram (plafond 60/jour)
  claps         int  not null default 0,
  tomatoes      int  not null default 0,
  visited       boolean not null default false,
  chats         int  not null default 0,
  ideas         int  not null default 0,
  ig_comments   int  not null default 0,
  ig_tags       int  not null default 0,
  missions_done text[] not null default '{}',
  updated_at    timestamptz not null default now(),
  primary key (day, handle)
);
create index if not exists noise_tickets_day_idx on public.noise_tickets(day, tickets desc);
create index if not exists noise_tickets_handle_idx on public.noise_tickets(handle);
create table if not exists public.noise_daily_commenters (
  day date not null, handle text not null, post_id text, created_at timestamptz not null default now(),
  primary key (day, handle)
);
create table if not exists public.noise_ig_awards (
  comment_id text primary key, handle text not null, kind text not null, day date not null,
  tickets int not null default 0, created_at timestamptz not null default now()
);
create table if not exists public.noise_fan_draws (
  day date primary key, handle text, n_eligible int not null default 0, drawn_at timestamptz not null default now()
);
create table if not exists public.noise_ideas (
  id bigint generated always as identity primary key,
  handle text not null,
  body text not null check (char_length(body) between 1 and 200),
  day date not null default ((now() at time zone 'Asia/Jerusalem')::date),
  status text not null default 'new',
  created_at timestamptz not null default now()
);
create table if not exists public.noise_chat (
  id bigint generated always as identity primary key,
  handle text not null,
  body text not null check (char_length(body) between 1 and 140),
  hidden boolean not null default false,
  reports int not null default 0,
  created_at timestamptz not null default now()
);
create index if not exists noise_chat_created_idx on public.noise_chat(created_at desc);
create table if not exists public.noise_chat_reports (
  msg_id bigint not null references public.noise_chat(id) on delete cascade,
  reporter text not null, created_at timestamptz not null default now(),
  primary key (msg_id, reporter)
);

alter table public.noise_players          enable row level security;
alter table public.noise_tickets          enable row level security;
alter table public.noise_daily_commenters enable row level security;
alter table public.noise_ig_awards        enable row level security;
alter table public.noise_fan_draws        enable row level security;
alter table public.noise_ideas            enable row level security;
alter table public.noise_chat             enable row level security;
alter table public.noise_chat_reports     enable row level security;
drop policy if exists noise_chat_read on public.noise_chat;
create policy noise_chat_read on public.noise_chat for select to anon, authenticated using (hidden = false);
drop policy if exists noise_fan_read on public.noise_fan_draws;
create policy noise_fan_read on public.noise_fan_draws for select to anon, authenticated using (true);
grant select on public.noise_chat, public.noise_fan_draws to anon, authenticated;

do $$ begin
  if not exists (select 1 from pg_publication_tables where pubname='supabase_realtime' and tablename='noise_chat') then
    alter publication supabase_realtime add table public.noise_chat;
  end if;
end $$;

-- ---------- modération (chat + idées) ----------
-- renvoie null si OK, sinon un code : link / phone / email / bad
create or replace function public.noise_mod_check(body text) returns text language plpgsql immutable as $$
declare b text := lower(coalesce(body,'')); flat text;
begin
  if b ~ '(https?://|www\.|t\.me|wa\.me|bit\.ly)' or b ~ '[a-z0-9-]+\.(com|net|org|io|co|il|ly|me|gg|tv|app|xyz|info|link|site|online|ru|biz|shop|store)([^a-z]|$)' then return 'link'; end if;
  if b ~ '[^\s@]+@[^\s@]+\.[a-z]{2,}' then return 'email'; end if;
  if b ~ '\+?\d[\d\s().-]{5,}\d' and exists (select 1 from regexp_matches(b, '(\+?\d[\d\s().-]{5,}\d)', 'g') as m where length(regexp_replace(m[1], '\D', '', 'g')) >= 7) then return 'phone'; end if;
  -- mots interdits (insultes / sexuel), hébreu : préfixe ו/ה/ש/ב/ל/מ/כ possible
  if (' '||regexp_replace(b, '[^a-zא-ת0-9]+', ' ', 'g')||' ') ~ '[^א-ת][והשבלמכ]?(זונה|זונות|שרמוטה|שרמוטות|שרמוט|זין|זיון|זיונים|לזיין|תזדיין|מזדיין|תזדייני|כוסאמק|כוסאמא|כוסעמק|כוסית|מניאק|מניאקית|חרא|מפגר|מפגרת|מפגרים|מטומטם|מטומטמת|דביל|דבילית|אידיוט|אידיוטית|סקס|פורנו|ציצים|ציצי|זקפה|אורגזמה|עירום|עירומה|נודס|קוקסינל|בןזונה|יאזונה|שמוק|מזדיינת)[^א-ת]' then return 'bad'; end if;
  if b ~ 'כוס\s*(אמק|אמא|עמק|אמ)' or b ~ 'בן\s*(של\s*)?זונה' or b ~ 'יא\s*זונה' then return 'bad'; end if;
  flat := ' ' || regexp_replace(translate(b, '013457$', 'oieasts'), '[^a-z\s]', '', 'g') || ' ';
  if flat ~ '(fuck|fuk|shit|bitch|cunt|pussy|porn|nude|slut|whore|asshole|nigg|penis|boobs|horny|onlyfans|motherf)' then return 'bad'; end if;
  if flat ~ '\s(sex|sexy|ass|cock|cum|xxx|nsfw|dick|fag|fags|tits|wtf|stfu)\s' then return 'bad'; end if;
  return null;
end $$;

-- ---------- missions ----------
create or replace function public.noise_mission_pool() returns jsonb language sql immutable as $$ select '[
 {"k":"visit","g":1,"t":"להיכנס לאולפן היום 🎬","goal":1,"r":10,"m":"visited"},
 {"k":"chat1","g":1,"t":"לכתוב הודעה בצ׳אט של הקהל 💬","goal":1,"r":15,"m":"chats"},
 {"k":"idea1","g":1,"t":"לשלוח רעיון לתיבת הרעיונות 💡","goal":1,"r":15,"m":"ideas"},
 {"k":"clap20","g":2,"t":"למחוא כפיים 20 פעם 👏","goal":20,"r":20,"m":"claps"},
 {"k":"clap40","g":2,"t":"40 מחיאות כפיים – שהבמה תרעד 👏👏","goal":40,"r":30,"m":"claps"},
 {"k":"tom10","g":2,"t":"לזרוק 10 עגבניות על הזייפנים 🍅","goal":10,"r":20,"m":"tomatoes"},
 {"k":"tom20","g":2,"t":"20 עגבניות – סלט על הבמה 🍅🥗","goal":20,"r":30,"m":"tomatoes"},
 {"k":"comment","g":3,"t":"להגיב על הפוסט של היום ב־@the_noise_2026 📸","goal":1,"r":30,"m":"commented"},
 {"k":"tag","g":3,"t":"לתייג בתגובה חבר שמזייף במקלחת 🚿","goal":1,"r":30,"m":"ig_tags"}
]'::jsonb $$;

create or replace function public.noise_day_missions(d date) returns jsonb language plpgsql stable as $$
declare res jsonb := '[]'::jsonb; g int; grp jsonb; n int; idx int;
begin
  for g in 1..3 loop
    select jsonb_agg(x) into grp from jsonb_array_elements(noise_mission_pool()) x where (x->>'g')::int = g;
    n := jsonb_array_length(grp);
    idx := ((hashtext(d::text || ':' || g)::bigint % n) + n) % n;
    res := res || jsonb_build_array(grp->idx);
  end loop;
  return res;
end $$;

-- évalue les missions du jour, crédite les nouvelles, renvoie les clés nouvellement validées
create or replace function public.noise_sync(h text, d date default null) returns text[]
language plpgsql security definer set search_path = public as $$
declare dd date := coalesce(d, noise_today()); t noise_tickets; m jsonb; prog int; fresh text[] := '{}';
begin
  insert into noise_tickets(day, handle) values (dd, h) on conflict do nothing;
  select * into t from noise_tickets where day = dd and handle = h for update;
  for m in select * from jsonb_array_elements(noise_day_missions(dd)) loop
    if (m->>'k') = any(t.missions_done) then continue; end if;
    prog := case m->>'m'
      when 'visited'   then case when t.visited then 1 else 0 end
      when 'commented' then case when exists (select 1 from noise_daily_commenters c where c.day = dd and c.handle = h) then 1 else 0 end
      when 'chats'     then t.chats
      when 'ideas'     then t.ideas
      when 'claps'     then t.claps
      when 'tomatoes'  then t.tomatoes
      when 'ig_tags'   then t.ig_tags
      else 0 end;
    if prog >= (m->>'goal')::int then
      t.missions_done := t.missions_done || (m->>'k');
      t.tickets := t.tickets + (m->>'r')::int;
      fresh := fresh || (m->>'k');
    end if;
  end loop;
  if cardinality(fresh) > 0 then
    update noise_tickets set missions_done = t.missions_done, tickets = t.tickets, updated_at = now() where day = dd and handle = h;
  end if;
  return fresh;
end $$;

-- ---------- état du joueur ----------
create or replace function public.noise_me(h text, fresh text[] default '{}') returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); dd date := noise_today(); t noise_tickets; p noise_players; tot record; ms jsonb := '[]'::jsonb; m jsonb; prog int;
  commented boolean; rt int; rtot int; fan record; lastfan record; ndone int;
begin
  select * into t from noise_tickets where day = dd and handle = hh;
  select * into p from noise_players where handle = hh;
  select coalesce(sum(tickets),0) tk, coalesce(sum(claps),0) cl, coalesce(sum(tomatoes),0) tm, coalesce(sum(cardinality(missions_done)),0) md, count(*) days
    into tot from noise_tickets where handle = hh;
  commented := exists (select 1 from noise_daily_commenters c where c.day = dd and c.handle = hh);
  for m in select * from jsonb_array_elements(noise_day_missions(dd)) loop
    prog := case m->>'m'
      when 'visited' then case when coalesce(t.visited,false) then 1 else 0 end
      when 'commented' then case when commented then 1 else 0 end
      when 'chats' then coalesce(t.chats,0) when 'ideas' then coalesce(t.ideas,0)
      when 'claps' then coalesce(t.claps,0) when 'tomatoes' then coalesce(t.tomatoes,0)
      when 'ig_tags' then coalesce(t.ig_tags,0) else 0 end;
    ms := ms || jsonb_build_array(m || jsonb_build_object('progress', least(prog,(m->>'goal')::int), 'done', coalesce((m->>'k') = any(t.missions_done), false)));
  end loop;
  select 1 + count(*) into rt from noise_tickets where day = dd and tickets > coalesce(t.tickets,0);
  select 1 + count(*) into rtot from (select handle, sum(tickets) s from noise_tickets group by handle) x where x.s > tot.tk;
  select day, handle into fan from noise_fan_draws where day = dd - 1;
  select day, handle into lastfan from noise_fan_draws where day = dd;
  return jsonb_build_object(
    'handle', hh, 'day', dd, 'in_audience', exists (select 1 from noise_people where handle = hh),
    'goal', 100, 'today', coalesce(t.tickets,0), 'total', tot.tk, 'commented', commented,
    'claps_today', coalesce(t.claps,0), 'tomatoes_today', coalesce(t.tomatoes,0),
    'claps_total', tot.cl, 'tomatoes_total', tot.tm, 'missions_total', tot.md, 'days', tot.days,
    'ideas_today', coalesce(t.ideas,0), 'react_tickets', coalesce(t.react_tickets,0), 'ig_tickets', coalesce(t.ig_tickets,0),
    'streak', coalesce(p.streak,0), 'best_streak', coalesce(p.best_streak,0), 'wins', coalesce(p.wins,0),
    'missions', ms, 'fresh', to_jsonb(coalesce(fresh,'{}')),
    'rank_today', case when coalesce(t.tickets,0) > 0 then rt end, 'rank_total', case when tot.tk > 0 then rtot end,
    'fan_today', fan.handle, 'drawn_today', lastfan.handle, 'drawn', lastfan.day is not null
  );
end $$;

-- ---------- actions du site ----------
create or replace function public.noise_visit(h text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); dd date := noise_today(); p noise_players; was boolean;
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
    update noise_tickets set visited = true, tickets = tickets + 10, updated_at = now() where day = dd and handle = hh;
  end if;
  return noise_me(hh, noise_sync(hh, dd));
end $$;

-- 1 🎟️ par 👏/🍅 (plafond 50 🎟️/jour), 15 max de chaque par appel, 1 appel / 2 s
create or replace function public.noise_play(h text, claps int, tomatoes int) returns jsonb
language plpgsql security definer set search_path = public as $$
#variable_conflict use_column
declare hh text := noise_h(h); dd date := noise_today(); c int := least(greatest(coalesce(claps,0),0),15); tm int := least(greatest(coalesce(tomatoes,0),0),15); lp timestamptz; gain int;
begin
  if not exists (select 1 from noise_people where handle = hh) then raise exception 'not_in_audience'; end if;
  insert into noise_players(handle) values (hh) on conflict do nothing;
  select last_play into lp from noise_players where handle = hh for update;
  if lp is not null and lp > now() - interval '2 seconds' then return noise_me(hh); end if;
  update noise_players set last_play = now() where handle = hh;
  if c > 0 then insert into noise_reactions(day, kind, n) values (dd, 'clap', c) on conflict (day, kind) do update set n = noise_reactions.n + c; end if;
  if tm > 0 then insert into noise_reactions(day, kind, n) values (dd, 'tomato', tm) on conflict (day, kind) do update set n = noise_reactions.n + tm; end if;
  insert into noise_tickets(day, handle) values (dd, hh) on conflict do nothing;
  select least(c + tm, greatest(0, 50 - react_tickets)) into gain from noise_tickets where day = dd and handle = hh for update;
  update noise_tickets set claps = claps + c, tomatoes = tomatoes + tm, react_tickets = react_tickets + gain, tickets = tickets + gain, updated_at = now()
    where day = dd and handle = hh;
  return noise_me(hh, noise_sync(hh, dd));
end $$;

create or replace function public.noise_chat_post(h text, body text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); b text := btrim(regexp_replace(coalesce(body,''), '\s+', ' ', 'g')); lc timestamptz; bad text; dd date := noise_today();
begin
  if not exists (select 1 from noise_people where handle = hh) then raise exception 'not_in_audience'; end if;
  if char_length(b) < 1 or char_length(b) > 140 then raise exception 'bad_length'; end if;
  bad := noise_mod_check(b); if bad is not null then raise exception 'mod_%', bad; end if;
  insert into noise_players(handle) values (hh) on conflict do nothing;
  select last_chat into lc from noise_players where handle = hh for update;
  if lc is not null and lc > now() - interval '10 seconds' then raise exception 'too_fast'; end if;
  update noise_players set last_chat = now() where handle = hh;
  insert into noise_chat(handle, body) values (hh, b);
  insert into noise_tickets(day, handle) values (dd, hh) on conflict do nothing;
  update noise_tickets set chats = chats + 1, updated_at = now() where day = dd and handle = hh;
  return noise_me(hh, noise_sync(hh, dd));
end $$;

create or replace function public.noise_chat_report(h text, mid bigint) returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); n int;
begin
  if not exists (select 1 from noise_people where handle = hh) then raise exception 'not_in_audience'; end if;
  if exists (select 1 from noise_chat where id = mid and handle = hh) then raise exception 'own_message'; end if;
  insert into noise_chat_reports(msg_id, reporter) values (mid, hh) on conflict do nothing;
  get diagnostics n = row_count;
  if n > 0 then
    update noise_chat set reports = reports + 1, hidden = hidden or reports + 1 >= 3 where id = mid;
  end if;
  return jsonb_build_object('ok', true, 'new', n > 0);
end $$;

create or replace function public.noise_idea_post(h text, body text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare hh text := noise_h(h); b text := btrim(regexp_replace(coalesce(body,''), '\s+', ' ', 'g')); bad text; dd date := noise_today();
begin
  if not exists (select 1 from noise_people where handle = hh) then raise exception 'not_in_audience'; end if;
  if char_length(b) < 3 or char_length(b) > 200 then raise exception 'bad_length'; end if;
  bad := noise_mod_check(b); if bad is not null then raise exception 'mod_%', bad; end if;
  if (select count(*) from noise_ideas where handle = hh and day = dd) >= 3 then raise exception 'idea_limit'; end if;
  insert into noise_ideas(handle, body, day) values (hh, b, dd);
  insert into noise_tickets(day, handle) values (dd, hh) on conflict do nothing;
  update noise_tickets set ideas = ideas + 1, updated_at = now() where day = dd and handle = hh;
  return noise_me(hh, noise_sync(hh, dd));
end $$;

-- ---------- classement + stats globales ----------
create or replace function public.noise_board() returns jsonb
language sql security definer set search_path = public stable as $$
  select jsonb_build_object(
    'day', noise_today(),
    'today', coalesce((select jsonb_agg(jsonb_build_object('handle', handle, 'n', tickets) order by tickets desc, updated_at asc)
              from (select handle, tickets, updated_at from noise_tickets where day = noise_today() and tickets > 0 order by tickets desc, updated_at asc limit 10) a), '[]'::jsonb),
    'total', coalesce((select jsonb_agg(jsonb_build_object('handle', handle, 'n', s) order by s desc)
              from (select handle, sum(tickets) s from noise_tickets group by handle having sum(tickets) > 0 order by s desc limit 10) b), '[]'::jsonb),
    'players_today', (select count(*) from noise_tickets where day = noise_today() and tickets > 0),
    'tickets_today', (select coalesce(sum(tickets),0) from noise_tickets where day = noise_today()),
    'qualified_today', (select count(*) from noise_tickets where day = noise_today() and tickets >= 100),
    'fan_today', (select handle from noise_fan_draws where day = noise_today() - 1),
    'fans', coalesce((select jsonb_agg(jsonb_build_object('day', day, 'handle', handle) order by day desc) from (select * from noise_fan_draws where handle is not null order by day desc limit 7) f), '[]'::jsonb),
    'chat_today', (select count(*) from noise_chat where created_at >= (noise_today()::timestamp at time zone 'Asia/Jerusalem'))
  )
$$;

-- ---------- routine (PAS accessible au public) ----------
-- Points Instagram → 🎟️ : commentaire +10, tag d'ami +30 (plafond 60 🎟️ Instagram/jour). Idempotent par comment_id.
create or replace function public.noise_ig_award(h text, kind text, cid text, d date default null) returns int
language plpgsql security definer set search_path = public as $$
#variable_conflict use_variable
declare hh text := noise_h(h); dd date := coalesce(d, noise_today()); want int; gain int;
begin
  if kind not in ('comment','tag') then raise exception 'bad kind'; end if;
  if exists (select 1 from noise_ig_awards where comment_id = cid || ':' || kind) then return 0; end if;
  want := case kind when 'comment' then 10 else 30 end;
  insert into noise_tickets(day, handle) values (dd, hh) on conflict do nothing;
  select least(want, greatest(0, 60 - ig_tickets)) into gain from noise_tickets where day = dd and handle = hh for update;
  update noise_tickets set ig_tickets = ig_tickets + gain, tickets = tickets + gain,
    ig_comments = ig_comments + case when kind = 'comment' then 1 else 0 end,
    ig_tags = ig_tags + case when kind = 'tag' then 1 else 0 end, updated_at = now()
    where day = dd and handle = hh;
  insert into noise_ig_awards(comment_id, handle, kind, day, tickets) values (cid || ':' || kind, hh, kind, dd, gain);
  perform noise_sync(hh, dd);
  return gain;
end $$;

-- commentateur du post du jour (condition du tirage + mission « comment »)
create or replace function public.noise_mark_commenter(h text, post_id text, d date default null) returns void
language plpgsql security definer set search_path = public as $$
#variable_conflict use_variable
declare hh text := noise_h(h); dd date := coalesce(d, noise_today());
begin
  insert into noise_daily_commenters(day, handle, post_id) values (dd, hh, post_id) on conflict do nothing;
  perform noise_sync(hh, dd);
end $$;

-- tirage « מעריץ היום » : ≥100 🎟️ ET commentaire du post du jour. Une seule fois par jour.
create or replace function public.noise_fan_draw(d date default null) returns jsonb
language plpgsql security definer set search_path = public as $$
declare dd date := coalesce(d, noise_today()); r noise_fan_draws; n int; w text;
begin
  select * into r from noise_fan_draws where day = dd;
  if found then return jsonb_build_object('already', true, 'day', dd, 'handle', r.handle, 'n_eligible', r.n_eligible); end if;
  select count(*) into n from noise_tickets t where t.day = dd and t.tickets >= 100 and exists (select 1 from noise_daily_commenters c where c.day = dd and c.handle = t.handle);
  select t.handle into w from noise_tickets t where t.day = dd and t.tickets >= 100 and exists (select 1 from noise_daily_commenters c where c.day = dd and c.handle = t.handle) order by random() limit 1;
  insert into noise_fan_draws(day, handle, n_eligible) values (dd, w, n);
  if w is not null then
    insert into noise_players(handle, wins) values (w, 1) on conflict (handle) do update set wins = noise_players.wins + 1;
    -- prix depuis le 31/10/2026 : plus d'argent, +300 tickets bonus
    update noise_tickets set tickets = tickets + 300, updated_at = now() where day = dd and handle = w;
    perform noise_sync(w, dd);
  end if;
  return jsonb_build_object('already', false, 'day', dd, 'handle', w, 'n_eligible', n, 'bonus', case when w is null then 0 else 300 end);
end $$;

-- ---------- admin (mot de passe de la ruche) ----------
create or replace function public.noise_admin_chat(pass text) returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  if not exists (select 1 from admin_secret where pass_hash = crypt(pass, pass_hash)) then raise exception 'bad password'; end if;
  return coalesce((select jsonb_agg(to_jsonb(c) order by c.id desc) from (select * from noise_chat order by id desc limit 100) c), '[]'::jsonb);
end $$;
create or replace function public.noise_admin_chat_delete(pass text, mid bigint) returns void
language plpgsql security definer set search_path = public, extensions as $$
begin
  if not exists (select 1 from admin_secret where pass_hash = crypt(pass, pass_hash)) then raise exception 'bad password'; end if;
  delete from noise_chat where id = mid;
end $$;
create or replace function public.noise_admin_ideas(pass text) returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
begin
  if not exists (select 1 from admin_secret where pass_hash = crypt(pass, pass_hash)) then raise exception 'bad password'; end if;
  return coalesce((select jsonb_agg(to_jsonb(i) order by i.id desc) from (select * from noise_ideas order by id desc limit 100) i), '[]'::jsonb);
end $$;

-- ---------- droits ----------
revoke all on function public.noise_sync(text, date) from public, anon, authenticated;
revoke all on function public.noise_ig_award(text, text, text, date) from public, anon, authenticated;
revoke all on function public.noise_mark_commenter(text, text, date) from public, anon, authenticated;
revoke all on function public.noise_fan_draw(date) from public, anon, authenticated;
revoke all on function public.noise_me(text, text[]) from public;
grant execute on function public.noise_me(text, text[]) to anon, authenticated;
grant execute on function public.noise_visit(text), public.noise_play(text, int, int), public.noise_chat_post(text, text),
  public.noise_chat_report(text, bigint), public.noise_idea_post(text, text), public.noise_board(),
  public.noise_admin_chat(text), public.noise_admin_chat_delete(text, bigint), public.noise_admin_ideas(text),
  public.noise_mod_check(text), public.noise_today() to anon, authenticated;
