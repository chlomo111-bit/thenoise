# The Noise — ROUTINE (règles obligatoires décidées par Shlomo le 30/10/2026)

## 🔁 OBJECTIF N°1 : FAIRE REPOSTER NOS REELS (Shlomo, 01/11/2026) — RÈGLE OBLIGATOIRE POUR TOUS LES JEUX
But : que les utilisateurs repostent / partagent nos reels (story, envoi à des amis, repost). C'est la meilleure façon d'avoir de nouveaux visiteurs. Tout le contenu est pensé pour ça.
1. **Reel pensé pour être partagé** : hook dès la 1re seconde, un moment drôle ou fou que les gens ont envie de montrer, et les vrais joueurs tagués (les gens repartagent quand ils se voient dans la vidéo).
2. **Appel au partage partout**, court et pas forcé : à la fin de chaque reel, dans la légende et dans le commentaire du compte. Ex. « 🔁 שתפו בסטורי ותייגו אותנו » / « שלחו למישהו שחייב לראות את זה 👀 ». On garde aussi « מה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת ».
3. **Récompense dans le jeu** : qui partage le reel du jour en story en taguant le compte reçoit un bonus dans la monnaie du jeu + un badge « 🔁 שגריר » sur son personnage, et un merci en story (repartager sa story quand c'est possible). Vérification : la mention de story arrive en message privé (INSTAGRAM_LIST_ALL_CONVERSATIONS), ou capture envoyée en DM. Jamais d'argent réel, jamais de condition « suivre le compte ».
4. **Chaque jour** : partager en story notre propre reel du jour (« פרק חדש! 👇 ») dès qu'il sort, et repartager les stories des joueurs qui nous taguent.
5. **Mesurer** : à chaque passage, relever les partages du reel du jour (INSTAGRAM_GET_IG_MEDIA_INSIGHTS, métriques `shares` et `reposts`) et noter quel type de reel est le plus partagé, pour refaire ce qui marche.
6. S'applique dès la prochaine vidéo (le chat vidéos du jeu) et dès le prochain passage (le chat automatisation du jeu).

Compte Instagram : Composio `instagram_howel-rootle` UNIQUEMENT (vérifier `username == the_noise_2026`, ig_user_id 28776506972012800 / user_id 17841441777719733).
Supabase : Composio `supabase_restow-lise`, outil SUPABASE_BETA_RUN_SQL_QUERY, ref `ohvmnaymozoxfirkbntt`, UNIQUEMENT les objets `noise_*`. Pas de Lovable.
Dépôt : chlomo111-bit/thenoise (GitHub Pages → thenoise.hakaveret.online, médias sous /media/AAAA-MM-JJ/). `git pull --rebase` avant chaque push.
Textes Instagram/joueurs : hébreu, style émission télé drôle (présentateur דודי מיקרופון, voix Nimrod). Compte-rendu à Shlomo : français.
Détails techniques des fonctions SQL : `tools/ROUTINE_FONCTIONS_COMMUNES.md`.

## État (30/10/2026)
- 3 abonnés. Le calendrier de l'émission (appel aux jurés, votes, inscriptions) est EN PAUSE jusqu'à 50 abonnés.
- Reel de lancement en collaboration : samedi 31/10 19:00 (tâche dédiée, ne pas refaire).
- Monnaie du jeu = 🎟️ כרטיסים. **Seuil du jour = 100 🎟️.**


## ⚠️ RÈGLE DE PUBLICATION (Shlomo, 01/11/2026)
- **MAXIMUM 1 post + 1 reel par jour** sur @the_noise_2026. Jamais plus (le post du jour du matin = LE post ; la vidéo du jour = LE reel). Avant toute publication FEED/REELS : INSTAGRAM_GET_IG_USER_MEDIA → s'il y a déjà un post (IMAGE/CAROUSEL) ou un reel aujourd'hui (heure d'Israël), ne pas en publier un autre du même type.
- **STORIES : autant qu'on veut** (« spam story »). À CHAQUE passage (6:00, 12:00, 17:00, 19:55) publier au moins 1 story (outil tools/story_soon.py : modes event / soon / teaser / launch / lot5 / nowin), toujours une vraie idée + un hook, variées : événement du jour, compteur d'abonnés (soon), rappel du post du jour, candidats, idée de la boîte à idées, teaser de la vidéo (~1 h avant le reel), résultat de la loterie. Chaque story une seule fois, copiée dans ~/Desktop/Jeux/The Noise/.

## 🆕 v3 (01/11/2026) — nouveautés validées par Shlomo (SQL : tools/supabase_noise_v3.sql)
- **Phase « early » = אודישנים מוקדמים** : l'émission a commencé AVANT 50 abonnés (« משהו שלא קרה באף עונה »). Les candidats intéressés sont dans noise_people (role=contestant, status=casting, song). Les 50 abonnés servent maintenant à CHOISIR LES JURÉS.
- **Audition du jour** (production du matin) : `noise_state.audition = {day, handle, name, song, n}` → le candidat suivant (tourner entre les candidats ; nouveaux candidats ajoutés depuis casting_interest / commentaires « nom + chanson »). Le site permet de voter ✅/❌ (noise_aud_vote, +5 🎟️, 1/jour). La vidéo de 19:00 montre son chant (version drôle Suno) ; le résultat du vote (select noise_aud_live()) est annoncé dans la vidéo du lendemain, et à 20:00 on note dans noise_people.status : 'in' si ✅ > ❌, sinon 'out' (sauf égalité → vidéo dramatique, on relance).
- **Jeu des masques** (quand il y a un événement masques) : `noise_state.mask = {day, options:[handles], clue}` + `insert into noise_mask_answer(day, answer)` (la réponse n'est JAMAIS dans noise_state avant la révélation). À 20:00 : `select noise_mask_reveal('AAAA-MM-JJ')` (+30 🎟️ aux bons devineurs) et révéler dans la story résultat + la vidéo du lendemain.
- **Parrainage** : lien `https://thenoise.hakaveret.online/?ref=<handle>` → +50 🎟️ au parrain par ami (max 10/jour), table noise_refs. En parler dans les stories.
- **Bonus de série** : noise_visit donne +10 🎟️ par jour de série (max +100).
- **Site** : compteur en direct sur l'accueil (public + abonnés + derniers arrivés), bandeau d'activité dans le studio, accueil en 3 étapes, compte à rebours du prochain épisode (19:00, samedi 19:30), boutons 🎤 אודישן היום / 🎭 מי במסכה? / 📲 הזמינו חבר (carte de siège à partager en story).

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

## 3. Loterie tous les soirs à 20:00 — PLUS D'ARGENT RÉEL (règle de Shlomo du 31/10/2026)
**Depuis le 31/10 au soir : plus jamais de vrai argent (ni Bit, ni ₪) dans The Noise.** Le gagnant reçoit :
+300 🎟️ (automatique dans noise_fan_draw), le siège 👑 le lendemain, un tag dans la vidéo, et LE POUVOIR de décider la chose extraordinaire qui arrive le lendemain dans le jeu (en plus du reste) — comme המגיב של היום. On lui demande en réponse et en story « מה יקרה מחר בזכותך? כתבו עד 12:00 ». Le grand gagnant de l'émission : גביע The Noise 🏆 + 1000 🎟️ (pas d'argent).
Plus de message « à payer par Bit » à Shlomo : le prévenir seulement en cas de problème.
- Un seul gagnant (bonus 🎟️ + pouvoir, aucun argent). Conditions : (a) commenter le POST DU JOUR épinglé, (b) ≥ 100 🎟️ dans la journée. Pas de condition d'abonnement.
- POST DU JOUR créé CHAQUE MATIN (image 4:5 1080×1350, hook + rappel des 2 conditions + « הגיבו כאן 👇 »), épinglé si possible (l'API ne permet pas d'épingler → l'indiquer à Shlomo seulement la première fois). Ne jamais l'oublier.
  Son media_id est noté dans noise_state `daily_post` {day, media_id, permalink}.
- Tirage : `select noise_fan_draw();` (ou avec la date du vendredi). Le site affiche le tirage en direct (noise_lottery_live) et le gagnant a le siège 👑 le lendemain.
- Puis story du résultat (1080×1920) (pas de message à Shlomo, pas d'argent).

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
3. Répondre à CHAQUE commentaire : hébreu, court, varié, jamais de copier-coller, pas d'URL (« הקישור בביו »), relance (100 🎟️ + תגובה = הגרלה ב־20:00 – הזוכה מחליט מה יקרה מחר ; תייגו חבר שמזייף). Commentaire insultant/sexuel/visant une vraie personne : pas de réponse, pas de points.
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

## Règle horaire (Shlomo, 02/11)
- RIEN n'est publié sur Instagram avant 08:00 (post, story, réponses). Production du matin à 8:02.

## RÈGLEMENT 03.11 (validé par Shlomo, en vigueur dès le mardi 03.11.2026) — PRIORITAIRE sur tout ce qui précède
Remplace « une vidéo du jour obligatoire chaque jour » et le décalage Shabbat à 18:30.
1. **Alternance reel / post (tous les jeux)** : mar 03.11 = REEL, mer 04 = post, jeu 05 = REEL, ven 06 = post (+ Shabbat), sam 07 soir = REEL (toujours, priorité absolue), dim 08 = post, lun 09 = REEL, mar 10 = post, mer 11 = REEL, jeu 12 = post, ven 13 = post (vendredi = toujours post), sam 14 soir = REEL, dim 15 = post… Règle : jamais deux reels de suite ; samedi soir = toujours reel ; vendredi et dimanche = toujours post ; sinon on alterne. Aucune vidéo de remplissage.
   - The Noise : le POST DU JOUR du matin (8:02) est publié TOUS les jours de semaine (c'est la base de la loterie de 20:00 : commenter le post du jour + 100 🎟️). Les jours REEL, le reel s'ajoute le soir (19:00) ; les jours POST, pas de reel (donc pas de textes de voix à Shlomo).
2. **Structure du reel** (épisode d'émission télé animée, ~45–60 s) : (1) explication courte : « The Noise – l'émission où les candidats ET le jury sont choisis parmi les abonnés » ; (2) « hier on en était à… (X candidats, Y juges en lice, Z abonnés) – aujourd'hui on est à… » ; (3) [מבזק au milieu – le journal de Danit] le commentaire du jour (le plus liké / l'idée du gagnant) ; (4) ce qui s'est passé hier (résultats des votes, éliminations, révélations) ; fin = cliffhanger + question à commenter.
3. **Ton** : épisode de télé-réalité animée : tension, éliminations, rebondissements, envie de voir la suite. Filmé sur le plateau 3D (tools/film3d_0211.py + tools/build_ep_0211.py), son calé image par image.
4. **Paliers d'abonnés** (noise_state `palier` = dernier palier fêté) : tous les +10 abonnés → TOUT le monde reçoit +50 🎟️ (select noise_palier_bonus(<abonnés>)) + story « 🎉 X abonnés! כולם קיבלו 50 🎟️ » ; tous les 100 → grand événement (prime spéciale ×2, invité surprise, fête au plateau…) annoncé en story + dans le prochain reel. Jamais de vrai argent.
5. **Shabbat** : vendredi = post normal seulement + story « שבת שלום » 1 h avant l'entrée de Shabbat (Tel Aviv, vérifier l'horaire chaque semaine, ex. ven 06.11 entrée ≈ 16:23 → story ≈ 15:20). Rien pendant Shabbat (pas de loterie le vendredi soir). Samedi soir après la sortie : REEL + loterie (vendredi + samedi).
6. **Stories** : minimum 3 par jour en semaine, sans maximum, en alternant images ET petites VIDÉOS en story (8–10 s, plateau 3D qui bouge + musique synthétique, jamais de voix ElevenLabs) : `python3 tools/story_video.py out.mp4 '<titre>' '<texte>' '<cta>'`. Cadrage vérifié avant chaque publication.
7. Rien n'est publié avant 08:00.

## Leçons des stats (04.11) – à appliquer à chaque reel
- Chiffres : lancement 31/10 = 1599 vues, 32 commentaires, 4 partages, 12,5 s de visionnage moyen ; 01/11 = 696 vues, 11 com., 1 partage ; 02/11 = 182 vues, 7 com., 0 partage ; 03/11 = 172 vues, 1 com., 0 partage, 8,9 s de visionnage moyen sur 56 s.
- Ce qui marche : une action simple et personnelle (« כתבו אני בקהל » → un siège à ton nom), de vraies personnes nommées/taguées, un défi à envoyer à un ami.
- Ce qui ne marche pas : vidéos de 50–56 s qui commencent par « ברוכים הבאים » → les gens partent à 9 s.
- Donc chaque reel : 25–35 s max ; hook choc dans les 2 premières secondes ; UNE mécanique de partage (« שלחו את הסרטון ל… ») qui récompense l'envoyeur ET l'ami (50 🎟️ chacun quand l'ami commente) ; se demander toujours « qui va envoyer ça à qui ? » (ex. à l'ami qui chante faux sous la douche, à l'ami qui ferait un bon juge) ; le mot-clé à commenter est répété à l'écran à la fin.
- Mécanique « אני מזייף » (dès le reel du 05/11) : quand quelqu'un commente « אני מזייף » (idéalement en taguant qui lui a envoyé) → il devient candidat (casting) + 50 🎟️, et la personne taguée reçoit aussi 50 🎟️ (noise_ig_award / insert noise_tickets).

## Horaire de publication des reels (analyse du 04.11)
Données réelles (heure d'Israël, UTC+2) :
- Reels : 31/10 sam. 19:01 → 1599 vues · 01/11 dim. 20:10 → 696 · 02/11 lun. 19:25 → 182 · 03/11 mar. 19:03 → 172.
- Commentaires des abonnés (64 relevés) : 3 pics → 06:00–09:00 (trajet), 12:00–15:00 (pause), **20:00–22:00 (le plus fort après un reel)**. Presque rien entre 16:00 et 19:30.
- `online_followers` indisponible sous 100 abonnés (à relancer au palier 100).
- À 18:00–19:00, 4 comptes de Shlomo publient déjà (סבתא test 18:00, השכנים 19:00, @chlomo.assouline 18:56) → même public, ils se cannibalisent.
DÉCISION (test à partir du jeu. 05.11) :
- **Reel de semaine à 20:30** (tâche programmée à 20:20, car elles partent 10–25 min en retard). Il sort APRÈS l'annonce de la loterie de 20:00 → la story résultat pousse vers le reel.
- **Samedi soir : reel à 19:00** (sortie de Shabbat ~17:25 ; le meilleur reel jusqu'ici est sorti un samedi à 19:01).
- Post du jour : 8:02 (inchangé).
- Juste après publication : répondre à TOUS les commentaires pendant la 1re heure + story « פרק חדש עכשיו 🔥 » (la 1re heure décide de la diffusion).
- Comparer après 3 reels à 20:30 (vues à 24 h, temps moyen, partages) ; si moins bien que 19:00 → revenir à 19:00.

## Hymne « אני מזייף » (validé par Shlomo le 04.11)
- Fichier : media/musique/hymne_v2.mp3 (Suno, 63 s, 136 BPM). Pas de stems → « ducking » : la musique descend à ~18 % sous les voix, remonte entre les répliques.
- Chaque reel : ouvre sur le refrain (+4 dB, public qui saute, Dudi + NissoC qui dansent, texte « אני מזייף, ואני גאה בזה! ») et finit sur le gros refrain + « תייגו חבר שמזייף כמוני 👇 ».
- Modèle validé « top » : tools/demo_hymne.py (exemple 10 s). Stories vidéo : l'hymne remplace la musique synthétique.

## Voix ElevenLabs — c'est Claude qui les génère (règle du 04.11, 20:51)
- Shlomo ne génère plus les voix : plus de texte à lui envoyer, plus d'attente des MP3.
- Outil : ElevenLabs creative_generate_speech, modèle eleven_v3 (tags [shouting] [whispers] [laughs] [excited]).
  Nimrod / Dudi = ZiofZHcEBTn5sRySe5h8 · Danit / présentatrice = s0T0DT6EAPeX57MQpn3I.
- 1 prise par voix (économie de crédits : ~13 crédits/seconde, un reel de 30 s ≈ 400 crédits) ; une seule génération, jamais de relance en double.
- Récupération : creative_get_flow_run_status → content_url → curl (elevenlabsusercontent.com fonctionne).
- Toujours écrire le texte APRÈS l'analyse du reel précédent + commentaires ; garder voix.txt dans media/AAAA-MM-JJ/.
