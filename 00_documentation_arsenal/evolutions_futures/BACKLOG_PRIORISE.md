# BACKLOG PRIORISÉ — DETTES RESTANTES

> Sources : audit climatisation (D1–D13), audit hystérésis transverse (H1–H3),
> runtime du dépôt. D8 clôturé. Aucun nouvel audit, aucune nouvelle dette.
> Échelle : P0 = incident probable · P1 = correction recommandée ·
> P2 = amélioration utile · P3 = cosmétique.

## Note de cadrage

Le seul incident fonctionnel avéré (D8) est corrigé. Il ne subsiste donc **aucun
P0 inconditionnel**. Deux items sont **P0 conditionnels** : ils deviennent P0 actifs
seulement sous une condition vérifiable immédiatement (H1, D4). Tout le reste relève
de gouvernance, d'explicabilité ou de maintenabilité — pas de panne.

---

## Classification et estimation, dette par dette

### Candidats P0 conditionnels

**H1 — Déshumidificateur : seuils potentiellement inversés**
- Type : **bug réel (latent)**.
- Proba incident : haute *si* `cave_rh_cible_off ≥ cave_rh_cible_on` (défauts d'usine
  sans `initial` → ON=60/OFF=65 = inversé) ; nulle si correctement réglé.
- Impact utilisateur : court-cycle du déshumidificateur (bruit, comportement erratique).
- Impact énergétique : réel (cycles compresseur rapprochés).
- Complexité : faible (ajouter `initial` + resserrer les plages).
- Régression : très faible.
- **Priorité : P1 — escalade P0 immédiate si les valeurs courantes sont inversées.**
  Vérification : comparer les deux helpers ; l'`integrite_reglages/deshumidificateur`
  le signale déjà s'il est armé.

**D4 — `correction.yaml` agit hors chaîne + course avec le Guard**
- Type : **bug réel** (couplage caché confort ↔ sécurité).
- Proba incident : modérée, **conditionnée** au déplacement du slider consigne COOL
  pendant clim éteinte.
- Impact utilisateur : clignotement du relais / écriture de consigne avortée.
- Impact énergétique : négligeable.
- Complexité : moyenne (décision d'architecture : sortir l'action de la chaîne, ou
  l'inhiber explicitement pendant la fenêtre d'écriture).
- Régression : moyenne (touche le relais physique).
- **Priorité : P1** (P0 si le geste est fréquent dans ton usage).

### P1 — corrections recommandées

**D1 — La raison de décision masque des causes réelles** (aération étage, absence prolongée)
- Type : **explicabilité** (Critique dans sa catégorie).
- Proba incident : nulle (la décision est correcte). Mais le **défaut se manifeste à
  chaque fois** que ces blocages sont actifs.
- Impact utilisateur : impossible de diagnostiquer une clim arrêtée par ces causes ;
  l'UI affirme « aucune condition ne justifie une action » à tort.
- Impact énergétique : nul.
- Complexité : moyenne (dériver la raison des vraies autorisations).
- Régression : faible (observabilité seule).
- **Priorité : P1.**

**D3 — Voyant `clim_bloquee` et carte « blocages » trompeurs**
- Type : **explicabilité** (le plus visible côté utilisateur).
- Proba : se manifeste dès qu'un blocage non agrégé est actif ; faux positif possible
  sur fenêtre d'étage.
- Impact utilisateur : la carte peut afficher « Aucun blocage » alors que la clim est
  bloquée. Affirmation fausse.
- Énergie : nul. · Complexité : moyenne. · Régression : faible (UI).
- **Priorité : P1.** Même chantier que D1.

**D9 — Application de la consigne COOL incomplète/asymétrique**
- Type : **bug réel mineur / maintenabilité** — *seul item restant touchant le
  comportement thermique.*
