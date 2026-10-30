# Anciennes tâches programmées de The Noise (archivées le 30/10/2026)

Rangement ordonné par le directeur : tout tourne désormais dans un seul chat « Automatisation – The Noise » (réveils send_later). Ces tâches étaient désactivées ; leur texte complet est conservé ici avant suppression.

---

## trig_01Ay5VUXkKd8zfYNTxprhzGy — The Noise – passages 6:00 / 12:00 / 17:00 / 19:55
Horaire : `CRON_TZ=Asia/Jerusalem 55 5,11,16,19 * * *` (désactivée le 30/10)

```
Passage du jeu Instagram « The Noise » (@the_noise_2026, thenoise.hakaveret.online). Réponds en français ; tout texte Instagram en hébreu, style émission télé drôle. Autonome et économe.

0. SHABBAT : regarde l'heure d'Israël (TZ=Asia/Jerusalem date). Si on est entre vendredi 16:00 et samedi 18:30 → termine IMMÉDIATEMENT sans rien faire.
1. Dépôt : clone chlomo111-bit/thenoise (si besoin add_repo owner chlomo111-bit, repo thenoise, access push), LIS tools/ROUTINE.md (§4 Passages, §3, §3 bis) et tools/ROUTINE_FONCTIONS_COMMUNES.md, et applique-les. git pull --rebase avant chaque push.
2. Outils Composio (ToolSearch : COMPOSIO_SEARCH_TOOLS puis COMPOSIO_MULTI_EXECUTE_TOOL). Instagram UNIQUEMENT account « instagram_howel-rootle » : vérifie d'abord INSTAGRAM_GET_USER_INFO (ig_user_id me, fields id,username,followers_count) → username == the_noise_2026, sinon STOP + PushNotification. Supabase UNIQUEMENT account « supabase_restow-lise », SUPABASE_BETA_RUN_SQL_QUERY, ref ohvmnaymozoxfirkbntt, objets noise_* seulement. Pas de Lovable.
3. Commentaires : publications des 14 derniers jours (INSTAGRAM_GET_IG_USER_MEDIA) puis INSTAGRAM_GET_IG_MEDIA_COMMENTS (fields id,text,username,timestamp,like_count ; pagine). Nouveaux = absents de noise_ig_seen et pas de the_noise_2026. Pour chacun (handle = lower(username)) : insert into noise_people(handle) … on conflict do nothing (+ comptes tagués) ; update noise_people set score=score+1 (+3 si tag) ; select noise_ig_award(h,'comment',cid) (+ noise_ig_award(h,'tag',cid) si @tag) — ne pas donner de points à un spam identique répété ; si le média = noise_state daily_post.media_id → select noise_mark_commenter(h, media_id) ; puis insert into noise_ig_seen(comment_id, handle).
4. Répondre à CHAQUE nouveau commentaire (INSTAGRAM_POST_IG_COMMENT_REPLIES) : hébreu, 1 phrase courte, drôle, différente à chaque fois, qui réagit vraiment ; jamais d'URL (« הקישור בביו ») ; relances variées (« 100 🎟️ + תגובה על הפוסט של היום = הגרלה של 20 ₪ ב־20:00 », « תייגו חבר שמזייף במקלחת », « מי יהיה המגיב של היום? 🗣️👑 »). Bienvenue spéciale si l'auteur n'est pas dans noise_ig_welcomed (puis l'y insérer). Insultant/sexuel/vraie personne : ni réponse ni points, à signaler dans la ligne finale.
5. Avant 12:00 : si noise_state top_commenter (day = hier) a power null, cherche sa réponse « ce qui arrivera demain » ; si acceptable, mets-la dans top_commenter.power et prépare-la dans le jeu (noise_state news / event) ; sinon propose-lui en réponse une version proche.
6. noise_state followers = {n, at}. Si followers ≥ 50 pour la première fois → SendUserMessage + PushNotification à Shlomo (reprise du calendrier jurés/votes).
7. Vérifie que le post du jour existe (noise_state daily_post.day = aujourd'hui). Sinon, crée-le comme décrit dans ROUTINE.md §3 (python3 tools/visuel.py post …, push dans media/AAAA-MM-JJ/, image_url raw.githubusercontent.com, publication, puis mise à jour de daily_post).
8. Passage de 19:55 SEULEMENT (et pas le vendredi) : story 1080×1920 « 5 דקות להגרלה! » (python3 tools/visuel.py story …) avec le nombre de participants (select noise_lottery_live()), le meilleur commentateur du moment (compte des noise_ig_awards kind='comment' du jour) et le rappel des 2 conditions ; publier en STORIES une seule fois (vérifier INSTAGRAM_GET_IG_USER_STORIES).
9. ÉCONOMIE : s'il n'y a aucun nouveau commentaire et rien à faire (et que ce n'est pas 19:55), termine tout de suite.
Termine par une ligne : abonnés, nouveaux commentaires, réponses, 🎟️ distribués, participants à la loterie. Ne préviens Shlomo qu'en cas de problème grave. Ne touche à aucune autre tâche programmée.
```

---

## trig_01WhX6dXEWijvoeTzTx2z69E — The Noise – loterie 20 ₪ (20:00)
Horaire : `CRON_TZ=Asia/Jerusalem 0 20 * * 0-4,6` (désactivée le 30/10)

