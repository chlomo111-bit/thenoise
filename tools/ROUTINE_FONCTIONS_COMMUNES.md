# The Noise — fonctions communes (V2, 29.10.2026, ordre du directeur des jeux validé par Shlomo)

Supabase : compte Composio `supabase_restow-lise`, ref `ohvmnaymozoxfirkbntt`, UNIQUEMENT les objets `noise_*`.
Instagram : compte Composio `instagram_howel-rootle` UNIQUEMENT (vérifier username = the_noise_2026).
Schéma complet : `tools/supabase_noise_v2.sql` (déjà appliqué en base le 29.10).

## 1. Monnaie : 🎟️ כרטיסים (table noise_tickets, une ligne par joueur et par jour, jour = heure d'Israël)
- Le joueur s'identifie sur le site (recherche de son @ → « זה אני! »).
- Entrée quotidienne +10 (noise_visit, gère aussi la série de jours dans noise_players).
- Chaque 👏 / 🍅 = +1 (plafond 50 🎟️/jour, noise_play — met aussi à jour le compteur global noise_reactions).
- Instagram (fait par la ROUTINE, pas par le site) : commentaire +10, tag d'ami +30, plafond 60 🎟️ Instagram/jour.
  `select noise_ig_award('<username>','comment','<comment_id>');` et, si le commentaire tague quelqu'un,
  `select noise_ig_award('<username>','tag','<comment_id>');` — idempotent par comment_id (aucun double compte).
  ⚠️ Ces fonctions ne modifient PAS noise_people.score (les points VIP +1/+3 restent gérés comme avant).
- Missions du jour : +10 à +30.

## 2. 🎁 Loterie 20 ₪ (depuis le 30.10 : remplace « מעריץ היום » ; voir tools/ROUTINE.md §3 et §3 bis)
- Éligible : ≥ 100 🎟️ dans la journée ET commentaire sur le « post du jour » épinglé de @the_noise_2026.
- Post du jour = noise_state `daily_post` {day, media_id, permalink}. Chaque commentateur du jour :
  `select noise_mark_commenter('<username>','<media_id>');`
- Tirage 20:00 (une seule fois par jour) : `select noise_fan_draw();` → {handle, n_eligible, already}. Vendredi : fait samedi 18:30 avec `noise_fan_draw('<date du vendredi>')`.
- Le gagnant reçoit 20 ₪ par Bit (Shlomo) + le siège 👑 le lendemain (le site lit noise_fan_draws, jour = hier) + tag dans la vidéo (noise_state `fan_to_cite`).
- Le site affiche le tirage en direct : `noise_lottery_live(d)` → {drawn, handle, drawn_at, participants[], qualified, commenters}.
- 🗣️ המגיב של היום : noise_state `top_commenter` {day, handle, n, power} → couronne sur le personnage + ligne dans « השורה הראשונה ».

## 3. Missions du jour (3 par jour, changent à minuit heure d'Israël)
- Tirées de façon déterministe par noise_day_missions(date) dans 3 groupes : (1) entrée / chat / idée,
  (2) 👏 ou 🍅 (20 à 40), (3) Instagram : commenter le post du jour / taguer un ami qui chante faux.
- Validation automatique côté serveur (noise_sync) ; le site affiche barre de progression + animation.
- Pool modifiable dans noise_mission_pool() (SQL).

## 4. 💡 Boîte à idées (table noise_ideas, 200 caractères max, 3 par jour, modérée)
- La routine du soir / la tâche du tirage lit les idées `status='new'`, et SEULEMENT s'il y a de bonnes idées
  envoie à Shlomo UNE ligne de résumé ; puis `update noise_ideas set status='seen' where status='new';`.

## 5. 💬 Chat public du public (table noise_chat, realtime + polling)
- 140 caractères, signé du @, 1 message / 10 s, réservé aux spectateurs (noise_people).
- Modération serveur noise_mod_check : insultes / contenu sexuel (hébreu + anglais), liens, téléphones, e-mails.
- 🚩 Signaler (noise_chat_report) : masqué automatiquement à 3 signalements. Suppression depuis #admin.
- Jeu ouvert à tous les âges : AUCUN message privé, seulement ce chat public modéré.

## 6–7. Statistiques et classement
- noise_me(h) : 🎟️ jour/total, série, missions, 👏/🍅, victoires, rang du jour et général.
- noise_board() : top 10 du jour et général (le site met en avant la place du joueur même hors top 10),
  stats globales. Abonnés : noise_state `followers` {n, at} (mis à jour par la tâche du tirage).

## 8. Annonce
- Popup « 🆕 חדש באולפן! » (une fois par visiteur ; rejouable avec #new).
- Actualité prête dans noise_state `news_v2_pending` : à copier dans `news` QUAND le site V2 est en ligne :
  `update noise_state set value=(select value from noise_state where key='news_v2_pending'), updated_at=now() where key='news';`