- Proba : élevée (à chaque entrée en COOL et à chaque bascule présence↔absence en cours
  de refroidissement, la consigne n'est pas (ré)appliquée).
- Impact utilisateur : la clim refroidit à la consigne interne précédente, pas à la
  consigne calculée ; `consigne_clim_appliquee` ment sur ce qui est réellement appliqué.
- Impact énergétique : **réel mais conditionnel** (dépend de la consigne retenue par
  l'appareil).
- Complexité : moyenne (automation « entrée en cool → appliquer », symétrique à HEAT).
- Régression : faible à moyenne (ajoute des `set_temperature`).
- **Priorité : P1.** C'est le point sur lequel je nuance « fonctionnellement sain ».

### P2 — améliorations utiles

**D2 — Raison vs décision : fenêtre brute vs temporisée**
- Type : explicabilité. Sous-ensemble du cluster Observabilité (D1/D3). Faible impact
  isolé. Complexité/Régression faibles. **P2** (à traiter dans le même chantier).

**D6 — Logique métier dans l'UI** (recompute horaire en JS, dépend de l'horloge client)
- Type : maintenabilité / gouvernance. Proba divergence faible (fuseau/horloge client).
  Complexité faible (lire `clim_blocage_horaire_reel`). Régression faible. **P2** (cluster).

**D7 — `clim_action_en_cours` = « bloquée » pendant un refroidissement actif** (poêle)
- Type : explicabilité. Proba : quand poêle on + COOL actif. Impact : survol trompeur.
  Énergie nul. Complexité faible. **P2** (cluster).

**D5 — Notification d'échec persistant non matérialisée**
- Type : gouvernance (contrat 08 vs runtime). Proba incident : faible (échec infra
  prolongé). Impact : un échec d'exécution reste silencieux. Complexité faible (notif,
  ou corriger le contrat). Régression faible. **P2.**

**D13 — Couverture CI partielle** (seule l'admissibilité + extinction COOL sont testées)
- Type : gouvernance. Proba : nulle directe, mais **aucun filet anti-régression** sur
  raison/blocages/observabilité — ce qui fragilise précisément les chantiers P1 ci-dessus.
- Complexité moyenne. Régression nulle. **P2** — à enchaîner *après* le cluster
  Observabilité pour le figer.

**H2 — VMC : seuils OFF morts mais validés**
- Type : **gouvernance** (faux sens de contrôle). Proba incident : nulle (le verrou
  temporel de 15 min fonctionne). Impact : un réglage UI validé sans effet réel.
  Énergie : marginale (run-on temporel ≠ vraie hystérésis). Complexité faible (câbler
  `seuil_off` à la libération, ou supprimer le paramètre + sa validation). Régression
  faible. **P2.**

**H3a — Aération : seuil unique sans bande morte**
- Type : bug potentiel / explicabilité. Proba : oscillation de la recommandation si bruit
  autour de `ha_min`/`dt_min`. Impact : scintillement d'un signal **consultatif** (+ jitter
  propagé à la voie HR de la VMC, amorti par son verrou). Énergie : faible. Complexité
  moyenne (ajouter deadband/mémoire). Régression moyenne (modifie le comportement de
  recommandation). **P2.**
- *Pré-chantier : confirmer d'abord si `tentative_en_grace` amortit déjà en aval.*

**D-tuile — Polarité de `clim_synthese_status_72` (reportée)**
- Type : explicabilité / maintenabilité. Défaut de modèle du template partagé (concerne
  aussi HEAT) ; `clim_maintien_cool` est une entité fantôme. Complexité moyenne.
  Régression faible (UI). **P2**, en attente de l'observation runtime post-déploiement déjà
  prévue.

**D10 — Duplication humidex DRY + organisation de fichiers**
- Type : maintenabilité. Impact : confusion, capteur quasi-orphelin. Complexité faible.
  Régression faible. **P2/P3.**

### P3 — cosmétique / à laisser tel quel

**H3b — Aération : helpers d'hystérésis déclaratifs non câblés** — gouvernance/cosmétique.
Les supprimer (ou les câbler avec H3a). **P3.**

**D11 — Dérive sémantique `chauffage_clim_active_en_hiver`** — maintenabilité (nommage).
Le renommer casserait des références (régression) ; **laisser tel quel** ou clarifier en
commentaire. **P3.**

**D12 — Divers** : IDs d'automation hétérogènes, plage `clim_offset_off` à −3, doc fantôme
`clim_etat_reel`. Sans danger. **P3 — laisser tel quel** (nettoyage opportuniste seulement).

**DRY — bande morte −1 codée en dur** (audit hystérésis §2bis) — lisibilité. **P3.**

