# The Noise — ROUTINE (règles obligatoires décidées par Shlomo le 30/10/2026)

Compte Instagram : Composio `instagram_howel-rootle` UNIQUEMENT (vérifier `username == the_noise_2026`, ig_user_id 28776506972012800 / user_id 17841441777719733).
Supabase : Composio `supabase_restow-lise`, outil SUPABASE_BETA_RUN_SQL_QUERY, ref `ohvmnaymozoxfirkbntt`, UNIQUEMENT les objets `noise_*`. Pas de Lovable.
Dépôt : chlomo111-bit/thenoise (GitHub Pages → thenoise.hakaveret.online, médias sous /media/AAAA-MM-JJ/). `git pull --rebase` avant chaque push.
Textes Instagram/joueurs : hébreu, style émission télé drôle (présentateur דודי מיקרופון, voix Nimrod). Compte-rendu à Shlomo : français.
Détails techniques des fonctions SQL : `tools/ROUTINE_FONCTIONS_COMMUNES.md`.

## État (30/10/2026)
- 3 abonnés. Le calendrier de l'émission (appel aux jurés, votes, inscriptions) est EN PAUSE jusqu'à 50 abonnés.
- Reel de lancement en collaboration : samedi 31/10 19:00 (tâche dédiée, ne pas refaire).
- Monnaie du jeu = 🎟️ כרטיסים. **Seuil du jour = 100 🎟️.**

