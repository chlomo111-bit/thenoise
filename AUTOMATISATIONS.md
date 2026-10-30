# Automatisations du jeu (sauvegarde du directeur des jeux, 30/10/2026 12:45)

Inventaire de toutes les tâches programmées actives de ce jeu avant remise à zéro.
Les textes complets des tâches restent consultables dans les tâches désactivées (même ID) ;
la logique détaillée est dans tools/ROUTINE.md.

Règles communes (30/10) : vidéo du jour (le commentaire le plus liké décide), un événement extraordinaire par jour,
loterie 20 ₪ à 20:00 (commentaire sur le post du jour + seuil de monnaie, pas d'abonnement obligatoire),
« המגיב של היום » (badge + pouvoir de choisir un événement le lendemain), passages 6:00 / 12:00 / 17:00 / 19:55,
Shabbat : rien de vendredi 16:00 à samedi 18:30, tout est décalé à samedi 18:30.

## Organisation actuelle (rangement du 30/10/2026, ordre du directeur)
Tout The Noise tourne dans UN seul chat : « Automatisation – The Noise », qui se réveille avec des send_later
(planning dans tools/ROUTINE.md). Aucune tâche récurrente. Les anciennes tâches désactivées ont été archivées
dans tools/ANCIENNES_TACHES.md puis supprimées.

| ID | Type | Horaire (heure d'Israël) | Chat | Rôle |
|---|---|---|---|---|
| trig_01GSwhba4RNwD9NqK85xjtR8 | send_later | sam. 31/10 18:30 | Automatisation – The Noise | Rattrapage sortie de Shabbat : loterie du vendredi, passage complet, réveil 19:55 |
| trig_015TyePiqqk3StF117wadcdd | send_later | sam. 31/10 19:00 | chat de création du jeu (session 01K8i1w3yD9CDquGsWHdGjZx) | Publication du reel collab de lancement (anti-doublon intégré) — remplace trig_01LWntE2dFQhdcMrXyiviQCF, désactivée |

Ensuite, chaque réveil programme le suivant (6:00 · 12:00 · 17:00 · 19:55, loterie 20:00 ; vendredi 6:00 et 12:00 ; rien entre vendredi 16:00 et samedi 18:30).

Supprimées le 30/10 (texte complet dans tools/ANCIENNES_TACHES.md) :
trig_01Ay5VUXkKd8zfYNTxprhzGy (passages), trig_01WhX6dXEWijvoeTzTx2z69E (loterie 20:00),
trig_01XuNQ4wjAUyjSLYEkh7ykki et trig_01DccFmmaD4JAXF4T6cg4grY (rappels jurés, obsolètes tant que < 50 abonnés).

Seuil : 100 jetons · calendrier jurés/votes en pause jusqu'à 50 abonnés

## Tâches du directeur qui touchent ce jeu
| ID | Nom | Horaire | Rôle |
|---|---|---|---|
| trig_01CKRu6aTLCyHxQjn1bZYJsZ | Jeux – passages du vendredi | ven. 7:50 · 13:50 | Déclenche ruche + savta |
| trig_016xihjQtAaUGjNW17P6RXG2 | Jeux – décaler Shabbat | ven. 15:45 | Décale les ponctuels à sam. 18:30 |
| trig_01SweqkEFqGvYW3p6ffWU83f | Jeux – rattrapage sortie de Shabbat | sam. 18:30 | Tirage du vendredi ruche + passages ruche/savta |