```
Loterie du soir du jeu Instagram « The Noise » (@the_noise_2026, thenoise.hakaveret.online), règles décidées par Shlomo le 30/10/2026. Réponds en français ; textes Instagram en hébreu, style émission télé drôle. Autonome.

0. SHABBAT : heure d'Israël (TZ=Asia/Jerusalem date). Entre vendredi 16:00 et samedi 18:30 → termine immédiatement.
1. Dépôt chlomo111-bit/thenoise (add_repo owner chlomo111-bit, repo thenoise, access push si besoin), clone, LIS tools/ROUTINE.md (§3, §3 bis) et tools/ROUTINE_FONCTIONS_COMMUNES.md. git pull --rebase avant chaque push.
2. Composio : Instagram UNIQUEMENT account « instagram_howel-rootle » (vérifie INSTAGRAM_GET_USER_INFO me → username the_noise_2026, sinon STOP + PushNotification) ; Supabase UNIQUEMENT account « supabase_restow-lise », SUPABASE_BETA_RUN_SQL_QUERY, ref ohvmnaymozoxfirkbntt, objets noise_* seulement. Pas de Lovable.
3. Dernier relevé rapide : nouveaux commentaires du post du jour (noise_state daily_post.media_id) absents de noise_ig_seen → appliquer le §4 de ROUTINE.md pour eux (points, noise_mark_commenter, réponse) avant le tirage.
4. SAMEDI : fais d'abord le tirage du VENDREDI : select noise_fan_draw('<date de vendredi>'); puis celui du jour.
5. Tirage : select noise_fan_draw(); → {handle, n_eligible, already}. Si already=true, ne refais rien (pas de seconde story). Le site montre le tirage en direct. Mets noise_state fan_to_cite = {day, handle}.
6. המגיב של היום : parmi les noise_ig_awards kind='comment' du jour, le handle avec le plus de lignes (égalité : celui qui a atteint ce nombre le premier, created_at). Spam identique répété déjà exclu. → noise_state top_commenter = {day, handle, n, power:null}. Réponds à son dernier commentaire : « 👑 אתם המגיב של היום! מה יקרה מחר באולפן בזכותכם? כתבו כאן עד 12:00 ».
7. Story résultat 1080×1920 (python3 tools/visuel.py story media/AAAA-MM-JJ/story_tirage.jpg '{json}' avec NM pointant vers un node_modules contenant three@0.128.0 et @fontsource/heebo) : « 🎉 הזוכה בהגרלה: @x · 20 ₪ » + « 🗣️ המגיב של היום: @y – מה יקרה מחר בזכותך? » + « <n> משתתפים · מחר עוד הגרלה ב־20:00 » (ou « אף אחד לא עמד בתנאים… 😱 »). Push, image_url raw.githubusercontent.com, publication STORIES une seule fois (vérifier INSTAGRAM_GET_IG_USER_STORIES).
8. Message à Shlomo (SendUserMessage + PushNotification avec <routine_summary>) : gagnant @… + « 20 ₪ à payer par Bit » (+ celui du vendredi le samedi), nombre de participants, המגיב של היום. Si personne : une ligne.
9. Boîte à idées : lis noise_ideas status='new' ; seulement s'il y a de bonnes idées, ajoute UNE ligne au message ; puis update noise_ideas set status='seen' where status='new'.
Ne touche à aucune autre tâche programmée.
```

---

## trig_01XuNQ4wjAUyjSLYEkh7ykki — The Noise – voix vidéo jurés élus + inscriptions (obsolète)
Rappel ponctuel mer. 4/11 16:00 (send_later, désactivé le 30/10 : calendrier jurés en pause jusqu'à 50 abonnés)

```
Rappel The Noise : la vidéo « annonce des 4 jurés + ouverture des inscriptions chanteurs » sort ce soir mercredi 4/11 à 19:00. Compte les votes sous le post de vote (compte instagram_howel-rootle ; égalité = vidéo dramatique et vote relancé), mets les jurés élus dans la base (noise_people, statut elected, chaise 1-4), puis écris à Shlomo le texte du présentateur (« בפרק הקודם » + annonce des 4 jurés + comment s'inscrire : commenter son nom + sa chanson + « בפרק הבא ») pour ElevenLabs (Nimrod) et demande-lui le MP3. Ensuite, sois autonome : vidéo + publication 19:00. Pense aussi à programmer les rappels voix des épisodes suivants (2-3 h avant chaque vidéo).
```

---

## trig_01DccFmmaD4JAXF4T6cg4grY — The Noise – voix vidéo vote des jurés (obsolète)
Rappel ponctuel lun. 2/11 16:00 (send_later, désactivé le 30/10 : calendrier jurés en pause jusqu'à 50 abonnés)

```
Rappel The Noise : la vidéo « vote des jurés » sort ce soir lundi 2/11 à 19:00. Récupère d'abord les 8 commentaires les plus likés sous le post d'appel aux jurés (compte instagram_howel-rootle), puis écris à Shlomo le texte du présentateur (« בפרק הקודם » + présentation des 8 candidats numérotés 1-8, le public vote en commentaire + « בפרק הבא ») pour ElevenLabs (Nimrod, Eleven v3, Creative) et demande-lui le MP3. Ensuite, sois autonome : vidéo + publication 19:00.
```

---

Note : la vidéo « appel aux jurés » (voix Nimrod du 30/10, épisode 1) est prête mais NON programmée, car le calendrier jurés/votes est en pause jusqu'à 50 abonnés. Elle servira quand le seuil sera atteint (le texte parle des jurés, pas d'une date).