## 0. Shabbat
Rien entre vendredi 16:00 et samedi 18:30 (heure d'Israël). Toute tâche qui se déclenche dans ce créneau s'arrête immédiatement.
La loterie du vendredi est faite (vidéo : chat « The Noise – vidéos ») samedi à partir de 18:30 (loterie du vendredi d'abord, `noise_fan_draw('<date du vendredi>')`), puis celle du samedi à 20:00.
Le vendredi : production du matin + passages 6:00 et 12:00 seulement ; pas de passage 17:00 ni 19:55, pas de loterie 20:00.

## 1. Vidéo du jour (à partir du dimanche 1/11)
- **RÈGLE DE SHLOMO DU 30/10 : TOUTES LES VIDÉOS SONT FAITES UNIQUEMENT DANS LE CHAT « The Noise – vidéos » (session_01K8i1w3yD9CDquGsWHdGjZx)** : texte de la voix, réception du MP3, montage, couverture, publication du reel, sauvegarde bureau + chat. Le chat « Automatisation – The Noise » ne fait AUCUNE vidéo et ne programme aucun réveil vidéo : il fait le post du jour, l'événement, les passages, la loterie, et note dans noise_state `news` ce qui s'est passé (la vidéo s'en sert).
- Le Mac de Shlomo est allumé en permanence : la copie sur le bureau se fait à chaque vidéo.
- Chaque jour un reel qui raconte ce qui s'est passé dans le jeu (vrais @ tagués, vrais chiffres : public, 🎟️, 👏/🍅, gagnant de la loterie, המגיב של היום et son pouvoir, événement extraordinaire).
- Thème actuel (en attendant 50 abonnés) : « la salle qui se remplit » — sièges, tomates, public, coulisses de l'émission.
- AVANT d'écrire : lire TOUS les commentaires du post/reel précédent ; le commentaire valable le plus liké décide de ce qui arrive (on écarte insultant, sexuel, visant une vraie personne, impossible → le suivant).
- Fin obligatoire : « מה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת ».
- Texte écrit pour la voix (hébreu, balises Eleven v3, ~25 s, nombres en toutes lettres) envoyé à Shlomo 2–3 h avant la mise en ligne (SendUserMessage + PushNotification) : c'est LA SEULE chose qu'on lui demande (MP3 Nimrod). Mise en ligne 19:00 (samedi : après 18:30).
- SAUVEGARDE DE CHAQUE VIDÉO (règle de Shlomo du 30/10/2026) : dès qu'une vidéo est montée, (1) l'envoyer dans le chat avec SendUserFile, nommée « The Noise – AAAA-MM-JJ – <titre>.mp4 » (+ sa couverture), et (2) la copier sur le bureau de Shlomo dans ~/Desktop/Jeux/The Noise/Vidéos/ avec le même nom (outils mcp__remote-devices__ : device_commit_files ; si le bureau n'est pas encore autorisé, device_request_folder_access ~/Desktop). Si l'ordinateur n'est pas joignable, le dire en une ligne et réessayer au passage suivant. Ne jamais supprimer de fichier sur le bureau.
- **JOURNAL DU JOUR (règle de Shlomo du 30/10, chaque vidéo)** : au MILIEU de la vidéo, une pause « flash spécial » : on coupe vers un plateau télé de journal (décor à valider avec Shlomo, voir tools/PLATEAU.md), le présentateur lit LE COMMENTAIRE DU JOUR = le commentaire valable le plus liké d'hier (affiché à l'écran : @auteur + texte + nombre de ❤️), annonce que c'est fait « comme promis », on montre la chose réalisée DANS LE JEU (capture du site où l'idée a été mise en place), puis on reprend l'épisode. Ce commentaire doit donc être mis en place dans le jeu (noise_state news/event) AVANT la vidéo. Le texte voix envoyé à Shlomo contient ce passage (« [מבזק] … »). Sans commentaire valable : le journal annonce « אף אחד לא הציע… מחר זה יכול להיות אתם ».
- Couverture dédiée (jamais une image noire), légende avec CTA + « המבצע אינו קשור לאינסטגרם ואינו ממומן על ידה » + 5 hashtags.

## 2. Chaque jour quelque chose d'extraordinaire
Un événement fou / surprise / nouveauté visible dans le jeu (ex. pluie de tomates géante, un fauteuil de juré qui tourne tout seul, un invité surprise sur scène, double 🎟️ pendant 1 h…), idéalement inspiré du commentaire le plus liké ou de la boîte à idées (`noise_ideas`).
Il est annoncé dans noise_state `news` (titre + texte) et raconté dans la vidéo.

## 3. Loterie 20 ₪ tous les soirs à 20:00
- Un seul gagnant, payé par Shlomo par Bit. Conditions : (a) commenter le POST DU JOUR épinglé, (b) ≥ 100 🎟️ dans la journée. Pas de condition d'abonnement.
- POST DU JOUR créé CHAQUE MATIN (image 4:5 1080×1350, hook + rappel des 2 conditions + « הגיבו כאן 👇 »), épinglé si possible (l'API ne permet pas d'épingler → l'indiquer à Shlomo seulement la première fois). Ne jamais l'oublier.
  Son media_id est noté dans noise_state `daily_post` {day, media_id, permalink}.
- Tirage : `select noise_fan_draw();` (ou avec la date du vendredi). Le site affiche le tirage en direct (noise_lottery_live) et le gagnant a le siège 👑 le lendemain.
- Puis story du résultat (1080×1920) + message à Shlomo : gagnant + « 20 ₪ à payer par Bit » (ou « personne n'a rempli les conditions »).

## 3 bis. המגיב של היום (meilleur commentateur)
- À 20:00 avec la loterie : le joueur avec le plus de commentaires valables de la journée sur tous les posts du compte (pas de spam identique répété ; égalité = celui qui a atteint ce nombre en premier).
  Comptage : `noise_ig_awards` (kind='comment', day = aujourd'hui) — un comment_id par commentaire valable.
- Gagne : couronne/badge « המגיב של היום » sur son personnage jusqu'au lendemain soir → noise_state `top_commenter` {day, handle, n, power:null}.
- Annoncé dans la story du résultat + tagué dans la vidéo du lendemain. Pas d'argent mais un POUVOIR : il choisit une chose extraordinaire qui arrivera le lendemain EN PLUS du reste.
- La story et une réponse à son commentaire lui demandent « מה יקרה מחר בזכותך? ». Il répond en commentaire avant 12:00 le lendemain.
  Refuser insultant / sexuel / vraie personne / impossible (proposer une version proche). Mettre en place dans le jeu, noter `power` dans top_commenter, raconter dans la vidéo (« @x החליט ש… »). Sans réponse avant 12:00 : rien de plus.

## 3 ter. Inscription par le site (30/10)
À la première visite, le site demande le @ Instagram et donne un siège tout de suite (noise_people.src='site'). Un inscrit du site qui ne commente jamais ne peut pas gagner la loterie (condition « commenter le post du jour »). Aux passages : si un @ inscrit via le site semble faux/insultant, le supprimer de noise_people.

## 4. Passages 6:00 / 12:00 / 17:00 / 19:55
1. Lire tous les nouveaux commentaires des publications récentes (exclure ceux de the_noise_2026 et ceux déjà dans noise_ig_seen).
2. Pour chacun : `insert into noise_people(handle) … on conflict do nothing` (+ tagués), score VIP +1 (+3 si tag), `noise_ig_award(h,'comment',cid)` (+ 'tag'), et si c'est le post du jour `noise_mark_commenter(h, media_id)`. Insérer dans noise_ig_seen.
3. Répondre à CHAQUE commentaire : hébreu, court, varié, jamais de copier-coller, pas d'URL (« הקישור בביו »), relance (100 🎟️ + תגובה = הגרלה של 20 ₪ ב־20:00 ; תייגו חבר שמזייף). Commentaire insultant/sexuel/visant une vraie personne : pas de réponse, pas de points.
4. Repérer la réponse du המגיב של היום d'hier (avant 12:00).
5. noise_state `followers` {n, at} ; si ≥ 50 abonnés → prévenir Shlomo (reprise du calendrier de l'émission).
6. Vérifier que le post du jour existe (sinon le créer).
7. À 19:55 en plus : story « 5 דקות להגרלה! » (nombre de participants = noise_lottery_live().participants, meilleur commentateur du moment, rappel des 2 conditions).
Économie : rien de nouveau → terminer immédiatement (sauf 19:55 : la story est toujours faite).

## 5. Tâches programmées (une seule de chaque)
- « The Noise – production du matin » 5:43 dim–ven (avant le passage de 6:00) : post du jour + événement extraordinaire + débrief court (PAS de texte vidéo : c'est le chat « The Noise – vidéos »).
- Chat « The Noise – vidéos » : réveil 16:00 dim–jeu (texte voix → MP3 → reel 19:00), vendredi 12:00 (texte de la vidéo du samedi), samedi 18:35 (montage, reel 19:30). Chaque réveil programme le suivant.
- « The Noise – passages » 6:00, 12:00, 17:00, 19:55 (vendredi : 6:00, 12:00).
- « The Noise – loterie 20:00 » dim–jeu + sam 20:00 ; samedi 18:30 : loterie du vendredi.
- « The Noise – publier le reel collab » (ponctuelle, 31/10 19:00, dans le chat « The Noise – vidéos »).