**Contrat 05 — « aucun deadlock thermique »** désormais vrai depuis le fix. Réalignement
doc trivial. **P3.**

**Chauffage** — système modulant par conception. **Aucun chantier** ; la grille ON/OFF ne
s'applique pas. Laisser tel quel.

---

## Backlog unique

| Priorité | Dette | Type | Risque | Bénéfice | Effort |
|---|---|---|---|---|---|
| **P0?** | H1 — déshum seuils inversés | Bug latent | Court-cycle compresseur **si OFF≥ON** | Élimine oscillation matérielle | Faible |
| **P0?** | D4 — correction.yaml vs Guard | Bug réel | Relais qui clignote sur geste slider | Supprime conflit confort↔sécurité | Moyen |
| P1 | D1 — raison masque causes | Explicabilité | UI affirme le faux | Diagnostic clim restauré | Moyen |
| P1 | D3 — voyant/carte blocages trompeurs | Explicabilité | « Aucun blocage » faux | Fin des messages mensongers | Moyen |
| P1 | D9 — consigne COOL non appliquée | Bug mineur thermique | Mauvaise consigne / énergie | Fidélité consigne + économies | Moyen |
| P2 | D2 — fenêtre brut vs délai | Explicabilité | Raison transitoire fausse | Cohérence raison↔décision | Faible (cluster) |
| P2 | D6 — logique métier en UI | Maintenabilité | Divergence horloge client | Vérité côté backend | Faible (cluster) |
| P2 | D7 — action « bloquée » en cooling | Explicabilité | Survol trompeur (poêle) | Survol exact | Faible (cluster) |
| P2 | D5 — notif échec persistant | Gouvernance | Échec exécution silencieux | Visibilité des pannes | Faible |
| P2 | D13 — CI partielle | Gouvernance | Pas de filet anti-régression | Fige les chantiers P1 | Moyen |
| P2 | H2 — VMC seuils OFF morts | Gouvernance | Réglage UI sans effet | Contrôle réel ou param supprimé | Faible |
| P2 | H3a — aération sans deadband | Bug potentiel | Oscillation recommandation | Stabilité du conseil | Moyen |
| P2 | D-tuile — polarité status_72 | Explicabilité | Tuile diagnostic inversée | Diagnostic COOL/HEAT correct | Moyen |
| P2/P3 | D10 — duplication humidex DRY | Maintenabilité | Confusion capteur orphelin | Domaine DRY lisible | Faible |
| P3 | H3b — helpers hystérésis aération morts | Gouvernance | Faux signal de réglage | Cohérence UI | Faible |
| P3 | D11 — nom `…active_en_hiver` | Maintenabilité | Compréhension future | Sémantique claire | Faible (doc) |
| P3 | D12 — IDs / offset / doc fantôme | Cosmétique | Friction maintenance | Hygiène | Faible |
| P3 | DRY deadband −1 en dur | Maintenabilité | Non paramétrable | Lisibilité | Faible |
| P3 | Contrat 05 « aucun deadlock » | Gouvernance/doc | Contrat daté | Cohérence doc | Trivial |
| — | Chauffage (modulant) | — | — | Ne rien forcer | Nul |

---

## Lecture stratégique

- **À faire en premier, ce week-end :** vérifier H1 (30 s). C'est le seul item au risque
  matériel et le moins cher à corriger.
- **Un seul vrai chantier de valeur :** le cluster **Observabilité COOL** (D1, D3, puis
  D2, D6, D7 dans la foulée), verrouillé ensuite par **D13**. C'est lui qui répond à la
  conclusion « non explicable » de l'audit.
- **Deux items qui touchent le réel :** D9 (consigne/énergie) et D4 (relais). À traiter
  isolément, hors du cluster UI.
- **Tout le reste (P3) peut rester tel quel** sans dette opérationnelle : à nettoyer
  seulement de façon opportuniste, jamais comme chantier dédié.
- **Pré-vérifications avant tout chantier P2** (sans en faire un audit) : l'amortissement
  `tentative_en_grace` en aval de l'aération, et la cohérence `vmc_duree_min_haute` ↔
  `vmc_duree_haute_vitesse`. Tant que non confirmées, H3a et H2 restent des estimations.
